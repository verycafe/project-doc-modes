---
description: Inspect the repository, ask short setup questions, then scaffold or migrate docs with project-doc-modes.
argument-hint: [goal, mode, or language]
---

Use the `project-doc-modes` workflow for this task.

For SDD-RIPER-only work, `/sdd` is the shorter command, but this command may also handle SDD-RIPER when the user asks for it.

Primary source of truth:
- @SKILL.md

Read the minimum extra context you need:
- @references/collaboration-mode.md when the repo is using `collaboration mode`
- @references/iterative-mode.md when the repo is using `iterative mode`
- @references/verification.md before finishing

Expected behavior:
1. Inspect the target repository before changing docs.
2. Ask 1 to 3 short setup questions at a time instead of dumping a long checklist.
3. Confirm the mode, language, and current role or phase context before restructuring.
4. If `collaboration mode` is chosen, confirm the current role, editable paths, read-only or forbidden paths, and handoff rules before writing docs.
5. Keep root Markdown limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`; put generated docs under categorized `docs/` folders.
6. Keep generated docs local-only in Git unless the user explicitly asks to track, stage, or commit them.
7. For iterative docs, follow `PRD -> PHASE -> SPEC`: requirements first, phase plans next, SPEC docs under each phase.
8. When team vibe coding or SDD-RIPER is requested, read @references/sdd-riper.md and record stage, approval gates, review path, and Reverse Sync path.
9. For upgrades, copy a snapshot into `docs/archive/` before updating current docs; do not empty `docs/` unless the user requests a full reset.
10. Scaffold or migrate the repository docs with minimal changes.
11. Run the verification checklist before claiming completion.

If the user supplied extra arguments, treat them as additional intent:

$ARGUMENTS
