#!/system/bin/sh
echo "NOW=$(date '+%Y-%m-%d %H:%M:%S')"
echo "PID=$(pidof com.luna.music)"
echo "TOMBSTONES_TOP:"
ls -lt /data/tombstones 2>/dev/null | head -15
echo "HEAP_HITS_LAST_MINUTES:"
# scan newest tombstones for HeapTaskDaemon / luna
for t in $(ls -t /data/tombstones/tombstone_* 2>/dev/null | head -10); do
  if grep -q HeapTaskDaemon "$t" 2>/dev/null; then
    echo "HEAP_IN $t"
    grep -m1 -E '>>>|Process name|Timestamp|HeapTaskDaemon' "$t" 2>/dev/null
    ls -l "$t"
  fi
done
# also check if any tombstone mtime is after our start window (today after 16:30 local)
echo "FILES_MTIME_TODAY_AFTER_1630:"
ls -lt /data/tombstones 2>/dev/null | head -10