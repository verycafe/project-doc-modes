# Verification Checklist

Run this checklist after creating or migrating a repository doc structure.

## 1. Structure Check

- verify the expected root folders exist
- verify current-version docs exist
- verify archive folders exist if historical docs were moved
- verify runtime code directories still exist if they existed before the migration
- if the repository started empty, verify no unrequested code roots were created

Suggested commands:

```bash
find . -maxdepth 2 -type d | sort
find docs -maxdepth 4 -type f | sort
find archive -maxdepth 4 -type f | sort
```

## 2. Entrypoint Check

- root `README.md` points to the active docs
- root `AGENTS.md` points to the active rules
- `docs/README.md` points to the active version
- `docs/product/CURRENT.md` points to the correct version path
- archive docs are labeled historical
- current entrypoint docs use the chosen document language consistently
- current user-facing mode labels follow the chosen display language
- when the repo already had code, the generated docs reflect the confirmed role and current phase-doc context
- when collaboration mode is active, the current role and role-specific editable/forbidden paths are explicit

## 3. Stale Reference Check

Search current-entry docs for:
- old absolute paths
- old version folders
- old mode-specific current directories
- stale role names if the repo has migrated to unified mode

Suggested command pattern:

```bash
rg -n "old-path|old-version|legacy-mode-name" AGENTS.md README.md STATUS.md WORKFLOW.md RELEASES.md docs -g '!archive/**'
```

The result should be empty or intentionally limited to historical mentions.

## 4. Final Rule

Do not declare success until:
- the active mode is clear
- current entrypoints are internally consistent
- archive content is historical only
- no accidental duplicate current source-of-truth remains
- any original empty code directories were preserved when present
- an originally empty repository remains free of invented code roots unless the user requested placeholders
- the language of newly created current docs is explicit or can be clearly inferred from the repository context
- current Markdown docs are consistently Chinese or consistently English unless bilingual output was explicitly requested
- for non-empty code repositories, the mode, role, phase-doc context, and document language were explicitly gathered or confirmed before restructuring
- for empty or documentation-first repositories, the mode, role or ownership plan, initial version or phase, starter-code-directory choice, and document language were explicitly gathered or confirmed before restructuring
- for collaboration mode, the current operating role and the edit matrix for each role were explicitly gathered, confirmed, or deliberately marked as pending
