/* TB371FC legacy schedtune compatibility.
 * Init owns the hierarchy. This process never mounts, restarts another service,
 * changes frequency/affinity/nice, or writes another controller's settings.
 */
#include "foreground_policy.inc"
#include <sys/vfs.h>
#include <limits.h>

static const char *tasks="/dev/tb371fc-schedtune/foreground/tasks";
static const char *lock_path="/data/misc/tb371fc-scheduler/controller.lock";
static const char *ui_package="com.android.systemui";
static const char *home_package="com.android.launcher";

/* The fixed package names establish identity. Do not replace a dead watched PID
 * with whichever process later happens to reuse its number. */
static int package_uid(const char *package,uid_t *result) {
 FILE *f=fopen("/data/system/packages.list","r");if(!f)return -1;
 char line[4096],name[256];unsigned uid;int found=0;
 while(fgets(line,sizeof(line),f)) {
  if(sscanf(line,"%255s %u",name,&uid)!=2||strcmp(name,package))continue;
  if(!allow_uid(uid)||found){fclose(f);return -1;}
  *result=(uid_t)uid;found=1;
 }
 int error=ferror(f);fclose(f);return found&&!error?0:-1;
}

static int matches_package(pid_t pid,uid_t expected,const char *package) {
 uid_t uid;ino_t inode;unsigned long long birth;
 if(!process_identity(pid,&uid,&inode,&birth)||uid!=expected)return 0;
 char path[96],cmdline[256];snprintf(path,sizeof(path),"/proc/%d/cmdline",pid);
 int fd=open(path,O_RDONLY|O_CLOEXEC|O_NOFOLLOW);if(fd<0)return 0;
 ssize_t n=read(fd,cmdline,sizeof(cmdline));close(fd);
 if(n<=0||!memchr(cmdline,0,(size_t)n)||strcmp(cmdline,package))return 0;
 uid_t after_uid;ino_t after_inode;unsigned long long after_birth;
 return process_identity(pid,&after_uid,&after_inode,&after_birth)
  &&identity_divergence_class(uid,inode,birth,after_uid,after_inode,after_birth)==0;
}

static int discover_ui(void) {
 uid_t wanted_ui,wanted_home;
 if(package_uid(ui_package,&wanted_ui)||package_uid(home_package,&wanted_home))return 0;
 DIR *d=opendir("/proc");if(!d)return 0;
 struct dirent *e;pid_t found_ui=0,found_home=0;int ambiguous=0;
 while((e=readdir(d))) {
  char *last;long id=strtol(e->d_name,&last,10);if(*last||id<=0||id>INT_MAX)continue;
  pid_t pid=(pid_t)id;uid_t uid=uid_of(pid);
  if(uid==wanted_ui&&matches_package(pid,wanted_ui,ui_package)) {
   if(found_ui){ambiguous=1;break;}found_ui=pid;
  }
  if(uid==wanted_home&&matches_package(pid,wanted_home,home_package)) {
   if(found_home){ambiguous=1;break;}found_home=pid;
  }
 }
 closedir(d);
 if(ambiguous||!found_ui||!found_home)return 0;
 ui_uid=wanted_ui;launcher_uid=wanted_home;ui_pid=found_ui;launcher_pid=found_home;
 memset(classifications,0,sizeof(classifications));memset(process_cache,0,sizeof(process_cache));
 have_top_signature=0;identity_state=0;failed_stage=NULL;return 1;
}

/* Neutralize before returning any member, including after identity loss.
 * A failure stops admission; it is never converted into successful cleanup. */
static int release_owned(void) {
 if(value(group,"schedtune.boost","0")||value(group,"schedtune.prefer_idle","0"))return -1;
 for(int attempt=0;attempt<20;attempt++) {
  pid_t own[8192];size_t n=read_tasks(tasks,own,8192);
  if(n==(size_t)-1)return -1;if(!n)return 0;
  for(size_t i=0;i<n;i++) {
   if(!own_group(own[i]))continue;
   if(move_task(root,own[i])&&errno!=ESRCH&&errno!=ENOENT)return -1;
  }
  usleep(20000);
 }
 errno=EBUSY;return -1;
}

static int valid_hierarchy(void) {
 struct stat st;struct statfs fs;
 if(lstat(root,&st)||!S_ISDIR(st.st_mode)||st.st_uid!=0)return 0;
 if(statfs(root,&fs)||(unsigned long)fs.f_type!=0x27e0ebUL)return 0;
 if(lstat(group,&st)||!S_ISDIR(st.st_mode)||st.st_uid!=0)return 0;
 FILE *f=fopen("/proc/self/mountinfo","r");if(!f)return 0;
 char line[4096];int found=0;
 while(fgets(line,sizeof(line),f))if(strstr(line," /dev/tb371fc-schedtune ")
   &&strstr(line," - cgroup schedtune "))found++;
 fclose(f);return found==1;
}

static int acquire_owner(void) {
 const char *dir="/data/misc/tb371fc-scheduler";struct stat st;
 if(lstat(dir,&st)||!S_ISDIR(st.st_mode)||st.st_uid!=0||(st.st_mode&0777)!=0700)return -1;
 int fd=open(lock_path,O_CREAT|O_RDWR|O_CLOEXEC|O_NOFOLLOW,0600);if(fd<0)return -1;
 if(fstat(fd,&st)||!S_ISREG(st.st_mode)||st.st_uid!=0||(st.st_mode&0777)!=0600
    ||flock(fd,LOCK_EX|LOCK_NB)){close(fd);return -1;}
 return fd;
}

static int apply_selected(const pid_t *top,size_t tn,const pid_t *uit,size_t un) {
 pid_t own[8192];size_t n=read_tasks(tasks,own,8192);if(n==(size_t)-1)return -1;
 qsort(own,n,sizeof(*own),compare_pid);
 for(int source=0;source<2;source++) {
  const pid_t *list=source?uit:top;size_t count=source?un:tn;
  for(size_t i=0;i<count;i++) {
   pid_t tid=list[i];if(contains(tid,own,n))continue;
   if(!critical_task(tid,1))continue;
   uid_t uid=uid_of(tid);
   if(!allow_uid(uid)||(source&&uid!=ui_uid&&uid!=launcher_uid))continue;
   int core=uid==ui_uid||uid==launcher_uid;
   if(!core&&!critical_task(tid,0))continue;
   if(core?!ui_foreground_task(tid):!top_task(tid))continue;
   if(!move_task(group,tid))attachments++;
   else if(errno!=ESRCH&&errno!=ENOENT)return -1;
  }
 }
 n=read_tasks(tasks,own,8192);if(n==(size_t)-1)return -1;
 for(size_t i=0;i<n;i++) {
  uid_t uid=uid_of(own[i]);int core=uid==ui_uid||uid==launcher_uid;
  int eligible=allow_uid(uid)&&critical_task(own[i],core)
    &&(core?ui_foreground_task(own[i]):top_task(own[i]));
  if(eligible)continue;
  if(!move_task(root,own[i]))returns++;
  else if(errno!=ESRCH&&errno!=ENOENT)return -1;
 }
 return 0;
}

int main(int argc,char **argv) {
 if(argc!=2||strcmp(argv[1],"--run")||getuid()!=0)return 2;
 int lock=acquire_owner();if(lock<0)return 24;
 if(!valid_hierarchy()){close(lock);return 5;}
 signal(SIGTERM,signal_stop);signal(SIGINT,signal_stop);signal(SIGHUP,signal_stop);
 setbuf(stdout,NULL);
 int rc=0,ready=0,boosted=0;double retry_at=0;
 if(release_owned()){close(lock);return 14;}
 printf("TB371FC_SCHEDULER_NATIVE_START\n");
 while(!stop_requested) {
  int on=display_on();
  if(on<=0) {
   if(boosted&&release_owned()){rc=14;break;}boosted=0;
   usleep(100000);continue;
  }
  if(!ready) {
   if(now()<retry_at){usleep(100000);continue;}
   retry_at=now()+2;
   if(!discover_ui()){usleep(100000);continue;}
   ready=1;
   printf("UI_IDENTITY_ADMITTED ui=%d home=%d\n",ui_pid,launcher_pid);
  }
  selection_time=now();pid_t top[8192],uit[8192];
  size_t tn=top_critical_tasks(top,8192);if(tn==(size_t)-1){rc=9;break;}
  selection_time=now();size_t un=ui_tasks(uit,8192);
  if(un==(size_t)-1||un==(size_t)-2) {
   if(release_owned()){rc=14;break;}boosted=0;
   if(un==(size_t)-1) {
    printf("UI_IDENTITY_WITHDRAWN pid=%d stage=%s\n",failed_pid,failed_stage?failed_stage:"unavailable");
    ready=0;retry_at=now()+.1;
   }
   usleep(100000);continue;
  }
  if(!boosted) {
   if(value(group,"schedtune.boost","30")||value(group,"schedtune.prefer_idle","1")){rc=8;break;}
   boosted=1;
  }
  if(apply_selected(top,tn,uit,un)){rc=10;break;}
  cycles++;usleep(100000);
 }
 if(release_owned())rc=14;
 printf("TB371FC_SCHEDULER_NATIVE_STOP status=%d attached=%u returned=%u cycles=%u\n",rc,attachments,returns,cycles);
 close(lock);return rc;
}
