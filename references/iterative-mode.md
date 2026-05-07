# Iterative Mode

Use iterative mode when a repository is under unified development and the team wants versioned source-of-truth docs.

## Purpose

This mode is for projects where:
- current work should point to one active version
- old versions should remain readable but inactive
- repo-wide workflow rules should have root entrypoints but detailed docs should live under `docs/`
- documentation should be organized around product versions instead of role boundaries

## Typical Structure

```text
repo/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── docs/
│   ├── README.md
│   ├── governance/
│   │   ├── STATUS.md
│   │   ├── WORKFLOW.md
│   │   ├── RELEASES.md
│   │   └── context/
│   │       ├── CODEMAP.md
│   │       └── CONTEXT_BUNDLE.md
│   ├── product/
│       ├── CURRENT.md
│       └── v0.3/
│           ├── README.md
│           ├── requirements/
│           │   ├── PRD.md
│           │   ├── BUYER.md
│           │   ├── SELLER.md
│           │   └── ADMIN.md
│           ├── phases/
│           │   ├── README.md
│           │   └── PHASE-01/
│           │       ├── PLAN.md
│           │       ├── STATUS.md
│           │       └── specs/
│           │           ├── API_SPEC.md
│           │           ├── DATA_MODEL.md
│           │           └── TRACE_SPEC.md
│           └── decisions/
│   └── archive/
│       ├── README.md
│       ├── versions/
│       │   └── v0.2/
│       └── bootstrap/
└── engine/ api/ web/
```

## Required Outputs

### Root entrypoints

- `README.md`
- `AGENTS.md`
- `CLAUDE.md` when Claude Code should use the workflow

No other generated root Markdown is allowed unless the user explicitly asks for it.

### Governance docs

- `docs/governance/STATUS.md`
- `docs/governance/WORKFLOW.md`
- `docs/governance/RELEASES.md`
- `docs/governance/context/` for CodeMap and context bundles when SDD-RIPER is active

### Current product docs

- `docs/README.md`
- `docs/product/CURRENT.md`
- `docs/product/vX.Y/README.md`
- requirements docs under `docs/product/vX.Y/requirements/`
- phase plans under `docs/product/vX.Y/phases/PHASE-*/`
- SPEC docs and technical contracts under `docs/product/vX.Y/phases/PHASE-*/specs/`
- decision records under `docs/product/vX.Y/decisions/`

Default authoring order is requirements first, then phase planning, then phase-level SPEC split.

Do not put PRDs, phase plans, and SPEC docs in the same folder. A SPEC should normally have a phase directory as its parent context.

When SDD-RIPER is active:
- requirements and phase plans must be reviewed before code execution
- phase specs should be executable enough for implementation with near-zero freedom
- review reports should compare spec and implementation
- implementation records should capture Reverse Sync updates before archive completion

### Archive

- `docs/archive/README.md`
- archived previous-version snapshots
- archived bootstrapping docs, drafts, and legacy work instructions

## Required Rules

- exactly one current version is active
- archive is historical only
- current entrypoints must point to the active version
- previous versions must be snapshotted under `docs/archive/` before current docs are upgraded
- default upgrades must not empty `docs/`
- runtime code directories must stay intact unless the user explicitly requests code moves
- generated docs must not be staged, committed, or pushed unless the user asks
- newly generated untracked docs should be kept local through `.git/info/exclude`, not repository `.gitignore`

## Migration Rules

When converting from a previous layout:
- copy old current docs into `docs/archive/` as a historical snapshot
- keep active docs in `docs/` while the new current version is prepared
- rewrite root entrypoints so they point only to the new current version
- preserve old docs with clear historical labels
- verify that active docs no longer mention old current paths

Only move all current docs out of `docs/` when the user explicitly requests a full reset.
