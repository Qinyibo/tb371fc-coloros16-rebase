#!/bin/bash
set -eu
root=/mnt/d/TB371FC-release/clean-rebase-20261104
mkdir -p "$root/tb-readback"
debugfs -R "dump /etc/vintf/manifest.xml $root/tb-readback/vendor-manifest.xml" "$root/tb-inputs/vendor_a.img"
debugfs -R "dump /etc/fstab.qcom $root/tb-readback/fstab.qcom" "$root/tb-inputs/vendor_a.img"
debugfs -R "dump /build.prop $root/tb-readback/vendor-build.prop" "$root/tb-inputs/vendor_a.img"
debugfs -R "rdump /etc/vintf $root/tb-readback" "$root/tb-inputs/vendor_a.img"
debugfs -R "ls -l /apex" /mnt/d/TB371FC-release/v26-r104-build/system_ext_a.img > "$root/tb-readback/system-ext-apex.txt" 2>&1
for name in system_ext product my_product vendor odm; do
  test -f "$root/donor-images/$name.img"
  test ! -e "$root/donor-tree/$name"
  mkdir "$root/donor-tree/$name"
  fsck.erofs --extract="$root/donor-tree/$name" "$root/donor-images/$name.img" > "$root/fsck-$name.log" 2>&1
  echo "EROFS_EXTRACT_PASS $name"
done
