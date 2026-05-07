# Testing

[中文说明](TESTING.zh-CN.md)

This guide covers the current validation path for `project-doc-modes` across both Codex and Claude Code.

## Scope

The testing strategy has three layers:

- structure validation for the skill itself
- runtime-isolated installation checks for Codex and Claude Code
- real end-to-end trigger checks in the local Codex and Claude Code CLIs

Source of truth:

- [`scripts/install_runtime.py`](scripts/install_runtime.py)
- [`scripts/test_runtime_install.py`](scripts/test_runtime_install.py)
- [`SKILL.md`](SKILL.md)

## Automated Checks

### 1. Skill Validation

```bash
python3 /Users/tvwoo/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/tvwoo/Projects/project-doc-modes
```

Expected result:

```text
Skill is valid!
```

### 2. Cross-Runtime Smoke Test

```bash
python3 scripts/test_runtime_install.py
```

Expected result:

```text
Codex install verified.
Claude install verified.
Cross-runtime file isolation verified.
Ambiguous auto-detection verified.
```

This confirms:

- Codex installs only `SKILL.md`, `references/`, and `agents/openai.yaml`
- Claude Code installs only `SKILL.md`, `references/`, `CLAUDE.md`, `.claude/commands/project-doc-modes.md`, and `.claude/commands/sdd.md`
- auto-detection refuses ambiguous targets instead of guessing

## Manual End-To-End

### Codex

1. Install or update the skill:

```bash
python3 scripts/install_runtime.py ~/.codex/skills/project-doc-modes --runtime codex --force
```

2. Restart Codex so it reloads `~/.codex/skills`.

3. Open a new Codex session and send:

```text
Use $project-doc-modes to inspect this repository and answer in one short sentence what kind of repo it is and what your first setup question would be.
```

Expected signs of success:

- Codex recognizes `project-doc-modes`
- it inspects the repository before answering
- for an empty repo, it asks whether to use `collaboration mode` or `iterative mode`

CLI fallback:

```bash
codex exec --skip-git-repo-check --ephemeral -C /path/to/repo 'Use $project-doc-modes to inspect this repository and answer in one short sentence what kind of repo it is and what your first setup question would be.'
```

Important:

- wrap the prompt in single quotes so the shell does not expand `$project-doc-modes`

### Claude Code

1. Install the Claude runtime files into the target repository:

```bash
python3 scripts/install_runtime.py /path/to/repo --runtime claude --force
```

2. From that repository, run:

```text
/project-doc-modes
```

For the SDD-RIPER shortcut:

```text
/sdd
```

Or use the CLI:

```bash
claude -p '/project-doc-modes inspect this repository and answer in one short sentence what kind of repo it is and what your first setup question would be.'
claude -p '/sdd inspect this repository and answer in one short sentence what setup question you need before adding SDD-RIPER governance.'
```

Expected signs of success:

- Claude loads the project-local slash command
- it inspects the repository before answering
- it asks a short setup question that matches the repo state

## Latest Local Evidence

The most recent local maintainer run verified:

- Codex end-to-end trigger via `codex exec`
- Claude Code end-to-end trigger via `claude -p`
- project-local Claude command discovery through `.claude/commands/project-doc-modes.md` and `.claude/commands/sdd.md`

## Troubleshooting

- Codex does not see the skill:
  restart Codex after installing or updating a custom skill
- Codex CLI receives `-doc-modes` instead of `$project-doc-modes`:
  quote the prompt with single quotes
- Claude Code cannot run in a restricted sandbox:
  allow access to its normal local state such as `~/.claude.json`
- `--runtime auto` fails:
  pass `--runtime codex` or `--runtime claude` explicitly when the target path is ambiguous
