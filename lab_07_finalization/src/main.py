"""CLI entrypoint for Lab 07 finalization."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config_loader import load_config
from .finalization_setup import initialize_finalization
from .logging_utils import write_audit_csv, write_summary
from .release_report import build_release_report
from .repo_audit import run_repo_audit
from lab_06_operations.src.config_loader import load_config as load_lab_06_config
from lab_06_operations.src.operations_pipeline import run_operations_pipeline
from lab_06_operations.src.operations_setup import initialize_operations


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run Lab 7 finalization scaffold')
    parser.add_argument('--config', default='lab_07_finalization/configs/default.json')
    parser.add_argument('--output', default='lab_07_finalization/data/run_summary.json')
    parser.add_argument('--audit-output', default='lab_07_finalization/data/repo_audit.csv')
    parser.add_argument('--save-audit', action='store_true')
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    config = load_config(args.config)
    context = initialize_finalization(config, Path.cwd())
    lab_06_config = load_lab_06_config(context.lab_06_config_path)
    lab_06_context = initialize_operations(lab_06_config, Path.cwd())
    operations_summary = run_operations_pipeline(lab_06_context, project_root=Path.cwd())
    audit_summary = run_repo_audit(context, project_root=Path.cwd())
    summary = build_release_report(context, operations_summary, audit_summary)
    write_summary(summary, args.output)
    if args.save_audit:
        write_audit_csv(summary, args.audit_output)
    print(f'Lab7 run complete. Summary: {args.output}')
    if args.save_audit:
        print(f'Audit written to: {args.audit_output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
