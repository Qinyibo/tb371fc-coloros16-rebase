# 用户反馈与当时负载

用户在此前重载采集后报告“太卡了”。本地 V5／V6 深度分析记录，V5 操作偏抖音、汽水音乐和微信小程序，V6 偏微信、QQ。工作负载不同，不能单凭这两轮断言 V6 单项改动导致退化。原报告 `D:/TB371FC-release/clean-rebase-20261104/scheduler-compat/deep-analysis/JANK_ROOT_CAUSE_DEEP_ANALYSIS_20261105.md`。

仓库三轮开启／撤出／恢复是另一次抖音单应用对照。详见既有 evidence 的 protocol、时间窗口和逐帧数据。用户反馈与该组数据没有逐秒对齐的前台记录。汽水曾在 A1 时间窗有 CPU 活动，不能据此判定帧差来源。
