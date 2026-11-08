# 旧 R94 平行视界材料

已找到两份旧组件。旧版“平行视窗”的逐应用列表在 `com.android.settings` 的 `ParallelWorldFragment`。历史真机页面显示了哔哩哔哩、汽水音乐、微信和一加社区及开关状态。

## 导出文件

源刷机包为 `D:\TB371FC-release\R94T-v27-r106-20261103-CANDIDATE\images\super-R94.img`，读取其中的 `system_ext_a` 分区。独立的旧构建镜像 `D:\TB371FC-release\R94T-v23-build\system_ext_a.img` 中下列三份文件的 SHA-256 全部一致。

| 导出文件 | 分区内来源路径 | versionName / versionCode | SHA-256 | 平行视界应用列表 |
| --- | --- | --- | --- | --- |
| `Settings.apk` | `/system_ext/priv-app/Settings/Settings.apk` | `16.0.0` / `16000000` | `72228F3DE25535411456D49BBF16FDC17A85319C21929B514344C6EA66FBA2F1` | **有**。DEX 有 `ParallelWorldFragment.loadAppList`，读取 `magicwindow`，界面通过 `res/xml/parallel_world_preference.xml` 建立 `parallel_world_support_app_list` 分类。旧真机页面已显示逐应用条目。 |
| `OplusFlexibleWindowUI.apk` | `/system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk` | `2.0.0` / `20` | `19D328584BB1E8AD2B677B9D06E2C492675E306FFB214B3022CADE48B00AF7E2` | **未找到该列表**。APK 为旧版 `com.oplus.pscanvas`，哈希与现机不同。查到浮窗设置和 `SupportGameListActivity`。 |
| `oat/arm64/OplusFlexibleWindowUI.vdex` | `/system_ext/app/OplusFlexibleWindowUI/oat/arm64/OplusFlexibleWindowUI.vdex` | 随同上面的旧 APK，无独立版本号 | `F63339EB4C9AD1FC714A4F2CE020D81BBC7343B4C677AF382D9F4E74901EDA43` | 同一镜像的预优化伴随文件。 |

## 历史记录与对照

- `D:\TB371FC-work\codex-20261028\Settings-live-20261030.apk` 与导出的 `Settings.apk` 字节一致。`D:\TB371FC-release\v24-build\base-inputs\Settings-live-20261030.apk` 也一致。
- `D:\TB371FC-work\codex-20261028\WeChat-parallel-settings-source.txt` 和 `WeChat-parallel-settings-calls.txt` 记录了 `com.oplus.settings.feature.display.parallel.ParallelWorldFragment` 的 XML、列表分类键和 `loadAppList`。同目录的 `WeChat-parallel-settings-ui.xml` 和 `WeChat-parallel-final-ui.xml` 保留旧设备上实际渲染的条目。
- 同时检查了 `D:\TB371FC-release\v24-build\system_ext_a.img` 和 `D:\TB371FC-release\v26-r104-build\system_ext_a.img` 的目录，两者都含 `Settings.apk` 与旧 FlexibleWindowUI 对应路径。
- 现机留档的 `OplusFlexibleWindowUI.apk` 同为 `2.0.0`，实算 SHA-256 为 `01450E66939EAC2A0E188396244B1F59725E862342BE978CA60CD8E218BE7BB8`，已排除。新母包的 `Settings.apk` 为 `16.1.0`，其偏好 XML 也有 `parallel_world_support_app_list`。这只确认资源存在，当前构建的入口及显示条件尚未核实。
- 已核对的范围是旧包文件和历史页面。当前构建的兼容性、逐应用列表能否显示、是否提供额外布局档位均未做真机验证。此次仅离线读取与导出。

目录中既有 `README.txt` 的 `NO_ALTERNATE_APK_FOUND` 来自较早的查找。上面的结果来自对旧 R94 镜像内部分区的实际提取，以本清单及实算哈希为准。
