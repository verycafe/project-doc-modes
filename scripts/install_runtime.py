#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "project-doc-modes"
COMMON_PATHS = [
    Path("SKILL.md"),
    Path("references"),
]
CODEX_ONLY_PATHS = [
    Path("agents/openai.yaml"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install project-doc-modes for Codex or Claude Code without copying the "
            "other runtime's wrapper files."
        )
    )
    parser.add_argument(
        "target",
        help=(
            "Destination root. For Codex, this must be the skill directory "
            "(for example ~/.codex/skills/project-doc-modes). For Claude Code, "
            "this must be the user-level skill directory "
            "(for example ~/.claude/skills/project-doc-modes)."
        ),
    )
    parser.add_argument(
        "--runtime",
        choices=("auto", "codex", "claude"),
        default="auto",
        help="Install target runtime. Defaults to auto-detection.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files at the destination.",
    )
    return parser.parse_args()


def detect_runtime(target: Path) -> str:
    target_str = str(target)

    if is_standard_skill_target(target, "codex"):
        return "codex"

    if is_standard_skill_target(target, "claude"):
        return "claude"

    if looks_like_repository_root(target):
        raise ValueError(
            "Refusing to install Claude runtime files into a repository root. "
            "Use a Claude user-level skill target such as "
            "~/.claude/skills/project-doc-modes."
        )

    if target.name == "project-doc-modes" and target.parent.name == "skills":
        raise ValueError(
            "Could not tell whether this skills directory is for Codex or Claude. "
            "Pass --runtime codex or --runtime claude."
        )

    raise ValueError(
        "Could not auto-detect runtime for target "
        f"{target_str}. Pass --runtime codex or --runtime claude."
    )


def marker_for_runtime(runtime: str) -> str:
    if runtime == "codex":
        return ".codex"
    if runtime == "claude":
        return ".claude"
    raise ValueError(f"Unsupported runtime: {runtime}")


def expected_target_hint(runtime: str) -> str:
    if runtime == "codex":
        return "~/.codex/skills/project-doc-modes"
    if runtime == "claude":
        return "~/.claude/skills/project-doc-modes"
    raise ValueError(f"Unsupported runtime: {runtime}")


def expected_skill_target(runtime: str) -> Path:
    return (Path.home() / marker_for_runtime(runtime) / "skills" / SKILL_NAME).resolve()


def is_standard_skill_target(target: Path, runtime: str) -> bool:
    return target == expected_skill_target(runtime)


def looks_like_repository_root(target: Path) -> bool:
    return (
        (target / ".git").exists()
        or (target / ".claude").exists()
        or (target / "CLAUDE.md").exists()
    )


def repository_root_for(target: Path) -> Path | None:
    home = Path.home().resolve()
    for candidate in (target, *target.parents):
        if candidate == home:
            if (candidate / ".git").exists() or (candidate / "CLAUDE.md").exists():
                return candidate
            return None
        if looks_like_repository_root(candidate):
            return candidate
    return None


def validate_install_target(runtime: str, target_root: Path) -> None:
    if is_standard_skill_target(target_root, runtime):
        return

    repository_root = repository_root_for(target_root)
    if repository_root:
        raise ValueError(
            "Refusing to install runtime files inside a repository tree "
            f"({repository_root}). "
            "Use a user-level runtime skill target such as "
            f"{expected_target_hint(runtime)}."
        )

    if looks_like_repository_root(target_root):
        raise ValueError(
            "Refusing to install runtime files into a repository-like target. "
            "Use a runtime skill target such as "
            f"{expected_target_hint(runtime)}."
        )

    raise ValueError(
        f"Refusing to install {runtime} runtime files outside a standard "
        f"{runtime} user-level skill target. Use {expected_target_hint(runtime)}."
    )


def selected_paths(runtime: str) -> list[Path]:
    if runtime == "codex":
        return COMMON_PATHS + CODEX_ONLY_PATHS
    if runtime == "claude":
        return COMMON_PATHS
    raise ValueError(f"Unsupported runtime: {runtime}")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def copy_entry(source: Path, target: Path, force: bool) -> None:
    if target.exists():
        if not force:
            raise FileExistsError(f"Refusing to overwrite existing path: {target}")
        remove_path(target)

    ensure_parent(target)

    if source.is_dir():
        shutil.copytree(source, target)
    else:
        shutil.copy2(source, target)


def destination_paths(runtime: str, target_root: Path) -> list[Path]:
    destinations = [target_root / relative_path for relative_path in selected_paths(runtime)]
    if runtime == "claude":
        destinations.extend(claude_command_paths(target_root))
    return destinations


def preflight_parent_paths(paths: list[Path]) -> None:
    for path in paths:
        for parent in reversed(path.parents):
            if parent.exists() and not parent.is_dir():
                raise FileExistsError(f"Refusing to create path through non-directory: {parent}")


def preflight_overwrites(runtime: str, target_root: Path, force: bool) -> None:
    destinations = destination_paths(runtime, target_root)
    preflight_parent_paths(destinations)

    if force:
        return

    for destination in destinations:
        if destination.exists():
            raise FileExistsError(f"Refusing to overwrite existing path: {destination}")


def install(runtime: str, target_root: Path, force: bool) -> list[Path]:
    validate_install_target(runtime, target_root)
    preflight_overwrites(runtime, target_root, force=force)

    installed: list[Path] = []
    for relative_path in selected_paths(runtime):
        source = ROOT / relative_path
        destination = target_root / relative_path
        copy_entry(source, destination, force=force)
        installed.append(destination)

    if runtime == "claude":
        installed.extend(install_claude_commands(target_root, force=force))

    return installed


def claude_home_for_skill_target(target_root: Path) -> Path:
    parts = target_root.parts
    claude_index = parts.index(".claude")
    return Path(*parts[: claude_index + 1])


def claude_command_paths(skill_root: Path) -> list[Path]:
    commands_root = claude_home_for_skill_target(skill_root) / "commands"
    return [commands_root / "project-doc-modes.md", commands_root / "sdd.md"]


def command_text(command: str, skill_root: Path) -> str:
    if command == "project-doc-modes":
        return f"""---
description: Inspect the repository, ask short setup questions, then scaffold or migrate docs with project-doc-modes.
argument-hint: [goal, mode, or language]
---

Use the installed `project-doc-modes` workflow for this task.

For SDD-RIPER-only work, `/sdd` is the shorter command, but this command may also handle SDD-RIPER when the user asks for it.

Primary source of truth:
- @{skill_root / "SKILL.md"}

Read the minimum extra context you need:
- @{skill_root / "references" / "collaboration-mode.md"} when the repo is using `collaboration mode`
- @{skill_root / "references" / "iterative-mode.md"} when the repo is using `iterative mode`
- @{skill_root / "references" / "sdd-riper.md"} when the user asks for team vibe coding, SDD, or SDD-RIPER
- @{skill_root / "references" / "verification.md"} before finishing

Expected behavior:
1. Inspect the target repository before changing docs.
2. Ask 1 to 3 short setup questions at a time instead of dumping a long checklist.
3. Confirm the mode, language, and current role or phase context before restructuring.
4. If `collaboration mode` is chosen, confirm the current role, editable paths, read-only or forbidden paths, and handoff rules before writing docs.
5. Keep root Markdown limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`; put generated docs under categorized `docs/` folders.
6. Make generated `AGENTS.md` the canonical cross-agent governance entrypoint.
7. Make generated `CLAUDE.md` a Claude Code bridge that tells Claude to read `AGENTS.md` first.
8. Do not write `project-doc-modes`, `/project-doc-modes`, `/sdd`, `$project-doc-modes`, `SKILL.md`, or local install paths into generated target docs.
9. Keep generated docs local-only in Git unless the user explicitly asks to track, stage, or commit them.
10. For iterative docs, follow `PRD -> PHASE -> SPEC`: requirements first, phase plans next, SPEC docs under each phase.
11. When team vibe coding or SDD-RIPER is requested, read the SDD-RIPER reference and record stage, approval gates, review path, and Reverse Sync path.
12. For upgrades, copy a snapshot into `docs/archive/` before updating current docs; do not empty `docs/` unless the user requests a full reset.
13. Scaffold or migrate the repository docs with minimal changes.
14. Run the verification checklist before claiming completion.

If the user supplied extra arguments, treat them as additional intent:

$ARGUMENTS
"""

    if command == "sdd":
        return f"""---
description: Start or apply SDD-RIPER governance with project-doc-modes.
argument-hint: [goal, version, phase, or language]
---

Use the installed `project-doc-modes` workflow in SDD-RIPER mode.

Primary source of truth:
- @{skill_root / "SKILL.md"}
- @{skill_root / "references" / "sdd-riper.md"}

Read the minimum extra context you need:
- @{skill_root / "references" / "iterative-mode.md"} when the repo should use versioned product docs
- @{skill_root / "references" / "collaboration-mode.md"} when the repo should use role boundaries
- @{skill_root / "references" / "verification.md"} before finishing

Expected behavior:
1. Inspect the target repository before changing docs.
2. Ask 1 to 3 short setup questions at a time.
3. Keep generated docs local-only in Git unless the user explicitly asks to track, stage, or commit them.
4. Organize work as `PRD -> PHASE -> SPEC`.
5. Make generated `AGENTS.md` the canonical cross-agent governance entrypoint.
6. Make generated `CLAUDE.md` a Claude Code bridge that tells Claude to read `AGENTS.md` first.
7. Do not write `project-doc-modes`, `/project-doc-modes`, `/sdd`, `$project-doc-modes`, `SKILL.md`, or local install paths into generated target docs.
8. Put CodeMap and context bundles under `docs/governance/context/`.
9. Record the current RIPER stage, human approval gates, spec-vs-code review path, and Reverse Sync path.
10. For upgrades, copy a snapshot into `docs/archive/` before updating current docs; do not empty `docs/` unless the user requests a full reset.
11. Run the verification checklist before claiming completion.

If the user supplied extra arguments, treat them as additional intent:

$ARGUMENTS
"""

    raise ValueError(f"Unsupported Claude command: {command}")


def install_claude_commands(skill_root: Path, force: bool) -> list[Path]:
    claude_home = claude_home_for_skill_target(skill_root)
    commands_root = claude_home / "commands"
    commands_root.mkdir(parents=True, exist_ok=True)

    installed: list[Path] = []
    for command, destination in zip(("project-doc-modes", "sdd"), claude_command_paths(skill_root)):
        if destination.exists():
            if not force:
                raise FileExistsError(f"Refusing to overwrite existing path: {destination}")
            remove_path(destination)
        ensure_parent(destination)
        destination.write_text(command_text(command, skill_root), encoding="utf-8")
        installed.append(destination)

    return installed


def main() -> int:
    args = parse_args()
    try:
        target_root = Path(args.target).expanduser().resolve()

        runtime = args.runtime
        if runtime == "auto":
            runtime = detect_runtime(target_root)

        installed = install(runtime=runtime, target_root=target_root, force=args.force)
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"runtime={runtime}")
    print(f"target={target_root}")
    for path in installed:
        print(path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
