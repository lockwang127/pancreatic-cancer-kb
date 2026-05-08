#!/usr/bin/env python3
"""Sync pancreatic cancer knowledge base to GitHub repository."""

import os
import subprocess
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_cmd(cmd, check=True):
    """Run a shell command."""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=REPO_DIR, capture_output=True, text=True)
    if result.stdout:
        print(f"  {result.stdout.strip()}")
    if result.stderr:
        print(f"  [stderr] {result.stderr.strip()}")
    if check and result.returncode != 0:
        print(f"Error: command failed with exit code {result.returncode}")
        sys.exit(1)
    return result


def sync():
    """Sync to GitHub."""
    print("=" * 60)
    print("Pancreatic Cancer KB - GitHub Sync")
    print("=" * 60)

    print("\n[CHECK] Git status...")
    run_cmd("git status --short")

    print("\n[CHECK] Remote origin...")
    result = run_cmd("git remote get-url origin", check=False)
    if result.returncode != 0:
        print("\n[INFO] No remote origin set. To connect to GitHub:")
        print("  1. Create repository at https://github.com/new")
        print("  2. Run: git remote add origin git@github.com:lockwang127/pancreatic-cancer-kb.git")
        print("  3. Run: git push -u origin main")
        return

    print(f"  Remote: {result.stdout.strip()}")

    print("\n[BUILD] Building knowledge base...")
    build_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_kb.py")
    run_cmd(f"python3 {build_script}")

    print("\n[ADD] Staging changes...")
    run_cmd("git add -A")

    result = run_cmd("git status --porcelain", check=False)
    if not result.stdout.strip():
        print("\n[INFO] No changes to commit. Repository is up to date.")
        return

    timestamp = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
    run_cmd(f'git commit -m "Update knowledge base - {timestamp}"')

    print("\n[PUSH] Pushing to GitHub...")
    run_cmd("git push origin main")

    print("\n[DONE] Sync complete!")


if __name__ == "__main__":
    sync()
