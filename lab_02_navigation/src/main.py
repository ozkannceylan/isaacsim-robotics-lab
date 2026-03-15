"""CLI entrypoint for Lab 2 navigation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config_loader import load_config
from .logging_utils import write_path_csv, write_summary
from .navigation_setup import initialize_navigation
from .planner import run_planner


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Lab 2 navigation scaffold")
    parser.add_argument("--config", default="lab_02_navigation/configs/default.json")
    parser.add_argument("--output", default="lab_02_navigation/data/run_summary.json")
    parser.add_argument("--path-output", default="lab_02_navigation/data/path.csv")
    parser.add_argument("--save-path", action="store_true")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    config = load_config(args.config)
    context = initialize_navigation(config, Path.cwd())
    summary = run_planner(context, collect_path=args.save_path)
    write_summary(summary, args.output)
    if args.save_path:
        write_path_csv(summary, args.path_output)
    print(f"Lab2 run complete. Summary: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
