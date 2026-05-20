# project-doc-modes Hook Binding

Use this file when an AI assistant is asked to bind `project-doc-modes` automation to the current tool.

Binding hooks is separate from installing the Skill. Installation only places runtime files in the tool's Skill folder; hook binding connects the current tool to `project-doc-modes sync` and optional verification after the initial project docs exist.

## One-Line Entry

Ask an AI assistant inside the target project:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md
```

Optional parameters:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with action=bind scope=project
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with action=bind scope=global
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with action=inspect scope=project
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with action=unbind scope=project
```

## Defaults

When parameters are missing, use these defaults:

```text
action=bind
scope=project
tool=current
project_root=current repository or current working directory
workflow=sync-then-verify
```

Rules:
- Default binding is project-local.
- Global binding is allowed only when the user explicitly writes `scope=global`.
- Default tool is the tool where the user pasted this instruction.
- Do not bind another tool unless the user explicitly sets `tool=codex`, `tool=claude`, or another supported tool.
- Do not create or migrate project docs while binding hooks.

## Scope Rules

Project scope:
- Bind only the current project.
- Prefer the current tool's project-level hook configuration when it exists.
- If the tool has no project-level hook mechanism, do not silently fall back to global scope. Report that project-local binding is unsupported for the current tool.

Global scope:
- Proceed only when the request explicitly includes `scope=global`.
- Bind only the current tool unless the user explicitly names another tool.
- Before writing, inspect the exact global hook file or command registry the current tool uses.
- Preserve existing hooks and add only a clearly named `project-doc-modes` entry.

## Action Rules

`action=inspect`:
- Inspect current hook support, current project root, and existing project/global bindings.
- Report whether `project-doc-modes` is already bound.
- Do not modify files.

`action=bind`:
- Verify that the `project-doc-modes` Skill is installed for the current tool.
- Inspect the current tool's real hook mechanism from local docs, config, or existing examples.
- Add or update a managed binding for `project-doc-modes` without overwriting unrelated hooks.
- Use a stable managed name such as `project-doc-modes sync`.
- Record the touched file paths and the effective scope.

`action=unbind`:
- Remove only the managed `project-doc-modes` hook binding.
- Leave unrelated hooks untouched.
- If no managed binding exists, report that no change was needed.

## Hook Behavior

The managed hook should run after a user-agent session, turn, or equivalent tool lifecycle event that has enough context to summarize the latest work.

The hook must invoke the installed workflow as:

```text
project-doc-modes sync
project-doc-modes verify
```

For Claude Code command wrappers, the equivalent behavior is:

```text
/project-doc-modes-sync
/project-doc-modes-verify
```

Expected hook evidence:
- latest session summary when available
- changed files or `git status --short`
- relevant diff summary when needed
- verification commands and actual output when available
- user decisions, implementation discoveries, unresolved risks, and rejected options

If active project docs do not exist yet, the hook must not run a full migration. It should report that `project-doc-modes init` is required before automatic sync can produce durable updates.

## Safety Rules

- Do not invent hook APIs, event names, config files, or command formats.
- Inspect the current tool's real hook support before editing.
- Do not edit global configuration unless `scope=global` is explicit.
- Do not install packages or dependencies for hook binding unless the current tool's documented hook mechanism requires them and the user explicitly agrees.
- Do not modify user code, tests, runtime configuration, dependencies, APIs, schemas, or product logic.
- Do not stage, commit, or push hook changes unless the user explicitly asks.
- Keep generated target-project docs free of this file name, local install paths, and invocation commands.

## Verification

After binding or unbinding:
- show the effective `action`, `scope`, `tool`, and `project_root`
- list every modified hook/config file
- show the managed hook name and lifecycle event if the tool exposes one
- confirm unrelated hooks were preserved
- confirm global config was not touched unless `scope=global`
- for project scope, confirm the binding is located under the current project or in the current tool's project binding registry
