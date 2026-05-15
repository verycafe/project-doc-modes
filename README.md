# project-doc-modes

`project-doc-modes` 是一个 Markdown-first 的文档治理 Skill。GitHub 仓库只保存 Skill 原始包；用户安装后，只有在自己的目标项目中激活这个 Skill，才会生成该项目自己的 `AGENTS.md`、`CLAUDE.md`、`README.md` 和 `docs/` 文档结构。

## 配图

```mermaid
flowchart LR
    subgraph P1["1 安装 Skill 原始包"]
        A1["GitHub 仓库<br/>只保存 Skill 原始文件"]
        A2["install_runtime.py"]
        A3["安装到 Codex<br/>~/.codex/skills/project-doc-modes"]
        A4["安装到 Claude Code<br/>~/.claude/skills/project-doc-modes"]
        A1 --> A2
        A2 --> A3
        A2 --> A4
    end

    subgraph P2["2 在目标项目中激活"]
        B1["打开用户项目"]
        B2["Codex: project-doc-modes"]
        B3["Claude: /project-doc-modes 或 /sdd"]
        B4["先检查仓库结构<br/>Git 状态 / 代码目录 / 文档路径"]
        B1 --> B2
        B1 --> B3
        B2 --> B4
        B3 --> B4
    end

    subgraph P3["3 先备份再理解"]
        C1{"已有文档？"}
        C2["先复制到 docs/archive/"]
        C3["备份存在后<br/>再阅读旧文档"]
        C4["结合真实代码和配置<br/>校验文档逻辑"]
        C5["MIGRATION_NOTES.tmp.md<br/>临时记录避免失忆"]
        C1 -- "有" --> C2 --> C3 --> C4 --> C5
        C1 -- "无" --> C4
    end

    subgraph P4["4 生成规范文档结构"]
        D1["AGENTS.md<br/>跨 agent 主规则入口"]
        D2["CLAUDE.md<br/>桥接到 AGENTS.md"]
        D3["docs/product/vX.Y<br/>PRD -> PHASE -> SPEC"]
        D4["docs/governance<br/>状态 / 工作流 / 上下文"]
        D5["docs/archive<br/>历史快照"]
        D1 --- D2
        D3 --- D4
        D4 --- D5
    end

    subgraph P5["5 执行治理和验证"]
        E1["生成文档默认 local-only"]
        E2["不得删除或修改用户代码逻辑"]
        E3["升级时复制归档<br/>不清空 docs/"]
        E4["校验泄漏、结构、Git 状态"]
        E5["SDD-RIPER<br/>Spec Review / Plan / Execute / Reverse Sync"]
        E1 --> E2 --> E3 --> E4 --> E5
    end

    P1 --> P2 --> P3 --> P4 --> P5
```

## 安装

Codex:

```bash
python3 scripts/install_runtime.py ~/.codex/skills/project-doc-modes --runtime codex --force
```

Claude Code:

```bash
python3 scripts/install_runtime.py ~/.claude/skills/project-doc-modes --runtime claude --force
```

Claude Code 安装后会额外生成用户级命令：

```text
~/.claude/commands/project-doc-modes.md
~/.claude/commands/sdd.md
```

安装自测：

```bash
python3 scripts/install_runtime.py --self-test
```

GitHub 上的 Skill 原始包只包含：

```text
.gitignore
README.md
SKILL.md
agents/openai.yaml
references/rules.md
scripts/install_runtime.py
```

## 使用

在目标项目中打开 Codex，然后激活 `project-doc-modes` Skill。

在 Claude Code 中进入目标项目后使用：

```text
/project-doc-modes
```

如需启用 SDD-RIPER / 团队氛围编码治理，使用：

```text
/sdd
```

激活后，Skill 会先检查目标项目，再用少量问题确认模式、语言、版本、阶段或角色边界，然后才创建或迁移文档。

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
    │   └── context/
    │       ├── CODEMAP.md
    │       ├── CONTEXT_BUNDLE.md
    │       └── MIGRATION_NOTES.tmp.md
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

协作模式会使用 `docs/collaboration/` 管理角色、边界、状态和交接文档。迭代模式会使用 `docs/product/vX.Y/` 管理版本化产品文档。SDD-RIPER 可以叠加在任一模式上。

## 工作流程

1. 安装 Skill 到 Codex 或 Claude Code。
2. 在目标项目中激活 Skill。
3. 检查仓库结构、Git 状态、代码目录、配置文件和已有文档路径。
4. 如果已有文档，先复制一份到 `docs/archive/`，再阅读和理解文档内容。
5. 结合真实代码和配置校验旧文档是否准确，记录不一致之处。
6. 确认使用协作模式或迭代模式，以及语言、版本、阶段或角色边界。
7. 按规范生成 `AGENTS.md`、`CLAUDE.md`、`README.md` 和分类 `docs/`。
8. 运行结构、泄漏、Git local-only、代码不可变等验证。

## 规范逻辑和约束

- GitHub 仓库是 Skill 原始包，不是目标项目初始化后的文档结构。
- 目标项目文档只在用户激活 Skill 后生成。
- 生成文档默认不进入 Git；除非用户明确要求，否则不得 `git add`、`git commit` 或 `git push`。
- 除 `AGENTS.md`、`CLAUDE.md`、`README.md` 外，其他生成的 Markdown 默认放在 `docs/` 下。
- `AGENTS.md` 是跨 agent 的主治理入口；`CLAUDE.md` 必须桥接到 `AGENTS.md`，不能另起一套规则。
- 需求、阶段、规格必须遵循 `PRD -> PHASE -> SPEC`：先需求方案，再 PHASE 规划，最后把 SPEC 拆到对应 PHASE 下。
- 不得删除、移动、重写或重构用户代码、配置、运行逻辑、API、依赖、测试，除非用户明确要求代码变更。
- 如果目标项目已有文档，必须先备份，再阅读、理解、迁移和重写。
- 文档升级时默认复制当前版本到 `docs/archive/`，然后升级当前文档；不得默认清空 `docs/`。
- 上一个版本的功能逻辑默认锁定为历史基线，除非用户明确要求修改。
- 生成的目标项目文档不得写入 `project-doc-modes`、`/project-doc-modes`、`/sdd`、`SKILL.md` 或本机安装路径。
- 复杂迁移可使用 `docs/governance/context/MIGRATION_NOTES.tmp.md` 做临时记录，避免迁移过程中丢失上下文。
