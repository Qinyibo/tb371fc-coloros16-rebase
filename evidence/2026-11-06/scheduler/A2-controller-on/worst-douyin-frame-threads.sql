SELECT p.name AS process,p.pid,t.name AS thread,t.tid,s.state,
 MAX(s.ts,11022371064127) AS interval_start_ns,MIN(s.ts+s.dur,11022415180637)-MAX(s.ts,11022371064127) AS clipped_duration_ns,s.io_wait,s.blocked_function
 FROM thread_state s JOIN thread t USING(utid) JOIN process p USING(upid)
 WHERE s.dur>0 AND s.ts<11022415180637 AND s.ts+s.dur>11022371064127
 AND (p.upid=1 OR p.name IN ('com.android.launcher','com.android.systemui','/system/bin/surfaceflinger'))
 AND (t.tid=p.pid OR t.name='RenderThread' OR t.name GLOB 'hwuiTask*' OR t.name IN ('wmshell.main','RE Completion','RenderEngine')) ORDER BY s.ts;
