"""CLI entrypoint for Lab 3 perception."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config_loader import load_config
from .feature_extractor import extract_features
from .logging_utils import write_frame_features_csv, write_summary
from .perception_setup import initialize_perception
from .sensor_sim import generate_sensor_frames


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Lab 3 perception scaffold")
    parser.add_argument("--config", default="lab_03_perception/configs/default.json")
    parser.add_argument("--output", default="lab_03_perception/data/run_summary.json")
    parser.add_argument("--features-output", default="lab_03_perception/data/frame_features.csv")
    parser.add_argument("--save-features", action="store_true")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    config = load_config(args.config)
    context = initialize_perception(config, Path.cwd())
    samples = generate_sensor_frames(context)
    summary = extract_features(samples)
    write_summary(summary, args.output)
    if args.save_features:
        write_frame_features_csv(summary, args.features_output)
    print(f"Lab3 run complete. Summary: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
