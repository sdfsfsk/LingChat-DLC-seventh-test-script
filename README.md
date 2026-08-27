# 第七个测试剧本 — LingChat 恐怖剧本 DLC

> 一个本不该出现在列表里的剧本。

《第七个测试剧本》是 [LingChat](https://github.com/SlimeBoyOwO/LingChat) 的**原创 meta 恐怖剧本 DLC**：四幕多周目叙事、DDLC 风格的崩坏演出（突脸 / 立绘崩坏 / 鼠标磁吸强制选择 / 假死机 / 写诗小游戏崩坏 / 日志污染……），共 45 个章节，并按玩家选择进入解放或循环结局。


**v2.10.2 更新**：周末终场的 `Static+UiCorrupt+BloodUI` 改为常驻到最后一句台词，修复血红 UI 只显示 0.32 秒便恢复蓝色的问题；离开本章前会显式清除，不污染下一章。

**v2.10.1 更新**：把首日 `RUNTIME // roster` 异常名单窗口从默认蓝色 CMD 改为血红背景 CMD，让 `characters: 2 / observers: 3` 的首次越界提示更符合恐怖演出。

**v2.10.0 更新**：加入参考 DDLC Act 2 `rigged_choice` 的三选项鼠标抢夺演出；故障音和震屏会在选项出现时触发，真实系统指针按原版 30Hz、`current×0.9 + target×0.1` 被牵向最下方答案，但不会自动点击；按 Esc、切出窗口或超过 5 秒都会停止牵引，玩家仍需亲自确认强制项。

**v2.9.0 更新**：适配最新 LingChat `dev` 与 Live2D 角色舞台；剧本进入时按 `main_character: DeepSeek` 自动切换并锁定主角/读档，退出后按队列顺序恢复原主角；静态角色的崩坏闪现与噪点侵蚀改为挂载到新版共享舞台 effects layer，组合背景特效、扩展事件和条件表达式也已与最新版编辑器校验规则对齐。

**v2.8.0 更新**：幽灵锁定全面黑白化，加入黑白崩坏教室与幽灵钦灵立绘；失控独白增加眼睛/嘴部噪点慢炖侵蚀，重绘写诗 Q 版贴纸，并移除效果不佳的崩坏 logo 两连闪。

**v2.7.2 更新**：修复角色明确请求删除 `MAIN.chr` 时仍被实时监视器误判为“不速之删”的竞态；桌面演出彻底移除 PowerShell/pwsh 宿主，错误/警告改为 Windows 原生 TaskDialog，残页直接由 Notepad 打开，控制台改为真实 CMD，并新增血红背景 CMD；所有窗口受全局 4 个、最长 12 秒与剧本退出清理约束。

## ⚠️ 内容警告（务必阅读）

- **建议 16 岁以上游玩**。本 DLC 包含：强烈恐怖演出、突脸惊吓（jumpscare）、画面崩坏与闪烁、血色 UI。**不含自杀/自残描写**。
- 光敏性癫痫患者、易受惊吓者请勿游玩。
- 经你确认内容警告后，部分场景会在桌面上弹出**真实系统窗口**（Windows 原生错误/警告 TaskDialog、直接打开的 Notepad 残页、蓝色或血红背景的真实 CMD；不会出现 PowerShell/pwsh 宿主），并在主窗口聚焦时短暂牵引系统鼠标（只移动、不代点，按 Esc、切出窗口或 5 秒后立即停止）；同时会在 `data` 同级的 `characters/standalone/第七个测试剧本/` 写入两个无害 `.chr` 剧情标记。所有能力均由当前剧本票据约束，不会执行剧本文字、模拟真实系统崩溃或修改 LingChat 角色模型。
- 游玩过程中如感到不适，请立即退出。

## 安装

**方式一（推荐）：DLC 管理界面导入**

1. 在 [Releases](../../releases) 下载最新的 `seventh-test-script-v*.zip`（无需解压；GitHub 资产名仅使用 ASCII，包内目录仍为中文名）
2. 游戏内打开 **游戏配置 → 高级设置 → DLC 管理**
3. 点「添加 DLC 包（zip）」，选择下载的 zip
4. 识别成功后主菜单右下角会显示「已识别 DLC：第七个测试剧本」，剧本列表里直接可玩

**方式二：手动安装**

把本仓库的 `第七个测试剧本/` 整个文件夹复制到游戏的 `data/game_data/scripts/standalone/` 目录下，重启游戏。

## 卸载 / 重置

- 卸载：**DLC 管理**页点「卸载」；兼容引擎先用同盘原子重命名把包移出剧本扫描区，再清周目、菜单和本 DLC 的标记。进程中断或 Windows 部分删除失败时会在下次启动继续清理，且不会把半个包当成已安装剧本。
- 重置周目记忆：剧本列表中本剧本名旁的「重置记忆」小字按钮。重置先快照标记/菜单并写入持久重置事务，再移除周目状态、恢复 `MAIN.chr` / `ql.chr` 并清标题效果；普通 I/O 失败会回滚，强制中断后引擎启动恢复器会继续完成，因此删除标记不会造成永久锁死。
- 标记实际位于便携版 `bin/characters/standalone/第七个测试剧本/`（即 `data/` 旁边）；它们是纯文本剧情道具，不是角色模型或可执行文件。
- 本剧本在剧本编辑器中不可编辑（`editor_locked` 自锁，属正常现象）。

## 引擎要求

本 DLC 使用了剧本引擎的扩展事件（`jumpscare` / `force_choice` / `poem_game` / `voice_shift` / `character_file` / `main_menu_effect` / `glitch_window` / `console_window` / `watch_file` 等）、组合背景特效、DLC 包管理与 `main_character` 主角锁定。文件、菜单和系统窗口能力均由引擎做剧本归属、固定样式、数量/时长与路径白名单校验，旧引擎无法完整运行 v2.10.2：

- 上游支持 PR：[SlimeBoyOwO/LingChat#677](https://github.com/SlimeBoyOwO/LingChat/pull/677) 当前仍为 Draft；在合并发版前必须使用包含该 PR 最新提交的定制构建
- 最低版本：LingChat `0.5.3`；导入/扫描会强制校验 `dlc.json.min_engine`，旧构建没有带活动票据、焦点/边界校验、Esc/失焦取消和后端 forced 校验的安全鼠标抢夺能力
- `main_character: DeepSeek` 要求全局角色库中保留 `data/game_data/characters/DeepSeek/settings.yml`；进入剧本后角色切换和读档会暂时锁定，退出时恢复原主角
- 新版导入会在 `data/.dlc-import/` 扫描区外做有界解压（条目数、文件/总量、路径与压缩比限制），校验并刷盘后才用同盘原子重命名提交

## 素材与版权

- **剧本文本、剧情、崩坏背景/立绘等生成素材**：本仓库原创内容，以 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 授权（署名-非商业性使用）。
- **DDLC 素材**（`Assets/` 中的 `1/2/6/g1/ghostmenu/heartbeat/d.ogg` 及 `glitch1-3 / mscare / eyes / giggle / s_kill_glitch1.ogg`）来自免费游戏《Doki Doki Literature Club》，版权属 **Team Salvato** 所有，依其 [IP Guidelines](https://teamsalvato.com/ip-guidelines/) 作非商业社区二创使用。**这些素材不在本仓库协议覆盖范围内，请勿二次分发或商用。**
- 本 DLC 为免费社区内容，与 Team Salvato 及 LingChat 官方无隶属关系。

## 目录结构

```
第七个测试剧本/
├── story_config.yaml   # 剧本清单（含 editor_locked、persistent_vars 声明）
├── dlc.json            # DLC 清单（版本/作者/最低引擎版本）
├── Chapters/           # 四幕共 45 章（含实时文件检查、双结局与旧存档修复门）
├── CharacterFiles/     # 只读打包模板；重置时恢复两个无害 .chr 标记
├── Assets/             # 背景/立绘/音乐/音效/环境音（含两张现行隐藏诗页素材）
├── characters/         # 剧本自带角色（含崩坏与完整情绪差分）
└── poem_words.yaml     # 写诗小游戏词库
```
