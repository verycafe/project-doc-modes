# Incremental Sync

Use this reference for hook-driven or session-end documentation updates after initial activation.

## When To Use

Use `sync` when active docs already exist and the input is one of:

- latest session summary
- hook payload
- changed file list
- `git status --short`
- relevant diff summary
- verification output
- user decisions, rejected options, implementation discoveries, or unresolved risks

`sync` is not a lightweight spelling of `init`.

## Required First Read

Read the minimum active context:

```text
AGENTS.md
CLAUDE.md
README.md
docs/README.md
docs/product/CURRENT.md
docs/collaboration/ROLE_MATRIX.md
```

Only read paths that exist and apply to the active mode.

For SDD-RIPER projects, also read the active phase:

```text
PLAN.md
specs/
REVIEW.md
IMPLEMENTATION_RECORD.md
```

## Allowed Updates

Update only docs affected by the latest evidence:

- `docs/governance/STATUS.md`
- `docs/governance/context/CODEMAP.md`
- `docs/governance/context/CONTEXT_BUNDLE.md`
- `docs/governance/context/GLOSSARY.md`
- `docs/governance/research/`
- `docs/governance/experience/`
- active `IMPLEMENTATION_RECORD.md`
- active `REVIEW.md`
- decision records
- release notes
- role status and handoff docs
- entrypoint indexes affected by the session

Update PRD, PHASE, or SPEC only when the session explicitly changes requirements, intended behavior, architecture, acceptance criteria, or delivery scope.

## Forbidden During Sync

Do not:

- ask setup questions during a hook
- choose or change repository mode
- run a broad pre-migration archive
- rebuild or relocate the docs tree
- move historical docs
- rewrite unrelated PRD, PHASE, SPEC, README, or governance sections
- edit code, tests, dependencies, runtime config, APIs, schemas, or product logic
- stage, commit, or push unless the user explicitly asked for Git actions

## Missing Input Rule

If the hook payload lacks enough evidence, do not stop for a question. Record a concise pending item in the safest existing status or implementation record, or report the missing input when no safe doc target exists.

## Verification

After sync, run the relevant read-only checks from `verify.md`:

- changed docs stay in the active mode layout
- entrypoint links still point to active docs
- local-only rules cover newly generated untracked docs
- no local path leakage exists in active docs
- verification commands and actual output are recorded
