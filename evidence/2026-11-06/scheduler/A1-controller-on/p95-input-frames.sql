CREATE PERFETTO TABLE frames AS
 SELECT CASE WHEN f.layer_name LIKE '%com.ss.android.ugc.aweme/%' THEN 'com.ss.android.ugc.aweme' ELSE p.name END AS app,
 f.upid,f.surface_frame_token,MIN(f.ts) AS ts,MAX(f.dur) AS dur,
 MAX(f.jank_type GLOB '*App Deadline Missed*') AS missed,MAX(f.present_type='Late Present') AS late
 FROM actual_frame_timeline_slice f JOIN process p USING(upid)
 WHERE f.ts>=10923090000000 AND f.ts+f.dur<=10939810000000 AND f.dur>0 AND f.surface_frame_token>0
 GROUP BY app,f.upid,f.surface_frame_token;
 SELECT app,upid,surface_frame_token,ts AS frame_start_ns,dur AS timeline_duration_ns,missed,late FROM frames
 WHERE app IN ('com.ss.android.ugc.aweme','com.android.launcher','com.android.systemui') ORDER BY app,ts;
