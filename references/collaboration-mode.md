# Collaboration Mode

Use collaboration mode when a repository is intentionally split by role or ownership.

## Purpose

This mode is for projects where:
- one role owns one subsystem
- another role owns another subsystem
- handoff documents are required
- code boundaries are enforced
- the doc system is part onboarding guide, part contract

## Typical Structure

```text
repo/
├── AGENTS.md
├── DEV-A/
│   └── handoff or interface docs
├── docs/
│   └── dev-b/
│       ├── GUIDE.md
│       ├── STATUS.md
│       ├── DEV_A_HANDOFF.md
│       ├── DEVB_MASTER.md
│       └── Phase*_Week*_Instructions.md
├── engine/   # owned by one side
├── api/      # owned by another side
└── web/
```

## Required Outputs

### Root governance

- `AGENTS.md`
  - define ownership boundaries
  - define the current operating role when known, or mark it as pending confirmation
  - define editable paths for each role
  - define forbidden directories
  - define read-only directories or docs for each role
  - define required reading order before work starts
  - define verification commands

### Role-specific docs

- role guide
- role status board
- handoff document from the other side
- staged instructions such as phase/week/day docs

## Required Rules

- which directories are read-only for each role
- which directories or docs are directly editable for each role
- which internal interfaces are the source-of-truth
- what files must be read before work begins
- what verification commands must be run
- what status file must be updated after each task
- what handoff document is required before crossing a role boundary

## Default Documentation-Only Pattern

If the repository has no code yet, define role boundaries over documentation paths instead of inventing code roots.

Typical default pattern:
- each role may edit its own role folder
- each role may edit its outgoing handoff doc
- shared phase docs are read-only unless explicitly assigned
- archive remains controlled and should not be used as a current working area

## Do Not Mix With Iterative Mode By Default

Avoid having both of these active at the same time unless the user explicitly wants a hybrid:
- role-split current docs
- versioned current docs

If migrating away from collaboration mode:
- move the old role docs into archive
- keep them available for history
- remove them from current entrypoints
