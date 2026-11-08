# 竖屏多任务／流畅度 · 观察与试跑边界

## 竖屏多任务

handoff `recents/original-paths.json` + 脚本。既有：第 4／8 次右滑几何一致；旋转轮退回桌面 ≠ 合格后台。  
**本轮不部署边界补丁。** 真机复现仍用第三方重载场景；原图在 D 盘。

## 调度／流畅度

A1／B／A2 Perfetto 原 trace 路径见 `scheduler/trace-paths.json`。缺合格预热与内容身份 → **不得**从现有 P95 裁决永久保留或移除自定义 schedtune。  
GPU min_pwrlevel=4 仅有历史同次对照支持“该次等待受益”，非整体流畅证明。  
`anim_level` ≠ 刷新率／HWC／SF／芯片追帧证明。EROFS 内核叠加 ≠ 完整已装内核。

主观仍卡备注见 `scheduler/subjective-feedback.md`（不足绑定秒级前台）。

## 试跑（若做）

1. 同条件 remove／restore 自定义调度，完整预热后再比第三方 App  
2. 不用系统 App／合成 benchmark 替代  
3. 无稳定收益且无副作用证据前：保持现状，不叠参数  

本项交付物止于试跑清单，不宣称可部署通过。

## �ȴ�ϸ��֣�2026-11-06 �ƽ���

��ֹ force-stop���ű�: `warm-interrupt-trial.ps1`��
�������ֺ�����: `blackscreen-capture.ps1`��
