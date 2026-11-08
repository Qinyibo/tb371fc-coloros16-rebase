#!/system/bin/sh
SKIPUNZIP=0
ui_print "- TB371FC 鲸鲮 Office V2.1 systemize"
ui_print "- package com.yozo.office -> system/app/YozoOffice/YozoOffice.apk"
ui_print "- source SHA-256 0CC7977DB6C35EAB3DD3E919800B06D59D0035A819F30FA464726AEB5E508461"
ui_print "- versionName 3.1.3813.1 / versionCode 313813 (modified+fonts build)"
ui_print "- Keep T2/refresh/FWUI/fantasy/pen/luna/interconnect untouched"
set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/system/app/YozoOffice/YozoOffice.apk" 0 0 0644