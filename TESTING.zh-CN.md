# 测试指南

[English](TESTING.md)

这份文档说明 `project-doc-modes` 目前在 Codex 和 Claude Code 两侧的验证方式。

## 范围

当前测试分成三层：

- skill 自身的结构校验
- Codex / Claude Code 的隔离安装检查
- 本机 Codex 和 Claude Code 的真实端到端触发检查

当前 source of truth：

- [`scripts/install_runtime.py`](scripts/install_runtime.py)
- [`scripts/test_runtime_install.py`](scripts/test_runtime_install.py)
- [`SKILL.md`](SKILL.md)

## 自动化检查

### 1. Skill 结构校验

```bash
python3 /Users/tvwoo/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/tvwoo/Projects/project-doc-modes
```

预期结果：

```text
Skill is valid!
```

### 2. 双运行时 Smoke Test

```bash
python3 scripts/test_runtime_install.py
```

预期结果：

```text
Codex install verified.
Claude install verified.
Cross-runtime file isolation verified.
Repository-root install refusal verified.
Nonstandard target refusal verified.
Preflight overwrite refusal verified.
Ambiguous auto-detection verified.
```

这一步会确认：

- Codex 只安装 `SKILL.md`、`references/`、`agents/openai.yaml`
- Claude Code 会把 `SKILL.md` 和 `references/` 安装到用户级 skill 目录，并把 `/project-doc-modes` 与 `/sdd` 命令包装写入用户级 Claude commands 目录
- 指向仓库根目录、仓库内部路径、普通非标准目录的安装目标都会被拒绝，避免 runtime 文件变成目标项目文档
- Claude 命令覆盖冲突会在复制 skill 文件前被发现
- 自动检测遇到歧义目标时会拒绝猜测

## 手动端到端测试

### Codex

1. 安装或更新 skill：

```bash
python3 scripts/install_runtime.py ~/.codex/skills/project-doc-modes --runtime codex --force
```

2. 重启 Codex，让它重新加载 `~/.codex/skills`。

3. 开一个新的 Codex 会话，发送：

```text
Use $project-doc-modes to inspect this repository and answer in one short sentence what kind of repo it is and what your first setup question would be.
```

预期成功信号：

- Codex 能识别 `project-doc-modes`
- 它会先检查仓库，再回答
- 对空仓库会先问使用 `collaboration mode` 还是 `iterative mode`

CLI 兜底方式：

```bash
codex exec --skip-git-repo-check --ephemeral -C /path/to/repo 'Use $project-doc-modes to inspect this repository and answer in one short sentence what kind of repo it is and what your first setup question would be.'
```

注意：

- prompt 要用单引号包住，否则 shell 会把 `$project-doc-modes` 当变量展开

### Claude Code

1. 安装或更新 Claude 用户级 skill 和命令：

```bash
python3 scripts/install_runtime.py ~/.claude/skills/project-doc-modes --runtime claude --force
```

2. 在目标仓库中运行：

```text
/project-doc-modes
```

SDD-RIPER 快捷命令：

```text
/sdd
```

也可以直接用 CLI：

```bash
claude -p '/project-doc-modes inspect this repository and answer in one short sentence what kind of repo it is and what your first setup question would be.'
claude -p '/sdd inspect this repository and answer in one short sentence what setup question you need before adding SDD-RIPER governance.'
```

预期成功信号：

- Claude 能加载用户级 slash command
- 它会先检查仓库，再回答
- 它会根据仓库现状提出一条简短的 setup 问题
- 生成到目标仓库的 `CLAUDE.md` 会明确要求 Claude Code 先读 `AGENTS.md`
- 生成到目标仓库的文档不会包含 `project-doc-modes`、`/project-doc-modes`、`/sdd`、已安装的 `SKILL.md`、`.codex/skills`、`.claude/skills` 或本机绝对安装路径，除非目标仓库就是这个 Skill 包本身

## 最近一次本地验证

最近一次维护者本地验证已经确认：

- Codex 通过 `codex exec` 完成了真实触发
- Claude Code 通过 `claude -p` 完成了真实触发
- Claude 的用户级命令发现路径来自 `~/.claude/commands/project-doc-modes.md` 和 `~/.claude/commands/sdd.md`

## 常见问题

- Codex 看不到 skill：
  安装或更新自定义 skill 后要重启 Codex
- Codex CLI 收到的是 `-doc-modes` 而不是 `$project-doc-modes`：
  说明 shell 把变量展开了，要改用单引号
- Claude Code 在受限沙箱里无法运行：
  需要允许它访问自己的本地状态文件，例如 `~/.claude.json`
- `--runtime auto` 报错：
  当目标路径不够明确时，显式传入 `--runtime codex` 或 `--runtime claude`
