# project-doc-modes

[English](README.md)

[快速开始](#快速开始) · [模式对比](#模式对比) · [示例场景](#示例场景) · [仓库内容](#仓库内容)

`project-doc-modes` 是一个用于搭建、整理和迁移仓库文档治理结构的 Codex Skill。

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

## 快速开始

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

## 模式

### 协作模式

适合按角色或 ownership 拆分的仓库。

典型输出：
- `AGENTS.md`
- 角色指南与状态文档
- 交接文档
- 阶段指令文档
- 每个角色明确的可编辑 / 只读 / 禁止编辑路径

### 迭代模式

适合围绕单一产品持续演进的仓库。

典型输出：
- `README.md`
- `AGENTS.md`
- `STATUS.md`
- `WORKFLOW.md`
- `RELEASES.md`
- `docs/product/CURRENT.md`
- `docs/product/vX.Y/` 下的版本化文档
- `archive/`

## 模式对比

| 维度 | 协作模式 | 迭代模式 |
| --- | --- | --- |
| 适合场景 | 多角色拆分协作 | 单产品持续推进 |
| 主要关注点 | ownership 边界与 handoff | 当前版本与 archive 流程 |
| 核心结构 | 角色指南、状态文档、交接文档 | `docs/product/` 下的版本化文档 |
| 当前入口 | 面向角色的当前工作文档 | 唯一当前版本入口 |
| 约束方式 | 每个角色的可编辑 / 只读 / 禁止编辑路径 | 只有一个 current，archive 只存历史 |
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
Use $project-doc-modes to migrate this repository to iterative mode, keep current docs in Chinese, and move replaced material into archive.
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

## 仓库内容

- [SKILL.md](SKILL.md)：主工作流与提问规则
- [agents/openai.yaml](agents/openai.yaml)：界面展示信息与默认提示词
- [references/collaboration-mode.md](references/collaboration-mode.md)：协作模式参考
- [references/iterative-mode.md](references/iterative-mode.md)：迭代模式参考
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
