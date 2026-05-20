# project-doc-modes Hook Binding

Use this file when an AI assistant is asked to bind `project-doc-modes` automation to the current tool.

Hook binding is separate from Skill installation and from project documentation initialization. Installation places the Skill in the tool runtime. Hook binding connects the current project to the incremental `sync` then `verify` workflow after active project docs already exist.

## One-Line Entry

Ask an AI assistant inside the target project:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md
```

That default command must install the current tool's project-local binding when a supported binding exists. Do not make the user repeat support-discovery questions.

## Codex Quick Start

From inside the target project, paste:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md
```

That is the install action. It creates or updates:

```text
.codex/hooks.json
.codex/hooks/project_doc_modes_stop.py
```

After these files exist and the installer reports `bound=True`, hook binding is installed.

Codex may still surface its own hook review UI before a non-managed command hook runs. That is Codex runtime security, not a second installation command. If Codex asks for review, use `/hooks` and trust the managed hook named:

```text
project-doc-modes sync + verify
```

Optional parameters:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with action=bind scope=project
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with action=inspect scope=project
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with action=unbind scope=project
Fetch and follow instructions from https://raw.githubusercontent.com/verycafe/project-doc-modes/main/hooks.md with action=bind scope=global
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
- Default tool is the tool where the user pasted the instruction.
- Do not bind another tool unless the user explicitly sets `tool=codex`, `tool=claude`, or another supported tool.
- Global binding is allowed only when the user explicitly writes `scope=global`.
- Do not create, migrate, or initialize project docs while binding hooks.

## Supported Binding Matrix

Known support must be used directly. Do not re-investigate these rows during normal `action=bind`.

| Tool | Scope | Status | Binding |
| --- | --- | --- | --- |
| Codex | project | supported | `<repo>/.codex/hooks.json` plus `<repo>/.codex/hooks/project_doc_modes_stop.py` |
| Codex | global | not default | requires explicit `scope=global`; do not modify global config from the default command |
| Claude Code | project/global | not managed here | use installed `/project-doc-modes-sync` and `/project-doc-modes-verify` wrappers manually until a Claude hook binder is added |

Codex project binding details:
- Codex loads project hooks from `<repo>/.codex/hooks.json`.
- Project hooks merge with `~/.codex/hooks.json`; they do not replace global hooks.
- The project `.codex` layer must be trusted by Codex before the command hook runs.
- Non-managed command hooks require Codex review/trust before they run; Codex exposes that through `/hooks` when review is needed.
- The installed hook uses the `Stop` event and a command handler. It returns a continuation prompt that asks Codex to run `project-doc-modes sync` semantics and then `verify` semantics.
- The hook guards `stop_hook_active` to avoid an infinite continuation loop.
- If active docs do not exist yet, the hook reports that `project-doc-modes init` is required and does not run a migration automatically.

## Codex Project Binding

For `action=bind scope=project tool=codex`, run this from the target project root:

```bash
tmp_file="$(mktemp -t project-doc-modes-hook.XXXXXX.py)"
curl -fsSL https://raw.githubusercontent.com/verycafe/project-doc-modes/main/scripts/bind_codex_project_hook.py -o "$tmp_file"
/usr/bin/python3 "$tmp_file" --action bind --project "$(pwd)"
rm -f "$tmp_file"
```

If the current checkout already contains `scripts/bind_codex_project_hook.py`, the assistant may use the local file instead:

```bash
/usr/bin/python3 scripts/bind_codex_project_hook.py --action bind --project "$(pwd)"
```

Expected modified files:

```text
.codex/hooks.json
.codex/hooks/project_doc_modes_stop.py
```

The managed `Stop` hook command is:

```text
/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/project_doc_modes_stop.py"
```

The managed hook name/status is:

```text
project-doc-modes sync + verify
```

## Codex Inspect And Unbind

For `action=inspect scope=project tool=codex`:

```bash
tmp_file="$(mktemp -t project-doc-modes-hook.XXXXXX.py)"
curl -fsSL https://raw.githubusercontent.com/verycafe/project-doc-modes/main/scripts/bind_codex_project_hook.py -o "$tmp_file"
/usr/bin/python3 "$tmp_file" --action inspect --project "$(pwd)"
rm -f "$tmp_file"
```

For `action=unbind scope=project tool=codex`:

```bash
tmp_file="$(mktemp -t project-doc-modes-hook.XXXXXX.py)"
curl -fsSL https://raw.githubusercontent.com/verycafe/project-doc-modes/main/scripts/bind_codex_project_hook.py -o "$tmp_file"
/usr/bin/python3 "$tmp_file" --action unbind --project "$(pwd)"
rm -f "$tmp_file"
```

Unbind removes only the managed `project-doc-modes sync + verify` hook and its managed script. It leaves unrelated hooks untouched.

## Hook Behavior

The managed Codex hook runs on `Stop`, after an assistant turn has enough context to summarize recent work.

The continuation prompt instructs Codex to:
- use `project-doc-modes sync` semantics first
- use `project-doc-modes verify` semantics after sync
- read available evidence from the hook payload, transcript path when readable, `git status --short`, changed files, relevant diff summary, verification output mentioned in the session, user decisions, implementation discoveries, unresolved risks, and rejected options
- update only active docs affected by this session
- avoid setup questions, full migration, broad archives, code edits, staging, commits, and pushes

The hook does not execute `/project-doc-modes-sync` as a shell command. That slash command is a chat/Skill entrypoint, not a terminal executable. The project hook uses Codex `Stop` continuation so the AI can run the installed Skill workflow with the latest conversation context.

## Scope Rules

Project scope:
- Bind only the current project.
- For Codex, use the supported project binding above directly.
- If the current tool is not in the supported binding matrix, do not silently fall back to global scope. Report that project-local binding is unsupported for the current tool.

Global scope:
- Proceed only when the request explicitly includes `scope=global`.
- Bind only the current tool unless the user explicitly names another tool.
- Before writing, inspect the exact global hook file or command registry the current tool uses.
- Preserve existing hooks and add only a clearly named `project-doc-modes` entry.

## Safety Rules

- Do not invent hook APIs, event names, config files, or command formats.
- For known supported Codex project binding, use this file's installer directly instead of rediscovering support.
- Do not edit global configuration unless `scope=global` is explicit.
- Do not install packages or dependencies for hook binding.
- Do not modify user code, tests, runtime configuration, dependencies, APIs, schemas, or product logic.
- Do not mutate Codex `hooks.state` trust records directly. Trust must happen through Codex's `/hooks` review flow.
- Do not stage, commit, or push hook changes unless the user explicitly asks.
- Keep generated target-project docs free of this file name, local install paths, and invocation commands.

## Verification

After binding or unbinding:
- show the effective `action`, `scope`, `tool`, and `project_root`
- list every modified hook/config file
- show the managed hook name and lifecycle event
- confirm unrelated hooks were preserved
- confirm global config was not touched unless `scope=global`
- for project scope, confirm the binding is under the current project
- mention that Codex may require `/hooks` review before the non-managed command hook runs
