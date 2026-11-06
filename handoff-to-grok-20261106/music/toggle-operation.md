# 已执行的有限开关实验

设备文件 `/data/user/0/com.luna.music/shared_prefs/luna_launch_local_shared_preferences.xml`。先用 `am force-stop com.luna.music` 停止该应用，在应用未运行时原位改写同一文件，只把一个 `enableArtHeapExpandV4` 的 `true` 换成 `false`。备份完整原件一次。实际写入经 root shell 的 base64 解码管道完成，原先尝试的 ADB stdin 写入超时，未把那个尝试当作成功。写完验证设备文件哈希与生成的测试副本一致，并实读 `false`。本次没有改进程属性。

然后正常前台启动，约 35 秒后 PID 31376 仍在运行，堆区 `02000000–42000000`，观察窗中无新崩溃，配置实读已经回到 `true`。此处保留同一键的三个值和测量字段，原文件路径和哈希见 before／test 单键文件。写回来源与完整网络日志未保全。
