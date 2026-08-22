#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve the notes target folder from an explicit path or an env var."
    )
    parser.add_argument(
        "--target-folder",
        help="Explicit notes folder. When set, it wins over the env var.",
    )
    parser.add_argument(
        "--env-var",
        default="NOTES_DIR",
        help="Environment variable to read when --target-folder is omitted.",
    )
    parser.add_argument(
        "--fallback-env-var",
        default="ZK_NOTEBOOK_DIR",
        help="Environment variable to read when the primary env var is unset.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    raw_value = (
        args.target_folder
        or os.environ.get(args.env_var)
        or os.environ.get(args.fallback_env_var)
    )
    if not raw_value:
        print(
            f"Missing target folder. Set --target-folder or export "
            f"{args.env_var} (or {args.fallback_env_var}).",
            file=sys.stderr,
        )
        return 1

    target = Path(raw_value).expanduser().resolve()
    if not target.exists():
        print(f"Target folder does not exist: {target}", file=sys.stderr)
        return 1
    if not target.is_dir():
        print(f"Target path is not a directory: {target}", file=sys.stderr)
        return 1

    print(str(target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
