#define _GNU_SOURCE
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/file.h>
#include <sys/vfs.h>
#include <sys/wait.h>
#include <dirent.h>
#include <signal.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <stdarg.h>
#include <limits.h>

/* Execute the real production main and selectors. Only kernel cgroup/display
 * I/O and time are emulated. Package identity comes from real Linux processes. */
static FILE *test_fopen(const char *,const char *);
static int test_open(const char *,int,...);
static ssize_t test_write(int,const void *,size_t);
static int test_lstat(const char *,struct stat *);
static int test_statfs(const char *,struct statfs *);
static int test_usleep(useconds_t);
static int test_clock_gettime(clockid_t,struct timespec *);
#define fopen test_fopen
#define open test_open
#define write test_write
#define lstat test_lstat
#define statfs(path,buf) test_statfs(path,buf)
#define usleep test_usleep
#define clock_gettime test_clock_gettime
#define main production_main
#include "../src/runtime.c"
#undef main
#undef fopen
#undef open
#undef write
#undef lstat
#undef statfs
#undef usleep
#undef clock_gettime

static char fixture[PATH_MAX],mapped[PATH_MAX];
static pid_t live_ui,live_home,live_app,old_home;
static pid_t members[32];static size_t member_count;
static int kinds[1024],top_active=1,screen_on=1,step,failures,deny_config,foreign_member;
static double mock_time=100;
int tb371fc_is_interactive(void){return screen_on;}

static void check(const char *name,int ok) {
 printf("%s %s\n",ok?"PASS":"FAIL",name);if(!ok)failures++;
}
static int member(pid_t id) {
 for(size_t i=0;i<member_count;i++)if(members[i]==id)return 1;return 0;
}
static int setting(const char *field) {
 char p[PATH_MAX];snprintf(p,sizeof(p),"%s/cgroup/foreground/%s",fixture,field);
 FILE *f=fopen(p,"r");int n=-1;if(f){if(fscanf(f,"%d",&n)!=1)n=-1;fclose(f);}return n;
}
static const char *map_path(const char *p) {
 const char *suffix=NULL,*kind=NULL;
 if(!strncmp(p,"/dev/tb371fc-schedtune",22)){suffix=p+22;kind="cgroup";}
 if(!strncmp(p,"/data/misc/tb371fc-scheduler",28)){suffix=p+28;kind="data";}
 if(!kind)return p;
 if(snprintf(mapped,sizeof(mapped),"%s/%s%s",fixture,kind,suffix)>=(int)sizeof(mapped))abort();
 return mapped;
}
static FILE *memory_file(const char *text) {
 FILE *f=tmpfile();if(!f)abort();fputs(text,f);rewind(f);return f;
}
static FILE *test_fopen(const char *p,const char *mode) {
 char b[8192];
 if(!strcmp(p,"/data/system/packages.list"))return memory_file("com.android.systemui 10108 /fake 0\ncom.android.launcher 10109 /fake 0\n");
 if(!strcmp(p,"/proc/self/mountinfo"))return memory_file("100 1 0:1 / /dev/tb371fc-schedtune rw - cgroup schedtune rw,schedtune\n");
 if(!strcmp(p,"/sys/class/drm/card0-DSI-1/dpms"))return memory_file(screen_on?"On\n":"Off\n");
 if(!strcmp(p,"/dev/cpuctl/top-app/cgroup.procs")) {
  snprintf(b,sizeof(b),top_active?"%d\n":"",live_app);return memory_file(b);
 }
 if(!strcmp(p,tasks)) {
  b[0]=0;for(size_t i=0;i<member_count;i++){char s[32];snprintf(s,sizeof(s),"%d\n",members[i]);strcat(b,s);}
  return memory_file(b);
 }
 pid_t id;char tail;
 if(sscanf(p,"/proc/%d/cgroup%c",&id,&tail)==1&&strstr(p,"/cgroup")) {
  int own=member(id)&&!foreign_member;
  const char *cpu=id==live_app?(top_active?"top-app":"background"):"foreground";
  snprintf(b,sizeof(b),"2:cpu:/%s\n6:schedtune:/%s\n",cpu,own?"foreground":"");return memory_file(b);
 }
 return fopen(map_path(p),mode);
}
static int test_open(const char *p,int flags,...) {
 mode_t mode=0;if(flags&O_CREAT){va_list args;va_start(args,flags);mode=(mode_t)va_arg(args,int);va_end(args);}
 if(deny_config&&strstr(p,"/foreground/schedtune.")){errno=EACCES;return -1;}
 int kind=!strcmp(p,tasks)?1:!strcmp(p,"/dev/tb371fc-schedtune/tasks")?2:0;
 int fd=open(map_path(p),flags,mode);
 if(fd>=0){if(fd>=1024)abort();kinds[fd]=kind;}return fd;
}
static ssize_t test_write(int fd,const void *data,size_t n) {
 int kind=fd>=0&&fd<1024?kinds[fd]:0;
 if(kind) {
  char id[32];if(n>=sizeof(id))abort();memcpy(id,data,n);id[n]=0;pid_t pid=(pid_t)strtol(id,NULL,10);
  if(kind==1){if(!member(pid)){if(member_count==32)abort();members[member_count++]=pid;}}
  else {
   check("withdrawal happens only after neutralization",setting("schedtune.boost")==0||screen_on);
   for(size_t i=0;i<member_count;i++)if(members[i]==pid){members[i]=members[--member_count];break;}
  }
 }
 return write(fd,data,n);
}
static int test_lstat(const char *p,struct stat *s){return lstat(map_path(p),s);}
static int test_statfs(const char *p,struct statfs *s) {
 int r=statfs(map_path(p),s);if(!r)s->f_type=0x27e0eb;return r;
}
static pid_t child(const char *name,uid_t uid) {
 int ready[2];if(pipe2(ready,O_CLOEXEC))abort();pid_t p=fork();if(p<0)abort();
 if(!p){close(ready[0]);if(setuid(uid))_exit(2);execl("/bin/sleep",name,"30",NULL);_exit(3);}
 close(ready[1]);char c;while(read(ready[0],&c,1)>0){}close(ready[0]);return p;
}
static int test_clock_gettime(clockid_t c,struct timespec *t) {
 if(c!=CLOCK_MONOTONIC)return clock_gettime(c,t);
 t->tv_sec=(time_t)mock_time;t->tv_nsec=(long)((mock_time-t->tv_sec)*1e9);return 0;
}
static int test_usleep(useconds_t u) {
 mock_time+=u/1000000.;if(u!=100000)return 0;
 switch(++step) {
  case 1:
   check("actual main admits foreground app and core UI",member(live_app)&&member(live_ui)&&member(live_home));
   check("active policy remains boost30 idle1",setting("schedtune.boost")==30&&setting("schedtune.prefer_idle")==1);
   top_active=0;break;
  case 2:
   check("app leaving top-app is withdrawn",!member(live_app)&&member(live_ui)&&member(live_home));screen_on=0;break;
  case 3:
   check("screen off empties owned group",member_count==0);
   check("screen off resets both controls",setting("schedtune.boost")==0&&setting("schedtune.prefer_idle")==0);
   old_home=live_home;kill(old_home,SIGTERM);waitpid(old_home,NULL,0);live_home=child(home_package,10109);screen_on=1;break;
  case 4:
   check("lost UI identity neutralizes before rediscovery",member_count==0&&setting("schedtune.boost")==0);break;
  case 5:
   check("same process handles replacement without service restart",member(live_ui)&&member(live_home)&&!member(old_home));screen_on=-1;break;
  case 6:
   check("unknown power state withdraws instead of enabling boost",member_count==0&&setting("schedtune.boost")==0);stop_requested=1;break;
  default:check("bounded lifecycle completed",0);stop_requested=1;break;
 }
 return 0;
}
int main(int argc,char **argv) {
 if(argc!=2||getuid()!=0)return 2;
 if(strlen(argv[1])>=sizeof(fixture))return 2;strcpy(fixture,argv[1]);
 live_ui=child(ui_package,10108);live_home=child(home_package,10109);live_app=child("tb371fc.test.foreground",10110);
 check("package cmdline and UID match",matches_package(live_home,10109,home_package));
 check("wrong UID is rejected",!matches_package(live_home,10108,home_package));
 check("wrong package is rejected",!matches_package(live_home,10109,ui_package));
 int lock=acquire_owner();check("native owner lock acquired",lock>=0);
 int other=acquire_owner();check("second owner refused",other<0);if(other>=0)close(other);if(lock>=0)close(lock);
 char *args[]={"tb371fc-scheduler","--run",NULL};int rc=production_main(2,args);
 check("real production main stops successfully",rc==0&&step==6);
 check("service stop leaves no boosted members",member_count==0&&setting("schedtune.boost")==0&&setting("schedtune.prefer_idle")==0);
 members[0]=live_ui;member_count=1;deny_config=1;
 check("configuration write failure reports failure",release_owned()!=0&&member_count==1);deny_config=0;
 check("owned membership can be cleaned after write permission restored",release_owned()==0&&member_count==0);
 members[0]=live_ui;member_count=1;foreign_member=1;
 check("unknown membership is not moved or reported clean",release_owned()!=0&&member_count==1);
 foreign_member=0;check("known owned membership cleaned",release_owned()==0);
 kill(live_ui,SIGTERM);kill(live_home,SIGTERM);kill(live_app,SIGTERM);
 waitpid(live_ui,NULL,0);waitpid(live_home,NULL,0);waitpid(live_app,NULL,0);
 printf("NATIVE_LIFECYCLE_FAILURES=%d\n",failures);return failures?1:0;
}
