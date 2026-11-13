# DO NOT APPLY

`hardware_success_claimed=false`

这个目录是警告样本，不是修复，不要执行 `install_tinno_vintf.sh`。

该脚本 `mount -o remount,rw /vendor`，并只拷入 `vendor.qti.hardware.tinno_keyboard@1.0-service.xml`。库存 `compatibility_matrix.xml` 的名字是 `vendor.mediatek.hardware.tinno_keyboard`，HAL 是 `vendor.qti.hardware.tinno_keyboard`。只加 device manifest、不改矩阵，会 VINTF 失败并 bootloop。remount rw 还会破坏 dm-verity，事后删掉片段也不能把 verity 树补回来。

成对、systemless、不写 vendor 分区的做法在 `packages/tinno_vintf_pair_20261109/`。不要用关闭 verity 或改 vbmeta 来绕过半套片段。
