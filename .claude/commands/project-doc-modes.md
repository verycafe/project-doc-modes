---
description: Inspect the repository, ask short setup questions, then scaffold or migrate docs with project-doc-modes.
argument-hint: [goal, mode, or language]
---

Use the `project-doc-modes` workflow for this task.

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
5. Scaffold or migrate the repository docs with minimal changes.
6. Run the verification checklist before claiming completion.

If the user supplied extra arguments, treat them as additional intent:

$ARGUMENTS
