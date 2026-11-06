# 笔 V4 · 可部署刷入／回退封板

`hardware_success_claimed=false`（未刷入、无真笔／充电／游戏输入验收）。

## 身份门禁（刷前必须全过）

| 项 | 期望 |
| --- | --- |
| 工作根 | `D:/TB371FC-release/clean-rebase-20261104` |
| 通道 | Bootloader **fastboot**（`is-userspace=no`） |
| 设备 | `product=spinel`，`unlocked=yes`，slot `a`，`partition-size:super=0x300000000`，`battery-soc-ok=yes` |
| 当前物理 super | 必须等于 V3 `cac703a493dce9be832c3ca81a01b4ca74c47852bc0ad2ff7ac275cb314e5a9e` |
| boot_a | 保持 `5b4acefcc109ece2d3b84ce646b3496de6dfe2dc4b33d459bd2557d4d9a38b3a`（V4 不改 boot） |
| 目标 super | V4 `31dbe4eafed965806ff4de4242f44103056ada235bdc0dea7acaaaea2470908e` |
| 差分范围 | 仅 `system_a`，RAW 变化 114536448 |
| Magisk | 现装 31.1 用于读回校验；笔代码本身不依赖 Magisk 模块 |
| 笔固件包 | **不依赖**额外 CTN730 固件包；实物型号待真笔核对 |

权威路径见 handoff `pen/execution-environment.md`、`pen/image-inventory.json`、`pen/delta-result.json`、`pen/rollback.json`。

V3 CoreService 现场：系统曾发起启动，`app=null`／PID 空（`pen/v3-core-start-dumpsys.txt`）。V4 设计：真实 CTN730 → 原 manifest 接收器 → 校验 SYSTEM_UID → 应用自管 CoreService；离线编译／容器／正反差分已过 ≠ 运行通过。

## 正向刷入（V3→V4）

在工作根、已加载 `task_env.ps1`、TEMP 在 D 盘：

```
python tools/flash_candidate_delta.py --work pen-sharing-compat/candidate-v4 --receipt pen-sharing-compat/candidate-v3/physical-delta-receipt.json
```

脚本内会：校验 receipt／boot／super 基线 → `adb reboot bootloader` → 校验 getvar → 按序 `fastboot flash super` 五段差分 → `fastboot reboot` → 写 `physical-delta-receipt.json`（`DELTA_WRITTEN_REBOOT_SENT_RUNTIME_PENDING`）。

**刷前重读**当前物理 super／boot，与 V3 基线不一致则中止。不要加 `--allow-vendor-*` 等与笔无关开关。

差分五段（正向）SHA-256：

1. `c4f9b645d60d4c5cc8dc1e97f9ee2a1af1d1e6dce39c6a0d1870b919df355586`
2. `214704d49df0253c6c9a20d89ea9d8a396e72fdac14b492e4a49b082450226a6`
3. `c80582e85b60a5a882a3ff7c1b0a01ec0cb64c471277a83a134de3f232bd26d7`
4. `c4a5f29944d4174dffae1dc3076b47b2d6c0b95fd4710441ac343b7121fb1d80`
5. `ccdb96322111557e892cdfe7b2c2bd4608a7b7b04c2221e95fcfffd146e1e298`

## 回退（V4→V3）

仅当当前 super **已是** V4 `31dbe4ea…` 时可用反向五段（`pen/rollback.json`／`candidate-v4/rollback-v2/`）：

1. `707170d27496295322d24c6c8a93eecbf87b69d605af464f0d1c9677b4c801cc`
2. `9e6167bd44d83e47c225dc483de704185b175772fcdd9ae4b5e9d520fa5a43a7`
3. `f6c3f7907d102863f8344bf231aab5fb7c23864d43bd9e6616ac8aa2b7c0230a`
4. `5d90d74d319355717f63e968dba32522560f0711b9a97034dfc79556411578f1`
5. `76fc79eccb6338acdf4bfede5a19016540b11df391c9e0c54263a2cdc777d5a6`

`userdata_wipe_required=false`。部分刷入／基线不符／无法验证分区时：**不要**用反向差分当通用救援，改刷完整 V3 super 原件 `super-pen-sharing-v3-OFFLINE.img`。

## 刷后验收清单（分项，任一项失败不得写硬件通过）

1. 开机 Enforcing；super 读回 = `31dbe4ea…`；boot 未变  
2. CoreService：对比 V3 的 `app=null`，确认是否出现非空 PID／自动拉起（有 log 再判）  
3. 真笔：连接、电量、压感、侧键 **分开**记  
4. 应用内书写 vs 游戏／部分应用输入（旧反馈游戏无效）分开记  
5. 未把笔全局转手指、未按 BLE 关掉整个 NVT  

缺真笔条件 → 停在“已刷入待硬件验收”，`hardware_success_claimed` 保持 false。
