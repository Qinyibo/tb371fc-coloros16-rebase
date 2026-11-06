SELECT p.name AS process,p.pid,t.name AS thread,t.tid,s.state,
 MAX(s.ts,10975688277529) AS interval_start_ns,MIN(s.ts+s.dur,10975735834560)-MAX(s.ts,10975688277529) AS clipped_duration_ns,s.io_wait,s.blocked_function
 FROM thread_state s JOIN thread t USING(utid) JOIN process p USING(upid)
 WHERE s.dur>0 AND s.ts<10975735834560 AND s.ts+s.dur>10975688277529
 AND (p.upid=752 OR p.name IN ('com.android.launcher','com.android.systemui','/system/bin/surfaceflinger'))
 AND (t.tid=p.pid OR t.name='RenderThread' OR t.name GLOB 'hwuiTask*' OR t.name IN ('wmshell.main','RE Completion','RenderEngine')) ORDER BY s.ts;
