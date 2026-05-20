---
name: project-doc-modes
description: Use this skill when a user wants Codex or another coding agent to initialize, migrate, verify, or incrementally sync a repository's documentation governance. It supports role-split collaboration mode, versioned iterative mode, hook-safe Reverse Sync, and team vibe coding / SDD-RIPER workflows.
---

# Project Doc Modes

## Overview

This skill defines a reusable workflow for turning a repository into one of two document-management modes:
- `collaboration mode`: role-split ownership with explicit boundaries, handoff docs, and role-specific work instructions
- `iterative mode`: unified repository workflow with versioned product docs, archive rules, and repository-wide governance files

It can also layer SDD-RIPER rules onto either mode when the repository needs team vibe coding, spec-driven execution, or AI coding governance.

The workflow has three operating modes:
- `init`: first activation, migration, or full upgrade of a repository documentation system
- `sync`: hook-safe incremental Reverse Sync after the initial documentation system already exists
- `verify`: read-only structure, entrypoint, local-only, and leakage checks

Installation and activation are separate:
- the Git repository for this skill contains only the original skill package
- installing the skill copies the skill package into the user's Codex or Claude runtime
- activating the skill inside a target project is when project docs are created or migrated
- target-project outputs such as `AGENTS.md`, `CLAUDE.md`, `README.md`, and `docs/` are generated only inside that target project

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
- `AGENTS.md` is the canonical cross-agent governance entrypoint; generated `CLAUDE.md` must bridge Claude Code to `AGENTS.md`
- never delete, move, rewrite, or refactor user code, configuration, runtime logic, API behavior, dependencies, or tests unless the user explicitly asks for code changes
- if the target repository already has docs, back them up before reorganizing or rewriting them
- do not stage, commit, or push generated docs
- keep newly generated docs local-only by default in Git repositories
- for SDD-RIPER projects, active specs are the source of intended behavior and code execution requires an approved plan
- generated target-repository docs must be tool-agnostic: never mention this skill, its install path, or its invocation commands

For Git repositories, local-only means:
- do not run `git add`, `git commit`, or `git push` unless the user asks
- for newly generated untracked doc paths, append local ignore patterns to `.git/info/exclude` instead of editing `.gitignore`
- include newly generated archive snapshots, such as `docs/archive/...`, in local exclude coverage when they are untracked
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
- `docs/product/vX.Y/phases/`: phase index and roadmap only
- `docs/product/vX.Y/phases/PHASE-*/specs/`: SPEC files and technical contracts produced for that phase
- `docs/collaboration/`: collaboration-mode role matrix, role guides, status, handoffs, and SDD artifacts
- `docs/collaboration/sdd/requirements/`: collaboration-mode requirements when SDD-RIPER is active
- `docs/collaboration/sdd/phases/PHASE-*/specs/`: collaboration-mode phase specs when SDD-RIPER is active
- `docs/product/vX.Y/decisions/`: ADRs and decision records
- `docs/archive/`: historical snapshots and inactive docs

Default authoring flow:
1. write or update the requirement/proposal docs first
2. derive phase plans from those requirements
3. split each phase into the SPEC docs needed to execute that phase

Use the active mode to choose paths:
- iterative mode uses `docs/product/vX.Y/...`
- collaboration mode uses `docs/collaboration/...` and must not create `docs/product/vX.Y` unless the user explicitly requests a hybrid/versioned product flow

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

Exception: after an implementation-only session, `sync` and `verify` still apply when a hook or user asks to update status, implementation records, reviews, decisions, indexes, or documentation consistency from the session evidence.

## Command Entrypoints

These entrypoints are for invoking this skill only. They are implementation details, not target-project documentation.

Codex:
- invoke `project-doc-modes` from the Codex skill or command UI for the general workflow
- say `project-doc-modes init` for first activation, migration, or full upgrades
- say `project-doc-modes sync` for hook-safe incremental Reverse Sync from the latest session
- say `project-doc-modes verify` for read-only structure checks
- request SDD-RIPER or spec-driven governance in normal language after the workflow starts

Claude Code:
- use `/project-doc-modes` for init, migration, full upgrades, or argument-routed general workflow
- use `/project-doc-modes-sync` for hook-safe incremental Reverse Sync after an initial structure exists
- use `/project-doc-modes-verify` for read-only structure checks
- use `/sdd` as the short command for SDD-RIPER governance

Claude Code command wrappers are generated by the installer and must point back to this `SKILL.md` and the relevant `references/` files instead of forking the workflow.

Do not write these command names or any installed skill path into generated docs for another repository. In target docs, describe the project workflow directly, such as "use SDD-RIPER governance" or "follow the PRD -> PHASE -> SPEC chain."

## Operating Modes

Choose the operating mode before changing files.

Use `init` when:
- the repository has not yet been activated with this documentation system
- the user asks to scaffold, migrate, reorganize, or fully upgrade docs
- the active mode, language, version, or role boundaries are not yet recorded

Use `sync` when:
- the repository already has active docs and entrypoints
- a hook or user asks to summarize the latest session into docs
- the input is a session summary, changed files, git diff summary, verification output, or implementation discovery

Use `verify` when:
- the user asks whether the structure is valid
- a hook needs a read-only guardrail after sync
- changes should be reported without repairs

`sync` is not a lightweight spelling of `init`. In `sync` mode:
- do not ask setup questions
- do not choose or change the repository mode
- do not create a broad pre-migration archive
- do not rebuild the docs tree
- do not rewrite PRD, PHASE, or SPEC content unless the latest session explicitly changed requirements, intended behavior, architecture, or acceptance criteria
- update only the docs touched by the latest evidence and then run incremental verification

## Workflow

This full workflow applies to `init`, migrations, and full upgrades. For hook-driven work after initial setup, use `sync` mode instead.

### 1. Inspect First

Before writing files:
- inspect the repository root
- identify current code directories that must remain stable
- identify existing doc paths and repo-rule filenames that must be backed up before migration
- do not read, summarize, interpret, or rewrite existing doc contents before the pre-migration backup exists
- identify whether the repo already has historical docs that should be archived rather than deleted
- identify the dominant language of the current active docs, if any
- inspect `git status --short` when the target is a Git repository
- identify which docs are already tracked before deciding local-only exclude rules

Treat existing code, config, and active docs as source material. Do not invent paths. Code and runtime configuration are read-only evidence unless the user explicitly asks for implementation changes.

If existing docs are present before activation:
1. create a pre-migration backup under `docs/archive/` before rewriting, moving, or replacing them
2. exclude existing `docs/archive/` content from the backup to avoid recursive archives
3. only after the backup exists, read the backed-up docs and current docs before creating the new structure
4. inspect the repository code and config enough to check whether the docs match real behavior
5. record mismatches between docs and code instead of silently normalizing them away
6. if needed to avoid losing context during the migration, create `docs/governance/context/MIGRATION_NOTES.tmp.md` as local-only working notes, then either fold durable findings into active docs or leave it clearly labeled as temporary evidence

Do not delete old docs as part of migration. After backup, either move them into the archive with historical labels or leave them in place until the new active docs are internally consistent.

If the repository has no runtime code directories yet:
- treat it as a greenfield or documentation-first setup
- scaffold docs and governance around the requested mode
- do not invent `engine/`, `api/`, `web/`, or equivalent code roots unless the user explicitly asks for placeholders

If code directories exist but are empty:
- preserve those directories as intentional placeholders
- note that implementation has not started yet
- continue scaffolding docs without treating the empty directories as an error

If the target needs team vibe coding, SDD-RIPER, spec-driven execution, AI coding governance, or code-facing workflow gates, read:
- the SDD-RIPER section in `references/rules.md`

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
- ask after inspection and before creating, moving, or rewriting Markdown files
- ask 1 to 3 short questions per turn; do not dump a full checklist
- ask in the chosen display language and offer sensible defaults inline
- confirm strong repository evidence instead of silently deciding
- for code repositories, ask mode and role first, then phase-doc context and language
- for empty or documentation-first repositories, ask mode, initial version or phase, and language first
- for Chinese prompts, prefer `协作模式` and `迭代模式` unless English canonical names are needed
- once mode, role or ownership shape, phase/version context, and language are clear enough, proceed

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
- `references/rules.md`

### 3. Preserve Code, Reorganize Docs

Default rule:
- reorganize files, rules, and Markdown docs
- do not move runtime code directories unless the user explicitly asks
- do not edit user code, tests, dependencies, runtime configuration, API contracts, data schemas, or business logic while activating this documentation workflow

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
- create clear current-entry docs, archive rules, and repository-level governance files
- ensure only one current version is marked as source-of-truth
- snapshot historical material into archive paths instead of deleting context
- when pre-existing docs exist, use their backup plus the real codebase as evidence for the new docs
- keep root Markdown limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`
- make `AGENTS.md` the canonical root governance file for all agents
- make `CLAUDE.md` a bridge file that tells Claude Code to read `AGENTS.md` first and then follow the active docs under `docs/`
- keep all other generated Markdown under categorized `docs/` folders

Use the active mode reference for required outputs and folder layout:
- `references/rules.md`

### 4.5. Root Entrypoint Contract

Generated root entrypoints must be project-native:
- `AGENTS.md`: canonical cross-agent rules, active doc map, edit boundaries, Git policy, archive policy, verification rules
- `CLAUDE.md`: Claude Code bridge; it must read `AGENTS.md` first, with any Claude-specific rules as a short addendum
- `README.md`: human-facing project overview and links to active docs

Default `CLAUDE.md` bridge content should say, in the chosen document language:
- this file is the Claude Code entrypoint
- read `AGENTS.md` first for canonical project rules
- then read the active docs named by `docs/README.md` and mode-specific current entrypoints
- follow any Claude-specific notes listed in this file

Do not generate a `CLAUDE.md` that only describes a tool, plugin, or skill. If `CLAUDE.md` exists and lacks an `AGENTS.md` bridge, add the bridge. If the user requests Claude-specific governance, keep the bridge first and put Claude-specific rules after it.

### 5. Write Current-Version Docs

For the active mode, create the full document set the mode requires.

When writing the docs:
- use the chosen document language consistently across all newly created Markdown files
- preserve existing active-doc language in migrations unless the user explicitly requests a language switch
- if the user requests a language switch during migration, update current entrypoints to the new language and leave historical docs in archive with clear labels
- reflect the confirmed role and current phase-document context in the generated governance and handoff docs
- use the chosen display language for mode labels, section titles, prompts, and navigation text
- write target docs as project-native governance, not as instructions to invoke `project-doc-modes`, `/project-doc-modes`, `/project-doc-modes-sync`, `/project-doc-modes-verify`, `/sdd`, `$project-doc-modes`, or an installed `SKILL.md`
- never include absolute local paths such as `/Users/...`, `~/.codex/skills/...`, or `~/.claude/skills/...` in generated target docs
- ensure generated `CLAUDE.md` explicitly references `AGENTS.md` as the canonical project rules entrypoint
- in collaboration mode, record the current operating role and the editable, read-only, and forbidden paths for each role in the active docs
- if SDD-RIPER is active, record the current RIPER stage, required evidence, HIL gates, and Reverse Sync expectations in the active docs

Use the active mode reference for the exact output set. Do not duplicate mode-specific trees in ad hoc locations.

### 5.5. Upgrade And Archive Current Docs

When upgrading docs, do not empty `docs/` by default.

Default upgrade flow:
1. identify active current docs by mode
2. copy the current docs into `docs/archive/` as a timestamped or versioned snapshot
3. keep the active docs in place
4. update the active docs in place, or create the next current version only when the user requested a version bump
5. perform Reverse Sync updates when implementation discoveries changed requirements, specs, or decisions
6. update entrypoints after the new current docs are ready

When creating a next version, treat the previous version's behavior and functional logic as locked historical baseline unless the user explicitly asks to revise it.

Mode-specific active-doc discovery:
- iterative mode: include `docs/README.md`, `docs/product/CURRENT.md`, the active `docs/product/vX.Y/` tree, `docs/governance/`, and root entrypoints
- collaboration mode: include `docs/README.md`, `docs/collaboration/ROLE_MATRIX.md`, role guide/status/handoff docs, `docs/governance/`, and root entrypoints
- SDD-RIPER in iterative mode: also include `docs/governance/context/`, active `docs/product/vX.Y/requirements/`, and the active `docs/product/vX.Y/phases/PHASE-*/` directory
- SDD-RIPER in collaboration mode: also include `docs/governance/context/`, `docs/collaboration/sdd/requirements/`, and the active `docs/collaboration/sdd/phases/PHASE-*/` directory

Only move all current docs out of `docs/` or clear the current docs directory when the user explicitly asks for a full reset or destructive archive.

### 6. Update Entrypoints

After creating files:
- update root entrypoints to point to the active structure
- remove stale references to previous current-version paths
- keep archive references explicit and clearly labeled as historical
- keep root entrypoints from pointing at root `archive/`, root `STATUS.md`, root `WORKFLOW.md`, or root `RELEASES.md`

### 6.5. Hook-Safe Incremental Sync

Use this section only in `sync` mode.

Inputs may include:
- latest user or agent session summary
- changed files from `git status --short` or `git diff --name-status`
- verification commands and actual output
- implementation discoveries, bug fixes, rejected options, or unresolved risks

First inspect the existing documentation contract:
- root entrypoints: `AGENTS.md`, `CLAUDE.md`, `README.md`
- `docs/README.md`
- current mode pointer such as `docs/product/CURRENT.md` or `docs/collaboration/ROLE_MATRIX.md`
- active phase/spec/review/implementation-record paths when SDD-RIPER is active

Allowed sync updates:
- `docs/governance/STATUS.md`
- `docs/governance/context/CODEMAP.md` or `CONTEXT_BUNDLE.md` only for meaningful new evidence
- active `IMPLEMENTATION_RECORD.md`, `REVIEW.md`, decision records, release notes, or handoff/status docs
- root or docs indexes only when links are stale or new active docs were created by this sync
- PRD, PHASE, or SPEC docs only when the latest session explicitly changed requirements, intended behavior, architecture, or acceptance criteria

Forbidden in `sync` mode unless the user explicitly asks for a full upgrade:
- asking setup questions during a hook
- changing collaboration vs iterative mode
- broad archive snapshots of current docs
- recreating the documentation tree
- moving historical docs
- editing code, tests, dependencies, runtime configuration, APIs, schemas, or product logic

If required inputs are missing during a hook, do not block on a question. Record a concise pending item in the appropriate status or implementation record, or report the missing input when no safe doc target exists.

End every sync with incremental verification:
- confirm entrypoint links still point to active docs
- confirm changed docs remain under the active mode layout
- confirm local-only rules still apply for generated untracked docs
- run leakage checks on changed docs and active entrypoints
- report verification commands and actual output

### 7. Verify

Always run a structure check before claiming completion.

Read:
- `references/rules.md`

At minimum, verify the hard defaults, active mode layout, local-only Git policy, archive-by-copy behavior, SDD-RIPER gates when active, and target-doc anti-leakage. Do not declare success until the verification section in `references/rules.md` passes for the target repository.

## Cross-Tool Portability

This skill is intentionally Markdown-first so it can be reused outside Codex.

Portability rules:
- store the core workflow in `SKILL.md` and reference files
- avoid assuming Codex-only APIs in the main logic
- generate Claude Code command wrappers from the installer instead of keeping hand-written workflow copies
- in repositories generated or migrated by this skill, do not point project docs back to this skill package or to any local install path
- only add automation scripts later if repeated file generation becomes too mechanical
