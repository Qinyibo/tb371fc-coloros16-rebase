#!/system/bin/sh
echo "NOW=$(date '+%Y-%m-%d %H:%M:%S')"
echo "TOMBSTONES_RECENT:"
ls -lt /data/tombstones 2>/dev/null | head -20
echo "---"
# any HeapTaskDaemon mentions in latest tombstones
for t in /data/tombstones/tombstone_*; do
  [ -f "$t" ] || continue
  # skip if older than ~30 min via mtime print
  echo "CHECK $t $(ls -l $t | awk '{print $6,$7,$8}')"
done