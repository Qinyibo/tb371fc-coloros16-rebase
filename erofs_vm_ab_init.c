#define _GNU_SOURCE
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/reboot.h>
#include <sys/types.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int files,dirs,links,errors;
static unsigned long long bytes;
static void compare(const char *rel) {
 char a[4096],b[4096];snprintf(a,sizeof(a),"/erofs/%s",rel);snprintf(b,sizeof(b),"/reference/%s",rel);
 struct stat x,y;
 if(lstat(a,&x)||lstat(b,&y)){printf("FAIL stat %s errno=%d\n",rel,errno);errors++;return;}
 if((x.st_mode&S_IFMT)!=(y.st_mode&S_IFMT)){printf("FAIL type %s\n",rel);errors++;return;}
 if(!S_ISLNK(x.st_mode)&&(x.st_mode!=y.st_mode||x.st_uid!=y.st_uid||x.st_gid!=y.st_gid)){printf("FAIL metadata %s\n",rel);errors++;}
 if(S_ISDIR(x.st_mode)) {
  dirs++;DIR *d=opendir(b);if(!d){errors++;return;}struct dirent *e;
  while((e=readdir(d))) {if(!strcmp(e->d_name,".")||!strcmp(e->d_name,".."))continue;char child[4096];snprintf(child,sizeof(child),"%s%s%s",rel,*rel?"/":"",e->d_name);compare(child);}closedir(d);
 } else if(S_ISLNK(x.st_mode)) {
  links++;char aa[4096],bb[4096];ssize_t na=readlink(a,aa,sizeof(aa)),nb=readlink(b,bb,sizeof(bb));if(na<0||na!=nb||memcmp(aa,bb,na)){printf("FAIL link %s\n",rel);errors++;}
 } else if(S_ISREG(x.st_mode)) {
  files++;if(x.st_size!=y.st_size){printf("FAIL size %s\n",rel);errors++;return;}
  int fa=open(a,O_RDONLY),fb=open(b,O_RDONLY);if(fa<0||fb<0){errors++;if(fa>=0)close(fa);if(fb>=0)close(fb);return;}
  char aa[65536],bb[65536];ssize_t n,m;
  for(;;){n=read(fa,aa,sizeof(aa));m=read(fb,bb,sizeof(bb));if(n<0||m<0||n!=m||(n>0&&memcmp(aa,bb,n))){printf("FAIL bytes %s\n",rel);errors++;break;}if(!n)break;bytes+=n;}
  close(fa);close(fb);
 }
}
int main(void) {
 setvbuf(stdout,NULL,_IONBF,0);setvbuf(stderr,NULL,_IONBF,0);
 mount("proc","/proc","proc",0,NULL);mount("sysfs","/sys","sysfs",0,NULL);mount("devtmpfs","/dev","devtmpfs",0,NULL);
 for(int i=0;i<10&&access("/dev/vda",F_OK);i++)sleep(1);
 int f=open("/trial.ko",O_RDONLY);
 int k=f<0?-1:syscall(SYS_finit_module,f,"",0),ke=errno;
 if(f>=0)close(f);
 printf("MODULE load=%d errno=%d\n",k,ke);
 int a=k?-1:mount("/dev/vda","/erofs","erofs_ab",MS_RDONLY,NULL),ea=errno;
 int b=0,eb=0;
 printf("MOUNT compressed=%d errno=%d reference=%d errno=%d\n",a,ea,b,eb);
 if(a||b)errors++;else compare("");
 /* This test is pinned to the acquired runtime APEX, never an empty tree. */
 if(files!=21||dirs!=8||links!=15||bytes!=12134185ULL)errors++;
 printf("RESULT files=%d dirs=%d links=%d bytes=%llu errors=%d\n",files,dirs,links,bytes,errors);
 int u=umount("/erofs"),ue=errno;
 int unload=syscall(SYS_delete_module,"erofs",O_NONBLOCK),ule=errno;
 printf("MODULE unmount=%d errno=%d unload=%d errno=%d\n",u,ue,unload,ule);
 sync();reboot(RB_POWER_OFF);return errors?1:0;
}
