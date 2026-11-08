# dynframe A side (module ON) — 2026-11-06 14:47 Asia/Hong_Kong
MD5 live=fb92391a… (89×144, 0×120)
SAME PIDs: mm=9191 aweme=14298 luna=9150
PickRate=144 Preferred=[4,4,2,4]

| App | frames | janky% | p90 | High input latency (count) | count/frames |
| WeChat | 1569 | 11.15 | 16ms | 2112 | 1.35 |
| Douyin | 723 | 23.79 | 25ms | 987 | 1.37 |
| Luna | 1956 | 20.04 | 26ms | 2987 | 1.53 |

Pre-trial baseline (warm-switch-gfx-20261106-144225, before dynframe):
| WeChat | 430 | 16.74 | 23ms | 669 | 1.56 |
| Douyin | 311 | 29.26 | 46ms | 379 | 1.22 |
| Luna | 411 | 32.60 | 38ms | 504 | 1.23 |

Note: frame counts differ (more swipe load on A). Running B (module OFF) next with same protocol.
hardware_success_claimed=false
