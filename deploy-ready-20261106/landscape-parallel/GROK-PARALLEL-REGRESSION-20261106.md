# 给 Grok · 平行视窗新旧包差异与最小修复面

**结论**：保留新 Settings 16.1.0，先修逐应用规则和实际加载来源。完整列表、横屏单窗、可交互双窗是三个独立验收项。以下仅核对 D 盘原有文件，未执行任何设备脚本。 `hardware_success_claimed=false`。

## 已核对的差异

- **列表入口已经存在。** `ui-deploy-20261106/verify/parallel-ui-attempt2.xml` 在后续 FWUI 替换之前已录到 12 个应用的开关，和 `parallel-ui-after-fwui.xml` 一致。页面属于 Settings 的 `ParallelWorldFragment`，无需用 R94 Settings 16.0.0 覆盖新版本。新母包主 fantasy 表有 3026 条，2881 条 status=1。旧 R94 主表和 secondary 分别有 2263、743 条。静态名单规模解释不了每个应用能否双窗。
- **全屏策略曾覆盖双窗。** bulk 阶段将包括微信在内的 FO 拉到 `status=1, rao:true`，现场出现了 `mIsFullOrientation=true`。原厂 FO 在已对比的微信、B 站、QQ、抖音四行与旧原厂状态相同，分别为 2、0、2、2。应按应用与 Activity 管理冲突。
- **B 站是第一例可核对的回归。** R94 旧运行库 `magicwindow.status=1, installed=1, data_sources=2`，`config` 212 字节，`activityPairs` 有 `tv.danmaku.bili.MainActivityV2 → *` 与 `com.bilibili.search.main.BiliMainSearchActivity → *`，FO=0。最近已保存的新包 `qq-oldrestore-20261106/verify/fantasywindow.live-final.db` 同样 magic=1、installed=1，但 `data_sources=1` 且 `config` 为空，只有 `custom_config_body`，其中无 `activityPairs`。新快照仍有 `scaleWindow=-1`、PAD 窗口比例、直播全屏例外和新登录 Activity 例外，应该保留。该快照 FO=2、installed=0；同批最终产品 XML 的 B 站 FO=1、`rao:true`。这是保存材料间的差异，设备当前选用哪个来源需现场只读核对，不能直接断言 FO=1 正在生效。
- **微信当阳性对照，QQ 当反例。** 微信两边运行库均有约 8 KB 主配置，新包材料仍录到 app 自己组织相邻 TaskFragment。QQ 在旧 R94 数据库是 magic=2、`excludeDevice=FOLD|PAD`、`forceBlock=true`。此前强加 TIM 配对只进入单窗 magic；`GuildBlankActivity` 拼出两个容器后无法获得焦点。更新的 `qq-oldrestore-20261106/verify/verify-out.txt` 已看到 QQ 回到 FO=1、2944×1840 全屏，`sz=1`。以这份为准，别把更早的 v3 单窗描述当作最新。现有证据不支持把 QQ 当成旧版真双窗回归。

## 给 Grok 的单例任务

1. 先以 **B 站** 还原旧表现。用同版 B 站依次试首页→视频详情、搜索→结果页、进入／退出直播。先读实际加载的主／secondary／ROM Update 规则版本，以及 `t_config` 的 `status, installed, data_sources, config, custom_mode, custom_config_body`。同时记录 WM 的任务、两个可见窗格的 Activity 和 bounds、焦点。
2. 只定位为何老运行库的两条 `activityPairs` 没进入新运行库。核对当前 `OplusExSystemService` 的合并路径，确认从哪种构建时规则载入，确认 FO 对普通页和直播例外的优先级。能通过现有 schema 表达时，只合并这两条配对及必要的 FO 冲突修正，保留新包其余 app 规则和已有 Activity 例外。旧库、旧 Settings/FWUI 均可用于比对，交付不依赖运行库整库覆盖或反复写回。
3. 通过标准是普通详情和搜索两侧都可见、可交互、返回正常，直播仍走原全屏例外。一次正常重启后还要读回同一有效规则并重测，排除云规则覆盖或临时 DB 同步。若仅出现 Settings 开关、一个居中窗或无焦点的第二容器，判失败。B 站过关后才按同法挑下一款旧包已验证的应用。

## 本地证据入口

- 旧运行库 `D:/TB371FC-work/codex-20261028/WeChat-fantasywindow-readonly.db`，同目录 `sys_fantasy_window_managed-native-original.xml`、`sys_fantasy_window_managed_secondary-native-original.xml`。
- 旧构建源和验收 `D:/TB371FC-release/public-source/TB371FC-ColorOS16/patches/native-window-rules.json`、`docs/parallel-windows.md`。旧 R94 还有单独的 B 站居中宽度修改，双窗跑通后再核对几何；无需先移植其全量框架补丁。
- 新包保存的读回 [qq-oldrestore-20261106/verify/](qq-oldrestore-20261106/verify/)，同批 [产品 FO](qq-oldrestore-20261106/payload/sys_full_orientation_managed.final.xml)。原厂表在 `D:/TB371FC-release/clean-rebase-20261104/donor-tree-case/my_product/etc/fantasy/`。
