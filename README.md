# project-doc-modes

[中文说明](README.zh-CN.md)

[Quick Start](#quick-start) · [Mode Comparison](#mode-comparison) · [Example Scenarios](#example-scenarios) · [Repository Contents](#repository-contents)

`project-doc-modes` is a Codex skill for scaffolding, reorganizing, and migrating repository documentation into one of two operating styles:

- `collaboration mode`: role-split ownership, handoff docs, edit boundaries, and role-specific working rules
- `iterative mode`: one active versioned source of truth, repo-wide governance docs, and archive-friendly version flow

It is designed to ask a few short setup questions first, then generate the right documentation structure in either Chinese or English.

## What This Skill Does

- Inspects the target repository before changing docs
- Asks short interactive setup questions instead of dumping a long checklist
- Supports both Chinese and English for prompts, labels, and generated Markdown
- Preserves existing code directories unless the user explicitly asks to move them
- Builds current-entry docs, governance files, handoff docs, and archive structure

## Quick Start

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

## Modes

### Collaboration Mode

Use this when the repository is split by role or ownership.

Typical outputs:
- `AGENTS.md`
- role guides and status docs
- handoff docs
- phase instructions
- explicit editable / read-only / forbidden paths per role

### Iterative Mode

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

## Mode Comparison

| Topic | Collaboration Mode | Iterative Mode |
| --- | --- | --- |
| Best for | Role-split teams | One shared product flow |
| Primary focus | Ownership boundaries and handoffs | Current version and archive flow |
| Main structure | Role guides, status docs, handoff docs | Versioned docs under `docs/product/` |
| Current entrypoint | Role-specific working docs | One active version marked current |
| Boundary rules | Editable / read-only / forbidden paths by role | One current version, archive is historical only |
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
Use $project-doc-modes to migrate this repository to iterative mode, keep current docs in Chinese, and move replaced material into archive.
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

## Repository Contents

- [SKILL.md](SKILL.md): main workflow and prompting rules
- [agents/openai.yaml](agents/openai.yaml): UI metadata and default prompt
- [references/collaboration-mode.md](references/collaboration-mode.md): collaboration-mode reference
- [references/iterative-mode.md](references/iterative-mode.md): iterative-mode reference
- [references/verification.md](references/verification.md): verification checklist

## Example Trigger

```text
Use $project-doc-modes to inspect this repository, ask one or two short setup questions at a time, confirm the needed context, then scaffold the docs.
```
