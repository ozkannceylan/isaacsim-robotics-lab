"""Lab 01 foundations runtime entrypoint."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config_loader import load_config
from .logging_utils import write_run_summary, write_trajectory_csv
from .simulation_setup import initialize_simulation
from .task_loop import run_task_loop


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Lab 01 foundations scaffold")
    parser.add_argument(
        "--config",
        default="lab_01_foundations/configs/default.json",
        help="Path to runtime config (.json or .yaml/.yml)",
    )
    parser.add_argument(
        "--output",
        default="lab_01_foundations/data/run_summary.json",
        help="Path for summary JSON output",
    )
    parser.add_argument(
        "--trajectory-output",
        default="lab_01_foundations/data/trajectory.csv",
        help="Path for trajectory CSV output",
    )
    parser.add_argument(
        "--save-trajectory",
        action="store_true",
        help="If set, save per-step trajectory actions to CSV",
    )
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    root = Path.cwd()

    config = load_config(args.config)
    sim_context = initialize_simulation(config, project_root=root)
    summary = run_task_loop(sim_context, collect_trajectory=args.save_trajectory)
    write_run_summary(summary, args.output)
    if args.save_trajectory:
        write_trajectory_csv(summary, args.trajectory_output)

    print(f"Run complete. Summary written to: {args.output}")
    if args.save_trajectory:
        print(f"Trajectory written to: {args.trajectory_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
