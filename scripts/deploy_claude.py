#!/usr/bin/env python3
"""Copy Claude config files from this repo to their live locations.

Existing destination files that differ are backed up as <name>.bak.<timestamp>.
Empty source files are skipped.
"""

import argparse
import filecmp
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "claude"
CLAUDE_HOME = Path.home() / ".claude"

# (path relative to SOURCE, destination)
FILES = [
    ("CLAUDE.md", CLAUDE_HOME / "CLAUDE.md"),
    ("settings.json", CLAUDE_HOME / "settings.json"),
    ("keybindings.json", CLAUDE_HOME / "keybindings.json"),
    ("plugins/known_marketplaces.json", CLAUDE_HOME / "plugins" / "known_marketplaces.json"),
]

if sys.platform == "darwin":
    DESKTOP_DIR = Path.home() / "Library" / "Application Support" / "Claude"
elif sys.platform == "win32":
    DESKTOP_DIR = Path.home() / "AppData" / "Roaming" / "Claude"
else:
    DESKTOP_DIR = Path.home() / ".config" / "Claude"

DESKTOP_FILES = [
    ("claude-desktop/claude_desktop_config.json", DESKTOP_DIR / "claude_desktop_config.json"),
    ("claude-desktop/config.json", DESKTOP_DIR / "config.json"),
]


def deploy(src: Path, dest: Path, dry_run: bool, stamp: str) -> None:
    if not src.is_file():
        print(f"missing  {src}")
        return
    if src.stat().st_size == 0:
        print(f"empty    {src.relative_to(REPO_ROOT)} (skipped)")
        return
    if dest.is_file() and filecmp.cmp(src, dest, shallow=False):
        print(f"same     {dest}")
        return

    action = "update" if dest.exists() else "create"
    print(f"{action:8} {dest}")
    if dry_run:
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        backup = dest.with_name(f"{dest.name}.bak.{stamp}")
        shutil.copy2(dest, backup)
        print(f"         backup -> {backup}")
    shutil.copy2(src, dest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-n", "--dry-run", action="store_true", help="show actions without writing")
    parser.add_argument("--desktop", action="store_true", help="also deploy Claude Desktop config files")
    args = parser.parse_args()

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    files = FILES + (DESKTOP_FILES if args.desktop else [])
    for rel, dest in files:
        deploy(SOURCE / rel, dest, args.dry_run, stamp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
