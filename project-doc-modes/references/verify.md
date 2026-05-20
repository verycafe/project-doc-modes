# Verify Workflow

Use this reference for read-only structure, entrypoint, local-only, and leakage checks.

## Rules

`verify` must not modify files unless the user explicitly asks for repairs.

Report findings with exact file paths and commands run.

## Structure Checks

Check:

- root Markdown is limited to `AGENTS.md`, `CLAUDE.md`, and `README.md` for target repositories
- generated non-root Markdown lives under `docs/`
- archive docs live under `docs/archive/`
- `docs/README.md` exists
- active mode pointer exists:
  - iterative: `docs/product/CURRENT.md`
  - collaboration: `docs/collaboration/ROLE_MATRIX.md`
- PRD, PHASE, SPEC, and decisions are separate
- iterative SPEC docs sit under `docs/product/vX.Y/phases/PHASE-*/specs/`
- collaboration SPEC docs sit under `docs/collaboration/sdd/phases/PHASE-*/specs/`
- `docs/governance/context/GLOSSARY.md` exists or is intentionally deferred
- `docs/governance/research/` exists or is intentionally deferred
- `docs/governance/experience/` exists or is intentionally deferred
- generated docs were not staged or committed unless requested

## Entrypoint Checks

Check:

- root `README.md` points to active docs
- `AGENTS.md` is the canonical governance entrypoint
- `CLAUDE.md` tells Claude Code to read `AGENTS.md` first
- `docs/README.md` points to active docs
- archive docs are labeled historical
- target-project docs describe the project workflow directly instead of telling agents to invoke this skill

## Leakage Checks

For target repositories, these searches should be empty unless the target is this skill package itself:

```bash
rg -n 'project-doc-modes|(^|[^[:alnum:]_./-])(/project-doc-modes(-sdd|-sync|-verify)?|/sdd)([^[:alnum:]_./-]|$)|\$project-doc-modes|hooks\.md|\.codex/skills|\.claude/skills|SKILL\.md' AGENTS.md CLAUDE.md README.md docs -g '!docs/archive/**'
rg -n '/Users/|~/|\$HOME|/private/' AGENTS.md CLAUDE.md README.md docs -g '!docs/archive/**'
```

For this skill package source repo, `project-doc-modes`, `install.md`, `hooks.md`, and runtime paths may be intentional source-package references.

## Code Immutability Checks

For protected code/config/test paths:

```bash
git status --short -- <protected-code-config-test-paths>
git diff --name-status -- <protected-code-config-test-paths>
```

Both commands should be empty unless the user explicitly requested code changes.

## Local-Only Checks

Generated untracked docs should be covered by `.git/info/exclude`, not `.gitignore`.

Check:

```bash
git ls-files --others --exclude-standard
git status --short
```
