#!/usr/bin/env python3

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INSTALLER = ROOT / "scripts/install_runtime.py"


def validator_path() -> Path | None:
    candidates = [
        os.environ.get("PROJECT_DOC_MODES_VALIDATOR"),
        "/Users/tvwoo/.codex/skills/.system/skill-creator/scripts/quick_validate.py",
        str(Path.home() / ".claude/skills/skill-creator/scripts/quick_validate.py"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return Path(candidate)
    return None


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


def assert_contains(path: Path, text: str) -> None:
    if text not in path.read_text(encoding="utf-8"):
        raise AssertionError(f"Expected {path} to contain: {text}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="project-doc-modes-runtime-test.") as temp_dir:
        root = Path(temp_dir)

        codex_target = root / ".codex" / "skills" / "project-doc-modes"
        claude_target = root / ".claude" / "skills" / "project-doc-modes"
        claude_commands = root / ".claude" / "commands"
        runtime_env = dict(os.environ)
        runtime_env["HOME"] = str(root)
        repository_target = root / "sample-claude-repo"
        repository_target.mkdir(parents=True, exist_ok=True)
        (repository_target / ".git").mkdir()

        codex_result = run(
            [sys.executable, str(INSTALLER), str(codex_target), "--runtime", "auto"],
            env=runtime_env,
        )
        claude_result = run(
            [sys.executable, str(INSTALLER), str(claude_target), "--runtime", "auto"],
            env=runtime_env,
        )

        assert "runtime=codex" in codex_result.stdout
        assert "runtime=claude" in claude_result.stdout

        assert_exists(codex_target / "SKILL.md")
        assert_exists(codex_target / "references" / "verification.md")
        assert_exists(codex_target / "references" / "sdd-riper.md")
        assert_exists(codex_target / "agents" / "openai.yaml")
        assert_missing(codex_target / "CLAUDE.md")
        assert_missing(codex_target / ".claude")

        assert_exists(claude_target / "SKILL.md")
        assert_exists(claude_target / "references" / "verification.md")
        assert_exists(claude_target / "references" / "sdd-riper.md")
        assert_missing(claude_target / "CLAUDE.md")
        assert_missing(claude_target / ".claude")
        assert_missing(claude_target / "agents")
        assert_exists(claude_commands / "project-doc-modes.md")
        assert_exists(claude_commands / "sdd.md")
        assert_contains(claude_commands / "project-doc-modes.md", str(claude_target / "SKILL.md"))
        assert_contains(claude_commands / "sdd.md", str(claude_target / "references" / "sdd-riper.md"))

        validator = validator_path()
        if validator:
            validate_result = run([sys.executable, str(validator), str(codex_target)])
            if "Skill is valid!" not in validate_result.stdout:
                raise AssertionError("Codex-installed skill did not pass quick validation.")
            validate_result = run([sys.executable, str(validator), str(claude_target)])
            if "Skill is valid!" not in validate_result.stdout:
                raise AssertionError("Claude-installed skill did not pass quick validation.")
        else:
            print("Skill quick validation skipped: validator not found.")

        repository_result = run(
            [sys.executable, str(INSTALLER), str(repository_target), "--runtime", "auto"],
            check=False,
            env=runtime_env,
        )
        if repository_result.returncode == 0:
            raise AssertionError("Repository-root auto-detection should not install runtime files.")
        if "Refusing to install Claude runtime files into a repository root" not in repository_result.stderr:
            raise AssertionError("Repository-root refusal did not report the expected error.")
        repository_result = run(
            [sys.executable, str(INSTALLER), str(repository_target), "--runtime", "claude"],
            check=False,
            env=runtime_env,
        )
        if repository_result.returncode == 0:
            raise AssertionError("Explicit Claude repository-root install should not succeed.")
        if "Refusing to install runtime files inside a repository tree" not in repository_result.stderr:
            raise AssertionError("Explicit repository-root refusal did not report the expected error.")
        assert_missing(repository_target / "SKILL.md")
        assert_missing(repository_target / "references")
        assert_missing(repository_target / ".claude" / "commands" / "project-doc-modes.md")

        plain_claude_target = root / "plain-claude-target"
        plain_claude_result = run(
            [sys.executable, str(INSTALLER), str(plain_claude_target), "--runtime", "claude"],
            check=False,
            env=runtime_env,
        )
        if plain_claude_result.returncode == 0:
            raise AssertionError("Explicit Claude install to a plain directory should not succeed.")
        if "outside a standard claude user-level skill target" not in plain_claude_result.stderr:
            raise AssertionError("Plain Claude target refusal did not report the expected error.")
        assert_missing(plain_claude_target)

        plain_codex_target = root / "plain-codex-target"
        plain_codex_result = run(
            [sys.executable, str(INSTALLER), str(plain_codex_target), "--runtime", "codex"],
            check=False,
            env=runtime_env,
        )
        if plain_codex_result.returncode == 0:
            raise AssertionError("Explicit Codex install to a plain directory should not succeed.")
        if "outside a standard codex user-level skill target" not in plain_codex_result.stderr:
            raise AssertionError("Plain Codex target refusal did not report the expected error.")
        assert_missing(plain_codex_target)

        nested_claude_target = root / ".claude" / "skills" / "nested" / "project-doc-modes"
        nested_claude_result = run(
            [sys.executable, str(INSTALLER), str(nested_claude_target), "--runtime", "claude"],
            check=False,
            env=runtime_env,
        )
        if nested_claude_result.returncode == 0:
            raise AssertionError("Nested Claude skill target should not succeed.")
        if "outside a standard claude user-level skill target" not in nested_claude_result.stderr:
            raise AssertionError("Nested Claude target refusal did not report the expected error.")
        assert_missing(nested_claude_target / "SKILL.md")

        nested_codex_target = root / ".codex" / "skills" / "nested" / "project-doc-modes"
        nested_codex_result = run(
            [sys.executable, str(INSTALLER), str(nested_codex_target), "--runtime", "codex"],
            check=False,
            env=runtime_env,
        )
        if nested_codex_result.returncode == 0:
            raise AssertionError("Nested Codex skill target should not succeed.")
        if "outside a standard codex user-level skill target" not in nested_codex_result.stderr:
            raise AssertionError("Nested Codex target refusal did not report the expected error.")
        assert_missing(nested_codex_target / "SKILL.md")

        repository_nested_target = repository_target / ".claude" / "skills" / "project-doc-modes"
        nested_result = run(
            [sys.executable, str(INSTALLER), str(repository_nested_target), "--runtime", "claude"],
            check=False,
            env=runtime_env,
        )
        if nested_result.returncode == 0:
            raise AssertionError("Claude install inside a repository tree should not succeed.")
        if "inside a repository tree" not in nested_result.stderr:
            raise AssertionError("Nested repository target refusal did not report the expected error.")
        assert_missing(repository_nested_target / "SKILL.md")

        no_git_claude_repo = root / "no-git-claude-repo"
        no_git_claude_repo.mkdir()
        (no_git_claude_repo / "CLAUDE.md").write_text("# Claude repo marker\n", encoding="utf-8")
        no_git_nested_target = no_git_claude_repo / ".claude" / "skills" / "project-doc-modes"
        no_git_result = run(
            [sys.executable, str(INSTALLER), str(no_git_nested_target), "--runtime", "claude"],
            check=False,
            env=runtime_env,
        )
        if no_git_result.returncode == 0:
            raise AssertionError("Claude install inside a no-git repository-like tree should not succeed.")
        if "inside a repository tree" not in no_git_result.stderr:
            raise AssertionError("No-git repository-like target refusal did not report the expected error.")
        assert_missing(no_git_nested_target / "SKILL.md")

        conflict_home = root / "conflict-home"
        conflict_target = conflict_home / ".claude" / "skills" / "project-doc-modes"
        conflict_commands = conflict_home / ".claude" / "commands"
        conflict_env = dict(os.environ)
        conflict_env["HOME"] = str(conflict_home)
        conflict_commands.mkdir(parents=True)
        (conflict_commands / "project-doc-modes.md").write_text("existing", encoding="utf-8")
        conflict_result = run(
            [sys.executable, str(INSTALLER), str(conflict_target), "--runtime", "claude"],
            check=False,
            env=conflict_env,
        )
        if conflict_result.returncode == 0:
            raise AssertionError("Claude install with command overwrite conflict should not succeed.")
        if "Refusing to overwrite existing path" not in conflict_result.stderr:
            raise AssertionError("Claude command conflict did not report the expected error.")
        assert_missing(conflict_target / "SKILL.md")

        parent_conflict_home = root / "parent-conflict-home"
        parent_conflict_target = parent_conflict_home / ".claude" / "skills" / "project-doc-modes"
        parent_conflict_env = dict(os.environ)
        parent_conflict_env["HOME"] = str(parent_conflict_home)
        (parent_conflict_home / ".claude").mkdir(parents=True)
        (parent_conflict_home / ".claude" / "commands").write_text("not a dir", encoding="utf-8")
        parent_conflict_result = run(
            [sys.executable, str(INSTALLER), str(parent_conflict_target), "--runtime", "claude", "--force"],
            check=False,
            env=parent_conflict_env,
        )
        if parent_conflict_result.returncode == 0:
            raise AssertionError("Claude install through a non-directory commands path should not succeed.")
        if "non-directory" not in parent_conflict_result.stderr:
            raise AssertionError("Parent path conflict did not report the expected error.")
        assert_missing(parent_conflict_target / "SKILL.md")

        force_home = root / "force-home"
        force_target = force_home / ".claude" / "skills" / "project-doc-modes"
        force_env = dict(os.environ)
        force_env["HOME"] = str(force_home)
        force_command_dir = force_home / ".claude" / "commands" / "project-doc-modes.md"
        force_command_dir.mkdir(parents=True)
        force_result = run(
            [sys.executable, str(INSTALLER), str(force_target), "--runtime", "claude", "--force"],
            env=force_env,
        )
        if "runtime=claude" not in force_result.stdout:
            raise AssertionError("Claude force install did not report success.")
        assert_exists(force_target / "SKILL.md")
        if not (force_home / ".claude" / "commands" / "project-doc-modes.md").is_file():
            raise AssertionError("Claude force install did not replace command directory with a file.")

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
        print("Repository-root install refusal verified.")
        print("Nonstandard target refusal verified.")
        print("Preflight overwrite refusal verified.")
        print("Ambiguous auto-detection verified.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
