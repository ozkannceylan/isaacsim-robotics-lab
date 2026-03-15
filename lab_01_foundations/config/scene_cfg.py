"""Scene configuration dataclasses for Lab 01 foundations."""

from __future__ import annotations

from dataclasses import dataclass


Vec3 = tuple[float, float, float]
QuatWXYZ = tuple[float, float, float, float]


@dataclass(frozen=True)
class AssetReferenceCfg:
    """Reference to a USD asset that will be spawned into the scene."""

    usd_path: str
    prim_path: str
    translation: Vec3 = (0.0, 0.0, 0.0)
    orientation: QuatWXYZ = (1.0, 0.0, 0.0, 0.0)


@dataclass(frozen=True)
class RobotArmSceneCfg:
    """Configuration for the UR5e scene asset and motion profile."""

    usd_path: str
    prim_path: str
    base_position: Vec3
    base_orientation: QuatWXYZ
    joint_names: tuple[str, ...]
    joint_amplitudes_rad: tuple[float, ...]
    joint_phase_offsets_rad: tuple[float, ...]
    trajectory_frequency_hz: float


@dataclass(frozen=True)
class TableSceneCfg:
    """Configuration for the static support table."""

    prim_path: str
    position: Vec3
    size: Vec3
    color: tuple[float, float, float]


@dataclass(frozen=True)
class CameraSceneCfg:
    """Configuration for the RGB capture camera."""

    prim_path: str
    position: Vec3
    orientation: QuatWXYZ
    convention: str
    width: int
    height: int
    frame_count: int


@dataclass(frozen=True)
class FoundationsSceneCfg:
    """Top-level scene configuration for the Lab 01 capstone."""

    environment: AssetReferenceCfg
    robot: RobotArmSceneCfg
    table: TableSceneCfg
    camera: CameraSceneCfg
