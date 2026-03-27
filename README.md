# project-doc-modes

`project-doc-modes` is a Codex skill for scaffolding, reorganizing, and migrating repository documentation into one of two operating styles:

- `collaboration mode`: role-split ownership, handoff docs, edit boundaries, and role-specific working rules
- `iterative mode`: one active versioned source of truth, repo-wide governance docs, and archive-friendly version flow

It is designed to ask a few short setup questions first, then generate the right documentation structure in either Chinese or English.

## English

### What This Skill Does

- Inspects the target repository before changing docs
- Asks short interactive setup questions instead of dumping a long checklist
- Supports both Chinese and English for prompts, labels, and generated Markdown
- Preserves existing code directories unless the user explicitly asks to move them
- Builds current-entry docs, governance files, handoff docs, and archive structure

### Modes

#### Collaboration Mode

Use this when the repository is split by role or ownership.

Typical outputs:
- `AGENTS.md`
- role guides and status docs
- handoff docs
- phase instructions
- explicit editable / read-only / forbidden paths per role

#### Iterative Mode

Use this when the repository is evolving as one product.

Typical outputs:
- `README.md`
- `AGENTS.md`
- `STATUS.md`
- `WORKFLOW.md`
- `RELEASES.md`
- `docs/product/CURRENT.md`
- versioned product docs under `docs/product/vX.Y/`
- `archive/`

### Language Support

This skill supports two language modes:

- Chinese
- English

The selected language affects:
- user-facing setup questions
- mode labels
- generated Markdown headings and navigation text
- active governance and current-entry docs

### Repository Contents

- [SKILL.md](SKILL.md): main workflow and prompting rules
- [agents/openai.yaml](agents/openai.yaml): UI metadata and default prompt
- [references/collaboration-mode.md](references/collaboration-mode.md): collaboration-mode reference
- [references/iterative-mode.md](references/iterative-mode.md): iterative-mode reference
- [references/verification.md](references/verification.md): verification checklist

### Example Trigger

```text
Use $project-doc-modes to inspect this repository, ask one or two short setup questions at a time, confirm the needed context, then scaffold the docs.
```

## 中文

### 这个 Skill 做什么

`project-doc-modes` 是一个用于搭建、整理和迁移仓库文档治理结构的 Codex Skill。它会先检查仓库现状，再通过简短问答确认模式、角色、阶段信息和语言，然后把仓库组织成合适的文档结构。

它支持两种主要模式：

- `协作模式`：按角色或 ownership 拆分，强调交接文档、可编辑边界和角色规则
- `迭代模式`：围绕单一当前版本组织，强调当前入口、版本文档和历史归档

### 核心能力

- 修改前先检查仓库结构
- 用短轮次问答确认关键信息，而不是一次性抛出长清单
- 支持中文和英文两种语言模式
- 默认保留现有代码目录，不随意移动代码
- 生成当前入口、治理文档、交接文档和归档结构

### 语言模式

这个 Skill 支持两种语言模式：

- 中文
- 英文

语言设置会影响：
- 提问文本
- 模式标签
- 生成的 Markdown 标题与导航
- 当前治理文档和当前入口文档

### 仓库内容

- [SKILL.md](SKILL.md)：主工作流与提问规则
- [agents/openai.yaml](agents/openai.yaml)：界面展示信息与默认提示词
- [references/collaboration-mode.md](references/collaboration-mode.md)：协作模式参考
- [references/iterative-mode.md](references/iterative-mode.md)：迭代模式参考
- [references/verification.md](references/verification.md)：验证清单

### 适用场景

- 新仓库初始化文档结构
- 把旧文档体系迁移到统一的当前入口
- 给多人协作仓库建立角色边界和 handoff 规则
- 给单产品仓库建立版本化文档与 archive 结构
