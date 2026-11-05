#define _GNU_SOURCE
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/file.h>
#include <dirent.h>
#include <signal.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <errno.h>

/* One isolated cgroup hierarchy and a bounded foreground-only experiment.
 * No CPU affinity, CPU frequency, priority, thermal or existing cgroup writes. */
static volatile sig_atomic_t stop_requested;
static const char *root="/dev/tb371fc-schedtune";
static const char *group="/dev/tb371fc-schedtune/foreground";
static unsigned attachments,returns,cycles,thread_scans,metadata_reads,membership_reads,directory_reads;
static uid_t ui_uid,launcher_uid;
static pid_t ui_pid,launcher_pid;
#include "power.h"
static int display_on(void){return tb371fc_is_interactive();}
static void signal_stop(int s){(void)s;stop_requested=1;}
static int allow_uid(uid_t u){return (u>=10000 && u<20000) || (u>=90000 && u<100000);}
static uid_t uid_of(pid_t t) {
 char p[80];struct stat s;snprintf(p,sizeof(p),"/proc/%d",t);
 return stat(p,&s)==0?s.st_uid:(uid_t)-1;
}
static int value(const char *dir,const char *file,const char *v) {
 char path[512];snprintf(path,sizeof(path),"%s/%s",dir,file);
 int fd=open(path,O_WRONLY|O_CLOEXEC|O_NOFOLLOW);if(fd<0)return -1;
 size_t n=strlen(v);ssize_t k=write(fd,v,n);int e=errno;close(fd);errno=e;
 return k==(ssize_t)n?0:-1;
}
static int move_task(const char *dir,pid_t tid) {
 char s[32];snprintf(s,sizeof(s),"%d",tid);
 return value(dir,"tasks",s);
}
static int own_group(pid_t tid) {
 char path[80],line[1024];snprintf(path,sizeof(path),"/proc/%d/cgroup",tid);
 FILE *f=fopen(path,"r");if(!f)return 0;int own=0;
 while(fgets(line,sizeof(line),f))if(strstr(line,":schedtune:/foreground\n")){own=1;break;}
 fclose(f);return own;
}
static size_t read_tasks(const char *path,pid_t *list,size_t cap) {
 FILE *f=fopen(path,"r");if(!f)return (size_t)-1;
 size_t n=0;pid_t t;
 while(fscanf(f,"%d",&t)==1){if(n==cap){fclose(f);return (size_t)-1;}list[n++]=t;}
 fclose(f);return n;
}
static int compare_pid(const void *a,const void *b){pid_t x=*(const pid_t*)a,y=*(const pid_t*)b;return (x>y)-(x<y);}
static int contains(pid_t t,const pid_t *a,size_t n){return bsearch(&t,a,n,sizeof(*a),compare_pid)!=NULL;}
/* Classify only candidate TIDs. Cache names/TGIDs for 500ms, validating
 * proc inode + UID on every positive cache hit. UID and actual foreground
 * membership remain mandatory on every group admission. */
typedef struct {pid_t tid,parent;ino_t inode;uid_t uid;double expires;int role;} Classification;
static Classification classifications[8192];static double selection_time;
/* The process/task directory gives the thread group identity already.
 * Reading a full proc status generates unrelated VM statistics and locks.
 * Read only comm when refreshing the role; retain UID + proc inode checks. */
static int classify_known_task(pid_t tid,pid_t parent,int core_ui) {
 Classification *c=&classifications[(unsigned)tid%8192];
 /* A negative role can only deny admission. The parent identity is checked
  * by the process cache before discovery. Never reuse a positive role
  * without thread inode + UID and current CPU membership checks. */
 if(tid!=parent && c->tid==tid && c->parent==parent && c->role==0 && selection_time<c->expires)return 0;
 char path[96],name[64]={0};struct stat st;snprintf(path,sizeof(path),"/proc/%d",tid);
 if(stat(path,&st))return 0;
 if(c->tid==tid && c->parent==parent && selection_time<c->expires && c->inode==st.st_ino && c->uid==st.st_uid)
  return c->role==1 || (core_ui && c->role==2);
 snprintf(path,sizeof(path),"/proc/%d/comm",tid);FILE *f=fopen(path,"r");if(!f)return 0;
 metadata_reads++;int ok=fgets(name,sizeof(name),f)!=NULL;fclose(f);if(!ok)return 0;
 name[strcspn(name,"\n")]=0;int role=0;
 if(tid==parent || !strcmp(name,"RenderThread") || !strncmp(name,"hwuiTask",8))role=1;
 else if(!strcmp(name,"launcher.anim") || !strcmp(name,"GestureUI") || !strcmp(name,"onlineUXThread"))role=2;
 *c=(Classification){.tid=tid,.parent=parent,.inode=st.st_ino,.uid=st.st_uid,.expires=selection_time+.5,.role=role};
 return role==1 || (core_ui && role==2);
}
static int critical_task(pid_t tid,int core_ui) {
 Classification *c=&classifications[(unsigned)tid%8192];if(c->tid!=tid || c->parent<=0)return 0;
 char path[96];struct stat st;snprintf(path,sizeof(path),"/proc/%d/task/%d",c->parent,tid);
 if(stat(path,&st) || st.st_uid!=c->uid)return 0;
 return classify_known_task(tid,c->parent,core_ui);
}
static int ui_foreground_task(pid_t tid){
 membership_reads++;
 char path[80],line[256];snprintf(path,sizeof(path),"/proc/%d/cgroup",tid);FILE *f=fopen(path,"r");if(!f)return 0;int yes=0;
 while(fgets(line,sizeof(line),f))if(strstr(line,":cpu:/foreground\n") || strstr(line,":cpu:/top-app\n")){yes=1;break;}
 fclose(f);return yes;
}
static int top_task(pid_t tid){
 membership_reads++;
 char path[80],line[256];snprintf(path,sizeof(path),"/proc/%d/cgroup",tid);FILE *f=fopen(path,"r");if(!f)return 0;int yes=0;
 while(fgets(line,sizeof(line),f))if(strstr(line,":cpu:/top-app\n")){yes=1;break;}fclose(f);return yes;
}
/* Cache only discovery of critical TIDs. Eligibility is NEVER cached:
 * every admission and retained-member decision checks current CPU group.
 * A new foreground PID is scanned immediately; established processes are
 * rescanned every 250ms. Identity includes UID, proc inode and birth time. */
#define PROCESS_CACHE_SLOTS 64
#define PROCESS_CRITICAL_LIMIT 256
#define PROCESS_DISCOVERY_LIMIT 2048
typedef struct {
 pid_t pid;uid_t uid;ino_t inode;unsigned long long birth;
 double expires,warm_until;size_t count;pid_t tids[PROCESS_CRITICAL_LIMIT];
 size_t discovered_count;pid_t discovered[PROCESS_DISCOVERY_LIMIT];
} ProcessCache;
static ProcessCache process_cache[PROCESS_CACHE_SLOTS];
static unsigned long long top_signature;static int have_top_signature;
static int identity_state;
/* Failure evidence captured at the discrimination point, not at exit. */
static pid_t failed_pid;static const char *failed_stage;
static uid_t failed_uid_obs,failed_uid_cache;static ino_t failed_inode_obs,failed_inode_cache;
static unsigned long long failed_birth_obs,failed_birth_cache;static int failed_errno;
static void record_identity_failure(pid_t p,const char *stage,int e,uid_t uo,ino_t io,unsigned long long bo,uid_t uc,ino_t ic,unsigned long long bc){
 failed_pid=p;failed_stage=stage;failed_errno=e;
 failed_uid_obs=uo;failed_inode_obs=io;failed_birth_obs=bo;failed_uid_cache=uc;failed_inode_cache=ic;failed_birth_cache=bc;
 identity_state=-1;
}
/* 0=transient read failure, 1=identity read, -1=target gone or identity changed */
static int process_identity(pid_t pid,uid_t *uid,ino_t *inode,unsigned long long *birth) {
 char path[96],line[4096];struct stat st;
 snprintf(path,sizeof(path),"/proc/%d",pid);
 identity_state=0;
 if(stat(path,&st)){
  if(errno==ENOENT){record_identity_failure(pid,"stat_ENOENT",errno,0,0,0,0,0,0);return 0;}
  return 0;
 }
 *uid=st.st_uid;*inode=st.st_ino;
 snprintf(path,sizeof(path),"/proc/%d/stat",pid);FILE *f=fopen(path,"r");
 if(!f)return 0;int ok=fgets(line,sizeof(line),f)!=NULL;fclose(f);if(!ok)return 0;
 char *tail=strrchr(line,')');if(!tail)return 0;
 char *save=NULL,*tok=strtok_r(tail+2," ",&save);*birth=0;
 for(int field=3;tok;field++,tok=strtok_r(NULL," ",&save))if(field==22){
  char *end;*birth=strtoull(tok,&end,10);if(*end)return 0;break;
 }
 if(*birth==0)return 0;
 identity_state=1;return 1;
}
/* Core UI task IDs are still enumerated every active 100ms cycle.
 * Reuse name/classification discovery only while the exact sorted TID
 * set is unchanged. A new RenderThread is discovered in the same cycle;
 * identity and current eligibility are checked by the original callers.
 * Full role refresh remains bounded by the 500ms classification TTL.
 * Non-UI launch discovery intervals retain the existing warm behavior. */
/* Pure divergence classification between the entry identity read and the
 * post-discovery recheck read. 0=consistent; 1=uid or starttime changed
 * (proven replacement); 2=inode alone differs (cache-consistency event: the
 * snapshot is dropped and re-discovered via the bounded transient path, not
 * an identity change). */
static int identity_divergence_class(uid_t u1,ino_t i1,unsigned long long b1,uid_t u2,ino_t i2,unsigned long long b2){
 if(u1!=u2||b1!=b2)return 1;
 if(i1!=i2)return 2;
 return 0;
}

static ProcessCache *critical_process(pid_t pid,uid_t expected,int core_ui) {
 uid_t uid;ino_t inode;unsigned long long birth;
 if(!process_identity(pid,&uid,&inode,&birth))return NULL;
 if(uid!=expected || !allow_uid(uid)){record_identity_failure(pid,uid!=expected?"uid_mismatch":"uid_disallowed",0,uid,inode,birth,expected,inode,birth);return NULL;}
 ProcessCache *c=NULL,*oldest=&process_cache[0];
 for(int i=0;i<PROCESS_CACHE_SLOTS;i++){
  if(process_cache[i].pid==pid){c=&process_cache[i];break;}
  if(process_cache[i].expires<oldest->expires)oldest=&process_cache[i];
 }
 if(!c)c=oldest;
 int same_identity=c->pid==pid && c->uid==uid && c->inode==inode && c->birth==birth;
 if(core_ui && c->pid==pid && !same_identity){
  if(c->birth!=birth){
   /* starttime (birth) is unique per process incarnation: same pid with a
    * different birth is definitive PID reuse. */
   record_identity_failure(pid,"cache_birth_mismatch",0,uid,inode,birth,c->uid,c->inode,c->birth);
   return NULL;
  }
  /* Same pid, same uid, same birth, but inode differs alone: procfs dir
   * inode is not sufficient evidence of replacement. Invalidate this cache
   * entry and rebuild it; this is not a controller-level identity change. */
  memset(c,0,sizeof(*c));
 }
 if(!core_ui && same_identity && selection_time<c->expires)return c;
 double warm_until=core_ui?0:(same_identity?c->warm_until:selection_time+1);
 pid_t discovered[PROCESS_DISCOVERY_LIMIT];size_t count=0;
 char path[96];snprintf(path,sizeof(path),"/proc/%d/task",pid);
 DIR *d=opendir(path);if(!d)return NULL;struct dirent *e;directory_reads++;
 errno=0;
 while((e=readdir(d))){
  char *last;long t=strtol(e->d_name,&last,10);
  if(*last||t<=0||t>2147483647)continue;
  if(count==PROCESS_DISCOVERY_LIMIT){closedir(d);memset(c,0,sizeof(*c));return NULL;}
  discovered[count++]=(pid_t)t;
  errno=0;
 }
 int read_error=errno;closedir(d);
 if(read_error){memset(c,0,sizeof(*c));return NULL;}
 qsort(discovered,count,sizeof(*discovered),compare_pid);
 uid_t after_uid;ino_t after_inode;unsigned long long after_birth;
 /* Reuse follows the original cache-hit identity contract: the live
  * process identity was checked at entry and selected TIDs are checked by
  * the callers before admission/retention. A second process-stat read is
  * needed after classification rebuilding, not on every cache hit. */
 if(core_ui && same_identity && selection_time<c->expires && count==c->discovered_count && !memcmp(discovered,c->discovered,count*sizeof(*discovered)))return c;
 memset(c,0,sizeof(*c));thread_scans++;
 for(size_t i=0;i<count;i++){
  pid_t t=discovered[i];
  if(!classify_known_task(t,pid,core_ui))continue;
  if(c->count==PROCESS_CRITICAL_LIMIT){memset(c,0,sizeof(*c));return NULL;}
  c->tids[c->count++]=t;
 }
 if(!process_identity(pid,&after_uid,&after_inode,&after_birth)){memset(c,0,sizeof(*c));return NULL;}
 int divergence=identity_divergence_class(uid,inode,birth,after_uid,after_inode,after_birth);
 if(divergence==1){
  /* Both reads succeeded yet uid/birth differ: replaced mid-scan. */
  record_identity_failure(pid,"recheck_uid_birth_mismatch",0,after_uid,after_inode,after_birth,uid,inode,birth);
  memset(c,0,sizeof(*c));return NULL;
 }
 if(divergence==2){
  /* inode alone differs: the snapshot cannot be trusted, but this is not
   * evidence of replacement. Drop it and let the bounded transient path
   * re-discover; do not admit an untrusted snapshot and do not exit. */
  memset(c,0,sizeof(*c));return NULL;
 }
 c->pid=pid;c->uid=uid;c->inode=inode;c->birth=birth;c->warm_until=warm_until;
 c->expires=selection_time+(core_ui?.5:(selection_time<warm_until?.05:.25));
 if(core_ui){c->discovered_count=count;memcpy(c->discovered,discovered,count*sizeof(*discovered));}
 return c;
}
static size_t top_critical_tasks(pid_t *list,size_t cap){
 pid_t processes[8192];size_t pn=read_tasks("/dev/cpuctl/top-app/cgroup.procs",processes,8192),n=0;
 if(pn==(size_t)-1)return pn;
 qsort(processes,pn,sizeof(*processes),compare_pid);
 unsigned long long signature=1469598103934665603ULL;
 for(size_t i=0;i<pn;i++){signature^=(unsigned)processes[i];signature*=1099511628211ULL;}
 if(!have_top_signature || signature!=top_signature){
  for(int i=0;i<PROCESS_CACHE_SLOTS;i++)if(process_cache[i].pid!=ui_pid && process_cache[i].pid!=launcher_pid){process_cache[i].expires=0;process_cache[i].warm_until=selection_time+1;}
  top_signature=signature;have_top_signature=1;
 }
 for(size_t i=0;i<pn;i++){
  uid_t uid=uid_of(processes[i]);if(!allow_uid(uid) || uid==ui_uid || uid==launcher_uid)continue;
  ProcessCache *c=critical_process(processes[i],uid,0);if(!c)continue;
  for(size_t j=0;j<c->count;j++){
   pid_t t=c->tids[j];
   if(uid_of(t)!=uid || !critical_task(t,0) || !top_task(t))continue;
   if(n==cap)return (size_t)-1;list[n++]=t;
  }
 }return n;
}
static size_t ui_tasks(pid_t *list,size_t cap){
 pid_t pids[]={ui_pid,launcher_pid};size_t n=0;
 for(int i=0;i<2;i++){
  uid_t expected=i?launcher_uid:ui_uid;
  ProcessCache *c=critical_process(pids[i],expected,1);
  if(!c)return identity_state==-1?(size_t)-1:(size_t)-2;
  for(size_t j=0;j<c->count;j++){
   pid_t t=c->tids[j];
   if(uid_of(t)!=expected || !critical_task(t,1) || !ui_foreground_task(t))continue;
   if(n==cap)return (size_t)-1;list[n++]=t;
  }
 }qsort(list,n,sizeof(*list),compare_pid);return n;
}
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}
