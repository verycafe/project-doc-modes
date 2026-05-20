# Document Structure

Use this reference for default target-project document layout.

## Default Root

Target repositories normally keep only these root Markdown files:

```text
AGENTS.md
CLAUDE.md
README.md
```

All other generated Markdown belongs under `docs/`.

## Governance Docs

Default governance paths:

```text
docs/README.md
docs/governance/STATUS.md
docs/governance/WORKFLOW.md
docs/governance/RELEASES.md
docs/governance/context/CODEMAP.md
docs/governance/context/CONTEXT_BUNDLE.md
docs/governance/context/GLOSSARY.md
docs/governance/research/
docs/governance/experience/
docs/archive/
```

Meanings:

- `context/GLOSSARY.md`: project vocabulary. It defines domain and workflow terms. It is not a spec and should avoid implementation detail.
- `research/`: evidence-backed research notes, external repository analysis, official documentation findings, support matrices, and option comparisons.
- `experience/`: reusable lessons, user preferences, operational learnings, rejected over-design, and other valuable knowledge not yet ready for PRD.

Do not force research or experience notes into PRD. Reverse Sync them into PRD, PHASE, SPEC, or decisions only after they become requirements, constraints, acceptance criteria, or durable governance decisions.

## Iterative Mode

```text
docs/product/CURRENT.md
docs/product/vX.Y/README.md
docs/product/vX.Y/requirements/
docs/product/vX.Y/phases/PHASE-*/PLAN.md
docs/product/vX.Y/phases/PHASE-*/specs/
docs/product/vX.Y/phases/PHASE-*/REVIEW.md
docs/product/vX.Y/phases/PHASE-*/IMPLEMENTATION_RECORD.md
docs/product/vX.Y/decisions/
```

Authoring order:

```text
PRD -> PHASE -> SPEC
```

Do not put PRDs, phase plans, and SPEC docs in the same folder.

## Collaboration Mode

```text
docs/collaboration/ROLE_MATRIX.md
docs/collaboration/<role>/
docs/collaboration/sdd/requirements/
docs/collaboration/sdd/phases/PHASE-*/PLAN.md
docs/collaboration/sdd/phases/PHASE-*/specs/
docs/collaboration/sdd/phases/PHASE-*/REVIEW.md
docs/collaboration/sdd/phases/PHASE-*/IMPLEMENTATION_RECORD.md
```

Collaboration mode must define editable, read-only, and forbidden paths per role before claiming the structure is ready.

## Local-Only Defaults

Generated target-project docs are local-only in Git by default.

Use `.git/info/exclude`, not `.gitignore`, for newly generated untracked docs:

```text
# project-doc-modes local docs
docs/
AGENTS.md
CLAUDE.md
README.md
```

Only include patterns for generated paths that should remain local in that target repository. Do not add exclude rules for files that Git already tracks.
