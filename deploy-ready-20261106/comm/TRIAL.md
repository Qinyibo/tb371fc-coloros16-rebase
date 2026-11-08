# 通信共享 · 离线仅到试跑清单

**不适用离线通过。** 需真机手机配对、能力协商、建链、路由、手机流量网页实测。通话／短信单独验收。O+ Connect 电脑远控不算本项。

## 已核对身份

| 组件 | SHA-256／事实 |
| --- | --- |
| commcenterd | `25da3d0d…` 与 v17 一致 |
| oplus_vnet.ko | `01cb1335…` 与 v17 一致；V3 已观察到 ovnet0/1/2 |
| r94-commcenterd.rc | 全文在 handoff；`108b8e12…`；保留 oneshot |
| NAS | `NetworkAssistSys` OPEX／APK `2b2c65db…`；服务 `VirtualDataApiService`；启动日志节选已交，**未证明**对端协商 |
| OplusVirtualComm 新 | `7d8a11fe…`；v17 `959b3818…`（哈希不同 ≠ 回归结论） |
| WirelessSettings 集成 | 设备路径 `/system_ext/priv-app/WirelessSettings/WirelessSettings.apk` |

v17“开关两次可用”仅有口述／历史文档；`VCOMM_SHARE_NETWORK` 源码有、不能反推当时 UI。

## 试跑步骤（Codex／真机时）

1. 记录：平板 Wi‑Fi 开／关、是否连路由器、手机热点／共享开关初始态  
2. 打开无线设置里移动数据／共享相关项（勿假设缺省值是根因；勿自动双切）  
3. 手机配对 → 能力协商 → 建链 → 平板用手机流量打开网页  
4. 分别记：首次是否要二次开关、NAS 进程是否在、ovnet 接口、路由表  
5. 失败回退：恢复刷前 vendor／通信相关分区状态；本草案**不**附新通信差分  

禁止：编造“已共享成功”、把接口存在当成共享可用、叠白名单／永久调度。
