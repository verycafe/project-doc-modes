---
description: Start or apply SDD-RIPER governance with project-doc-modes.
argument-hint: [goal, version, phase, or language]
---

Use the `project-doc-modes` workflow in SDD-RIPER mode.

Primary source of truth:
- @SKILL.md
- @references/sdd-riper.md

Read the minimum extra context you need:
- @references/iterative-mode.md when the repo should use versioned product docs
- @references/collaboration-mode.md when the repo should use role boundaries
- @references/verification.md before finishing

Expected behavior:
1. Inspect the target repository before changing docs.
2. Ask 1 to 3 short setup questions at a time.
3. Keep generated docs local-only in Git unless the user explicitly asks to track, stage, or commit them.
4. Organize work as `PRD -> PHASE -> SPEC`.
5. Put CodeMap and context bundles under `docs/governance/context/`.
6. Record the current RIPER stage, human approval gates, spec-vs-code review path, and Reverse Sync path.
7. For upgrades, copy a snapshot into `docs/archive/` before updating current docs; do not empty `docs/` unless the user requests a full reset.
8. Run the verification checklist before claiming completion.

If the user supplied extra arguments, treat them as additional intent:

$ARGUMENTS
