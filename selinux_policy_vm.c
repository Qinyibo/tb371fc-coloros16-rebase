#define _GNU_SOURCE
#include <sys/mount.h>
#include <sys/reboot.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
static int read_file(const char *path,char *dst,size_t n) {
 int fd=open(path,O_RDONLY); if(fd<0)return -1;
 int r=read(fd,dst,n-1);close(fd);if(r<0)return -1;
 dst[r]=0;dst[strcspn(dst,"\n")]=0;return r;
}
int main(void) {
 setvbuf(stdout,NULL,_IONBF,0);char version[64],before[16],after[16];
 if(mount("selinuxfs","/selinux","selinuxfs",0,NULL)<0){perror("mount selinuxfs");goto stop;}
 if(read_file("/selinux/policyvers",version,sizeof(version))<0||
    read_file("/selinux/enforce",before,sizeof(before))<0){perror("selinux state");goto stop;}
 int p=open("/policy",O_RDONLY),l=open("/selinux/load",O_WRONLY);
 struct stat st;
 if(p<0||l<0||fstat(p,&st)<0){perror("policy open");goto stop;}
 void *data=mmap(NULL,st.st_size,PROT_READ,MAP_PRIVATE,p,0);
 if(data==MAP_FAILED){perror("policy map");goto stop;}
 printf("POLICY_PRE version=%s enforcing=%s bytes=%lld\n",version,before,(long long)st.st_size);
 errno=0;ssize_t w=write(l,data,st.st_size);int e=errno;
 if(read_file("/selinux/enforce",after,sizeof(after))<0)strcpy(after,"unavailable");
 printf("POLICY_LOAD written=%lld expected=%lld errno=%d enforcing_after=%s\n",(long long)w,(long long)st.st_size,e,after);
stop:
 reboot(RB_POWER_OFF);for(;;)pause();
}
