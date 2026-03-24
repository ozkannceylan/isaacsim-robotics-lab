"""CLI entrypoint for Lab 06 operations."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config_loader import load_config
from .logging_utils import write_checklist_csv, write_summary
from .operations_pipeline import run_operations_pipeline
from .operations_setup import initialize_operations


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run Lab 6 operations scaffold')
    parser.add_argument('--config', default='lab_06_operations/configs/default.json')
    parser.add_argument('--output', default='lab_06_operations/data/run_summary.json')
    parser.add_argument('--checklist-output', default='lab_06_operations/data/deployment_checklist.csv')
    parser.add_argument('--save-checklist', action='store_true')
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    config = load_config(args.config)
    context = initialize_operations(config, Path.cwd())
    summary = run_operations_pipeline(context, project_root=Path.cwd())
    write_summary(summary, args.output)
    if args.save_checklist:
        write_checklist_csv(summary, args.checklist_output)
    print(f'Lab6 run complete. Summary: {args.output}')
    if args.save_checklist:
        print(f'Checklist written to: {args.checklist_output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
