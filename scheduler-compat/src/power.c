#include "power.h"
#include <android/binder_ibinder.h>
#include <android/binder_parcel.h>
#include <android/binder_status.h>
#include <stdbool.h>
#include <stddef.h>

/* Platform service-manager API, linked against this donor's libbinder_ndk.
 * This declaration is not a replacement implementation or a private service.
 */
extern AIBinder *AServiceManager_checkService(const char *instance);

/* Extracted from this exact .600 framework IPowerManager.Stub. */
enum { TRANSACTION_IS_INTERACTIVE=0x15 };
static AIBinder *power;
static AIBinder_Class *power_class;
static void *proxy_create(void *data){return data;}
static void proxy_destroy(void *data){(void)data;}
static binder_status_t proxy_transact(AIBinder *binder,transaction_code_t code,
                                      const AParcel *in,AParcel *out) {
 (void)binder;(void)code;(void)in;(void)out;return STATUS_UNKNOWN_TRANSACTION;
}

int tb371fc_is_interactive(void) {
 if(!power_class)power_class=AIBinder_Class_define("android.os.IPowerManager",proxy_create,proxy_destroy,proxy_transact);
 if(!power_class)return -1;
 if(!power) {
  power=AServiceManager_checkService("power");
  if(!power)return -1;
  if(!AIBinder_associateClass(power,power_class)){AIBinder_decStrong(power);power=NULL;return -1;}
 }
 AParcel *in=NULL,*out=NULL;AStatus *exception=NULL;bool interactive=false;int result=-1;
 binder_status_t status=AIBinder_prepareTransaction(power,&in);
 if(status==STATUS_OK)status=AIBinder_transact(power,TRANSACTION_IS_INTERACTIVE,&in,&out,0);
 if(status==STATUS_OK)status=AParcel_readStatusHeader(out,&exception);
 if(status==STATUS_OK&&exception&&AStatus_isOk(exception)) {
  status=AParcel_readBool(out,&interactive);
  if(status==STATUS_OK)result=interactive?1:0;
 }
 if(exception)AStatus_delete(exception);
 if(in)AParcel_delete(in);if(out)AParcel_delete(out);
 if(result<0){AIBinder_decStrong(power);power=NULL;}
 return result;
}
