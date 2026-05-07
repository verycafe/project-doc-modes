---
name: project-doc-modes
description: Use this skill when a user wants Codex or another coding agent to scaffold, reorganize, or migrate a repository's documentation and governance structure into either a role-split collaboration mode, a versioned iterative mode, or a team vibe coding / SDD-RIPER workflow. It is for creating and updating folder layout, archive layout, repo rules, version entrypoints, PRD to PHASE to SPEC docs, and markdown source-of-truth documents based on the current codebase.
---

# Project Doc Modes

## Overview

This skill defines a reusable workflow for turning a repository into one of two document-management modes:
- `collaboration mode`: role-split ownership with explicit boundaries, handoff docs, and role-specific work instructions
- `iterative mode`: unified repository workflow with versioned product docs, archive rules, and repository-wide governance files

It can also layer SDD-RIPER rules onto either mode when the repository needs team vibe coding, spec-driven execution, or AI coding governance.

Keep the core portable:
- prefer Markdown rules, file templates, and verification steps
- do not depend on Node.js unless the user explicitly asks for automation scripts
- preserve current code directories unless the user explicitly asks to move code

## Non-Negotiable Defaults

Apply these defaults unless the user explicitly requests a different repository policy:

- root Markdown is limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- all other generated Markdown belongs under `docs/`
- historical material belongs under `docs/archive/`, not root `archive/`
- product requirements, phase plans, and specs must follow the `PRD -> PHASE -> SPEC` chain
- do not stage, commit, or push generated docs
- keep newly generated docs local-only by default in Git repositories
- for SDD-RIPER projects, active specs are the source of intended behavior and code execution requires an approved plan

For Git repositories, local-only means:
- do not run `git add`, `git commit`, or `git push` unless the user asks
- for newly generated untracked doc paths, append local ignore patterns to `.git/info/exclude` instead of editing `.gitignore`
- do not add `.git/info/exclude` rules for files that are already tracked
- if a tracked root entrypoint such as `README.md`, `AGENTS.md`, or `CLAUDE.md` must change, edit it minimally and report that it remains a tracked Git change

Use a marked block when appending local excludes so future agents can maintain it safely:

```text
# project-doc-modes local docs
docs/
AGENTS.md
CLAUDE.md
README.md
```

Only include patterns for generated paths that should remain local in that target repository.

## Document Placement Contract

Use lowercase `docs/` unless the target repository already has an intentional uppercase `DOCS/` convention. Do not create both.

Default current-doc categories:
- `docs/governance/`: workflow, status, release notes, operating rules, handoff rules
- `docs/governance/context/`: CodeMap, context bundles, and repo evidence packs
- `docs/product/`: current product entrypoint and version folders
- `docs/product/vX.Y/requirements/`: PRDs, user needs, business requirements, audience docs
- `docs/product/vX.Y/phases/`: phase roadmap, phase plans, and phase status
- `docs/product/vX.Y/phases/PHASE-*/specs/`: SPEC files and technical contracts produced for that phase
- `docs/product/vX.Y/decisions/`: ADRs and decision records
- `docs/archive/`: historical snapshots and inactive docs

Default authoring flow:
1. write or update the requirement/proposal docs first
2. derive phase plans from those requirements
3. split each phase into the SPEC docs needed to execute that phase

Do not put `PRD.md`, phase plans, and `SPEC.md` documents in the same folder. If the target repository uses names such as `SPEC.md`, classify by intent:
- requirement or product proposal -> `requirements/`
- phase plan, milestone, roadmap, rollout plan -> `phases/PHASE-*/`
- phase-level technical contract, API, data model, trace format -> `phases/PHASE-*/specs/`

## When To Use

Use this skill when the user asks for any of the following:
- create a reusable repository documentation standard
- choose between a collaboration workflow and an iterative workflow
- apply team vibe coding, SDD-RIPER, or spec-driven AI coding rules to a repository
- generate versioned docs and archive folders
- create repo governance docs such as `AGENTS.md`, `CLAUDE.md`, `README.md`, or files under `docs/governance/`
- reorganize old docs into a historical archive
- migrate a project from a role-split structure into a unified versioned structure
- recreate the same document system for a new project

Do not use this skill when the user only wants:
- a single feature PRD
- a one-off README rewrite
- implementation-only code changes without repository-structure work

## Command Entrypoints

Codex:
- use `$project-doc-modes` for the general workflow
- use `$project-doc-modes SDD` or `$project-doc-modes SDD-RIPER` when the user wants spec-driven team vibe coding

Claude Code:
- use `/project-doc-modes` for the general workflow
- use `/sdd` as the short command for SDD-RIPER governance

All command wrappers must point back to this `SKILL.md` and the relevant `references/` files instead of forking the workflow.

## Workflow

### 1. Inspect First

Before writing files:
- inspect the repository root
- identify current code directories that must remain stable
- inspect current docs and repo rules
- identify whether the repo already has historical docs that should be archived rather than deleted
- identify the dominant language of the current active docs, if any
- inspect `git status --short` when the target is a Git repository
- identify which docs are already tracked before deciding local-only exclude rules

Treat existing code, config, and active docs as source material. Do not invent paths.

If the repository has no runtime code directories yet:
- treat it as a greenfield or documentation-first setup
- scaffold docs and governance around the requested mode
- do not invent `engine/`, `api/`, `web/`, or equivalent code roots unless the user explicitly asks for placeholders

If code directories exist but are empty:
- preserve those directories as intentional placeholders
- note that implementation has not started yet
- continue scaffolding docs without treating the empty directories as an error

If the target needs team vibe coding, SDD-RIPER, spec-driven execution, AI coding governance, or code-facing workflow gates, read:
- `references/sdd-riper.md`

### 1.5. Ask Before Acting

Stay in questioning mode before restructuring docs.

For repositories that already contain runtime code, if the user has not already answered them, ask concise questions about:
- which mode to use: `collaboration mode` or `iterative mode`
- the user's current role or ownership boundary in the repository
- whether there is a current phase, sprint, week, or milestone document, and where it lives
- which language the generated Markdown docs should use: Chinese or English
- whether to enforce SDD-RIPER gates such as Spec Review, Plan Approved, code review, release approval, and Reverse Sync when the user asked for code-facing governance

For repositories that are empty or documentation-first, if the user has not already answered them, ask concise questions about:
- which mode to use: `collaboration mode` or `iterative mode`
- the user's current role, expected ownership boundary, or whether the repo is single-owner for now
- the initial version or phase name to use, such as `v0.1`, `MVP`, or `Phase 1`
- whether to create any starter code directories or keep the repository documentation-only for now
- which language the generated Markdown docs and skill-facing labels should use: Chinese or English

Questioning rules:
- ask these questions after inspection and before creating, moving, or rewriting Markdown files
- default to a friendly, conversational style instead of a dense requirements dump
- ask in short turns, usually 1 to 3 questions at a time
- prefer short bullet questions or short line-by-line prompts over long numbered paragraphs
- start with the highest-leverage questions first, then ask follow-up questions after the user answers
- do not ask every possible question up front when a smaller first turn will unblock the next step
- after each user reply, decide whether you have enough information to proceed or whether one more short follow-up turn is still needed
- if the repository already contains strong evidence for one answer, present that evidence and ask for confirmation rather than silently deciding
- if the user explicitly wants the skill's display language set, treat that as the language for generated Markdown headings, labels, and navigation text
- use the chosen display language for the questions themselves
- for repositories that already contain runtime code, usually ask mode and current role first, then ask about phase-doc context and language
- for empty or documentation-first repositories, usually ask mode, initial version or phase, and language first, then ask about ownership shape and starter code directories if still needed
- offer sensible defaults inline when they reduce friction
- keep user-facing mode labels natural: prefer `协作模式` and `迭代模式` in Chinese prompts unless the English canonical names are needed for clarity
- if a repository is empty or documentation-first and the user already provided mode, language, and initial version or phase, you may infer the rest conservatively

If `collaboration mode` is chosen, ask collaboration-specific follow-up questions before writing docs:
- which role the current user is acting as right now
- which paths that role may edit directly
- which paths are read-only or forbidden for that role
- whether there are shared docs that all roles may edit, or whether shared docs also require approval
- which handoff document is required before crossing a role boundary

Collaboration-mode intake rules:
- do not infer the current operating role from the repository structure alone when multiple roles exist
- if the user has role names but no edit matrix yet, propose a default path-boundary matrix and ask for confirmation
- if the repository is documentation-only, define edit scopes for docs and archive paths rather than inventing code paths
- if the repository has code, define edit scopes for both code directories and role-specific docs
- do not claim collaboration mode is set up until `AGENTS.md` or an equivalent active doc records editable, read-only, and forbidden paths per role

Suggested staged question flows:

For repositories that already contain runtime code, when the chosen display language is English:

```text
Turn 1
I checked the repo and it already has code in place. Before I change the doc structure, let me confirm two basics:

- Do you want collaboration mode or iterative mode?
- What is your current role or ownership boundary in this repo?

Turn 2
Thanks. One more thing before I lay out the docs:

- Do you already have a current phase or milestone doc? If yes, where is it?

Turn 3
Last detail: should the generated docs and labels use English or Chinese?

If collaboration mode is chosen, add:

Turn 4
To make the boundaries enforceable, I need your current operating role and edit scope:

- Which role are you acting as right now?
- Which paths may that role edit directly?
- Which paths should be read-only or forbidden for that role?
```

For repositories that already contain runtime code, when the chosen display language is Chinese:

```text
第 1 轮
我先看过仓库了，里面已经有代码目录。开始整理文档前，我先确认两件基础信息：

- 你想用协作模式还是迭代模式？
- 你当前负责哪一块，或者你的 ownership 边界是什么？

第 2 轮
好，我再确认一件和当前流程有关的事：

- 现在有没有正在使用的阶段文档或 milestone 文档？如果有，路径是什么？

第 3 轮
最后一个小设置：这次生成的文档和标签用中文还是英文？

如果你选的是协作模式，再补一轮：

第 4 轮
为了把边界写成可执行规则，我还要确认 3 件事：

- 你当前实际扮演的是哪个角色？
- 这个角色可以直接编辑哪些路径？
- 哪些路径对这个角色是只读或禁止编辑？
```

For repositories that are empty or documentation-first, when the chosen display language is English:

```text
Turn 1
I checked the repo and it is currently empty. To get the doc structure started, let me confirm three basics:

- Do you want collaboration mode or iterative mode?
- What initial version or phase name should I use? If you do not care, I can start with v0.1.
- Should the generated docs and labels use English or Chinese?

Turn 2
If needed, I can confirm two optional details before scaffolding:

- Is this repo single-owner for now, or do you already have role boundaries in mind?
- Do you want starter code directories, or should I keep it documentation-only for now?

If collaboration mode is chosen and multiple roles are planned, add:

Turn 3
Before I finalize the collaboration docs:

- Which role are you acting as right now?
- Do you want me to generate a default editable/forbidden path matrix for each role?
```

For repositories that are empty or documentation-first, when the chosen display language is Chinese:

```text
第 1 轮
我看过了，这个仓库现在还是空的。为了把文档结构起好步，我先确认 3 个基础设置：

- 你想用协作模式还是迭代模式？
- 初始版本或阶段名要用什么？如果你不在意，我可以先用 v0.1。
- 这次生成的文档和标签用中文还是英文？

第 2 轮
如果还需要，我再补确认两件可选项：

- 这个仓库暂时是单人 owner，还是已经有明确的角色边界？
- 你要不要我先创建代码目录占位？如果你不指定，我就先保持纯文档仓库。

如果你选的是协作模式，而且已经确定有多个角色，再补一轮：

第 3 轮
在我把协作约束写进文档前，还要确认两件事：

- 你当前实际扮演的是哪个角色？
- 你要不要我顺手给每个角色生成一份默认的“可编辑 / 只读 / 禁止编辑”路径矩阵？
```

Record the answers and use them as constraints for the rest of the workflow.

### 1.6. Choose The Document Language

Before creating Markdown files, decide whether the new docs should be written in Chinese or English.

Language rules:
- if the user explicitly requests Chinese or English, use that language for all newly created current docs
- if the repository already has active current docs, inherit their dominant language unless the user asks to change it
- if the repository is empty and the user did not specify a language, default to the language used in the user's request
- only create bilingual docs when the user explicitly asks for bilingual output

Consistency rules:
- keep all newly created current-entry Markdown docs in one language
- do not mix Chinese and English across root governance files and current product docs unless the user explicitly asks for bilingual docs
- historical archive docs may remain in their original language
- keep file and folder names stable unless the user explicitly asks for localized filenames

Display-language rules:
- support Chinese or English for the skill's user-facing questions and generated Markdown labels
- when the chosen language is Chinese, present mode names as `协作模式` and `迭代模式` in user-facing text
- when the chosen language is English, present mode names as `collaboration mode` and `iterative mode`
- when needed for clarity, you may include the English canonical mode name in parentheses after the Chinese label

### 2. Decide The Mode

If the user already chose a mode, use it.

If the repository contains runtime code and the user has not yet confirmed the mode after inspection:
- ask before proceeding
- do not silently choose a mode just because one seems plausible

If not, decide based on repository intent:
- use `collaboration mode` when teams are split by ownership or role and need strict boundaries
- use `iterative mode` when the repository is moving as one product and needs versioned source-of-truth docs

For empty or nearly empty repositories:
- default to `iterative mode` when there is no evidence of role-split ownership
- only choose `collaboration mode` by default when the user explicitly describes separate owners, handoffs, or restricted boundaries

If the user is evolving from one mode to the other, preserve the old structure in archive form.

Read:
- `references/collaboration-mode.md`
- `references/iterative-mode.md`

### 3. Preserve Code, Reorganize Docs

Default rule:
- reorganize files, rules, and Markdown docs
- do not move runtime code directories unless the user explicitly asks

Typical protected code roots:
- `engine/`
- `api/`
- `web/`
- or equivalent service directories in the target repository

If no runtime code roots exist yet:
- keep the repository code-free by default
- create only the documentation, governance, and archive structure needed for the chosen mode
- avoid adding empty code folders unless the user explicitly wants starter directories

### 4. Create Or Refresh The Required Outputs

For either mode:
- create clear current-entry docs
- create archive rules
- create repository-level governance files
- ensure only one current version is marked as source-of-truth
- snapshot historical material into archive paths instead of deleting context
- keep root Markdown limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- keep all other generated Markdown under categorized `docs/` folders

Use the reference files for required outputs and folder layout.

### 5. Write Current-Version Docs

For the active mode, create the full document set the mode requires.

When writing the docs:
- use the chosen document language consistently across all newly created Markdown files
- preserve existing active-doc language in migrations unless the user explicitly requests a language switch
- if the user requests a language switch during migration, update current entrypoints to the new language and leave historical docs in archive with clear labels
- reflect the confirmed role and current phase-document context in the generated governance and handoff docs
- use the chosen display language for mode labels, section titles, prompts, and navigation text
- in collaboration mode, record the current operating role and the editable, read-only, and forbidden paths for each role in the active docs
- if SDD-RIPER is active, record the current RIPER stage, required evidence, HIL gates, and Reverse Sync expectations in the active docs

In iterative mode, this usually includes:
- `docs/README.md`
- `docs/product/CURRENT.md`
- `docs/product/vX.Y/README.md`
- `docs/product/vX.Y/requirements/...`
- `docs/product/vX.Y/phases/PHASE-*/...`
- `docs/product/vX.Y/phases/PHASE-*/specs/...`
- `docs/product/vX.Y/decisions/...`
- root `README.md`
- root `AGENTS.md`
- root `CLAUDE.md` when Claude Code should use the workflow
- `docs/governance/STATUS.md`
- `docs/governance/WORKFLOW.md`
- `docs/governance/RELEASES.md`
- `docs/governance/context/...` when CodeMap or context bundles are needed
- `docs/archive/`

In collaboration mode, this usually includes:
- root `AGENTS.md` with ownership boundaries
- root `CLAUDE.md` when Claude Code should use the workflow
- role handoff docs under `docs/collaboration/`
- role-specific guide and status docs under `docs/collaboration/`
- phase or task instructions under `docs/governance/` or `docs/collaboration/`

### 5.5. Upgrade And Archive Current Docs

When upgrading docs, do not empty `docs/` by default.

Default upgrade flow:
1. identify the active current docs from `docs/README.md`, `docs/product/CURRENT.md`, and root entrypoints
2. copy the current docs into `docs/archive/` as a timestamped or versioned snapshot
3. keep the active docs in place
4. update the active docs in place, or create the next current version only when the user requested a version bump
5. perform Reverse Sync updates when implementation discoveries changed requirements, specs, or decisions
6. update entrypoints after the new current docs are ready

Only move all current docs out of `docs/` or clear the current docs directory when the user explicitly asks for a full reset or destructive archive.

### 6. Update Entrypoints

After creating files:
- update root entrypoints to point to the active structure
- remove stale references to previous current-version paths
- keep archive references explicit and clearly labeled as historical
- keep root entrypoints from pointing at root `archive/`, root `STATUS.md`, root `WORKFLOW.md`, or root `RELEASES.md`

### 7. Verify

Always run a structure check before claiming completion.

Read:
- `references/verification.md`

At minimum:
- confirm required files exist
- confirm current-entry files point to the right paths
- confirm old-current paths no longer appear in active docs
- confirm archive-only docs remain outside the active entrypoint chain
- confirm pre-existing code directories still exist
- if the repository started empty, confirm no unrequested code roots were created
- confirm root Markdown is limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- confirm generated non-root Markdown is under `docs/`
- confirm archive content lives under `docs/archive/`
- confirm requirements, phases, phase-level specs, and decisions are in separate folders
- if SDD-RIPER is active, confirm docs identify the RIPER stage, approval gates, spec-vs-code review path, and Reverse Sync record path
- confirm generated docs were not staged or committed unless the user requested Git tracking
- confirm newly generated untracked local-only docs are covered by `.git/info/exclude` when the target is a Git repository
- confirm the chosen document language is applied consistently across newly created current docs
- if the repository already had runtime code, confirm the mode, role, phase-doc context, and document language were gathered or explicitly confirmed before restructuring
- if the repository started empty, confirm the mode, role or ownership plan, initial version or phase, starter-code-directory choice, and document language were gathered or explicitly confirmed before restructuring
- if collaboration mode is active, confirm the current role and role-specific edit boundaries are explicit in the current docs

## Mode Selection Rules

### Collaboration Mode

Choose this when:
- teams are split by ownership
- boundaries are strict
- handoffs are part of the process
- one side must not edit the other side's code or docs without approval

See:
- `references/collaboration-mode.md`

### Iterative Mode

Choose this when:
- the repo is in unified development
- one shared version should be the current source-of-truth
- old versions need archiving
- governance entrypoints should live at the repo root while detailed governance docs live under `docs/governance/`

See:
- `references/iterative-mode.md`

For spec-driven execution or team vibe coding, also read:
- `references/sdd-riper.md`

## Output Standards

- keep docs concise and navigable
- create one obvious current-version entrypoint
- use archive paths for historical materials
- avoid parallel "current" structures
- preserve evidence of previous versions without letting them remain active
- archive by copying a snapshot before upgrading current docs; do not clear `docs/` by default
- keep the root Markdown surface limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- keep generated current docs categorized under `docs/`
- when SDD-RIPER is active, keep CodeMap/context bundles under `docs/governance/context/`
- when SDD-RIPER is active, encode No Spec/No Code, Spec Review, Plan Approved, Review, and Reverse Sync gates
- keep references accurate after file moves
- make the output language explicit or inferable from repository context
- support Chinese or English for generated Markdown content
- support Chinese or English for skill interaction text and mode labels
- avoid mixed-language current doc sets unless the user explicitly asks for bilingual output
- prefer explicit confirmation over silent inference when restructuring a non-empty codebase
- in collaboration mode, make role-specific edit authority explicit rather than implied

## Cross-Tool Portability

This skill is intentionally Markdown-first so it can be reused outside Codex.

Portability rules:
- store the core workflow in `SKILL.md` and reference files
- avoid assuming Codex-only APIs in the main logic
- treat `agents/openai.yaml` as a Codex convenience layer, not the core of the skill
- when exposing this workflow in Claude Code, point `CLAUDE.md` and any `.claude/commands/*.md` wrappers back to `SKILL.md` instead of forking the instructions
- only add automation scripts later if repeated file generation becomes too mechanical
