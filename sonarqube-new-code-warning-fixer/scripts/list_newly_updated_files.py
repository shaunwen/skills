#!/usr/bin/env python3
"""
List newly updated files for SonarQube new-code workflows.

Modes:
- auto: use uncommitted changes when any exist, otherwise branch diff
- uncommitted: staged + unstaged + untracked files
- branch: git diff against an inferred or explicit base branch
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

CODE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".m",
    ".mm",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".sql",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
    ".xml",
    ".yml",
    ".yaml",
}

SPECIAL_CODE_FILENAMES = {
    "Dockerfile",
    "Makefile",
    "Jenkinsfile",
}

TEST_DIR_MARKERS = ("test", "tests", "__tests__", "__test__")
TEST_NAME_REGEX = re.compile(
    r"(^test_.*)|"
    r"(.*[._-](test|spec)\.[^.]+$)|"
    r"(.*[._-](e2e-spec|int-spec)\.[^.]+$)|"
    r"(.*Test\.[^.]+$)"
)


def run_git(args: list[str], allow_fail: bool = False) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        if allow_fail:
            return ""
        msg = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {msg}")
    return result.stdout.strip()


def unique_sorted(items: Iterable[str]) -> list[str]:
    return sorted({item.strip() for item in items if item.strip()})


def has_uncommitted_changes() -> bool:
    return bool(run_git(["status", "--porcelain"], allow_fail=False))


def ref_exists(ref: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", ref],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def choose_base_branch(explicit_base: str | None) -> tuple[str | None, str | None]:
    if explicit_base:
        if ref_exists(f"refs/heads/{explicit_base}"):
            return explicit_base, f"refs/heads/{explicit_base}"
        if ref_exists(f"refs/remotes/origin/{explicit_base}"):
            return explicit_base, f"refs/remotes/origin/{explicit_base}"
        return None, None

    for name in ("develop", "master", "main"):
        if ref_exists(f"refs/heads/{name}"):
            return name, f"refs/heads/{name}"
    for name in ("develop", "master", "main"):
        if ref_exists(f"refs/remotes/origin/{name}"):
            return name, f"refs/remotes/origin/{name}"
    return None, None


def changed_files_uncommitted() -> list[str]:
    unstaged = run_git(["diff", "--name-only"], allow_fail=False).splitlines()
    staged = run_git(["diff", "--cached", "--name-only"], allow_fail=False).splitlines()
    untracked = run_git(["ls-files", "--others", "--exclude-standard"], allow_fail=False).splitlines()
    return unique_sorted([*unstaged, *staged, *untracked])


def changed_files_branch(base_ref: str) -> list[str]:
    return unique_sorted(run_git(["diff", "--name-only", f"{base_ref}...HEAD"], allow_fail=False).splitlines())


def is_code_file(path: str) -> bool:
    basename = os.path.basename(path)
    if basename in SPECIAL_CODE_FILENAMES:
        return True
    suffix = Path(path).suffix.lower()
    return suffix in CODE_EXTENSIONS


def is_test_file(path: str) -> bool:
    normalized = path.replace("\\", "/")
    basename = os.path.basename(normalized)
    parts = [part.lower() for part in normalized.split("/") if part]
    if any(marker in parts for marker in TEST_DIR_MARKERS):
        return True
    return bool(TEST_NAME_REGEX.match(basename))


def as_sonar_components(project_key: str, paths: list[str]) -> list[str]:
    return [f"{project_key}:{path}" for path in paths]


def main() -> int:
    parser = argparse.ArgumentParser(description="List newly updated files for SonarQube new-code scans.")
    parser.add_argument(
        "--mode",
        choices=("auto", "uncommitted", "branch"),
        default="auto",
        help="Change scope mode (default: auto).",
    )
    parser.add_argument(
        "--base",
        help="Base branch for branch mode. Defaults to develop/master/main resolution.",
    )
    parser.add_argument(
        "--only",
        choices=("code", "all"),
        default="code",
        help="Return only code files or all changed files (default: code).",
    )
    parser.add_argument(
        "--project-key",
        help="Optional SonarQube project key to emit sonar component keys.",
    )
    args = parser.parse_args()

    try:
        repo_root = run_git(["rev-parse", "--show-toplevel"], allow_fail=False)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    mode_used = args.mode
    base_branch = None

    try:
        if args.mode == "auto":
            if has_uncommitted_changes():
                mode_used = "uncommitted"
                all_changed = changed_files_uncommitted()
            else:
                resolved_name, resolved_ref = choose_base_branch(args.base)
                if not resolved_name or not resolved_ref:
                    print(
                        "No base branch found. Provide --base or create one of develop/master/main.",
                        file=sys.stderr,
                    )
                    return 1
                base_branch = resolved_name
                mode_used = "branch"
                all_changed = changed_files_branch(resolved_ref)
        elif args.mode == "uncommitted":
            all_changed = changed_files_uncommitted()
        else:
            resolved_name, resolved_ref = choose_base_branch(args.base)
            if not resolved_name or not resolved_ref:
                print(
                    f"Base branch '{args.base or ''}' not found locally or at origin.",
                    file=sys.stderr,
                )
                return 1
            base_branch = resolved_name
            all_changed = changed_files_branch(resolved_ref)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    selected = all_changed if args.only == "all" else [f for f in all_changed if is_code_file(f)]
    prod_files = [f for f in selected if not is_test_file(f)]
    test_files = [f for f in selected if is_test_file(f)]

    payload: dict[str, object] = {
        "repo_root": repo_root,
        "mode_requested": args.mode,
        "mode_used": mode_used,
        "base_branch": base_branch,
        "changed_files": all_changed,
        "selected_files": selected,
        "prod_files": prod_files,
        "test_files": test_files,
    }

    if args.project_key:
        payload["sonar_components"] = {
            "prod": as_sonar_components(args.project_key, prod_files),
            "test": as_sonar_components(args.project_key, test_files),
        }

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
