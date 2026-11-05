#define main native_service_main
#include "../src/runtime.c"
#undef main
int main(void) {
 if(getuid()!=0)return 2;
 if(!discover_ui()){fprintf(stderr,"IDENTITY_DISCOVERY_NOT_VERIFIED errno=%d\n",errno);return 25;}
 pid_t top[8192],ui[8192];selection_time=now();size_t tn=top_critical_tasks(top,8192);
 selection_time=now();size_t un=ui_tasks(ui,8192);
 if(tn==(size_t)-1||un==(size_t)-1||un==(size_t)-2){fprintf(stderr,"NATIVE_SELECTION_NOT_VERIFIED errno=%d identity=%d\n",errno,identity_state);return 9;}
 int power_state=display_on();if(power_state<0){fprintf(stderr,"POWER_ENDPOINT_NOT_VERIFIED\n");return 22;}
 printf("READ_ONLY_IDENTITY ui_pid=%d ui_uid=%u home_pid=%d home_uid=%u interactive=%d\n",ui_pid,ui_uid,launcher_pid,launcher_uid,power_state);
 printf("ELIGIBLE_TOP");for(size_t i=0;i<tn;i++)printf(" %d",top[i]);puts("");
 printf("ELIGIBLE_UI");for(size_t i=0;i<un;i++)printf(" %d",ui[i]);puts("");
 printf("READ_ONLY_SELECTION_COMPLETE top=%zu ui=%zu cgroup_writes=0\n",tn,un);
 return 0;
}
