#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = ROOT / "project-doc-modes"
EXPECTED_REFERENCES = [
    "init.md",
    "rules.md",
    "sdd.md",
    "structure.md",
    "sync.md",
    "verify.md",
]
CLAUDE_COMMANDS = [
    "project-doc-modes",
    "project-doc-modes-sdd",
    "project-doc-modes-sync",
    "project-doc-modes-verify",
]


class IntegrityError(Exception):
    pass


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        raise IntegrityError(f"missing file: {relative}")
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IntegrityError(message)


def require_contains(relative: str, needles: list[str]) -> None:
    content = read_text(relative)
    for needle in needles:
        require(needle in content, f"{relative} missing {needle!r}")


def check_runtime_references() -> None:
    for reference in EXPECTED_REFERENCES:
        path = SKILL_ROOT / "references" / reference
        require(path.is_file(), f"missing runtime reference: {path.relative_to(ROOT)}")

    installer = read_text("scripts/install_runtime.py")
    for reference in EXPECTED_REFERENCES:
        require(
            f'Path("references/{reference}")' in installer,
            f"installer does not copy references/{reference}",
        )


def check_command_contracts() -> None:
    installer = read_text("scripts/install_runtime.py")
    for command in CLAUDE_COMMANDS:
        require(f'"{command}"' in installer, f"installer missing Claude command {command}")

    readme_needles = [
        "/project-doc-modes",
        "/project-doc-modes-sdd",
        "/project-doc-modes-sync",
        "/project-doc-modes-verify",
        "docs/governance/context/GLOSSARY.md",
        "docs/governance/research/",
        "docs/governance/experience/",
    ]
    require_contains("README.md", readme_needles)
    require_contains("install.md", CLAUDE_COMMANDS)
    require_contains("project-doc-modes/SKILL.md", ["project-doc-modes init", "project-doc-modes sync", "project-doc-modes verify", "project-doc-modes sdd"])


def check_hook_contract() -> None:
    require_contains(
        "hooks.md",
        [
            ".codex/hooks.json",
            ".codex/hooks/project_doc_modes_stop.py",
            "project-doc-modes sync + verify",
            "sync",
            "verify",
        ],
    )
    require_contains(
        "scripts/bind_codex_project_hook.py",
        [
            'MANAGED_EVENT = "Stop"',
            'MANAGED_STATUS = "project-doc-modes sync + verify"',
            "project_doc_modes_stop.py",
            "project_doc_modes_stop.log",
            "append_audit",
        ],
    )


def check_claude_plugin() -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    require(plugin_path.is_file(), "missing .claude-plugin/plugin.json")
    data = json.loads(plugin_path.read_text(encoding="utf-8"))
    require(data.get("name") == "project-doc-modes", "plugin name mismatch")
    require(data.get("skills") == ["./project-doc-modes"], "plugin skills mismatch")


def check_specs_have_validation_loops() -> None:
    spec_root = ROOT / "docs" / "product"
    if not spec_root.exists():
        return
    for spec_path in spec_root.rglob("SPEC*.md"):
        if "archive" in spec_path.parts:
            continue
        text = spec_path.read_text(encoding="utf-8")
        require(
            "Validation Loop" in text,
            f"{spec_path.relative_to(ROOT)} missing Validation Loop",
        )


def main() -> int:
    try:
        check_runtime_references()
        check_command_contracts()
        check_hook_contract()
        check_claude_plugin()
        check_specs_have_validation_loops()
    except (IntegrityError, json.JSONDecodeError) as exc:
        print(f"repo integrity: failed: {exc}", file=sys.stderr)
        return 1

    print("repo integrity: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
