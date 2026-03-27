# Iterative Mode

Use iterative mode when a repository is under unified development and the team wants versioned source-of-truth docs.

## Purpose

This mode is for projects where:
- current work should point to one active version
- old versions should remain readable but inactive
- repo-wide workflow rules should live at the root
- documentation should be organized around product versions instead of role boundaries

## Typical Structure

```text
repo/
├── AGENTS.md
├── README.md
├── STATUS.md
├── WORKFLOW.md
├── RELEASES.md
├── archive/
│   ├── README.md
│   ├── versions/
│   │   └── v0.2/
│   └── mvp-bootstrap/
├── docs/
│   ├── README.md
│   └── product/
│       ├── CURRENT.md
│       └── v0.3/
│           ├── README.md
│           ├── PRD.md
│           ├── BUYER.md
│           ├── SELLER.md
│           ├── ADMIN.md
│           ├── PLATFORM_BACKEND.md
│           ├── API_SPEC.md
│           ├── DATA_MODEL.md
│           ├── STATE_MACHINES.md
│           ├── UI_GUIDELINES.md
│           ├── ROADMAP.md
│           ├── CHANGELOG.md
│           ├── OPEN_QUESTIONS.md
│           └── decisions/
└── engine/ api/ web/
```

## Required Outputs

### Repository-level governance

- `README.md`
- `AGENTS.md`
- `STATUS.md`
- `WORKFLOW.md`
- `RELEASES.md`

### Current product docs

- `docs/README.md`
- `docs/product/CURRENT.md`
- `docs/product/vX.Y/README.md`
- major product docs for each audience or concern

### Archive

- `archive/README.md`
- archived previous versions
- archived bootstrapping docs, specs, drafts, and legacy work instructions

## Required Rules

- exactly one current version is active
- archive is historical only
- current entrypoints must point to the active version
- previous versions must be moved, not left as parallel current trees
- runtime code directories must stay intact unless the user explicitly requests code moves

## Migration Rules

When converting from a previous layout:
- move old current docs into `archive/`
- rewrite root entrypoints so they point only to the new current version
- preserve old docs with clear historical labels
- verify that active docs no longer mention old current paths
