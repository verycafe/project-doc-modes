# project-doc-modes

`project-doc-modes` 是一个 Markdown-first 的文档治理 Skill，用来在目标项目中建立可持续的文档结构、版本治理和 SDD-RIPER 工作流。

## 维护文档

本仓库自身的活跃维护文档入口是 `docs/README.md`。当前采用迭代模式，当前版本为 `v0.1`，当前阶段为 `PHASE-1-sdd-knowledge-structure`。

## 配图

![project-doc-modes 工作流](assets/project-doc-modes-workflow.svg)

## 安装

安装请使用 `install.md`。它会把仓库内的 `project-doc-modes/` 干净 Skill 包安装到 Codex / Claude Code 的默认 Skill 文件夹。

推荐让 AI 助手执行：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/install.md
```

Hook 绑定是单独入口，默认只绑定当前项目。在 Codex 中，用户从 GitHub 安装 Hook 只需要在目标项目里粘贴：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md
```

这条命令会直接安装项目级 Hook，不再让 AI 每次重新判断支持情况。默认会写入当前仓库：

```text
.codex/hooks.json
.codex/hooks/project_doc_modes_stop.py
```

它使用 Codex 的 `Stop` 事件，在每轮会话结束后自动续跑一次 `project-doc-modes sync` 语义，然后执行 `verify` 语义。Codex 可能在首次运行非 managed command hook 前要求 `/hooks` review/trust；这是 Codex 运行时安全机制，不是第二个安装步骤。

全局绑定必须由用户显式改参数：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with scope=global
```

默认 Skill 文件夹是：

```text
Codex:      ${CODEX_HOME:-$HOME/.codex}/skills/project-doc-modes
Claude Code: ${CLAUDE_HOME:-$HOME/.claude}/skills/project-doc-modes
```

不要把整个仓库直接 clone 成最终 Skill 文件夹。最终 Skill 文件夹里只应该保留 `project-doc-modes/` 子目录中的运行时文件。

手动安装命令也在 `install.md` 中维护，README 不重复展开，避免安装入口分叉。

安装完成后，运行时 Skill 目录只包含最小 runtime payload：

```text
SKILL.md
references/init.md
references/rules.md
references/sdd.md
references/structure.md
references/sync.md
references/verify.md
```

Claude Code 安装还会生成用户级命令包装：

```text
$CLAUDE_HOME/commands/project-doc-modes.md
$CLAUDE_HOME/commands/project-doc-modes-sdd.md
$CLAUDE_HOME/commands/project-doc-modes-sync.md
$CLAUDE_HOME/commands/project-doc-modes-verify.md
```

`scripts/install_runtime.py` 是安装和同步脚本，只负责把 `project-doc-modes/` 子目录安装成最小运行时 payload、生成 Claude Code 命令包装、清理旧安装残留和运行自测。它不会在用户的目标项目里生成文档。

仓库结构：

```text
.gitignore
.claude-plugin/plugin.json
install.md
hooks.md
README.md
assets/project-doc-modes-workflow.svg
project-doc-modes/SKILL.md
project-doc-modes/references/init.md
project-doc-modes/references/rules.md
project-doc-modes/references/sdd.md
project-doc-modes/references/structure.md
project-doc-modes/references/sync.md
project-doc-modes/references/verify.md
scripts/bind_codex_project_hook.py
scripts/install_runtime.py
scripts/verify_repo_integrity.py
```

`scripts/bind_codex_project_hook.py` 是 Codex 项目级 Hook 绑定脚本，只负责在目标项目中创建、检查或移除 `.codex/hooks.json` 和 `.codex/hooks/project_doc_modes_stop.py` 的受管绑定。

## 使用

在目标项目中使用。

Codex：

1. 打开目标项目。
2. 激活 `project-doc-modes` Skill。
3. 用自然语言说明要初始化、迁移、整理文档，或启用 SDD-RIPER。

Codex 只显示一个 Skill 入口：`/project-doc-modes`。不同模式通过参数或自然语言路由：

```text
/project-doc-modes init
/project-doc-modes sync
/project-doc-modes verify
/project-doc-modes sdd
```

也可以直接说：

```text
用 project-doc-modes sync 模式，把本轮会话和代码变更同步回文档。
```

Claude Code：

1. 进入目标项目。
2. 调用已安装的 Skill；如果已生成命令包装，也可以使用：

```text
/project-doc-modes
```

初始化完成后，如果需要把单次会话、Hook payload、代码变更摘要和验证输出增量同步回文档，可以使用：

```text
/project-doc-modes-sync
```

只做结构检查、不改文档时，可以使用：

```text
/project-doc-modes-verify
```

如需启用 SDD-RIPER / 团队氛围编码治理，且已生成 Claude Code 命令包装，可以使用：

```text
/project-doc-modes-sdd
```

执行初始化或迁移时，Skill 会先检查目标项目，再用少量问题确认模式、语言、版本、阶段或角色边界，然后才创建或迁移文档。`sync` 不提问、不重建结构；`verify` 默认只读。

## 命令速查

```text
/project-doc-modes
= 初始化/迁移/整理文档治理

/project-doc-modes-sdd
= 启用规格驱动的开发治理

/project-doc-modes-sync
= 每轮会话后增量同步文档

/project-doc-modes-verify
= 检查文档结构和一致性
```

Codex 里只有 `/project-doc-modes` 一个 Skill 入口，使用 `init`、`sdd`、`sync`、`verify` 参数或自然语言表达模式。Claude Code 安装后会生成上面的独立命令包装。

## 启动后会发生什么

`/project-doc-modes` 会进入初始化、迁移或整理流程：

1. 检查仓库结构、已有文档、代码目录、配置文件和 `git status`。
2. 如已有活跃文档，先复制到 `docs/archive/`，再阅读和迁移。
3. 确认协作模式或迭代模式、文档语言、版本/阶段或角色边界。
4. 生成或整理 `AGENTS.md`、`CLAUDE.md`、`README.md` 和分类 `docs/`。
5. 验证根目录 Markdown、归档位置、本地路径泄漏、Git local-only 和代码不可变规则。

`/project-doc-modes-sdd` 会启用规格驱动开发治理：

1. 先检查当前仓库和已有文档，不直接写代码。
2. 建立或整理 `PRD -> PHASE -> SPEC` 链路。
3. 根据模式创建 SDD-RIPER 所需的 CodeMap、Context Bundle、PLAN、REVIEW、IMPLEMENTATION_RECORD。
4. 记录执行规则：No Spec, No Code；Spec is Truth；Reverse Sync。
5. 后续开发按 Research、Innovate、Plan、Execute、Review、Archive 的阶段推进。

简单选择：

```text
如果你只是想让一个仓库文档结构清楚，用：
/project-doc-modes

如果你希望之后 AI 写代码前必须先看 SPEC、先有计划、实现后同步文档，用：
/project-doc-modes-sdd
```

`/project-doc-modes-sync` 会做增量同步：

1. 读取本轮会话摘要、变更文件、`git status`、验证命令和输出。
2. 只更新受本轮证据影响的状态、索引、Implementation Record、Review、决策记录或 Release 记录。
3. 不重新询问模式，不重建文档结构，不做全量归档，不改代码。
4. 如果发现实现事实和旧文档不一致，只做必要的 Reverse Sync。
5. 最后做轻量结构和泄漏检查。

`/project-doc-modes-verify` 会做只读检查：

1. 检查根目录是否只保留 `AGENTS.md`、`CLAUDE.md`、`README.md`。
2. 检查 `docs/`、`docs/archive/`、`docs/product/` 或 `docs/collaboration/` 的结构是否符合当前模式。
3. 检查 `PRD -> PHASE -> SPEC` 是否放在正确层级。
4. 检查入口索引、Claude bridge、local-only 策略和本机路径泄漏。
5. 默认只报告问题，不创建、移动、归档、重写、stage、commit 或 push 文件。

## 项目结构

初始化后的目标项目文档结构通常是：

```text
.
├── AGENTS.md
├── CLAUDE.md
├── README.md
└── docs/
    ├── README.md
    ├── archive/
    ├── governance/
    │   ├── STATUS.md
    │   ├── WORKFLOW.md
    │   ├── RELEASES.md
    │   ├── context/
    │   │   ├── CODEMAP.md
    │   │   ├── CONTEXT_BUNDLE.md
    │   │   └── GLOSSARY.md
    │   ├── research/
    │   │   └── README.md
    │   └── experience/
    │       └── README.md
    └── product/
        ├── CURRENT.md
        └── v0.1/
            ├── README.md
            ├── requirements/
            ├── phases/
            │   └── PHASE-*/
            │       ├── PLAN.md
            │       ├── REVIEW.md
            │       ├── IMPLEMENTATION_RECORD.md
            │       └── specs/
            └── decisions/
```

这是迭代模式的典型结构。协作模式会使用 `docs/collaboration/` 管理角色、边界、状态和交接文档；SDD-RIPER 可以叠加在任一模式上。

复杂迁移时可以临时创建 `docs/governance/context/MIGRATION_NOTES.tmp.md` 记录迁移证据和上下文。它不是默认必建文件，迁移完成后应把长期有效的信息合并回正式文档。

`docs/governance/context/GLOSSARY.md` 是项目词汇表，记录稳定术语和禁止混用的说法。`docs/governance/research/` 放调研、外部资料、参考仓库和证据边界。`docs/governance/experience/` 放用户偏好、操作教训和暂时不适合进入 PRD 的经验知识；当这些内容变成需求、约束或验收标准时，再 Reverse Sync 到 PRD、PHASE、SPEC 或决策记录。

## 工作流程

1. 安装 Skill 到 Codex 或 Claude Code。
2. 在目标项目中激活 Skill。
3. 检查仓库结构、Git 状态、代码目录、配置文件和已有文档路径。
4. 如果已有文档，先复制一份到 `docs/archive/`，再阅读和理解文档内容。
5. 结合真实代码和配置校验旧文档是否准确，记录不一致之处。
6. 确认使用协作模式或迭代模式，以及语言、版本、阶段或角色边界。
7. 按规范生成 `AGENTS.md`、`CLAUDE.md`、`README.md` 和分类 `docs/`。
8. 运行结构、泄漏、Git local-only、代码不可变等验证。

后续 Hook 自动化不应重复执行完整初始化流程。Hook 应使用增量同步模式：读取本次会话摘要、变更文件和验证输出，只更新状态、索引、Implementation Record、Review、决策记录等受影响文档，然后做轻量结构和泄漏检查。

Hook 绑定默认作用于当前项目。Codex 项目级绑定已预置支持，默认通过 `.codex/hooks.json` 和 `.codex/hooks/project_doc_modes_stop.py` 安装；只有用户明确写 `scope=global` 时，AI 才能改当前工具的全局 Hook 配置；如果当前工具不在 `hooks.md` 的支持矩阵中，不能静默降级成全局绑定。

维护本仓库时，除了 installer 和 hook binder 自测，还可以运行：

```bash
python3 scripts/verify_repo_integrity.py
```

它会检查 README、install、hooks、runtime references、installer 和 `.claude-plugin/plugin.json` 的关键契约是否一致。

## 规范逻辑和约束

- 生成文档默认不进入 Git；除非用户明确要求，否则不得对这些文档执行 `git add`、`git commit` 或 `git push`。
- 新生成的 `docs/archive/` 快照也属于生成文档，默认要用 `.git/info/exclude` 保持 local-only。
- 如果目标项目已有被 Git 跟踪的 `README.md`、`AGENTS.md` 或 `CLAUDE.md`，修改后仍是 tracked change，不能用 `.git/info/exclude` 伪装成未跟踪文件。
- 除 `AGENTS.md`、`CLAUDE.md`、`README.md` 外，其他生成的 Markdown 默认放在 `docs/` 下。
- `AGENTS.md` 是跨 agent 的主治理入口；`CLAUDE.md` 必须桥接到 `AGENTS.md`，不能另起一套规则。
- 需求、阶段、规格必须遵循 `PRD -> PHASE -> SPEC`：先需求方案，再 PHASE 规划，最后把 SPEC 拆到对应 PHASE 下。
- 不得删除、移动、重写或重构用户代码、配置、运行逻辑、API、依赖、测试，除非用户明确要求代码变更。
- 如果目标项目已有文档，必须先备份，再阅读、理解、迁移和重写。
- 文档升级时默认复制当前版本到 `docs/archive/`，然后升级当前文档；不得默认清空 `docs/`。
- 上一个版本的功能逻辑默认锁定为历史基线，除非用户明确要求修改。
- 项目词汇表放在 `docs/governance/context/GLOSSARY.md`；调研放在 `docs/governance/research/`；经验沉淀放在 `docs/governance/experience/`，不要强行塞进 PRD。
- SDD-RIPER 下的可执行 SPEC 应包含 `Validation Loop`，说明用什么测试、脚本、hook inspect 或结构检查证明实现有效。
- 生成的目标项目文档不得写入 `project-doc-modes`、`/project-doc-modes`、`/project-doc-modes-sdd`、`/project-doc-modes-sync`、`/project-doc-modes-verify`、`/sdd`、`SKILL.md` 或本机安装路径。
- 复杂迁移可使用 `docs/governance/context/MIGRATION_NOTES.tmp.md` 做临时记录，避免迁移过程中丢失上下文。
