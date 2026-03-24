"""CLI entrypoint for Lab 5 integration."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config_loader import load_config
from .integration_pipeline import run_integration_pipeline
from .integration_setup import initialize_integration
from .logging_utils import write_scoreboard_csv, write_summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run Lab 5 integration scaffold')
    parser.add_argument('--config', default='lab_05_integration/configs/default.json')
    parser.add_argument('--output', default='lab_05_integration/data/run_summary.json')
    parser.add_argument('--scoreboard-output', default='lab_05_integration/data/subsystem_scoreboard.csv')
    parser.add_argument('--save-scoreboard', action='store_true')
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    config = load_config(args.config)
    context = initialize_integration(config, Path.cwd())
    summary = run_integration_pipeline(context, project_root=Path.cwd())
    write_summary(summary, args.output)
    if args.save_scoreboard:
        write_scoreboard_csv(summary, args.scoreboard_output)
    print(f'Lab5 run complete. Summary: {args.output}')
    if args.save_scoreboard:
        print(f'Scoreboard written to: {args.scoreboard_output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
