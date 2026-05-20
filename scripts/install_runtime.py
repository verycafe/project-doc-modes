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
PACKAGE_ROOT = ROOT / SKILL_NAME
CLAUDE_COMMANDS = (
    "project-doc-modes",
    "project-doc-modes-sdd",
    "project-doc-modes-sync",
    "project-doc-modes-verify",
)
CLAUDE_COMMAND_FILES = sorted(f"{command}.md" for command in CLAUDE_COMMANDS)
LEGACY_CLAUDE_COMMANDS = (
    "sdd",
)
LEGACY_CLAUDE_COMMAND_FILES = [f"{command}.md" for command in LEGACY_CLAUDE_COMMANDS]
COMMON_PATHS = [
    Path("SKILL.md"),
    Path("references/rules.md"),
]
LEGACY_SKILL_PATHS = [
    Path("references/collaboration-mode.md"),
    Path("references/iterative-mode.md"),
    Path("references/sdd-riper.md"),
    Path("references/verification.md"),
]
STALE_RUNTIME_PATHS = [
    Path("agents/openai.yaml"),
]
SOURCE_REPO_PATHS = [
    Path(".git"),
    Path("README.md"),
    Path("install.md"),
    Path("hooks.md"),
    Path("assets"),
    Path("scripts"),
    Path(SKILL_NAME),
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
            "(for example $CODEX_HOME/skills/project-doc-modes). For Claude Code, "
            "this must be the user-level skill directory "
            "(for example $CLAUDE_HOME/skills/project-doc-modes)."
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
            f"{expected_target_hint('claude')}."
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


def home_env_for_runtime(runtime: str) -> str:
    if runtime == "codex":
        return "CODEX_HOME"
    if runtime == "claude":
        return "CLAUDE_HOME"
    raise ValueError(f"Unsupported runtime: {runtime}")


def runtime_home(runtime: str) -> Path:
    env_value = os.environ.get(home_env_for_runtime(runtime))
    if env_value:
        return Path(env_value).expanduser().resolve()
    return (Path.home() / marker_for_runtime(runtime)).resolve()


def expected_target_hint(runtime: str) -> str:
    env_name = home_env_for_runtime(runtime)
    default = f"$HOME/{marker_for_runtime(runtime)}/skills/{SKILL_NAME}"
    return f"${env_name}/skills/{SKILL_NAME} (default: {default})"


def expected_skill_target(runtime: str) -> Path:
    return (runtime_home(runtime) / "skills" / SKILL_NAME).resolve()


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
    if runtime in {"codex", "claude"}:
        return COMMON_PATHS
    raise ValueError(f"Unsupported runtime: {runtime}")


def source_root() -> Path:
    if (PACKAGE_ROOT / "SKILL.md").is_file():
        return PACKAGE_ROOT
    if (ROOT / "SKILL.md").is_file():
        return ROOT
    raise FileNotFoundError(
        f"Could not find runtime package. Expected {PACKAGE_ROOT / 'SKILL.md'}."
    )


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
    in_place = ROOT.resolve() == target_root.resolve()
    payload_root = source_root()
    if force:
        cleanup_stale_runtime_files(target_root, in_place=in_place)

    installed: list[Path] = []
    for relative_path in selected_paths(runtime):
        source = payload_root / relative_path
        destination = target_root / relative_path
        if source.resolve() != destination.resolve():
            copy_entry(source, destination, force=force)
        installed.append(destination)

    if runtime == "claude":
        installed.extend(install_claude_commands(target_root, force=force))

    return installed


def cleanup_stale_runtime_files(target_root: Path, in_place: bool) -> None:
    if in_place:
        stale_paths = [*LEGACY_SKILL_PATHS, *STALE_RUNTIME_PATHS]
    else:
        stale_paths = [
            *MANAGED_PAYLOAD_DIRS,
            *LEGACY_SKILL_PATHS,
            *STALE_RUNTIME_PATHS,
            *SOURCE_REPO_PATHS,
        ]

    for relative_path in stale_paths:
        path = target_root / relative_path
        if path.exists():
            remove_path(path)

    if in_place:
        remove_empty_dirs(target_root, [target_root / "agents"])


def remove_empty_dirs(stop_at: Path, candidates: list[Path]) -> None:
    for candidate in candidates:
        path = candidate
        while path != stop_at and stop_at in path.parents:
            try:
                path.rmdir()
            except OSError:
                break
            path = path.parent


def claude_command_paths(skill_root: Path) -> list[Path]:
    commands_root = runtime_home("claude") / "commands"
    return [commands_root / f"{command}.md" for command in CLAUDE_COMMANDS]


def command_reference(path: Path) -> str:
    resolved = path.resolve()
    env_matches: list[tuple[int, str, Path]] = []
    for env_name in ("CODEX_HOME", "CLAUDE_HOME"):
        env_value = os.environ.get(env_name)
        if not env_value:
            continue
        env_root = Path(env_value).expanduser().resolve()
        try:
            relative = resolved.relative_to(env_root)
        except ValueError:
            continue
        env_matches.append((len(str(env_root)), env_name, relative))
    if env_matches:
        _, env_name, relative = max(env_matches)
        return f"${env_name}/{relative.as_posix()}"

    try:
        relative = resolved.relative_to(Path.home().resolve())
    except ValueError:
        return str(path)
    return f"~/{relative.as_posix()}"


def command_text(command: str, skill_root: Path) -> str:
    skill_md = command_reference(skill_root / "SKILL.md")
    rules_ref = command_reference(skill_root / "references" / "rules.md")

    if command == "project-doc-modes":
        return f"""---
description: Initialize, migrate, or fully upgrade repository docs with project-doc-modes.
argument-hint: [init goal, mode, language, or upgrade target]
---

Use the installed `project-doc-modes` workflow in `init` mode unless the user explicitly asks for `sync` or `verify`.

For SDD-RIPER-only work, `/project-doc-modes-sdd` is the namespaced command, but this command may also handle SDD-RIPER when the user asks for it.

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
12. Do not write `project-doc-modes`, `/project-doc-modes`, `/project-doc-modes-sdd`, `/project-doc-modes-sync`, `/project-doc-modes-verify`, `/sdd`, `$project-doc-modes`, `SKILL.md`, or local install paths into generated target docs.
13. Keep generated docs local-only in Git unless the user explicitly asks to track, stage, or commit them.
14. For iterative docs, follow `PRD -> PHASE -> SPEC`: requirements first, phase plans next, SPEC docs under each phase.
15. When team vibe coding or SDD-RIPER is requested, read the SDD-RIPER reference and record stage, approval gates, review path, and Reverse Sync path.
16. For upgrades, copy a snapshot into `docs/archive/` before updating current docs; do not empty `docs/` unless the user requests a full reset.
17. Scaffold or migrate the repository docs with minimal changes.
18. Run the verification checklist before claiming completion.

Use `/project-doc-modes-sync` for hook-safe incremental Reverse Sync after the initial structure already exists.
Use `/project-doc-modes-verify` for read-only structure checks.

If the user supplied extra arguments, treat them as additional intent:

$ARGUMENTS
"""

    if command == "project-doc-modes-sync":
        return f"""---
description: Incrementally reverse-sync project docs from the latest session or hook event.
argument-hint: [session summary, changed files, verification output]
---

Use the installed `project-doc-modes` workflow in `sync` mode.

This command is hook-safe: it is non-interactive, incremental, and must not rerun the full init or migration flow.

Primary source of truth:
- @{skill_md}
- @{rules_ref}

Read the minimum extra context you need:
- @{rules_ref} for incremental sync rules, SDD-RIPER Reverse Sync paths, and verification

Expected behavior:
1. Inspect current entrypoints, active mode markers, `docs/README.md`, `git status --short`, and changed file names.
2. Use the supplied session summary, changed files, verification commands and output, or hook payload as the evidence source.
3. Do not ask setup questions. If required context is missing, record a concise pending item or report the missing input.
4. Do not choose or change the repository mode, migrate the doc tree, run a broad pre-migration archive, or rewrite the documentation system.
5. Do not edit user code, tests, dependencies, runtime configuration, APIs, schemas, or product logic.
6. Update only docs affected by the latest session: status, context deltas, active implementation records, review notes, decisions, release notes, or stale entrypoint indexes.
7. Update PRD, PHASE, or SPEC content only when the session explicitly changed requirements, intended behavior, architecture, or acceptance criteria.
8. Preserve the `PRD -> PHASE -> SPEC` chain and write Reverse Sync records under the active mode path.
9. Keep generated docs local-only in Git unless the user explicitly asks to track, stage, commit, or push them.
10. Run the incremental verification checklist before claiming completion.

If the user supplied extra arguments or hook payload, treat them as the evidence for this sync:

$ARGUMENTS
"""

    if command == "project-doc-modes-verify":
        return f"""---
description: Verify repository documentation structure without changing docs.
argument-hint: [mode, version, or paths to check]
---

Use the installed `project-doc-modes` workflow in `verify` mode.

This command is read-only unless the user explicitly asks for repairs.

Primary source of truth:
- @{skill_md}
- @{rules_ref}

Read the minimum extra context you need:
- @{rules_ref} for structure, entrypoint, local-only, leakage, and SDD-RIPER checks

Expected behavior:
1. Inspect root Markdown files, `docs/`, active mode markers, current version pointers, and `git status --short`.
2. Run or emulate the verification checklist from the rules reference.
3. Check root Markdown limits, `docs/archive/`, `PRD -> PHASE -> SPEC` placement, entrypoint links, Claude bridge behavior, local-only policy, and local path leakage.
4. Check SDD-RIPER CodeMap, context bundle, review, and Reverse Sync paths only when SDD-RIPER is active.
5. Do not create, move, archive, rewrite, stage, commit, or push files unless the user explicitly asks for repairs.
6. Report findings by severity with exact file paths and commands run.

If the user supplied extra arguments, treat them as verification scope:

$ARGUMENTS
"""

    if command == "project-doc-modes-sdd":
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
11. Do not write `project-doc-modes`, `/project-doc-modes`, `/project-doc-modes-sdd`, `/project-doc-modes-sync`, `/project-doc-modes-verify`, `/sdd`, `$project-doc-modes`, `SKILL.md`, or local install paths into generated target docs.
12. Put CodeMap and context bundles under `docs/governance/context/`.
13. Record the current RIPER stage, human approval gates, spec-vs-code review path, and Reverse Sync path.
14. For upgrades, copy a snapshot into `docs/archive/` before updating current docs; do not empty `docs/` unless the user requests a full reset.
15. Run the verification checklist before claiming completion.

If the user supplied extra arguments, treat them as additional intent:

$ARGUMENTS
"""

    raise ValueError(f"Unsupported Claude command: {command}")


def install_claude_commands(skill_root: Path, force: bool) -> list[Path]:
    commands_root = runtime_home("claude") / "commands"
    commands_root.mkdir(parents=True, exist_ok=True)

    installed: list[Path] = []
    if force:
        for command_file in LEGACY_CLAUDE_COMMAND_FILES:
            legacy_path = commands_root / command_file
            if legacy_path.exists():
                remove_path(legacy_path)

    for command, destination in zip(CLAUDE_COMMANDS, claude_command_paths(skill_root)):
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
    return run_cli_with_script(Path(__file__).resolve(), args, home, ROOT)


def run_cli_with_script(
    script_path: Path, args: list[str], home: Path, cwd: Path
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def run_self_test() -> int:
    original_env = {
        "HOME": os.environ.get("HOME"),
        "CODEX_HOME": os.environ.get("CODEX_HOME"),
        "CLAUDE_HOME": os.environ.get("CLAUDE_HOME"),
    }
    try:
        os.environ.pop("CODEX_HOME", None)
        os.environ.pop("CLAUDE_HOME", None)

        with tempfile.TemporaryDirectory(prefix=f"{SKILL_NAME}-install-test-") as temp_dir:
            test_root = Path(temp_dir)

            os.environ["HOME"] = str(test_root / "home-codex")
            codex_target = expected_skill_target("codex")
            require(detect_runtime(codex_target) == "codex", "codex auto-detect failed")
            install("codex", codex_target, force=False)
            require_equal(
                "codex payload",
                relative_files(codex_target),
                ["SKILL.md", "references/rules.md"],
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
            (codex_target / "README.md").write_text("repo readme", encoding="utf-8")
            (codex_target / "hooks.md").write_text("repo hook instructions", encoding="utf-8")
            (codex_target / "assets").mkdir()
            (codex_target / SKILL_NAME).mkdir()
            install("codex", codex_target, force=True)
            require(not (codex_target / "README.md").exists(), "codex force install left repo README")
            require(not (codex_target / "hooks.md").exists(), "codex force install left repo hooks.md")
            require(not (codex_target / "assets").exists(), "codex force install left repo assets")
            require(not (codex_target / SKILL_NAME).exists(), "codex force install left nested package")

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
            commands_root = runtime_home("claude") / "commands"
            require_equal(
                "claude commands",
                relative_files(commands_root),
                CLAUDE_COMMAND_FILES,
            )
            (commands_root / "sdd.md").write_text("stale legacy command", encoding="utf-8")
            (commands_root / "project-doc-modes.md").unlink()
            (commands_root / "project-doc-modes.md").mkdir()
            install("claude", claude_target, force=True)
            require(
                (commands_root / "project-doc-modes.md").is_file(),
                "claude force install did not replace command directory",
            )
            require(not (commands_root / "sdd.md").exists(), "claude force install left legacy /sdd command")
            require_equal(
                "claude commands after legacy cleanup",
                relative_files(commands_root),
                CLAUDE_COMMAND_FILES,
            )
            project_command = (commands_root / "project-doc-modes.md").read_text(encoding="utf-8")
            sdd_command = (commands_root / "project-doc-modes-sdd.md").read_text(encoding="utf-8")
            sync_command = (commands_root / "project-doc-modes-sync.md").read_text(encoding="utf-8")
            verify_command = (commands_root / "project-doc-modes-verify.md").read_text(encoding="utf-8")
            for command_text_value in (project_command, sdd_command, sync_command, verify_command):
                require("@~/.claude/skills/project-doc-modes/SKILL.md" in command_text_value, "missing skill reference")
                require(
                    "@~/.claude/skills/project-doc-modes/references/rules.md" in command_text_value,
                    "missing rules reference",
                )
                require("$ARGUMENTS" in command_text_value, "missing argument passthrough")
                require("agents/openai.yaml" not in command_text_value, "claude command leaked Codex-only file")
                require(str(test_root) not in command_text_value, "claude command leaked temp absolute path")
            require("hook-safe" in sync_command, "sync command missing hook-safe contract")
            require("Do not ask setup questions" in sync_command, "sync command may prompt during hooks")
            require("read-only" in verify_command, "verify command missing read-only contract")

            os.environ["HOME"] = str(test_root / "home-custom-runtime")
            os.environ["CODEX_HOME"] = str(test_root / "custom-codex-home")
            custom_codex_target = expected_skill_target("codex")
            install("codex", custom_codex_target, force=True)
            require_equal(
                "custom codex payload",
                relative_files(custom_codex_target),
                ["SKILL.md", "references/rules.md"],
            )
            os.environ.pop("CODEX_HOME", None)

            os.environ["CLAUDE_HOME"] = str(test_root / "custom-claude-home")
            custom_claude_target = expected_skill_target("claude")
            install("claude", custom_claude_target, force=True)
            require_equal(
                "custom claude payload",
                relative_files(custom_claude_target),
                ["SKILL.md", "references/rules.md"],
            )
            custom_commands_root = runtime_home("claude") / "commands"
            require_equal(
                "custom claude commands",
                relative_files(custom_commands_root),
                CLAUDE_COMMAND_FILES,
            )
            for command_file in CLAUDE_COMMAND_FILES:
                custom_command = (custom_commands_root / command_file).read_text(encoding="utf-8")
                require(
                    "@$CLAUDE_HOME/skills/project-doc-modes/SKILL.md" in custom_command,
                    "custom claude command missing CLAUDE_HOME skill reference",
                )
                require(
                    "@$CLAUDE_HOME/skills/project-doc-modes/references/rules.md" in custom_command,
                    "custom claude command missing CLAUDE_HOME rules reference",
                )
                require(str(test_root) not in custom_command, "custom claude command leaked temp absolute path")
            os.environ.pop("CLAUDE_HOME", None)

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

            same_home = test_root / "home-same-target"
            same_target = same_home / ".claude" / "skills" / SKILL_NAME
            shutil.copytree(
                ROOT,
                same_target,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            (same_target / "agents").mkdir(exist_ok=True)
            (same_target / "agents" / "openai.yaml").write_text("stale", encoding="utf-8")
            same_result = run_cli_with_script(
                same_target / "scripts" / "install_runtime.py",
                [str(same_target), "--runtime", "claude", "--force"],
                same_home,
                same_target,
            )
            require(same_result.returncode == 0, f"same-target claude sync failed: {same_result.stderr}")
            require((same_target / "SKILL.md").is_file(), "same-target sync removed SKILL.md")
            require((same_target / "references" / "rules.md").is_file(), "same-target sync removed rules.md")
            require(not (same_target / "agents").exists(), "same-target sync left stale agents directory")
            same_commands = same_home / ".claude" / "commands"
            require_equal(
                "same-target claude commands",
                relative_files(same_commands),
                CLAUDE_COMMAND_FILES,
            )
    finally:
        for name, value in original_env.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

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
