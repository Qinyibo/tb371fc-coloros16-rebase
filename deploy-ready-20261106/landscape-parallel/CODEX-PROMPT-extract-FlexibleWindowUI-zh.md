# 给 Codex 的材料提取提示（原样粘贴）

请在本机 **D:\TB371FC-release** 与你的 Codex/agent 执行日志、会话产物、旧 flash 解包目录中，找出并导出 **旧可用包** 的平行视界 UI 材料。现网 ColorOS16 上的 `OplusFlexibleWindowUI.apk`（包名 `com.oplus.pscanvas`）版本 2.0.0，SHA256 为：

01450E66939EAC2A0E188396244B1F59725E862342BE978CA60CD8E218BE7BB8

我们需要 **SHA256 与上面不同** 的旧文件（那时候设置里平行视界有完整「按应用适配/布局」列表，而不是现在只有浮窗教程）。

请执行：
1. 递归搜索文件名：`OplusFlexibleWindowUI.apk`、`*FlexibleWindow*.apk`、以及含 `平行视界` / `MagicWindow` / `pscanvas` 的 APK/ZIP/IMG 解包产物。
2. 对每个命中的 APK 算 SHA256；只保留 ≠ 01450E66… 的副本。
3. 若在 `super.img` / `system_ext.img` / payload / R94 旧包中，请解出：
   - `system_ext/app/OplusFlexibleWindowUI/OplusFlexibleWindowUI.apk`（及同目录 oat 若有）
   - 可选：带「平行视界」Preference 的 `Settings.apk` / overlay 片段
4. 把可用文件复制到：
   `D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\materials-from-old-package\`
5. 写一份 `MANIFEST.txt`：路径、大小、SHA256、来源包名/日期。

不要改现网设备；只要材料落地即可。若全盘确认没有异哈希 APK，请明确写「未找到」并列出已搜根目录。