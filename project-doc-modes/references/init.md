# Init Workflow

Use this reference for first activation, migration, or full documentation upgrades.

## When To Use

Use `init` when:

- the repository has not yet been activated with this documentation system
- the user asks to scaffold, migrate, reorganize, or fully upgrade docs
- the active mode, language, version, or role boundaries are not recorded

Do not use `init` from hooks. Hooks should use `sync` and then `verify`.

## Inspect First

Before writing files:

1. Inspect the repository root.
2. Inspect `git status --short` when available.
3. Identify code, config, dependency, test, API, and runtime paths that must stay unchanged.
4. Identify existing docs and rule files.
5. Identify the current doc language.
6. Identify tracked vs untracked docs before adding local-only rules.

Code and runtime configuration are read-only evidence unless the user explicitly asks for code changes.

## Archive Before Reading Or Rewriting

If existing docs are present:

1. Copy current docs into `docs/archive/` before reading, interpreting, moving, rewriting, or replacing them.
2. Exclude existing `docs/archive/` content from the backup.
3. After backup, read current and archived docs.
4. Compare docs with real code/config behavior.
5. Record mismatches rather than silently normalizing them away.

Do not delete old docs as part of migration.

## Setup Questions

Ask only after inspection and before broad restructuring.

Ask 1 to 3 short questions at a time:

- collaboration mode or iterative mode
- language: Chinese or English
- current version, phase, sprint, role, or ownership boundary
- whether SDD-RIPER gates should be active

If the user has already given enough context, proceed with the most conservative documented assumption.

## Expected Outputs

Iterative mode normally creates or updates:

```text
AGENTS.md
CLAUDE.md
README.md
docs/README.md
docs/governance/STATUS.md
docs/governance/WORKFLOW.md
docs/governance/RELEASES.md
docs/governance/context/CODEMAP.md
docs/governance/context/CONTEXT_BUNDLE.md
docs/governance/context/GLOSSARY.md
docs/governance/research/README.md
docs/governance/experience/README.md
docs/product/CURRENT.md
docs/product/vX.Y/
```

Collaboration mode normally creates or updates:

```text
AGENTS.md
CLAUDE.md
README.md
docs/README.md
docs/governance/
docs/governance/context/
docs/governance/research/README.md
docs/governance/experience/README.md
docs/collaboration/ROLE_MATRIX.md
docs/collaboration/<role>/
```

## Final Check

Before claiming completion, run structure and leakage checks from `verify.md`, then report:

- archive path created
- active mode and current version/role
- generated paths
- protected code/config paths unchanged
- verification commands and actual output
