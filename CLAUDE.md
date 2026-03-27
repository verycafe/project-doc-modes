# project-doc-modes

This repository ships a Markdown-first workflow for scaffolding, reorganizing, and migrating repository documentation.

See @SKILL.md for the source-of-truth workflow.

When using this workflow in Claude Code:

- keep `SKILL.md` and the files under `references/` as the canonical instructions
- inspect the target repository before creating or moving Markdown files
- ask short setup questions in small turns instead of dumping a long checklist
- support either Chinese or English for prompts, labels, and generated Markdown
- in `collaboration mode`, confirm the current role, editable paths, read-only or forbidden paths, and handoff expectations before writing docs
- preserve existing runtime code roots unless the user explicitly asks to move them
- run the verification checklist before claiming completion

The project-specific slash command for this workflow lives at `.claude/commands/project-doc-modes.md`.
