# TB371FC 手写笔与通信适配源码

对应离线候选 V4，母包 OPD2413_16.0.10.600(CN01)。完整镜像与设备日志留在 D 盘工作目录，本目录只保存可编辑源码、构建入口和许可；镜像与原始证据不上传。

## 当前证据

- V4 编译、APK/JAR 容器和 native library 对齐检查、ext4 检查、完整 super 哈希及正反差分校验通过。V4 **未刷入、未做硬件验收**。
- V3 上 vnet 已随开机加载，ovnet0/1/2 存在；共享手机数据、电话与短信未验收。
- 旧版笔曾能书写，用户反馈游戏及部分应用无效。V4 的连接、电量与按键适配不能据此算作修复游戏输入。
- 旧版共享流量曾可用，但需切换两次开关，后来失效。底层通信程序和 vnet 与 v17 相同不能排除控制状态、配置、协议或路由问题。

## 结构

`src` 是原 IPeManager 的协议、会话和连接生命周期扩展；`system-src` 在系统中观察 NVTCapacitivePen 与 CTN730，保留真实输入类型与数据，不抢占输入。

真实 CTN730 状态通过明确组件、受权限约束且共享发送者身份的广播送到原 BluetoothStatusReceiver。接收器校验系统 UID，再由应用自身请求 CoreService。无真实附笔或配对时不伪造连接。系统框架不反复跨应用拉起服务。

`PenDexPatchV3.java` 是补丁工具名称，当前对新版 IPeManager 改17处，对 WirelessSettings 改1处；`ServicesPenPatch.java` 改2处系统入口。每次从已校验的原始输入构建，替换既有辅助代码，不叠加多层补丁。

`vendor-overlay` 用 init 在 post-fs-data 加载匹配 TB 内核的真实 vnet 模块。源码与来源在 `vnet-source`；不能用 TB710FU 的 boot/vendor_boot/BSP 模块替代。

## 构建

使用 D 盘工作目录的 task_env.ps1 设置临时目录。输入 APK/JAR 名称及 SHA256 由 build-pen.py 与 build-wireless.py 校验；需自行从对应官方母包/当前受审版本取得，不在此分发。

1. `python pen-sharing-compat/inspect-contracts.py`：读取原始输入并生成本机 DEX 工具配置及 API 契约，不覆盖适配源码。
2. `python pen-sharing-compat/build-pen.py --output build-v4`。
3. 如需重建无线设置：`python pen-sharing-compat/build-wireless.py --output build-v4`。
4. 集成脚本针对已经核验的 D 盘镜像和精确前序哈希；先确认输入存在，不能当通用刷机脚本直接运行。

修改的 OEM APK 仅用于现有可信预装构建方式。保留证书身份和 ZIP 布局不等于修改后的官方密码学签名有效；不是可作为普通签名更新安装的 APK，也未添加验证绕过。

## 功能边界

参考教程：https://wasddestroy.site/tb710fu-doc/generic/flash_fix_module_yu_c16.html 。参考适配器针对 TB710FU，具体来源及许可见 NOTICE.txt；本适配没有继承基于 BLE 状态关闭整个 NVT 输入设备的 PenInputGate。

共享数据控制路径是 WirelessSettings -> NAS VirtualDataApiService；通话/SMS另行验收。新版 NAS 本身已处理缺失的 VCOMM_SHARE_NETWORK 默认值并在注册观察器后读取当前值，未加入额外启动写值、自动双切或常驻守护。
