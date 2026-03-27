---
name: project-doc-modes
description: Use this skill when a user wants Codex or another coding agent to scaffold, reorganize, or migrate a repository's documentation and governance structure into either a role-split collaboration mode or a versioned iterative mode. It is for creating and updating folder layout, archive layout, repo rules, version entrypoints, and markdown source-of-truth documents based on the current codebase.
---

# Project Doc Modes

## Overview

This skill defines a reusable workflow for turning a repository into one of two document-management modes:
- `collaboration mode`: role-split ownership with explicit boundaries, handoff docs, and role-specific work instructions
- `iterative mode`: unified repository workflow with versioned product docs, archive rules, and repository-wide governance files

Keep the core portable:
- prefer Markdown rules, file templates, and verification steps
- do not depend on Node.js unless the user explicitly asks for automation scripts
- preserve current code directories unless the user explicitly asks to move code

## When To Use

Use this skill when the user asks for any of the following:
- create a reusable repository documentation standard
- choose between a collaboration workflow and an iterative workflow
- generate versioned docs and archive folders
- create repo governance docs such as `AGENTS.md`, `STATUS.md`, `WORKFLOW.md`, `RELEASES.md`
- reorganize old docs into a historical archive
- migrate a project from a role-split structure into a unified versioned structure
- recreate the same document system for a new project

Do not use this skill when the user only wants:
- a single feature PRD
- a one-off README rewrite
- implementation-only code changes without repository-structure work

## Workflow

### 1. Inspect First

Before writing files:
- inspect the repository root
- identify current code directories that must remain stable
- inspect current docs and repo rules
- identify whether the repo already has historical docs that should be archived rather than deleted
- identify the dominant language of the current active docs, if any

Treat existing code, config, and active docs as source material. Do not invent paths.

If the repository has no runtime code directories yet:
- treat it as a greenfield or documentation-first setup
- scaffold docs and governance around the requested mode
- do not invent `engine/`, `api/`, `web/`, or equivalent code roots unless the user explicitly asks for placeholders

If code directories exist but are empty:
- preserve those directories as intentional placeholders
- note that implementation has not started yet
- continue scaffolding docs without treating the empty directories as an error

### 1.5. Ask Before Acting

Stay in questioning mode before restructuring docs.

For repositories that already contain runtime code, if the user has not already answered them, ask concise questions about:
- which mode to use: `collaboration mode` or `iterative mode`
- the user's current role or ownership boundary in the repository
- whether there is a current phase, sprint, week, or milestone document, and where it lives
- which language the generated Markdown docs should use: Chinese or English

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
- move historical material into archive paths instead of deleting context

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

In iterative mode, this usually includes:
- `docs/README.md`
- `docs/product/CURRENT.md`
- `docs/product/vX.Y/...`
- root `README.md`
- root `AGENTS.md`
- root `STATUS.md`
- root `WORKFLOW.md`
- root `RELEASES.md`
- root `archive/`

In collaboration mode, this usually includes:
- root `AGENTS.md` with ownership boundaries
- role handoff docs
- role-specific guide and status docs
- phase or task instructions

### 6. Update Entrypoints

After creating files:
- update root entrypoints to point to the active structure
- remove stale references to previous current-version paths
- keep archive references explicit and clearly labeled as historical

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
- governance rules should live at the repo root

See:
- `references/iterative-mode.md`

## Output Standards

- keep docs concise and navigable
- create one obvious current-version entrypoint
- use archive paths for historical materials
- avoid parallel "current" structures
- preserve evidence of previous versions without letting them remain active
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
