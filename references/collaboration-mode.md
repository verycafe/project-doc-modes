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
├── CLAUDE.md
├── README.md
├── docs/
│   ├── README.md
│   ├── governance/
│   │   ├── STATUS.md
│   │   ├── WORKFLOW.md
│   │   ├── HANDOFF_RULES.md
│   │   └── context/
│   │       ├── CODEMAP.md
│   │       └── CONTEXT_BUNDLE.md
│   ├── collaboration/
│   │   ├── ROLE_MATRIX.md
│   │   ├── dev-a/
│   │   │   ├── GUIDE.md
│   │   │   ├── STATUS.md
│   │   │   └── HANDOFF.md
│   │   └── dev-b/
│   │       ├── GUIDE.md
│   │       ├── STATUS.md
│   │       └── DEV_A_HANDOFF.md
│   └── archive/
│       └── README.md
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
- `CLAUDE.md` as a Claude Code bridge to `AGENTS.md` when Claude Code should use the workflow
- `README.md`

No other generated root Markdown is allowed unless the user explicitly asks for it.

`AGENTS.md` is the canonical cross-agent governance file. `CLAUDE.md` should tell Claude Code to read `AGENTS.md` first, then follow the active collaboration docs under `docs/`.

### Role-specific docs

- role guide under `docs/collaboration/<role>/`
- role status board under `docs/collaboration/<role>/`
- handoff document from the other side under `docs/collaboration/<role>/`
- staged instructions under `docs/governance/` or `docs/collaboration/`
- shared role matrix under `docs/collaboration/ROLE_MATRIX.md`
- SDD-RIPER requirements, phase plans, and specs under `docs/collaboration/sdd/` when SDD-RIPER is active

When SDD-RIPER is active, role docs must name:
- the current RIPER stage
- who may approve specs and plans
- which role owns Reverse Sync updates
- which handoff is required before execution crosses a role boundary

## Required Rules

- which directories are read-only for each role
- which directories or docs are directly editable for each role
- which internal interfaces are the source-of-truth
- what files must be read before work begins
- what verification commands must be run
- what status file must be updated after each task
- what handoff document is required before crossing a role boundary
- generated docs must not be staged, committed, or pushed unless the user asks
- newly generated untracked docs should be kept local through `.git/info/exclude`, not repository `.gitignore`
- historical material belongs under `docs/archive/`

## Default Documentation-Only Pattern

If the repository has no code yet, define role boundaries over documentation paths instead of inventing code roots.

Typical default pattern:
- each role may edit its own role folder
- each role may edit its outgoing handoff doc
- shared phase docs are read-only unless explicitly assigned
- `docs/archive/` remains controlled and should not be used as a current working area

## Do Not Mix With Iterative Mode By Default

Avoid having both of these active at the same time unless the user explicitly wants a hybrid:
- role-split current docs
- versioned current docs

If migrating away from collaboration mode:
- copy the old role docs into `docs/archive/` before rewriting current docs
- keep them available for history
- remove them from current entrypoints

Only clear the current collaboration docs when the user explicitly requests a full reset.
