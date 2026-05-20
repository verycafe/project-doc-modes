# SDD-RIPER

Use this reference for spec-driven development, team vibe coding, and AI coding governance.

## Operating Laws

- No Spec, No Code: code edits need an active requirement, phase plan, and executable spec.
- Spec is Truth: active specs define intended behavior; implementation drift needs review.
- Reverse Sync: bugs and discoveries update specs first or in the same change as code.
- Validation Loop Required: every executable SPEC needs a concrete way to prove the change works.

If repository rules say implementation outranks docs, surface that conflict before changing governance.

## Stages

```text
Pre-Research -> Research -> Innovate -> Plan -> Execute -> Review -> Archive
```

- Pre-Research: CodeMap and context bundle after repository inspection.
- Research: evidence-backed findings.
- Innovate: 2-3 options with tradeoffs when multiple viable paths exist.
- Plan: atomic checklist with file paths and acceptance criteria.
- Execute: implement the approved plan; stop if the plan is wrong or incomplete.
- Review: compare spec and implementation.
- Archive: snapshot, Reverse Sync, reusable lessons; current docs stay available.

## Mode-Aware Paths

Iterative:

```text
docs/product/vX.Y/requirements/
docs/product/vX.Y/phases/PHASE-*/PLAN.md
docs/product/vX.Y/phases/PHASE-*/specs/
docs/product/vX.Y/phases/PHASE-*/REVIEW.md
docs/product/vX.Y/phases/PHASE-*/IMPLEMENTATION_RECORD.md
```

Collaboration:

```text
docs/collaboration/sdd/requirements/
docs/collaboration/sdd/phases/PHASE-*/PLAN.md
docs/collaboration/sdd/phases/PHASE-*/specs/
docs/collaboration/sdd/phases/PHASE-*/REVIEW.md
docs/collaboration/sdd/phases/PHASE-*/IMPLEMENTATION_RECORD.md
```

## SPEC Validation Loop

Every SPEC that leads to implementation should include:

````markdown
## Validation Loop

```bash
<command proving the change>
```
````

The loop can be:

- test command
- lint/typecheck
- smoke script
- hook inspect
- simulated hook payload
- structure search
- browser or CLI repro

Record actual command output in `IMPLEMENTATION_RECORD.md`.

## Human Gates

- HIL-1 Spec Review: approve requirements, phase plan, and specs before execution.
- HIL-2 Code Review: approve critical code or pull request changes.
- HIL-3 Release Approval: approve production deployment or irreversible operations.
- HIL-4 Reverse Sync Review: confirm implementation records and knowledge updates before archive completion.

When the user explicitly asks to develop from SDD in the same instruction, treat that instruction as authorization to create the spec and execute the scoped plan, unless the action is irreversible or high-blast-radius.

## Research And Experience Capture

Use:

```text
docs/governance/research/
docs/governance/experience/
```

Put high-value findings there before they become PRD-level commitments. Reverse Sync into PRD, PHASE, SPEC, or ADR only when they become requirements, constraints, acceptance criteria, or durable decisions.
