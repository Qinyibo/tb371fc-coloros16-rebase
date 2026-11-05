#define _GNU_SOURCE
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/sysmacros.h>
#include <sys/ioctl.h>
#include <sys/wait.h>
#include <linux/loop.h>
#include <sched.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char **argv) {
 int rc=1,loaded=0,attached=0,mounted=0,ctl=-1,loop=-1,image=-1,ko=-1,number=-1,private_node=0;
 char mod[4096],img[4096],manifest[4096],mnt[4096],node[4096],line[512];
 setvbuf(stdout,NULL,_IONBF,0);setvbuf(stderr,NULL,_IONBF,0);
 const char *prefix="/data/local/tmp/tb371fc-clean-rebase-erofs-";
 if(argc!=2||geteuid()!=0||strncmp(argv[1],prefix,strlen(prefix))){fprintf(stderr,"invalid probe scope\n");return 2;}
 snprintf(mod,sizeof(mod),"%s/erofs.ko",argv[1]);snprintf(img,sizeof(img),"%s/runtime.img",argv[1]);snprintf(manifest,sizeof(manifest),"%s/expected.sha256",argv[1]);snprintf(mnt,sizeof(mnt),"%s/mount",argv[1]);snprintf(node,sizeof(node),"%s/loop-device",argv[1]);
 FILE *mods=fopen("/proc/modules","r");if(!mods)return 3;
 while(fgets(line,sizeof(line),mods)) {
  if(!strncmp(line,"erofs ",6)){fclose(mods);fprintf(stderr,"preexisting erofs module; untouched\n");return 4;}
 }
 fclose(mods);
 if(unshare(CLONE_NEWNS)||mount(NULL,"/",NULL,MS_REC|MS_PRIVATE,NULL)){perror("private namespace");goto cleanup;}
 puts("NS_PRIVATE_OK");
 ko=open(mod,O_RDONLY|O_CLOEXEC);if(ko<0||syscall(__NR_finit_module,ko,"",0)){perror("finit_module");goto cleanup;}loaded=1;close(ko);ko=-1;puts("MODULE_LOADED");
 image=open(img,O_RDONLY|O_CLOEXEC);ctl=open("/dev/loop-control",O_RDWR|O_CLOEXEC);
 if(image<0||ctl<0||(number=ioctl(ctl,LOOP_CTL_GET_FREE))<0){perror("loop-control");goto cleanup;}
 /* This kernel uses loop.max_part=7: loop index is not the block minor.
  * Read the authoritative sysfs device number, and prefer ueventd's node. */
 char sysdev[256],canonical[256];unsigned int maj,min;
 snprintf(sysdev,sizeof(sysdev),"/sys/class/block/loop%d/dev",number);
 FILE *dev=fopen(sysdev,"r");if(!dev){perror("loop sysfs");goto cleanup;}
 int fields=fscanf(dev,"%u:%u",&maj,&min);fclose(dev);if(fields!=2){fprintf(stderr,"invalid loop dev number\n");goto cleanup;}
 snprintf(canonical,sizeof(canonical),"/dev/block/loop%d",number);
 struct stat st;
 if(!stat(canonical,&st)&&S_ISBLK(st.st_mode)&&st.st_rdev==makedev(maj,min))snprintf(node,sizeof(node),"%s",canonical);
 else {if(mknod(node,S_IFBLK|0600,makedev(maj,min))){perror("private loop node");goto cleanup;}private_node=1;}
 printf("LOOP_NODE=%s dev=%u:%u\n",node,maj,min);
 loop=open(node,O_RDWR|O_CLOEXEC);if(loop<0||ioctl(loop,LOOP_SET_FD,image)){perror("LOOP_SET_FD");goto cleanup;}attached=1;
 struct loop_info64 info={0};info.lo_flags=LO_FLAGS_READ_ONLY|LO_FLAGS_AUTOCLEAR;
 if(ioctl(loop,LOOP_SET_STATUS64,&info)){perror("LOOP_SET_STATUS64");goto cleanup;}
 if(mkdir(mnt,0700)&&errno!=EEXIST){perror("mkdir");goto cleanup;}
 if(mount(node,mnt,"erofs",MS_RDONLY|MS_NODEV|MS_NOSUID|MS_NOEXEC,NULL)){perror("mount erofs");goto cleanup;}mounted=1;puts("EROFS_MOUNTED_PRIVATE_READONLY");
 pid_t child=fork();if(child<0){perror("fork");goto cleanup;}
 if(!child){if(chdir(mnt))_exit(125);execl("/system/bin/toybox","toybox","sha256sum","-c",manifest,(char*)NULL);_exit(126);}
 int status;if(waitpid(child,&status,0)!=child){perror("waitpid");goto cleanup;}
 printf("HASH_CHILD_STATUS=%d\n",status);if(!WIFEXITED(status)||WEXITSTATUS(status))goto cleanup;rc=0;
cleanup:
 if(ko>=0)close(ko);
 if(mounted){if(umount2(mnt,0)){perror("unmount");rc=1;}else puts("UNMOUNTED");}
 if(attached){if(ioctl(loop,LOOP_CLR_FD,0)){perror("LOOP_CLR_FD");rc=1;}else puts("LOOP_CLEARED");}
 if(loop>=0)close(loop);
 if(image>=0)close(image);
 if(ctl>=0)close(ctl);
 if(private_node)unlink(node);
 if(loaded){if(syscall(__NR_delete_module,"erofs",O_NONBLOCK)){perror("delete_module");rc=1;}else puts("MODULE_UNLOADED");}
 printf("PROBE_RESULT=%d\n",rc);return rc;
}
