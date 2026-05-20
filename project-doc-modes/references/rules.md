# Project Doc Modes Rules

Use this reference for mode-specific layouts, SDD-RIPER governance, and final verification.

## Operating Modes

Choose one operating mode before acting:
- `init`: first activation, migration, or full upgrade of the repository documentation system.
- `sync`: hook-safe incremental Reverse Sync after the active documentation system already exists.
- `verify`: read-only structure, entrypoint, local-only, and leakage checks.

Mode rules:
- `init` may ask short setup questions, create pre-migration archive snapshots, and build or upgrade the active docs.
- `sync` must be non-interactive and must not rerun the full migration flow.
- `verify` must not modify files unless the user explicitly asks for repairs.
- Hooks should call `sync` first and optionally `verify` after sync, not `init`.

## Activation Safety

This section applies when the installed skill is activated inside a target repository.

Activation rules:
- The skill package repository is only the original package; target-project docs are generated only inside the target repository after activation.
- Treat user code, tests, dependencies, configuration, APIs, data schemas, and runtime behavior as read-only evidence unless the user explicitly asks for code changes.
- Do not delete, rewrite, refactor, move, or simplify user code or product logic while scaffolding documentation governance.
- If repository docs and code disagree, record the mismatch and prefer the real implementation as evidence; do not silently change code to match docs.
- If existing repository rules conflict with this workflow, surface the conflict before replacing governance.

Existing-docs migration rules:
- If any target-repository docs already exist, create a pre-migration backup under `docs/archive/` before reading, understanding, moving, rewriting, or replacing doc contents.
- Exclude existing `docs/archive/` content from the backup to avoid copying archives into themselves.
- Read the backed-up docs, current docs, and relevant code/config before producing the new active structure.
- Use code evidence to validate and correct the generated docs; distinguish confirmed behavior from assumptions.
- When context is complex, create `docs/governance/context/MIGRATION_NOTES.tmp.md` as local-only working notes during migration. Fold durable findings into active docs or leave the file clearly labeled as temporary evidence.
- Do not delete old docs during migration. Archive them with historical labels or leave them in place until the new active docs are internally consistent.

## Collaboration Mode

Use collaboration mode when a repository is intentionally split by role or ownership.

Required root entrypoints:
- `AGENTS.md`: canonical cross-agent governance, ownership boundaries, editable/read-only/forbidden paths, reading order, verification commands.
- `CLAUDE.md`: Claude Code bridge to `AGENTS.md` when Claude Code should use the workflow.
- `README.md`: human-facing project overview.

Required docs:
- role matrix: `docs/collaboration/ROLE_MATRIX.md`
- role guides/status/handoffs: `docs/collaboration/<role>/`
- governance/status/handoff rules: `docs/governance/`
- archive: `docs/archive/`
- context bundle when needed: `docs/governance/context/`

Rules:
- Do not infer the current operating role when multiple roles exist; confirm it or mark it pending.
- Define editable, read-only, and forbidden paths per role before claiming collaboration mode is ready.
- Each role guide must name the status file that gets updated after every task, and handoff docs must point to that status file.
- If no code exists, define role boundaries over docs instead of inventing code roots.
- Do not mix collaboration mode with versioned product docs unless the user explicitly asks for a hybrid.
- If migrating away from collaboration mode, copy current role docs into `docs/archive/` before rewriting current docs.

## Iterative Mode

Use iterative mode when one product/repository moves through versioned source-of-truth docs.

Required root entrypoints:
- `README.md`
- `AGENTS.md`
- `CLAUDE.md` as a Claude Code bridge to `AGENTS.md` when Claude Code should use the workflow.

Required docs:
- `docs/README.md`
- `docs/governance/STATUS.md`
- `docs/governance/WORKFLOW.md`
- `docs/governance/RELEASES.md`
- `docs/governance/context/` for CodeMap and context bundles when SDD-RIPER is active
- `docs/product/CURRENT.md`
- `docs/product/vX.Y/README.md`
- requirements under `docs/product/vX.Y/requirements/`
- phase plans under `docs/product/vX.Y/phases/PHASE-*/`
- specs under `docs/product/vX.Y/phases/PHASE-*/specs/`
- decisions under `docs/product/vX.Y/decisions/`
- historical snapshots under `docs/archive/`

Rules:
- Exactly one current version is active.
- Authoring order is requirements first, then phase planning, then phase-level SPEC split.
- Do not put PRDs, phase plans, and SPEC docs in the same folder.
- SPEC docs must normally sit under the phase they execute.
- Previous current docs must be copied into `docs/archive/` before current docs are upgraded.
- Default upgrades must not empty `docs/`.
- Runtime code directories stay intact unless the user explicitly requests code moves.
- If the repository started empty, do not create code roots unless the user asks for placeholders.

## SDD-RIPER

Use SDD-RIPER when the user asks for team vibe coding, spec-driven development, AI coding governance, or reproducible code execution.

Operating laws:
- No Spec, No Code: code edits need an active requirement, phase plan, and executable spec.
- Spec is Truth: active specs define intended behavior; implementation drift needs review.
- Reverse Sync: bugs and discoveries update specs first or in the same change as code.
- If existing repository rules say implementation outranks docs, surface that conflict before changing governance; do not silently replace the repository's rule hierarchy.

Stages:
- Pre-Research: CodeMap and context bundle after repository inspection.
- Research: evidence-backed findings.
- Innovate: 2-3 options with tradeoffs when multiple viable paths exist.
- Plan: atomic checklist with file paths and acceptance criteria; plan approval required before code.
- Execute: implement the approved plan; stop if the plan is wrong or incomplete.
- Review: compare spec and implementation.
- Archive: snapshot, Reverse Sync, reusable lessons; current docs stay available.

Mode-aware paths:
- CodeMap: `docs/governance/context/CODEMAP.md`
- Context bundle: `docs/governance/context/CONTEXT_BUNDLE.md`
- Iterative requirements: `docs/product/vX.Y/requirements/`
- Iterative phase plans: `docs/product/vX.Y/phases/PHASE-*/PLAN.md`
- Iterative specs: `docs/product/vX.Y/phases/PHASE-*/specs/`
- Iterative reviews: `docs/product/vX.Y/phases/PHASE-*/REVIEW.md`
- Iterative Reverse Sync: `docs/product/vX.Y/phases/PHASE-*/IMPLEMENTATION_RECORD.md`
- Collaboration requirements: `docs/collaboration/sdd/requirements/`
- Collaboration phase plans: `docs/collaboration/sdd/phases/PHASE-*/PLAN.md`
- Collaboration specs: `docs/collaboration/sdd/phases/PHASE-*/specs/`
- Collaboration reviews: `docs/collaboration/sdd/phases/PHASE-*/REVIEW.md`
- Collaboration Reverse Sync: `docs/collaboration/sdd/phases/PHASE-*/IMPLEMENTATION_RECORD.md`

Reverse Sync records must include changed behavior, verification commands and output, and unresolved risks. Write commit, PR, deploy, or issue links only when they already exist locally or the user provides them; never invent links.

Human gates:
- HIL-1 Spec Review: approve requirements, phase plan, and specs before execution.
- HIL-2 Code Review: approve critical code or pull request changes.
- HIL-3 Release Approval: approve production deployment or irreversible operations.
- HIL-4 Reverse Sync Review: confirm implementation records and knowledge updates before archive completion.

Portability:
- Treat Claude Code, Git hooks, CI, OpenSpec, MCP, deployment docs, and other tools as optional integrations.
- Generate tool-specific files only when the user explicitly asks or the target repository already uses them.
- If the user explicitly asks for OpenSpec-style dual directories, keep them under `docs/openspec/specs/` and `docs/openspec/changes/`, not root `specs/` or `changes/`.
- Keep the portable source of truth in Markdown under `docs/`.

## Incremental Sync

Use this section for hook-driven or session-end documentation updates after initial activation.

Inputs:
- latest session summary, if available
- changed file names from `git status --short` or `git diff --name-status`
- relevant diff hunks only when needed to understand behavior changes
- verification commands and actual output
- explicit user decisions, unresolved risks, rejected options, and implementation discoveries

Required first read:
- root entrypoints: `AGENTS.md`, `CLAUDE.md`, `README.md`
- `docs/README.md`
- the current mode pointer, such as `docs/product/CURRENT.md` or `docs/collaboration/ROLE_MATRIX.md`
- active phase, review, and Reverse Sync paths when SDD-RIPER is active

Allowed updates:
- `docs/governance/STATUS.md`
- `docs/governance/context/CODEMAP.md` or `docs/governance/context/CONTEXT_BUNDLE.md` when the session adds durable code evidence
- active `IMPLEMENTATION_RECORD.md`
- active `REVIEW.md`
- decision records, release notes, role status, handoff docs, or index files directly affected by the session
- PRD, PHASE, or SPEC docs only when the session explicitly changes requirements, intended behavior, architecture, acceptance criteria, or delivery scope

Forbidden during `sync` unless the user explicitly asks for a full upgrade:
- asking setup questions during a hook
- choosing or changing collaboration vs iterative mode
- creating broad pre-migration archives
- rebuilding or relocating the docs tree
- moving historical docs
- rewriting unrelated PRD, PHASE, SPEC, README, or governance sections
- editing code, tests, dependencies, runtime configuration, APIs, schemas, or product logic

Missing input rule:
- If a hook payload lacks enough evidence, do not stop for a question. Record a concise pending item in the safest existing status or implementation record, or report the missing input when no safe doc target exists.

Incremental verification:
- changed docs stay in the active mode layout
- entrypoint links still point to active docs
- root Markdown remains limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- local-only rules still cover newly generated untracked docs
- changed docs and active entrypoints pass the leakage checks
- verification commands and actual output are recorded in the sync result

## Git Local-Only Policy

Generated target-project docs are local-only in Git by default.

- Do not run `git add`, `git commit`, or `git push` for generated docs unless the user explicitly asks to track, stage, commit, or push them.
- For newly generated untracked docs, including archive snapshots under `docs/archive/`, add relative paths to `.git/info/exclude`, not `.gitignore`.
- Do not add `.git/info/exclude` entries for files that Git already tracks; if tracked docs need to become local-only, explain the tracking state and ask before changing it.
- If the user later asks to track generated docs, remove matching exclude entries or use an explicit user-approved Git command.

## Verification

Run a structure check before claiming completion.

Structure:
- root Markdown is limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- generated non-root Markdown lives under `docs/`
- archive docs live under `docs/archive/`
- pre-existing docs were backed up before being moved, rewritten, or replaced
- user code, config, tests, dependencies, API behavior, data schemas, and runtime logic were not changed unless explicitly requested
- requirements, phases, specs, and decisions are separate
- iterative SPEC docs sit under `docs/product/vX.Y/phases/PHASE-*/specs/`
- collaboration SDD-RIPER SPEC docs sit under `docs/collaboration/sdd/phases/PHASE-*/specs/`
- CodeMap and context bundles live under `docs/governance/context/` when SDD-RIPER is active
- generated docs were not staged or committed unless the user explicitly requested Git tracking
- newly generated untracked local-only docs, including archive snapshots, are covered by `.git/info/exclude`

Entrypoints:
- root `README.md` points to active docs
- root `AGENTS.md` is the canonical governance entrypoint
- root `CLAUDE.md` tells Claude Code to read `AGENTS.md` first and does not fork it
- generated or repaired `CLAUDE.md` bridges to `AGENTS.md` first, then active docs; it is not a tool, plugin, command, or skill usage note
- `docs/README.md` points to active docs for the chosen mode
- iterative `docs/product/CURRENT.md` points to the correct version
- collaboration role matrix and current role docs exist when role boundaries are active
- archive docs are labeled historical and not used as active memory
- current docs describe the project workflow directly instead of telling agents to invoke this skill

Stale reference and leakage checks:
```bash
rg -n "old-path|old-version|legacy-mode-name" AGENTS.md CLAUDE.md README.md docs -g '!docs/archive/**'
rg -n 'project-doc-modes|(^|[^[:alnum:]_./-])(/project-doc-modes(-sync|-verify)?|/sdd)([^[:alnum:]_./-]|$)|\$project-doc-modes|\.codex/skills|\.claude/skills|SKILL\.md' AGENTS.md CLAUDE.md README.md docs -g '!docs/archive/**'
rg -n '/Users/|~/|\$HOME|/private/' AGENTS.md CLAUDE.md README.md docs -g '!docs/archive/**'
test ! -f CLAUDE.md || rg -i 'read .*AGENTS\.md.*first|先.*AGENTS\.md' CLAUDE.md
test ! -f AGENTS.md || rg -i 'canonical|规范入口|治理入口|source of truth' AGENTS.md
```

The two denylist searches must be empty for target repositories unless the target repository is this skill package itself.

Code immutability checks:
1. Before migration, list protected code/config/test paths identified during inspection.
2. After migration, run status and diff checks against those protected paths:

```bash
git status --short -- <protected-code-config-test-paths>
git diff --name-status -- <protected-code-config-test-paths>
```

Both commands must be empty unless the user explicitly requested code changes. If the repository is not using Git, compare a before/after file manifest or checksum for the protected paths and report the method used.

Archive upgrades:
- copy current docs into `docs/archive/` before editing the active docs
- exclude `docs/archive/` from the snapshot to avoid copying archives into themselves
- for first-time activation with existing docs, copy the pre-migration docs into `docs/archive/` before landing the new structure
- keep active docs under `docs/`
- do not empty `docs/`
- keep the previous version's behavior and functional logic as the locked historical baseline unless the user explicitly asks to change it
- entrypoints point to upgraded current docs, not the archived snapshot
- active context docs such as `docs/governance/context/CONTEXT_BUNDLE.md` point to the upgraded current version
- no destructive reset happened unless the user explicitly requested it

Final rule:
- Do not declare success until the active mode is clear, current entrypoints are internally consistent, archive content is historical only, no duplicate current source-of-truth remains, generated docs are local-only in Git unless requested otherwise, and the chosen language is consistent across current docs.
