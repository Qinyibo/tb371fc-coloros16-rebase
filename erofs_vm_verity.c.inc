#include <linux/dm-ioctl.h>
#include <sys/ioctl.h>
#include <sys/sysmacros.h>
static void init_dm(struct dm_ioctl *d, size_t size) {
 memset(d,0,size);d->version[0]=4;d->data_size=size;d->data_start=sizeof(*d);
 snprintf(d->name,sizeof(d->name),"runtime-apex-verify");
}
static int verity(void) {
 int c=open("/dev/mapper/control",O_RDWR); if(c<0){perror("DM control");return -1;}
 struct { struct dm_ioctl d; struct dm_target_spec target; char params[1024]; } buf;
 init_dm(&buf.d,sizeof(buf));
 if(ioctl(c,DM_DEV_CREATE,&buf)<0){perror("DM create");return -1;}
 dev_t dev=buf.d.dev;
 init_dm(&buf.d,sizeof(buf));buf.d.target_count=1;buf.d.flags=DM_READONLY_FLAG;
 buf.target.length=AVB_DATA_BYTES/512;
 snprintf(buf.target.target_type,sizeof(buf.target.target_type),"verity");
 int n=snprintf(buf.params,sizeof(buf.params),"1 /dev/vda /dev/vda 4096 4096 %u %u sha256 %s %s",
     AVB_DATA_BYTES/4096, AVB_TREE_OFFSET/4096, AVB_ROOT_DIGEST, AVB_SALT);
 if(n<0||n>=sizeof(buf.params))return -1;
 buf.target.next=(sizeof(buf.target)+n+1+7)&~7;
 if(ioctl(c,DM_TABLE_LOAD,&buf)<0){perror("DM load");return -1;}
 init_dm(&buf.d,sizeof(buf));buf.d.flags=DM_READONLY_FLAG;
 if(ioctl(c,DM_DEV_SUSPEND,&buf)<0){perror("DM resume");return -1;}
 close(c);
 if(mknod("/dev/verity-apex",S_IFBLK|0600,dev)<0){perror("DM node");return -1;}
 printf("DM_VERITY_READY length=%u\n",AVB_DATA_BYTES);
 return 0;
}
