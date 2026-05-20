#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


MANAGED_EVENT = "Stop"
MANAGED_STATUS = "project-doc-modes sync + verify"
MANAGED_SCRIPT_NAME = "project_doc_modes_stop.py"
MANAGED_SCRIPT_RELATIVE = Path(".codex") / "hooks" / MANAGED_SCRIPT_NAME
MANAGED_COMMAND = (
    "/usr/bin/python3 "
    '"$(git rev-parse --show-toplevel)/.codex/hooks/project_doc_modes_stop.py"'
)
MANAGED_HOOK = {
    "type": "command",
    "command": MANAGED_COMMAND,
    "statusMessage": MANAGED_STATUS,
}

HOOK_SCRIPT = r'''#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ACTIVE_DOC_MARKERS = (
    ("AGENTS.md", "docs/README.md"),
    ("docs/product/CURRENT.md",),
    ("docs/collaboration/ROLE_MATRIX.md",),
)


def read_payload() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def git_root(cwd: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    root = result.stdout.strip()
    return Path(root).resolve() if root else None


def project_root(payload: dict) -> Path:
    cwd_value = payload.get("cwd") or os.getcwd()
    cwd = Path(str(cwd_value)).expanduser()
    if not cwd.exists():
        cwd = Path.cwd()
    return git_root(cwd) or cwd.resolve()


def active_docs_exist(root: Path) -> bool:
    for marker_group in ACTIVE_DOC_MARKERS:
        if all((root / marker).exists() for marker in marker_group):
            return True
    return False


def write_json(data: dict) -> None:
    sys.stdout.write(json.dumps(data, ensure_ascii=False))


def continuation_prompt(root: Path, payload: dict) -> str:
    transcript_path = payload.get("transcript_path")
    transcript_note = (
        f"- Transcript path from hook payload: {transcript_path}\n"
        if transcript_path
        else "- Transcript path from hook payload: not provided\n"
    )
    return (
        "Use the installed project-doc-modes Skill in sync mode, then verify mode for this repository.\n\n"
        "This is an automatic project-level Codex Stop hook continuation. Do not treat it as a new init request.\n\n"
        "Scope and evidence:\n"
        f"- Project root: {root}\n"
        f"{transcript_note}"
        "- Read the latest session evidence that is available: the hook payload, recent transcript when readable, "
        "git status --short, changed files, relevant diff summary, verification output mentioned in the session, "
        "user decisions, implementation discoveries, unresolved risks, and rejected options.\n\n"
        "Required behavior:\n"
        "1. Apply project-doc-modes sync semantics only: non-interactive, incremental, no setup questions, no broad archive, no doc-tree rebuild.\n"
        "2. Do not edit code, tests, dependencies, runtime configuration, APIs, schemas, or product behavior.\n"
        "3. Update only active docs affected by this session, such as status, indexes, implementation records, reviews, decisions, release notes, or Reverse Sync targets.\n"
        "4. Then apply project-doc-modes verify semantics and report structure or consistency findings.\n"
        "5. Do not stage, commit, or push unless the user explicitly asked for Git actions."
    )


def main() -> int:
    payload = read_payload()
    if payload.get("stop_hook_active"):
        write_json({})
        return 0

    root = project_root(payload)
    if not active_docs_exist(root):
        write_json(
            {
                "systemMessage": (
                    "project-doc-modes hook is installed, but active docs were not found. "
                    "Run project-doc-modes init before automatic sync can update durable docs."
                )
            }
        )
        return 0

    write_json({"decision": "block", "reason": continuation_prompt(root, payload)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bind, inspect, or unbind the project-local Codex hook for project-doc-modes."
    )
    parser.add_argument(
        "--action",
        choices=("bind", "inspect", "unbind"),
        default="bind",
        help="Hook action to perform. Defaults to bind.",
    )
    parser.add_argument(
        "--project",
        default=".",
        help="Target project root or any directory inside the target project. Defaults to cwd.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run isolated smoke tests and exit.",
    )
    return parser.parse_args()


def git_root(cwd: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    root = result.stdout.strip()
    return Path(root).resolve() if root else None


def project_root(path: Path) -> Path:
    candidate = path.expanduser().resolve()
    if candidate.is_file():
        candidate = candidate.parent
    if not candidate.exists():
        raise ValueError(f"Project path does not exist: {path}")
    return git_root(candidate) or candidate


def hooks_json_path(root: Path) -> Path:
    return root / ".codex" / "hooks.json"


def hook_script_path(root: Path) -> Path:
    return root / MANAGED_SCRIPT_RELATIVE


def read_hooks(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"hooks": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError(f"Expected hooks object in {path}")
    return data


def is_managed_hook(hook: Any) -> bool:
    if not isinstance(hook, dict):
        return False
    command = hook.get("command")
    status = hook.get("statusMessage")
    return (
        isinstance(command, str)
        and MANAGED_SCRIPT_NAME in command
        or status == MANAGED_STATUS
    )


def normalize_stop_groups(data: dict[str, Any]) -> list[dict[str, Any]]:
    hooks = data.setdefault("hooks", {})
    groups = hooks.setdefault(MANAGED_EVENT, [])
    if not isinstance(groups, list):
        raise ValueError(f"Expected hooks.{MANAGED_EVENT} to be an array")
    return groups


def bind_hook(data: dict[str, Any]) -> bool:
    groups = normalize_stop_groups(data)
    changed = False

    for group in groups:
        if not isinstance(group, dict):
            continue
        hooks = group.get("hooks")
        if not isinstance(hooks, list):
            continue
        for index, hook in enumerate(hooks):
            if is_managed_hook(hook):
                if hook != MANAGED_HOOK:
                    hooks[index] = dict(MANAGED_HOOK)
                    changed = True
                return changed

    groups.append({"hooks": [dict(MANAGED_HOOK)]})
    return True


def unbind_hook(data: dict[str, Any]) -> bool:
    hooks = data.setdefault("hooks", {})
    changed = False

    for event_name, groups in list(hooks.items()):
        if not isinstance(groups, list):
            continue
        kept_groups: list[Any] = []
        for group in groups:
            if not isinstance(group, dict):
                kept_groups.append(group)
                continue
            handlers = group.get("hooks")
            if not isinstance(handlers, list):
                kept_groups.append(group)
                continue
            kept_handlers = [handler for handler in handlers if not is_managed_hook(handler)]
            if len(kept_handlers) != len(handlers):
                changed = True
            if kept_handlers:
                updated_group = dict(group)
                updated_group["hooks"] = kept_handlers
                kept_groups.append(updated_group)
        if kept_groups:
            hooks[event_name] = kept_groups
        else:
            hooks.pop(event_name, None)

    return changed


def write_hooks(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_hook_script(path: Path) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = HOOK_SCRIPT + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)
    return True


def inspect(root: Path) -> dict[str, Any]:
    hooks_path = hooks_json_path(root)
    script_path = hook_script_path(root)
    data = read_hooks(hooks_path) if hooks_path.exists() else {"hooks": {}}
    bound = False
    for groups in data.get("hooks", {}).values():
        if not isinstance(groups, list):
            continue
        for group in groups:
            if not isinstance(group, dict):
                continue
            handlers = group.get("hooks")
            if not isinstance(handlers, list):
                continue
            if any(is_managed_hook(handler) for handler in handlers):
                bound = True
    return {
        "project": str(root),
        "hooks_json": str(hooks_path),
        "hook_script": str(script_path),
        "bound": bound,
        "script_exists": script_path.exists(),
    }


def active_docs_exist(root: Path) -> bool:
    markers = (
        ("AGENTS.md", "docs/README.md"),
        ("docs/product/CURRENT.md",),
        ("docs/collaboration/ROLE_MATRIX.md",),
    )
    return any(all((root / marker).exists() for marker in marker_group) for marker_group in markers)


def print_report(report: dict[str, Any]) -> None:
    for key, value in report.items():
        print(f"{key}={value}")


def run_action(action: str, root: Path) -> dict[str, Any]:
    if action == "inspect":
        report = inspect(root)
        report["action"] = action
        return report

    hooks_path = hooks_json_path(root)
    script_path = hook_script_path(root)
    data = read_hooks(hooks_path)

    if action == "bind":
        hooks_changed = bind_hook(data)
        script_changed = write_hook_script(script_path)
        if hooks_changed:
            write_hooks(hooks_path, data)
        report = inspect(root)
        report.update(
            {
                "action": action,
                "scope": "project",
                "tool": "codex",
                "event": MANAGED_EVENT,
                "managed_name": MANAGED_STATUS,
                "hooks_changed": hooks_changed,
                "script_changed": script_changed,
                "global_config_touched": False,
                "active_docs_exist": active_docs_exist(root),
            }
        )
        return report

    if action == "unbind":
        hooks_changed = unbind_hook(data)
        if hooks_changed:
            write_hooks(hooks_path, data)
        script_removed = False
        if script_path.exists():
            script_path.unlink()
            script_removed = True
        report = inspect(root)
        report.update(
            {
                "action": action,
                "scope": "project",
                "tool": "codex",
                "event": MANAGED_EVENT,
                "managed_name": MANAGED_STATUS,
                "hooks_changed": hooks_changed,
                "script_removed": script_removed,
                "global_config_touched": False,
            }
        )
        return report

    raise ValueError(f"Unsupported action: {action}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="project-doc-modes-hook-test-") as temp_dir:
        root = Path(temp_dir) / "repo"
        root.mkdir()
        subprocess.run(["git", "init"], cwd=root, text=True, capture_output=True, check=True)
        (root / "README.md").write_text("demo\n", encoding="utf-8")

        bind_report = run_action("bind", root)
        require(bind_report["bound"], "bind did not mark hook as bound")
        require((root / ".codex" / "hooks.json").is_file(), "hooks.json missing")
        require((root / ".codex" / "hooks" / MANAGED_SCRIPT_NAME).is_file(), "hook script missing")
        require(not bind_report["active_docs_exist"], "greenfield repo should not look initialized")

        hooks_data = json.loads((root / ".codex" / "hooks.json").read_text(encoding="utf-8"))
        require(
            hooks_data["hooks"][MANAGED_EVENT][0]["hooks"][0]["command"] == MANAGED_COMMAND,
            "managed command mismatch",
        )

        second_bind = run_action("bind", root)
        require(second_bind["bound"], "second bind lost hook")

        (root / "AGENTS.md").write_text("rules\n", encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs" / "README.md").write_text("docs\n", encoding="utf-8")
        payload = json.dumps({"cwd": str(root), "hook_event_name": "Stop", "stop_hook_active": False})
        hook_result = subprocess.run(
            [sys.executable, str(root / ".codex" / "hooks" / MANAGED_SCRIPT_NAME)],
            input=payload,
            text=True,
            capture_output=True,
            check=False,
        )
        require(hook_result.returncode == 0, f"hook script failed: {hook_result.stderr}")
        output = json.loads(hook_result.stdout)
        require(output.get("decision") == "block", "hook did not request continuation")
        require("project-doc-modes" in output.get("reason", ""), "continuation missing workflow name")

        active_payload = json.dumps({"cwd": str(root), "hook_event_name": "Stop", "stop_hook_active": True})
        active_result = subprocess.run(
            [sys.executable, str(root / ".codex" / "hooks" / MANAGED_SCRIPT_NAME)],
            input=active_payload,
            text=True,
            capture_output=True,
            check=False,
        )
        require(active_result.stdout == "{}", "stop_hook_active guard should return empty JSON object")

        unbind_report = run_action("unbind", root)
        require(not unbind_report["bound"], "unbind left hook bound")
        require(not (root / ".codex" / "hooks" / MANAGED_SCRIPT_NAME).exists(), "unbind left hook script")

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
        root = project_root(Path(args.project))
        report = run_action(args.action, root)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
