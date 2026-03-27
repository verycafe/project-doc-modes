#!/usr/bin/env python3

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INSTALLER = ROOT / "scripts/install_runtime.py"
VALIDATOR = Path("/Users/tvwoo/.codex/skills/.system/skill-creator/scripts/quick_validate.py")


def run(
    cmd: list[str],
    cwd: Path | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=check,
        capture_output=True,
        text=True,
        env=env,
    )


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Expected path to exist: {path}")


def assert_missing(path: Path) -> None:
    if path.exists():
        raise AssertionError(f"Expected path to be absent: {path}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="project-doc-modes-runtime-test.") as temp_dir:
        root = Path(temp_dir)

        codex_target = root / ".codex" / "skills" / "project-doc-modes"
        claude_target = root / "sample-claude-repo"
        claude_target.mkdir(parents=True, exist_ok=True)
        (claude_target / ".git").mkdir()

        codex_result = run(
            [sys.executable, str(INSTALLER), str(codex_target), "--runtime", "auto"]
        )
        claude_result = run(
            [sys.executable, str(INSTALLER), str(claude_target), "--runtime", "auto"]
        )

        assert "runtime=codex" in codex_result.stdout
        assert "runtime=claude" in claude_result.stdout

        assert_exists(codex_target / "SKILL.md")
        assert_exists(codex_target / "references" / "verification.md")
        assert_exists(codex_target / "agents" / "openai.yaml")
        assert_missing(codex_target / "CLAUDE.md")
        assert_missing(codex_target / ".claude")

        assert_exists(claude_target / "SKILL.md")
        assert_exists(claude_target / "references" / "verification.md")
        assert_exists(claude_target / "CLAUDE.md")
        assert_exists(claude_target / ".claude" / "commands" / "project-doc-modes.md")
        assert_missing(claude_target / "agents")

        validate_result = run([sys.executable, str(VALIDATOR), str(codex_target)])
        if "Skill is valid!" not in validate_result.stdout:
            raise AssertionError("Codex-installed skill did not pass quick validation.")

        ambiguous_home = root / "ambiguous-home"
        (ambiguous_home / ".codex").mkdir(parents=True)
        (ambiguous_home / ".claude").mkdir(parents=True)
        ambiguous_target = root / "ambiguous-target"
        ambiguous_env = dict(os.environ)
        ambiguous_env["HOME"] = str(ambiguous_home)

        ambiguous_result = run(
            [sys.executable, str(INSTALLER), str(ambiguous_target), "--runtime", "auto"],
            check=False,
            env=ambiguous_env,
        )
        if ambiguous_result.returncode == 0:
            raise AssertionError("Ambiguous auto-detection should not have succeeded.")
        if "Could not auto-detect runtime" not in ambiguous_result.stderr:
            raise AssertionError("Ambiguous auto-detection did not report the expected error.")

        print("Codex install verified.")
        print("Claude install verified.")
        print("Cross-runtime file isolation verified.")
        print("Ambiguous auto-detection verified.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
