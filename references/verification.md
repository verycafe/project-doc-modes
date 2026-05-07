# Verification Checklist

Run this checklist after creating or migrating a repository doc structure.

## 1. Structure Check

- verify the expected root folders exist
- verify current-version docs exist
- verify archive folders exist if historical docs were moved
- verify runtime code directories still exist if they existed before the migration
- if the repository started empty, verify no unrequested code roots were created
- verify root Markdown is limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- verify generated non-root Markdown lives under `docs/`
- verify archive docs live under `docs/archive/`
- verify requirements, phases, phase-level specs, and decisions are in separate folders
- in iterative mode, verify SPEC docs sit under a phase directory such as `docs/product/vX.Y/phases/PHASE-*/specs/`
- in collaboration mode with SDD-RIPER, verify SPEC docs sit under `docs/collaboration/sdd/phases/PHASE-*/specs/`
- when SDD-RIPER is active, verify CodeMap and context bundles live under `docs/governance/context/`
- verify generated docs were not staged or committed unless the user explicitly requested Git tracking
- verify newly generated untracked local-only docs are covered by `.git/info/exclude`

Suggested commands:

```bash
find . -maxdepth 1 -type f -name '*.md' | sort
find . -maxdepth 2 -type d | sort
find docs -maxdepth 7 -type f | sort
git status --short
```

## 2. Entrypoint Check

- root `README.md` points to the active docs
- root `AGENTS.md` points to the active rules
- root `CLAUDE.md` tells Claude Code to read `AGENTS.md` first when present
- root `CLAUDE.md` does not fork or replace `AGENTS.md`
- `docs/README.md` points to the active docs for the chosen mode
- in iterative mode, `docs/product/CURRENT.md` points to the correct version path
- in collaboration mode, `docs/collaboration/ROLE_MATRIX.md` and current role docs exist when role boundaries are active
- `docs/governance/` holds workflow, status, and release docs instead of root Markdown files
- archive docs are labeled historical
- archive docs are not used as active memory or task context
- active docs describe the project workflow directly instead of telling agents to invoke this skill
- current entrypoint docs use the chosen document language consistently
- current user-facing mode labels follow the chosen display language
- when the repo already had code, the generated docs reflect the confirmed role and current phase-doc context
- when collaboration mode is active, the current role and role-specific editable/forbidden paths are explicit
- when SDD-RIPER is active, active docs identify the current stage, HIL gates, Plan Approved requirement, Review path, and Reverse Sync record path

## 3. Stale Reference Check

Search current-entry docs for:
- old absolute paths
- old version folders
- old mode-specific current directories
- stale role names if the repo has migrated to unified mode
- tool leakage such as installed skill paths or command names

Suggested command pattern:

```bash
rg -n "old-path|old-version|legacy-mode-name" AGENTS.md CLAUDE.md README.md docs -g '!docs/archive/**'
```

The result should be empty or intentionally limited to historical mentions.

Suggested tool-leakage check:

```bash
rg -n 'project-doc-modes|(^|[^[:alnum:]_./-])(/project-doc-modes|/sdd)([^[:alnum:]_./-]|$)|\$project-doc-modes|\.codex/skills|\.claude/skills|SKILL\.md' AGENTS.md CLAUDE.md README.md docs -g '!docs/archive/**'
rg -n '/Users/|~/|\$HOME|/private/' AGENTS.md CLAUDE.md README.md docs -g '!docs/archive/**'
test ! -f CLAUDE.md || rg -i 'read .*AGENTS\.md.*first|先.*AGENTS\.md' CLAUDE.md
test ! -f AGENTS.md || rg -i 'canonical|规范入口|治理入口|source of truth' AGENTS.md
```

The two denylist searches must be empty for target repositories unless the target repository is the `project-doc-modes` skill package itself. The bridge checks must find the expected `CLAUDE.md` and `AGENTS.md` language when those files exist.
The slash-command pattern is intentionally command-shaped so legal paths such as `docs/collaboration/sdd/` are not flagged. Keep these regexes single-quoted so `$HOME` and `$project-doc-modes` are matched literally instead of expanded by the shell.

## 4. Root Layout Check

Generated root Markdown should be only:
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`

Root entrypoint responsibilities:
- `AGENTS.md`: canonical cross-agent governance
- `CLAUDE.md`: Claude Code bridge to `AGENTS.md`
- `README.md`: human-facing overview

If `STATUS.md`, `WORKFLOW.md`, `RELEASES.md`, `SPEC.md`, `PRD.md`, or root `archive/` exists:
- leave pre-existing files untouched unless migration was requested
- do not link them as current docs
- migrate or copy their content into the correct `docs/` category only when the user asked for restructuring

## 5. Archive Upgrade Check

For upgrades, confirm:
- a snapshot was copied into `docs/archive/`
- active docs still exist under `docs/`
- `docs/` was not emptied
- entrypoints point to the upgraded current docs, not the archived snapshot
- no destructive reset happened unless the user explicitly requested it

## 6. SDD-RIPER Check

When SDD-RIPER is active, confirm:
- requirements exist before phase plans
- phase plans exist before phase-level SPEC docs
- SPEC docs are nested under their phase
- SDD-RIPER paths match the active mode instead of forcing `docs/product/vX.Y` into collaboration mode
- code execution docs require approved plans
- review docs compare intended behavior with implementation
- bug-fix flow updates specs before or with code
- archive flow includes Reverse Sync notes or implementation records

## 7. Final Rule

Do not declare success until:
- the active mode is clear
- current entrypoints are internally consistent
- archive content is historical only
- no accidental duplicate current source-of-truth remains
- root Markdown is limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- `AGENTS.md` is the canonical cross-agent governance entrypoint
- `CLAUDE.md` bridges Claude Code to `AGENTS.md`
- generated non-root Markdown is categorized under `docs/`
- requirements, phases, specs, and decisions are not mixed into one folder
- SPEC docs are nested under the phase they execute
- generated target docs do not mention this skill, its commands, installed `SKILL.md`, or local absolute install paths
- SDD-RIPER projects identify stage, gates, review, and Reverse Sync paths
- any original empty code directories were preserved when present
- an originally empty repository remains free of invented code roots unless the user requested placeholders
- generated docs remain unstaged and uncommitted unless the user asked for Git tracking
- newly generated untracked local-only docs are protected through `.git/info/exclude`
- the language of newly created current docs is explicit or can be clearly inferred from the repository context
- current Markdown docs are consistently Chinese or consistently English unless bilingual output was explicitly requested
- for non-empty code repositories, the mode, role, phase-doc context, and document language were explicitly gathered or confirmed before restructuring
- for empty or documentation-first repositories, the mode, role or ownership plan, initial version or phase, starter-code-directory choice, and document language were explicitly gathered or confirmed before restructuring
- for collaboration mode, the current operating role and the edit matrix for each role were explicitly gathered, confirmed, or deliberately marked as pending
