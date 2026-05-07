# project-doc-modes

This repository ships a Markdown-first workflow for scaffolding, reorganizing, and migrating repository documentation.

See @SKILL.md for the source-of-truth workflow.

When using this workflow in Codex:

- keep `SKILL.md` and the files under `references/` as the canonical instructions
- inspect the target repository before creating or moving Markdown files
- ask short setup questions in small turns instead of dumping a long checklist
- support either Chinese or English for prompts, labels, and generated Markdown
- keep root Markdown limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- make generated `AGENTS.md` the canonical cross-agent governance entrypoint
- make generated `CLAUDE.md` a Claude Code bridge that tells Claude to read `AGENTS.md` first
- put generated non-root Markdown under categorized `docs/` folders
- keep generated docs local-only in Git unless the user explicitly asks to track or commit them
- in iterative mode, follow `PRD -> PHASE -> SPEC`: requirements first, phase plans next, SPEC docs under each phase
- when team vibe coding or SDD-RIPER is requested, record the current stage, human approval gates, spec-vs-code review path, and Reverse Sync path
- when upgrading docs, copy a snapshot into `docs/archive/` before updating current docs and do not empty `docs/` by default
- in `collaboration mode`, confirm the current role, editable paths, read-only or forbidden paths, and handoff expectations before writing docs
- preserve existing runtime code roots unless the user explicitly asks to move them
- run the verification checklist before claiming completion

The Claude Code slash commands live at `.claude/commands/project-doc-modes.md` and `.claude/commands/sdd.md`; Codex uses `SKILL.md` and `agents/openai.yaml`.
