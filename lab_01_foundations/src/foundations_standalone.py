"""Standalone entrypoint for the Lab 01 Isaac Sim foundations capstone."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .artifact_writers import write_run_artifacts
from .config_loader import ConfigError, apply_output_dir, load_config
from .isaaclab_runtime import RuntimeUnavailableError, run_isaaclab_foundations
from .mock_runtime import run_mock_foundations


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Lab 01 foundations script in real or mock mode."""
    cli_args = list(argv) if argv is not None else sys.argv[1:]
    mock_runtime = _detect_mock_runtime(cli_args)
    parser = _build_parser(include_app_launcher=not mock_runtime)
    args = parser.parse_args(cli_args)

    config = load_config(args.config)
    if args.output_dir is not None:
        config = apply_output_dir(config, args.output_dir)

    if mock_runtime:
        result = run_mock_foundations(config)
    else:
        if not args.headless:
            raise ConfigError("Lab 01 must be run with --headless")
        if not args.enable_cameras:
            raise ConfigError("Lab 01 requires --enable_cameras to save PNG frames")
        from isaaclab.app import AppLauncher

        app_launcher = AppLauncher(args)
        simulation_app = app_launcher.app
        try:
            result = run_isaaclab_foundations(config, getattr(args, "device", config.runtime.device))
        finally:
            simulation_app.close()

    artifact_paths = write_run_artifacts(config, result)
    print(f"Lab 01 completed with runtime: {result.runtime_name}")
    print(f"Summary: {artifact_paths.summary_path}")
    print(f"Joint states: {artifact_paths.joint_state_csv_path}")
    print(f"Frames written: {len(artifact_paths.frame_paths)}")
    return 0


def _detect_mock_runtime(argv: Sequence[str] | None) -> bool:
    preview_parser = argparse.ArgumentParser(add_help=False)
    preview_parser.add_argument("--mock-runtime", action="store_true")
    preview_args, _ = preview_parser.parse_known_args([] if argv is None else argv)
    return bool(preview_args.mock_runtime)


def _build_parser(include_app_launcher: bool) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lab 01 Isaac Sim foundations capstone runner")
    parser.add_argument("--config", default="lab_01_foundations/configs/local.yaml", help="Path to a JSON or YAML config")
    parser.add_argument("--output-dir", default=None, help="Override the configured output directory")
    parser.add_argument("--mock-runtime", action="store_true", help="Run the deterministic mock backend")
    if include_app_launcher:
        from isaaclab.app import AppLauncher

        AppLauncher.add_app_launcher_args(parser)
    return parser


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ConfigError, RuntimeUnavailableError) as exc:
        print(f"Lab 01 failed: {exc}")
        raise SystemExit(1) from exc
