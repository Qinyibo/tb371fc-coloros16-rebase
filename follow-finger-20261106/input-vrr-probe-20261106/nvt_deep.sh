#!/system/bin/sh
echo ===PROC===
ls -la /proc/nvt* 2>/dev/null
ls -la /proc/*nvt* 2>/dev/null
for f in /proc/nvt*; do
  echo FILE $f
  cat "$f" 2>/dev/null | head -c 800
  echo
done
echo ===SYSFS_FIND===
find /sys -iname '*nvt*' 2>/dev/null | head -100
echo ===SPI_DRIVER===
ls -la /sys/bus/spi/drivers/NVT-ts/ 2>/dev/null
ls -la /sys/bus/spi/devices/ 2>/dev/null
for d in /sys/bus/spi/drivers/NVT-ts/spi*; do
  echo DIR $d
  ls -la "$d" 2>/dev/null | head -80
done
echo ===SPI0===
find /sys/devices -path '*spi0.0*' 2>/dev/null | head -120
echo ===INPUT8===
ls -la /sys/devices/virtual/input/input8/ 2>/dev/null
ls -la /sys/class/input/event4/device/ 2>/dev/null | head -60
