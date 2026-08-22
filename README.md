# 第七个测试剧本 — LingChat 恐怖剧本 DLC

> 一个本不该出现在列表里的剧本。

《第七个测试剧本》是 [LingChat](https://github.com/SlimeBoyOwO/LingChat) 的**原创 meta 恐怖剧本 DLC**：四幕多周目叙事、DDLC 风格的崩坏演出（突脸 / 立绘崩坏 / 鼠标磁吸强制选择 / 假死机 / 写诗小游戏崩坏 / 日志污染……），共 29 个章节，并按玩家选择进入解放或循环结局。

**v1.1.0 更新**：新增「特殊的诗」投放机制（DDLC special poems 复刻：三张隐藏诗页按存档维度各投放一次，点到写诗小游戏的乱码词必掉一页）；写诗后的"眼睛"彩蛋改为一次性事件；新增低概率异常（BGM 变调 / 台词乱码化 / 假加载报错日志）；内容警告补充抑郁/自残/自杀暗示说明。

**v1.1.1 更新**：崩坏段语音全面低沉化——所有 `voice_shift` 叠加纯音调偏移（pitch -3 ~ -5 半音，语速与音调分离，配合播放倍率实现真正的"恶魔音"）；摊牌/重启段心跳底噪降速 0.9x。

**v2.0.0 更新**：重构为四幕 29 章结构；用持久 `current_act` 防止中途重开跳幕；三次 Act 2 写诗各投放一张无放回特殊诗；词池扩充到 200 个唯一词；新增 `normal / act2 / act2_final` 写诗模式、可见假控制台、Act 3 重进记忆，并彻底拆分 Act 4 解放/循环结局。⚠️ 完整效果需要包含 [#677](https://github.com/SlimeBoyOwO/LingChat/pull/677) 最新提交的引擎。

## ⚠️ 内容警告（务必阅读）

- **建议 18 岁以上游玩**。本 DLC 包含：强烈恐怖演出、突脸惊吓（jumpscare）、画面崩坏与闪烁、血色 UI、以及对**自杀/自我删除**的暗示性描写。
- 光敏性癫痫患者、易受惊吓者请勿游玩。
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

- 卸载：**DLC 管理**页点「卸载」（会删除全部文件）。
- 重置周目记忆：剧本列表中本剧本名旁的「重置记忆」小字按钮。
- 本剧本在剧本编辑器中不可编辑（`editor_locked` 自锁，属正常现象）。

## 引擎要求

本 DLC 使用了剧本引擎的扩展事件（jumpscare / force_choice / poem_game / voice_shift 等）与 DLC 识别功能：

- 上游支持 PR：[SlimeBoyOwO/LingChat#677](https://github.com/SlimeBoyOwO/LingChat/pull/677)（合并发版后，标注此处需要的最低版本）
- 在此之前，需要使用包含该 PR 的构建游玩

## 素材与版权

- **剧本文本、剧情、崩坏背景/立绘等生成素材**：本仓库原创内容，以 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 授权（署名-非商业性使用）。
- **DDLC 素材**（`Assets/` 中的 `1/2/6/g1/ghostmenu/heartbeat/d.ogg` 及 `glitch1-3 / mscare / eyes / giggle / s_kill_glitch1.ogg`）来自免费游戏《Doki Doki Literature Club》，版权属 **Team Salvato** 所有，依其 [IP Guidelines](https://teamsalvato.com/ip-guidelines/) 作非商业社区二创使用。**这些素材不在本仓库协议覆盖范围内，请勿二次分发或商用。**
- 本 DLC 为免费社区内容，与 Team Salvato 及 LingChat 官方无隶属关系。

## 目录结构

```
第七个测试剧本/
├── story_config.yaml   # 剧本清单（含 editor_locked、persistent_vars 声明）
├── dlc.json            # DLC 清单（版本/作者/最低引擎版本）
├── Chapters/           # 四幕共 29 章（含特殊诗、双结局与兼容入口）
├── Assets/             # 背景/立绘/音乐/音效/环境音（含三张隐藏诗页素材）
├── characters/         # 剧本自带角色（含崩坏差分）
└── poem_words.yaml     # 写诗小游戏词库
```
