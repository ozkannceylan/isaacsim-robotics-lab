"""Configuration loading and validation for Lab 01 foundations."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any, Sequence

from lab_01_foundations.config.scene_cfg import (
    AssetReferenceCfg,
    CameraSceneCfg,
    FoundationsSceneCfg,
    RobotArmSceneCfg,
    TableSceneCfg,
)
from lab_01_foundations.config.sim_cfg import Lab01Config, OutputCfg, RuntimeCfg


class ConfigError(ValueError):
    """Raised when a Lab 01 config is missing required fields or uses invalid values."""


def load_config(config_path: str | Path) -> Lab01Config:
    """Load a JSON or YAML configuration file."""
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
    elif suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ConfigError("PyYAML is required to load YAML configs.") from exc
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        raise ConfigError("Config must use .json, .yaml, or .yml extension")

    if not isinstance(payload, dict):
        raise ConfigError("Config payload must be a mapping at the top level")
    return validate_config(payload)


def validate_config(payload: dict[str, Any]) -> Lab01Config:
    """Validate the Lab 01 config payload and return typed config objects."""
    runtime_data = _require_mapping(payload, "runtime")
    output_data = _require_mapping(payload, "output")
    scene_data = _require_mapping(payload, "scene")

    runtime = RuntimeCfg(
        headless=bool(runtime_data.get("headless", True)),
        device=str(runtime_data.get("device", "cuda:0")),
        physics_dt=float(runtime_data.get("physics_dt", 1.0 / 60.0)),
        render_interval=int(runtime_data.get("render_interval", 1)),
        step_count=int(runtime_data.get("step_count", 300)),
        seed=int(runtime_data.get("seed", 0)),
    )
    output = OutputCfg(
        root_dir=str(output_data.get("root_dir", "lab_01_foundations/data/runs/local")),
        summary_filename=str(output_data.get("summary_filename", "run_summary.json")),
        joint_state_filename=str(output_data.get("joint_state_filename", "joint_states.csv")),
        frames_dirname=str(output_data.get("frames_dirname", "frames")),
    )

    environment_data = _require_mapping(scene_data, "environment")
    robot_data = _require_mapping(scene_data, "robot")
    table_data = _require_mapping(scene_data, "table")
    camera_data = _require_mapping(scene_data, "camera")

    scene = FoundationsSceneCfg(
        environment=AssetReferenceCfg(
            usd_path=str(environment_data["usd_path"]),
            prim_path=str(environment_data["prim_path"]),
            translation=_as_float_tuple(environment_data.get("translation", (0.0, 0.0, 0.0)), 3, "scene.environment.translation"),
            orientation=_as_float_tuple(environment_data.get("orientation", (1.0, 0.0, 0.0, 0.0)), 4, "scene.environment.orientation"),
        ),
        robot=RobotArmSceneCfg(
            usd_path=str(robot_data["usd_path"]),
            prim_path=str(robot_data["prim_path"]),
            base_position=_as_float_tuple(robot_data["base_position"], 3, "scene.robot.base_position"),
            base_orientation=_as_float_tuple(robot_data["base_orientation"], 4, "scene.robot.base_orientation"),
            joint_names=_as_str_tuple(robot_data["joint_names"], "scene.robot.joint_names"),
            joint_amplitudes_rad=_as_float_tuple(
                robot_data["joint_amplitudes_rad"], 6, "scene.robot.joint_amplitudes_rad"
            ),
            joint_phase_offsets_rad=_as_float_tuple(
                robot_data["joint_phase_offsets_rad"], 6, "scene.robot.joint_phase_offsets_rad"
            ),
            trajectory_frequency_hz=float(robot_data.get("trajectory_frequency_hz", 0.25)),
        ),
        table=TableSceneCfg(
            prim_path=str(table_data["prim_path"]),
            position=_as_float_tuple(table_data["position"], 3, "scene.table.position"),
            size=_as_float_tuple(table_data["size"], 3, "scene.table.size"),
            color=_as_float_tuple(table_data["color"], 3, "scene.table.color"),
        ),
        camera=CameraSceneCfg(
            prim_path=str(camera_data["prim_path"]),
            position=_as_float_tuple(camera_data["position"], 3, "scene.camera.position"),
            orientation=_as_float_tuple(camera_data["orientation"], 4, "scene.camera.orientation"),
            convention=str(camera_data.get("convention", "world")),
            width=int(camera_data.get("width", 640)),
            height=int(camera_data.get("height", 480)),
            frame_count=int(camera_data.get("frame_count", 30)),
        ),
    )

    _validate_lab01_config(runtime, scene)
    return Lab01Config(runtime=runtime, output=output, scene=scene)


def apply_output_dir(config: Lab01Config, output_dir: str | Path) -> Lab01Config:
    """Return a config copy with a different output root directory."""
    return replace(config, output=replace(config.output, root_dir=str(output_dir)))


def _validate_lab01_config(runtime: RuntimeCfg, scene: FoundationsSceneCfg) -> None:
    if not runtime.headless:
        raise ConfigError("Lab 01 must run with headless=True on the local RTX 4050 profile")
    if runtime.physics_dt <= 0.0:
        raise ConfigError("runtime.physics_dt must be > 0")
    if runtime.render_interval <= 0:
        raise ConfigError("runtime.render_interval must be > 0")
    if runtime.step_count <= 0:
        raise ConfigError("runtime.step_count must be > 0")
    if scene.camera.width <= 0 or scene.camera.height <= 0:
        raise ConfigError("scene.camera.width and scene.camera.height must be > 0")
    if scene.camera.frame_count <= 0:
        raise ConfigError("scene.camera.frame_count must be > 0")
    if scene.camera.frame_count > runtime.step_count:
        raise ConfigError("scene.camera.frame_count cannot exceed runtime.step_count")
    if len(scene.robot.joint_names) != 6:
        raise ConfigError("scene.robot.joint_names must contain the six UR5e arm joints")
    if len(scene.robot.joint_amplitudes_rad) != len(scene.robot.joint_names):
        raise ConfigError("scene.robot.joint_amplitudes_rad must align with scene.robot.joint_names")
    if len(scene.robot.joint_phase_offsets_rad) != len(scene.robot.joint_names):
        raise ConfigError("scene.robot.joint_phase_offsets_rad must align with scene.robot.joint_names")
    if scene.robot.trajectory_frequency_hz <= 0.0:
        raise ConfigError("scene.robot.trajectory_frequency_hz must be > 0")


def _require_mapping(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ConfigError(f"Missing required mapping: {key}")
    return value


def _as_float_tuple(raw: Sequence[Any], expected_len: int, field_name: str) -> tuple[float, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)) or len(raw) != expected_len:
        raise ConfigError(f"{field_name} must be a sequence with length {expected_len}")
    return tuple(float(value) for value in raw)


def _as_str_tuple(raw: Sequence[Any], field_name: str) -> tuple[str, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ConfigError(f"{field_name} must be a sequence of strings")
    return tuple(str(value) for value in raw)
