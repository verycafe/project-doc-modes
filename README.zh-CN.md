# project-doc-modes

[English](README.md)

[快速开始](#快速开始) · [模式对比](#模式对比) · [示例场景](#示例场景) · [测试](#测试) · [仓库内容](#仓库内容)

`project-doc-modes` 是一套 Markdown-first 的仓库文档治理工作流，同时提供 Codex 和 Claude Code 两种入口，用来搭建、整理和迁移仓库文档结构。

它支持两种主要模式：

- `协作模式`：按角色或 ownership 拆分，强调交接文档、可编辑边界和角色规则
- `迭代模式`：围绕单一当前版本组织，强调当前入口、版本文档和历史归档

它会先通过简短问答确认关键信息，再按中文或英文输出合适的文档结构。

## 这个 Skill 做什么

- 修改前先检查仓库结构
- 用短轮次问答确认关键信息，而不是一次性抛出长清单
- 支持中文和英文两种语言模式
- 默认保留现有代码目录，不随意移动代码
- 生成当前入口、治理文档、交接文档和归档结构
- 除非用户要求进入 Git，否则生成文档默认保持本地化，不主动 stage/commit
- 按 `PRD -> PHASE -> SPEC` 分离需求方案、阶段规划和执行规格
- 支持团队 Vibe Coding 的 SDD-RIPER 关卡：Research、Plan Approved、Execute、Review、Reverse Sync
- 同一套核心规则既可作为 Codex skill 使用，也可作为 Claude Code 命令使用

## 快速开始

### Codex

你可以在 Codex 里直接这样触发：

```text
Use $project-doc-modes to inspect this repository, ask one or two short setup questions at a time, confirm the needed context, then scaffold the docs.
```

```text
Use $project-doc-modes to set up this repository in collaboration mode and keep the docs in Chinese.
```

```text
Use $project-doc-modes to migrate this repository to iterative mode and make docs/product/v0.1 the current source of truth.
```

```text
Use $project-doc-modes SDD to add SDD-RIPER governance and organize docs as PRD -> PHASE -> SPEC.
```

### Claude Code

这个仓库同时提供了 Claude Code 的项目记忆文件 [CLAUDE.md](CLAUDE.md)、通用 slash command [`.claude/commands/project-doc-modes.md`](.claude/commands/project-doc-modes.md)，以及 SDD 快捷命令 [`.claude/commands/sdd.md`](.claude/commands/sdd.md)。

在 Claude Code 里进入仓库后，可以直接使用：

```text
/project-doc-modes
```

如果要启动 SDD-RIPER，直接用：

```text
/sdd
```

也可以顺手附带目标：

```text
/project-doc-modes 把这个仓库迁移到迭代模式，并保持当前文档为中文
```

```text
/sdd 用中文启动 Phase 1，并保持生成文档默认不进入 Git
```

## 安装

如果你希望按运行环境安装，并且不要把另一套运行时包装文件一起拷过去，可以直接使用 [scripts/install_runtime.py](scripts/install_runtime.py)。

### 安装到 Codex

```bash
python3 scripts/install_runtime.py ~/.codex/skills/project-doc-modes --runtime codex --force
```

安装或更新自定义 Codex skill 之后，需要重启 Codex，应用才会重新加载技能目录。

会安装：
- `SKILL.md`
- `references/`
- `agents/openai.yaml`

不会安装：
- `CLAUDE.md`
- `.claude/commands/project-doc-modes.md`
- `.claude/commands/sdd.md`

### 安装到 Claude Code

```bash
python3 scripts/install_runtime.py /path/to/your/repository --runtime claude --force
```

会安装：
- `SKILL.md`
- `references/`
- `CLAUDE.md`
- `.claude/commands/project-doc-modes.md`
- `.claude/commands/sdd.md`

不会安装：
- `agents/openai.yaml`

### 自动检测运行环境

```bash
python3 scripts/install_runtime.py /target/path --runtime auto
```

自动检测规则：
- 如果目标路径看起来像 Codex skill 目录，例如 `~/.codex/skills/project-doc-modes`，就按 Codex 安装
- 如果目标路径看起来像仓库根目录，并且带有 `.git`、`.claude` 或 `CLAUDE.md`，就按 Claude Code 安装
- 如果机器上两边环境都存在，而目标路径本身又不够明确，就停止并要求显式传入 `--runtime`

## 模式

### 协作模式

适合按角色或 ownership 拆分的仓库。

典型输出：
- `AGENTS.md`
- 需要 Claude Code 使用该流程时生成 `CLAUDE.md`
- `docs/collaboration/` 下的角色指南与状态文档
- `docs/collaboration/` 下的交接文档
- `docs/governance/` 或 `docs/collaboration/` 下的阶段指令文档
- 每个角色明确的可编辑 / 只读 / 禁止编辑路径

### 迭代模式

适合围绕单一产品持续演进的仓库。

典型输出：
- `README.md`
- `AGENTS.md`
- 需要 Claude Code 使用该流程时生成 `CLAUDE.md`
- `docs/governance/STATUS.md`
- `docs/governance/WORKFLOW.md`
- `docs/governance/RELEASES.md`
- 需要 CodeMap 或 Context Bundle 时使用 `docs/governance/context/`
- `docs/product/CURRENT.md`
- `docs/product/vX.Y/` 下的版本化文档
- `docs/product/vX.Y/requirements/` 下的需求方案
- `docs/product/vX.Y/phases/PHASE-*/` 下的阶段规划
- `docs/product/vX.Y/phases/PHASE-*/specs/` 下的 SPEC
- `docs/archive/` 下的历史快照

## 模式对比

| 维度 | 协作模式 | 迭代模式 |
| --- | --- | --- |
| 适合场景 | 多角色拆分协作 | 单产品持续推进 |
| 主要关注点 | ownership 边界与 handoff | 当前版本与 archive 流程 |
| 核心结构 | `docs/` 下的角色指南、状态文档、交接文档 | `docs/product/` 下的版本化文档 |
| 当前入口 | 面向角色的当前工作文档 | 唯一当前版本入口 |
| 约束方式 | 每个角色的可编辑 / 只读 / 禁止编辑路径 | 只有一个 current，archive 只存历史，生成文档默认不进入 Git |
| SDD-RIPER 适配 | 角色审批、handoff、Reverse Sync 负责人 | 需求方案、阶段规划、阶段 SPEC、Review 记录 |
| 典型提问顺序 | 模式、角色、阶段文档、编辑边界、语言 | 模式、版本/阶段、语言、current/archive 结构 |

## 示例场景

### 初始化空仓库

```text
Use $project-doc-modes to inspect this empty repository, ask short setup questions in Chinese, and scaffold it in iterative mode with v0.1 as the current version.
```

### 整理多角色协作仓库

```text
Use $project-doc-modes to inspect this repository, confirm the current role and edit boundaries, then set it up in collaboration mode.
```

### 把现有文档迁移到版本化结构

```text
Use $project-doc-modes to migrate this repository to iterative mode, keep current docs in Chinese, and snapshot replaced material into docs/archive.
```

### 加入团队 Vibe Coding 关卡

```text
Use $project-doc-modes to add SDD-RIPER governance to this repository, keep generated docs local-only in Git, and organize docs as PRD -> PHASE -> SPEC.
```

## 语言模式

这个 Skill 支持两种语言模式：

- 中文
- 英文

语言设置会影响：
- 提问文本
- 模式标签
- 生成的 Markdown 标题与导航
- 当前治理文档和当前入口文档

## 运行入口

- Codex：通过 [SKILL.md](SKILL.md) 触发，并使用 [agents/openai.yaml](agents/openai.yaml) 作为界面便利层
- Claude Code：通过 [CLAUDE.md](CLAUDE.md)、[`.claude/commands/project-doc-modes.md`](.claude/commands/project-doc-modes.md) 和 [`.claude/commands/sdd.md`](.claude/commands/sdd.md) 触发，核心规则仍然来自同一份 `SKILL.md`

## 测试

如果你要确认 Codex 和 Claude Code 两套安装都可用，而且不会把彼此的包装文件装进去，可以运行这条 smoke test：

```bash
python3 scripts/test_runtime_install.py
```

这个仓库已经实际跑过本地端到端验证：
- Codex：安装到 `~/.codex/skills/project-doc-modes` 后通过了 `quick_validate.py`，并且用 `codex exec` 成功触发了 `$project-doc-modes`
- Claude Code：安装到临时仓库后，用 `claude -p` 成功触发了 `/project-doc-modes`；`/sdd` 会作为 SDD-RIPER 快捷命令一起安装

完整测试说明见 [TESTING.zh-CN.md](TESTING.zh-CN.md)。

## 仓库内容

- [SKILL.md](SKILL.md)：主工作流与提问规则
- [TESTING.md](TESTING.md)：英文测试指南
- [TESTING.zh-CN.md](TESTING.zh-CN.md)：中文测试指南
- [CLAUDE.md](CLAUDE.md)：Claude Code 项目记忆入口
- [`.claude/commands/project-doc-modes.md`](.claude/commands/project-doc-modes.md)：Claude Code 项目级 slash command
- [`.claude/commands/sdd.md`](.claude/commands/sdd.md)：Claude Code 的 SDD-RIPER 快捷命令
- [agents/openai.yaml](agents/openai.yaml)：界面展示信息与默认提示词
- [scripts/install_runtime.py](scripts/install_runtime.py)：按运行环境安装的脚本
- [scripts/test_runtime_install.py](scripts/test_runtime_install.py)：Codex / Claude Code 的烟雾测试
- [references/collaboration-mode.md](references/collaboration-mode.md)：协作模式参考
- [references/iterative-mode.md](references/iterative-mode.md)：迭代模式参考
- [references/sdd-riper.md](references/sdd-riper.md)：SDD-RIPER 与团队 Vibe Coding 参考
- [references/verification.md](references/verification.md)：验证清单

## 适用场景

- 新仓库初始化文档结构
- 把旧文档体系迁移到统一的当前入口
- 给多人协作仓库建立角色边界和 handoff 规则
- 给单产品仓库建立版本化文档与 archive 结构

## 示例触发方式

```text
Use $project-doc-modes to inspect this repository, ask one or two short setup questions at a time, confirm the needed context, then scaffold the docs.
```
