# project-doc-modes Installation

Use this file when an AI assistant is asked to install `project-doc-modes`.

Do not create or migrate any target-project docs during installation. Installation only places the Skill runtime files into the user's Codex or Claude Code Skill folder.

## Source

- GitHub repo: `https://github.com/verycafe/project-doc-modes`
- Runtime package inside repo: `project-doc-modes/`
- Runtime payload:

```text
SKILL.md
references/rules.md
```

## Targets

Install into the default Skill folder for the requested runtime:

```text
Codex:      ${CODEX_HOME:-$HOME/.codex}/skills/project-doc-modes
Claude Code: ${CLAUDE_HOME:-$HOME/.claude}/skills/project-doc-modes
```

Do not directly clone the GitHub repo into the final Skill folder. The repo contains maintainer files such as `README.md`, `install.md`, `assets/`, and `scripts/`; the final Skill folder should contain only the runtime payload above.

## Install Codex

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
tmp="$(mktemp -d)"
git clone --depth 1 https://github.com/verycafe/project-doc-modes.git "$tmp/project-doc-modes"
python3 "$tmp/project-doc-modes/scripts/install_runtime.py" "$CODEX_HOME/skills/project-doc-modes" --runtime codex --force
rm -rf "$tmp"
```

## Install Claude Code

```bash
export CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
tmp="$(mktemp -d)"
git clone --depth 1 https://github.com/verycafe/project-doc-modes.git "$tmp/project-doc-modes"
python3 "$tmp/project-doc-modes/scripts/install_runtime.py" "$CLAUDE_HOME/skills/project-doc-modes" --runtime claude --force
rm -rf "$tmp"
```

Claude Code installation also creates:

```text
$CLAUDE_HOME/commands/project-doc-modes.md
$CLAUDE_HOME/commands/project-doc-modes-sync.md
$CLAUDE_HOME/commands/project-doc-modes-verify.md
$CLAUDE_HOME/commands/sdd.md
```

## Verify

After installation, verify that the final Skill folder contains the runtime payload and not the source repo:

```bash
find "${CODEX_HOME:-$HOME/.codex}/skills/project-doc-modes" -maxdepth 3 -type f | sort
find "${CLAUDE_HOME:-$HOME/.claude}/skills/project-doc-modes" -maxdepth 3 -type f | sort
```

Expected runtime files:

```text
SKILL.md
references/rules.md
```

The Claude Code commands are expected only for Claude Code installs. Use `/project-doc-modes` for init or migration, `/project-doc-modes-sync` for hook-safe incremental Reverse Sync, `/project-doc-modes-verify` for read-only checks, and `/sdd` for SDD-RIPER governance.
