#define _GNU_SOURCE
#include <linux/loop.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/reboot.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int files,dirs,links,errors,random_reads;
static unsigned long long bytes;
static char root[64];
static void fail(const char *type,const char *name) {
 printf("FAIL %s %s errno=%d\n",type,name,errno);errors++;
}
static void compare(const char *rel) {
 char a[8192],b[8192];
 if(snprintf(a,sizeof(a),"/erofs/%s",rel)>=sizeof(a)||
    snprintf(b,sizeof(b),"%s/%s",root,rel)>=sizeof(b)) {fail("path",rel);return;}
 struct stat x,y;
 if(lstat(a,&x)||lstat(b,&y)){fail("stat",rel);return;}
 if((x.st_mode&S_IFMT)!=(y.st_mode&S_IFMT)){fail("type",rel);return;}
 if((!S_ISLNK(x.st_mode)&&x.st_mode!=y.st_mode)||x.st_uid!=y.st_uid||x.st_gid!=y.st_gid)fail("metadata",rel);
 if(S_ISDIR(x.st_mode)) {
  dirs++;DIR *d=opendir(b);if(!d){fail("opendir reference",rel);return;}
  struct dirent *e;
  int expected=0,actual=0;
  while((e=readdir(d))) {
   if(!strcmp(e->d_name,".")||!strcmp(e->d_name,".."))continue;
   expected++; char child[8192];
   if(snprintf(child,sizeof(child),"%s%s%s",rel,*rel?"/":"",e->d_name)>=sizeof(child)){fail("child",rel);continue;}
   compare(child);
  }
  closedir(d);
  d=opendir(a);if(!d){fail("opendir source",rel);return;}
  while((e=readdir(d)))if(strcmp(e->d_name,".")&&strcmp(e->d_name,".."))actual++;
  closedir(d);
  if(expected!=actual)fail("directory count",rel);
 } else if(S_ISLNK(x.st_mode)) {
  links++;char aa[8192],bb[8192];ssize_t na=readlink(a,aa,sizeof(aa)),nb=readlink(b,bb,sizeof(bb));if(na<0||na!=nb||memcmp(aa,bb,na))fail("link",rel);
 } else if(S_ISREG(x.st_mode)) {
  files++;if(x.st_size!=y.st_size){fail("size",rel);return;}
  int fa=open(a,O_RDONLY),fb=open(b,O_RDONLY);
  if(fa<0||fb<0){fail("open",rel);if(fa>=0)close(fa);if(fb>=0)close(fb);return;}
  char aa[65536],bb[65536];ssize_t n,m;
  if(x.st_size>4096) {
   uint64_t s=(uint64_t)x.st_size;
   for(int k=0;k<12;k++) {
    s=s*6364136223846793005ULL+1442695040888963407ULL;
    off_t off=(off_t)(s%(x.st_size-511));
    /* First reads after opening each loop-mounted file are deliberately nonsequential. */
    n=pread(fa,aa,511,off);m=pread(fb,bb,511,off);
    if(n!=511||m!=511||memcmp(aa,bb,511)){fail("random bytes",rel);break;}random_reads++;
   }
  }
  for(;;){n=read(fa,aa,sizeof(aa));m=read(fb,bb,sizeof(bb));if(n<0||m<0||n!=m||(n>0&&memcmp(aa,bb,n))){fail("sequential bytes",rel);break;}if(!n)break;bytes+=n;}
  close(fa);close(fb);
 } else fail("unknown file type",rel);
}
int main(void) {
 setvbuf(stdout,NULL,_IONBF,0);setvbuf(stderr,NULL,_IONBF,0);
 if(mount("proc","/proc","proc",0,NULL)||mount("sysfs","/sys","sysfs",0,NULL)||mount("devtmpfs","/dev","devtmpfs",0,NULL))goto stop;
 int f=open("/trial.ko",O_RDONLY);
 if(f<0||syscall(SYS_finit_module,f,"",0))goto stop;
 close(f);
 FILE *pkgs=fopen("/packages","r");if(!pkgs)goto stop;
 char pkg[1024];int idx=0,total=0;
 while(fgets(pkg,sizeof(pkg),pkgs)) {
  pkg[strcspn(pkg,"\n")]=0;
  char path[64]; snprintf(path,sizeof(path),"/payload/%d",idx);
  snprintf(root,sizeof(root),"/reference/%d",idx++);
  files=dirs=links=errors=random_reads=0;bytes=0;
  int image=open(path,O_RDONLY),loop=open("/dev/loop0",O_RDONLY);
  if(image<0||loop<0||ioctl(loop,LOOP_SET_FD,image)){fail("loop attach",pkg);}
  else {
   if(mount("/dev/loop0","/erofs","erofs_ab",MS_RDONLY,"cache_strategy=disabled"))fail("mount",pkg);
   else { compare("");if(umount("/erofs"))fail("unmount",pkg); }
   if(ioctl(loop,LOOP_CLR_FD,0))fail("loop detach",pkg);
  }
  if(image>=0)close(image);
  if(loop>=0)close(loop);
  printf("APEX %s files=%d dirs=%d links=%d bytes=%llu random_reads=%d errors=%d\n",pkg,files,dirs,links,bytes,random_reads,errors);
  total+=errors;
 }
 fclose(pkgs);
 printf("BATCH packages=%d errors=%d\n",idx,total);
 reboot(RB_POWER_OFF);return total?1:0;
stop:printf("FATAL init errno=%d\n",errno);reboot(RB_POWER_OFF);return 1;
}
