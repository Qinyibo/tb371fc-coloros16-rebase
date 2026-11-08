# 鲸鲮 Office V2.1 · DEPLOY

`hardware_success_claimed=false`

## 前置

- adb 设备在线，Magisk root（`su -c id`）
- 工作根：`D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\jingling-office-v21`
- 若缺 zip：`python build-zip.py`

## 一键刷入

```
flash-jingling-office.cmd
```

步骤：push zip → `magisk --install-module` → 卸载 `/data` 用户版 `com.yozo.office`（避免盖住 Magisk system/app）→ reboot → `check-verify.cmd`

## 验收门禁

- 模块 `/data/adb/modules/tb371fc_jingling_office_v21` 存在且无 `disable`/`remove`
- 模块内 APK SHA = `0CC7977D…E508461`
- `pm path com.yozo.office` 有输出
- monkey 可冷启出进程
- 其它 Magisk 模块仍在（luna / refresh / dynframe / sf / vrr）

## 回滚

```
rollback-jingling-office.cmd
```

## 否定条件

- 为腾地方删其它模块
- 改 ART / GC / ro.product.*
- 无 SHA 门禁宣称成功
- `hardware_success_claimed=true`（本包禁止）
