#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMMON_PATHS = [
    Path("SKILL.md"),
    Path("references"),
]
CODEX_ONLY_PATHS = [
    Path("agents/openai.yaml"),
]
CLAUDE_ONLY_PATHS = [
    Path("CLAUDE.md"),
    Path(".claude/commands/project-doc-modes.md"),
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
            "Destination root. For Codex, this should be the skill directory "
            "(for example ~/.codex/skills/project-doc-modes). For Claude Code, "
            "this should be the target repository root."
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
    target_parts = target.parts

    if ".codex" in target_parts and "skills" in target_parts:
        return "codex"

    if target.name == "project-doc-modes" and target.parent.name == "skills":
        return "codex"

    if (target / ".git").exists() or (target / ".claude").exists() or (target / "CLAUDE.md").exists():
        return "claude"

    home = Path.home()
    codex_home = home / ".codex"
    claude_home = home / ".claude"

    codex_exists = codex_home.exists()
    claude_exists = claude_home.exists()

    if codex_exists and not claude_exists:
        return "codex"

    if claude_exists and not codex_exists:
        return "claude"

    raise ValueError(
        "Could not auto-detect runtime for target "
        f"{target_str}. Pass --runtime codex or --runtime claude."
    )


def selected_paths(runtime: str) -> list[Path]:
    if runtime == "codex":
        return COMMON_PATHS + CODEX_ONLY_PATHS
    if runtime == "claude":
        return COMMON_PATHS + CLAUDE_ONLY_PATHS
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


def install(runtime: str, target_root: Path, force: bool) -> list[Path]:
    installed: list[Path] = []
    for relative_path in selected_paths(runtime):
        source = ROOT / relative_path
        destination = target_root / relative_path
        copy_entry(source, destination, force=force)
        installed.append(destination)
    return installed


def main() -> int:
    args = parse_args()
    try:
        target_root = Path(args.target).expanduser().resolve()
        target_root.mkdir(parents=True, exist_ok=True)

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
