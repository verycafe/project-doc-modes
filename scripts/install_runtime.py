#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "project-doc-modes"
COMMON_PATHS = [
    Path("SKILL.md"),
    Path("references/rules.md"),
]
CODEX_ONLY_PATHS = [
    Path("agents/openai.yaml"),
]
LEGACY_SKILL_PATHS = [
    Path("references/collaboration-mode.md"),
    Path("references/iterative-mode.md"),
    Path("references/sdd-riper.md"),
    Path("references/verification.md"),
]
MANAGED_PAYLOAD_DIRS = [
    Path("references"),
    Path("agents"),
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
        nargs="?",
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
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run isolated installer smoke tests and exit.",
    )
    args = parser.parse_args()
    if args.self_test and args.target:
        parser.error("--self-test does not accept a target")
    if not args.self_test and not args.target:
        parser.error("target is required unless --self-test is used")
    return args


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
    if force:
        cleanup_stale_runtime_files(target_root)

    installed: list[Path] = []
    for relative_path in selected_paths(runtime):
        source = ROOT / relative_path
        destination = target_root / relative_path
        copy_entry(source, destination, force=force)
        installed.append(destination)

    if runtime == "claude":
        installed.extend(install_claude_commands(target_root, force=force))

    return installed


def cleanup_stale_runtime_files(target_root: Path) -> None:
    stale_paths = [*MANAGED_PAYLOAD_DIRS, *LEGACY_SKILL_PATHS]

    for relative_path in stale_paths:
        path = target_root / relative_path
        if path.exists():
            remove_path(path)


def claude_home_for_skill_target(target_root: Path) -> Path:
    parts = target_root.parts
    claude_index = parts.index(".claude")
    return Path(*parts[: claude_index + 1])


def claude_command_paths(skill_root: Path) -> list[Path]:
    commands_root = claude_home_for_skill_target(skill_root) / "commands"
    return [commands_root / "project-doc-modes.md", commands_root / "sdd.md"]


def command_reference(path: Path) -> str:
    try:
        relative = path.resolve().relative_to(Path.home().resolve())
    except ValueError:
        return str(path)
    return f"~/{relative.as_posix()}"


def command_text(command: str, skill_root: Path) -> str:
    skill_md = command_reference(skill_root / "SKILL.md")
    rules_ref = command_reference(skill_root / "references" / "rules.md")

    if command == "project-doc-modes":
        return f"""---
description: Inspect the repository, ask short setup questions, then scaffold or migrate docs with project-doc-modes.
argument-hint: [goal, mode, or language]
---

Use the installed `project-doc-modes` workflow for this task.

For SDD-RIPER-only work, `/sdd` is the shorter command, but this command may also handle SDD-RIPER when the user asks for it.

Primary source of truth:
- @{skill_md}
- @{rules_ref}

Read the minimum extra context you need:
- @{rules_ref} for mode-specific paths, SDD-RIPER rules, and verification before finishing

Expected behavior:
1. Inspect the target repository before changing docs.
2. Ask 1 to 3 short setup questions at a time instead of dumping a long checklist.
3. Confirm the mode, language, and current role or phase context before restructuring.
4. If `collaboration mode` is chosen, confirm the current role, editable paths, read-only or forbidden paths, and handoff rules before writing docs.
5. Keep root Markdown limited to `AGENTS.md`, `CLAUDE.md`, and `README.md`; put generated docs under categorized `docs/` folders.
6. Make generated `AGENTS.md` the canonical cross-agent governance entrypoint.
7. Make generated `CLAUDE.md` a Claude Code bridge that tells Claude to read `AGENTS.md` first.
8. Do not delete, rewrite, refactor, move, or simplify user code, tests, config, dependencies, APIs, schemas, or runtime logic unless the user explicitly asks for code changes.
9. If existing docs are present, back them up into `docs/archive/` before reading, interpreting, moving, rewriting, or replacing doc contents.
10. After the backup exists, read the docs and check them against the real codebase before landing the new structure.
11. Use `docs/governance/context/MIGRATION_NOTES.tmp.md` as local-only working notes when needed to avoid losing migration context.
12. Do not write `project-doc-modes`, `/project-doc-modes`, `/sdd`, `$project-doc-modes`, `SKILL.md`, or local install paths into generated target docs.
13. Keep generated docs local-only in Git unless the user explicitly asks to track, stage, or commit them.
14. For iterative docs, follow `PRD -> PHASE -> SPEC`: requirements first, phase plans next, SPEC docs under each phase.
15. When team vibe coding or SDD-RIPER is requested, read the SDD-RIPER reference and record stage, approval gates, review path, and Reverse Sync path.
16. For upgrades, copy a snapshot into `docs/archive/` before updating current docs; do not empty `docs/` unless the user requests a full reset.
17. Scaffold or migrate the repository docs with minimal changes.
18. Run the verification checklist before claiming completion.

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
- @{skill_md}
- @{rules_ref}

Read the minimum extra context you need:
- @{rules_ref} for SDD-RIPER paths, mode-specific rules, and verification before finishing

Expected behavior:
1. Inspect the target repository before changing docs.
2. Ask 1 to 3 short setup questions at a time.
3. Keep generated docs local-only in Git unless the user explicitly asks to track, stage, or commit them.
4. Organize work as `PRD -> PHASE -> SPEC`.
5. Make generated `AGENTS.md` the canonical cross-agent governance entrypoint.
6. Make generated `CLAUDE.md` a Claude Code bridge that tells Claude to read `AGENTS.md` first.
7. Do not delete, rewrite, refactor, move, or simplify user code, tests, config, dependencies, APIs, schemas, or runtime logic unless the user explicitly asks for code changes.
8. If existing docs are present, back them up into `docs/archive/` before reading, interpreting, moving, rewriting, or replacing doc contents.
9. After the backup exists, read the docs and check them against the real codebase before landing the new structure.
10. Use `docs/governance/context/MIGRATION_NOTES.tmp.md` as local-only working notes when needed to avoid losing migration context.
11. Do not write `project-doc-modes`, `/project-doc-modes`, `/sdd`, `$project-doc-modes`, `SKILL.md`, or local install paths into generated target docs.
12. Put CodeMap and context bundles under `docs/governance/context/`.
13. Record the current RIPER stage, human approval gates, spec-vs-code review path, and Reverse Sync path.
14. For upgrades, copy a snapshot into `docs/archive/` before updating current docs; do not empty `docs/` unless the user requests a full reset.
15. Run the verification checklist before claiming completion.

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


def relative_files(root: Path) -> list[str]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def relative_dirs(root: Path) -> list[str]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_dir())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_equal(name: str, actual: list[str], expected: list[str]) -> None:
    if actual != expected:
        raise AssertionError(f"{name}: expected {expected}, got {actual}")


def require_raises(name: str, expected: type[Exception], action) -> None:
    try:
        action()
    except expected:
        return
    except Exception as exc:  # noqa: BLE001 - smoke test reports unexpected failures.
        raise AssertionError(f"{name}: expected {expected.__name__}, got {type(exc).__name__}: {exc}") from exc
    raise AssertionError(f"{name}: expected {expected.__name__}")


def run_cli(args: list[str], home: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def run_self_test() -> int:
    original_home = os.environ.get("HOME")
    try:
        with tempfile.TemporaryDirectory(prefix=f"{SKILL_NAME}-install-test-") as temp_dir:
            test_root = Path(temp_dir)

            os.environ["HOME"] = str(test_root / "home-codex")
            codex_target = expected_skill_target("codex")
            require(detect_runtime(codex_target) == "codex", "codex auto-detect failed")
            install("codex", codex_target, force=False)
            require_equal(
                "codex payload",
                relative_files(codex_target),
                ["SKILL.md", "agents/openai.yaml", "references/rules.md"],
            )
            (codex_target / "references" / "iterative-mode.md").write_text("stale", encoding="utf-8")
            (codex_target / "references" / "nested").mkdir()
            install("codex", codex_target, force=True)
            require(
                not (codex_target / "references" / "iterative-mode.md").exists(),
                "codex force install left stale legacy reference",
            )
            require(
                not (codex_target / "references" / "nested").exists(),
                "codex force install left stale reference directory",
            )
            require_raises(
                "codex overwrite refusal",
                FileExistsError,
                lambda: install("codex", codex_target, force=False),
            )

            os.environ["HOME"] = str(test_root / "home-claude")
            claude_target = expected_skill_target("claude")
            require(detect_runtime(claude_target) == "claude", "claude auto-detect failed")
            install("claude", claude_target, force=False)
            require_equal("claude payload", relative_files(claude_target), ["SKILL.md", "references/rules.md"])
            (claude_target / "agents").mkdir()
            (claude_target / "agents" / "openai.yaml").write_text("stale", encoding="utf-8")
            install("claude", claude_target, force=True)
            require_equal("claude payload after cleanup", relative_files(claude_target), ["SKILL.md", "references/rules.md"])
            require("agents" not in relative_dirs(claude_target), "claude force install left stale agents directory")
            commands_root = Path.home().resolve() / ".claude" / "commands"
            require_equal(
                "claude commands",
                relative_files(commands_root),
                ["project-doc-modes.md", "sdd.md"],
            )
            (commands_root / "project-doc-modes.md").unlink()
            (commands_root / "project-doc-modes.md").mkdir()
            install("claude", claude_target, force=True)
            require(
                (commands_root / "project-doc-modes.md").is_file(),
                "claude force install did not replace command directory",
            )
            project_command = (commands_root / "project-doc-modes.md").read_text(encoding="utf-8")
            sdd_command = (commands_root / "sdd.md").read_text(encoding="utf-8")
            for command_text_value in (project_command, sdd_command):
                require("@~/.claude/skills/project-doc-modes/SKILL.md" in command_text_value, "missing skill reference")
                require(
                    "@~/.claude/skills/project-doc-modes/references/rules.md" in command_text_value,
                    "missing rules reference",
                )
                require("$ARGUMENTS" in command_text_value, "missing argument passthrough")
                require("agents/openai.yaml" not in command_text_value, "claude command leaked Codex-only file")
                require(str(test_root) not in command_text_value, "claude command leaked temp absolute path")

            os.environ["HOME"] = str(test_root / "home-wrong")
            wrong_target = (test_root / "not-a-standard-skill" / SKILL_NAME).resolve()
            require_raises(
                "wrong codex target refusal",
                ValueError,
                lambda: install("codex", wrong_target, force=True),
            )
            ambiguous_target = (test_root / "skills" / SKILL_NAME).resolve()
            require_raises("ambiguous runtime refusal", ValueError, lambda: detect_runtime(ambiguous_target))
            repo_root = (test_root / "fake-repo").resolve()
            (repo_root / ".git").mkdir(parents=True)
            require_raises(
                "repository root refusal",
                ValueError,
                lambda: install("claude", repo_root, force=True),
            )
            nested_repo_target = repo_root / ".claude" / "skills" / SKILL_NAME
            require_raises(
                "nested repository install refusal",
                ValueError,
                lambda: install("claude", nested_repo_target, force=True),
            )
            claude_marked_root = (test_root / "claude-marked-repo").resolve()
            claude_marked_root.mkdir()
            (claude_marked_root / "CLAUDE.md").write_text("repo marker", encoding="utf-8")
            require_raises(
                "CLAUDE.md repository marker refusal",
                ValueError,
                lambda: install("claude", claude_marked_root, force=True),
            )

            os.environ["HOME"] = str(test_root / "home-bad-parent")
            Path.home().mkdir(parents=True)
            (Path.home() / ".codex").write_text("file parent", encoding="utf-8")
            bad_parent_target = expected_skill_target("codex")
            require_raises(
                "non-directory parent refusal",
                FileExistsError,
                lambda: install("codex", bad_parent_target, force=True),
            )

            cli_home = test_root / "home-cli"
            cli_target = cli_home / ".codex" / "skills" / SKILL_NAME
            cli_result = run_cli([str(cli_target), "--runtime", "codex"], cli_home)
            require(cli_result.returncode == 0, f"cli codex install failed: {cli_result.stderr}")
            require("runtime=codex" in cli_result.stdout, "cli stdout missing runtime")
            cli_repeat = run_cli([str(cli_target), "--runtime", "codex"], cli_home)
            require(cli_repeat.returncode == 2, "cli overwrite refusal returned wrong status")
            require("Refusing to overwrite existing path" in cli_repeat.stderr, "cli overwrite stderr missing refusal")
    finally:
        if original_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = original_home

    print("self-test: ok")
    return 0


def main() -> int:
    args = parse_args()
    if args.self_test:
        try:
            return run_self_test()
        except AssertionError as exc:
            print(f"self-test failed: {exc}", file=sys.stderr)
            return 1

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
