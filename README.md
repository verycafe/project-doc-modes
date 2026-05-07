# project-doc-modes

[中文说明](README.zh-CN.md)

[Quick Start](#quick-start) · [Mode Comparison](#mode-comparison) · [Example Scenarios](#example-scenarios) · [Testing](#testing) · [Repository Contents](#repository-contents)

`project-doc-modes` is a Markdown-first repository-doc workflow packaged for both Codex and Claude Code. It scaffolds, reorganizes, and migrates repository documentation into one of two operating styles:

- `collaboration mode`: role-split ownership, handoff docs, edit boundaries, and role-specific working rules
- `iterative mode`: one active versioned source of truth, repo-wide governance docs, and archive-friendly version flow

It is designed to ask a few short setup questions first, then generate the right documentation structure in either Chinese or English.

## What This Skill Does

- Inspects the target repository before changing docs
- Asks short interactive setup questions instead of dumping a long checklist
- Supports both Chinese and English for prompts, labels, and generated Markdown
- Preserves existing code directories unless the user explicitly asks to move them
- Builds current-entry docs, governance files, handoff docs, and archive structure
- Keeps generated docs local-only in Git by default unless the user asks to track them
- Separates requirements, phase plans, and SPEC docs as `PRD -> PHASE -> SPEC`
- Supports SDD-RIPER gates for team vibe coding: research, plan approval, execution, review, and Reverse Sync
- Works as a Codex skill and as a Claude Code slash command without forking the core workflow

## Quick Start

### Codex

Use one of these prompts in Codex:

```text
Use $project-doc-modes to inspect this repository, ask one or two short setup questions at a time, confirm the needed context, then scaffold the docs.
```

```text
Use $project-doc-modes to set up this repository in collaboration mode and keep the docs in English.
```

```text
Use $project-doc-modes to migrate this repository to iterative mode and make docs/product/v0.1 the current source of truth.
```

```text
Use $project-doc-modes SDD to add SDD-RIPER governance and organize docs as PRD -> PHASE -> SPEC.
```

### Claude Code

This repository includes project memory in [`CLAUDE.md`](CLAUDE.md), a general slash command at [`.claude/commands/project-doc-modes.md`](.claude/commands/project-doc-modes.md), and an SDD shortcut at [`.claude/commands/sdd.md`](.claude/commands/sdd.md).

In Claude Code, open the repository and use:

```text
/project-doc-modes
```

For SDD-RIPER, use the short command:

```text
/sdd
```

You can also pass extra intent inline:

```text
/project-doc-modes migrate this repository to iterative mode and keep the docs in Chinese
```

```text
/sdd start Phase 1 in Chinese and keep generated docs local-only
```

## Install

Use [`scripts/install_runtime.py`](scripts/install_runtime.py) when you want a runtime-specific install without copying the other runtime's wrapper files.

### Install For Codex

```bash
python3 scripts/install_runtime.py ~/.codex/skills/project-doc-modes --runtime codex --force
```

After installing or updating a custom Codex skill, restart Codex so the app reloads the skills directory.

Installed file set:
- `SKILL.md`
- `references/`
- `agents/openai.yaml`

Not installed:
- `CLAUDE.md`
- `.claude/commands/project-doc-modes.md`
- `.claude/commands/sdd.md`

### Install For Claude Code

```bash
python3 scripts/install_runtime.py ~/.claude/skills/project-doc-modes --runtime claude --force
```

Installed file set:
- `SKILL.md`
- `references/`

Also written:
- `~/.claude/commands/project-doc-modes.md`
- `~/.claude/commands/sdd.md`

Not installed:
- `agents/openai.yaml`
- target repository root files such as `SKILL.md`, `references/`, or command wrappers

### Auto-Detect The Runtime

```bash
python3 scripts/install_runtime.py /target/path --runtime auto
```

Auto-detection rules:
- install as Codex only when the target path is the current user's standard Codex skill directory: `~/.codex/skills/project-doc-modes`
- install as Claude Code only when the target path is the current user's standard Claude skill directory: `~/.claude/skills/project-doc-modes`
- refuse nonstandard targets and any target inside a repository tree so runtime files are not copied into project documentation
- stop and ask for an explicit runtime when the target path is ambiguous

## Modes

### Collaboration Mode

Use this when the repository is split by role or ownership.

Typical outputs:
- `AGENTS.md`
- `CLAUDE.md` bridge when Claude Code should use the workflow
- role guides and status docs under `docs/collaboration/`
- handoff docs under `docs/collaboration/`
- phase instructions under `docs/governance/` or `docs/collaboration/`
- explicit editable / read-only / forbidden paths per role

### Iterative Mode

Use this when the repository is evolving as one product.

Typical outputs:
- `README.md`
- `AGENTS.md`
- `CLAUDE.md` bridge when Claude Code should use the workflow
- `docs/governance/STATUS.md`
- `docs/governance/WORKFLOW.md`
- `docs/governance/RELEASES.md`
- `docs/governance/context/` when CodeMap or context bundles are needed
- `docs/product/CURRENT.md`
- versioned product docs under `docs/product/vX.Y/`
- requirements under `docs/product/vX.Y/requirements/`
- phase plans under `docs/product/vX.Y/phases/PHASE-*/`
- SPEC docs under `docs/product/vX.Y/phases/PHASE-*/specs/`
- historical snapshots under `docs/archive/`

## Mode Comparison

| Topic | Collaboration Mode | Iterative Mode |
| --- | --- | --- |
| Best for | Role-split teams | One shared product flow |
| Primary focus | Ownership boundaries and handoffs | Current version and archive flow |
| Main structure | Role guides, status docs, handoff docs under `docs/` | Versioned docs under `docs/product/` |
| Current entrypoint | Role-specific working docs | One active version marked current |
| Boundary rules | Editable / read-only / forbidden paths by role | One current version, archive is historical only, docs stay local-only in Git by default |
| SDD-RIPER fit | Role approvals, handoffs, Reverse Sync owners | Requirements, phase plans, phase specs, review records |
| Typical question flow | Mode, role, phase doc, edit boundaries, language | Mode, version/phase, language, archive/current setup |

## Example Scenarios

### Start an Empty Repository

```text
Use $project-doc-modes to inspect this empty repository, ask short setup questions in English, and scaffold it in iterative mode with v0.1 as the current version.
```

### Organize a Role-Split Repository

```text
Use $project-doc-modes to inspect this repository, confirm the current role and edit boundaries, then set it up in collaboration mode.
```

### Migrate Existing Docs Into a Versioned Flow

```text
Use $project-doc-modes to migrate this repository to iterative mode, keep current docs in Chinese, and snapshot replaced material into docs/archive.
```

### Add Team Vibe Coding Gates

```text
Use $project-doc-modes to add SDD-RIPER governance to this repository, keep generated docs local-only in Git, and organize docs as PRD -> PHASE -> SPEC.
```

## Language Support

This skill supports two language modes:

- Chinese
- English

The selected language affects:
- user-facing setup questions
- mode labels
- generated Markdown headings and navigation text
- active governance and current-entry docs

## Runtime Support

- Codex: use [`SKILL.md`](SKILL.md) with [`agents/openai.yaml`](agents/openai.yaml) as the UI convenience layer
- Claude Code: use [`CLAUDE.md`](CLAUDE.md), [`.claude/commands/project-doc-modes.md`](.claude/commands/project-doc-modes.md), and [`.claude/commands/sdd.md`](.claude/commands/sdd.md) as thin wrappers around the same `SKILL.md`; generated target-project `CLAUDE.md` files should bridge Claude Code to `AGENTS.md`

## Testing

Run the cross-runtime smoke test to verify that the Codex and Claude installs both work and do not copy each other's wrapper files:

```bash
python3 scripts/test_runtime_install.py
```

Local end-to-end checks already run for this repository:
- Codex: installed into `~/.codex/skills/project-doc-modes`, passed `quick_validate.py`, and successfully triggered via `codex exec` with `$project-doc-modes`
- Claude Code: installed into a temporary user-level skill directory with global `/project-doc-modes` and `/sdd` command wrappers

For the full testing guide, see [TESTING.md](TESTING.md).

## Repository Contents

- [SKILL.md](SKILL.md): main workflow and prompting rules
- [TESTING.md](TESTING.md): English testing guide
- [TESTING.zh-CN.md](TESTING.zh-CN.md): Chinese testing guide
- [CLAUDE.md](CLAUDE.md): Claude Code bridge entrypoint
- [.claude/commands/project-doc-modes.md](.claude/commands/project-doc-modes.md): Claude Code project slash command
- [.claude/commands/sdd.md](.claude/commands/sdd.md): Claude Code SDD-RIPER shortcut command
- [agents/openai.yaml](agents/openai.yaml): UI metadata and default prompt
- [scripts/install_runtime.py](scripts/install_runtime.py): runtime-aware installer
- [scripts/test_runtime_install.py](scripts/test_runtime_install.py): Codex/Claude smoke test
- [references/collaboration-mode.md](references/collaboration-mode.md): collaboration-mode reference
- [references/iterative-mode.md](references/iterative-mode.md): iterative-mode reference
- [references/sdd-riper.md](references/sdd-riper.md): SDD-RIPER and team vibe coding reference
- [references/verification.md](references/verification.md): verification checklist

## Example Trigger

```text
Use $project-doc-modes to inspect this repository, ask one or two short setup questions at a time, confirm the needed context, then scaffold the docs.
```
