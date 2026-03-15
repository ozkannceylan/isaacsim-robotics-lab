"""Mock runtime used to validate the Lab 01 artifact contract without Isaac Lab."""

from __future__ import annotations

from lab_01_foundations.config.sim_cfg import Lab01Config

from .control import compute_capture_steps, generate_joint_targets, generate_joint_velocities
from .models import CapturedFrame, JointStateRecord, LabRunResult


def run_mock_foundations(config: Lab01Config) -> LabRunResult:
    """Create deterministic Lab 01 artifacts without launching Isaac Sim."""
    joint_names = config.scene.robot.joint_names
    base_positions = (0.0,) * len(joint_names)
    capture_steps = set(compute_capture_steps(config.runtime.step_count, config.scene.camera.frame_count))

    joint_records: list[JointStateRecord] = []
    frames: list[CapturedFrame] = []
    frame_index = 0

    for step in range(config.runtime.step_count):
        sim_time_s = (step + 1) * config.runtime.physics_dt
        joint_targets = generate_joint_targets(
            base_positions,
            config.scene.robot.joint_amplitudes_rad,
            config.scene.robot.joint_phase_offsets_rad,
            config.scene.robot.trajectory_frequency_hz,
            sim_time_s,
        )
        joint_velocities = generate_joint_velocities(
            config.scene.robot.joint_amplitudes_rad,
            config.scene.robot.joint_phase_offsets_rad,
            config.scene.robot.trajectory_frequency_hz,
            sim_time_s,
        )
        joint_records.append(
            JointStateRecord(
                step=step,
                sim_time_s=round(sim_time_s, 6),
                joint_targets_rad=joint_targets,
                joint_positions_rad=joint_targets,
                joint_velocities_rad_s=joint_velocities,
            )
        )
        if step in capture_steps:
            frames.append(
                CapturedFrame(
                    frame_index=frame_index,
                    step=step,
                    width=config.scene.camera.width,
                    height=config.scene.camera.height,
                    rgb_bytes=_make_mock_frame(config.scene.camera.width, config.scene.camera.height, frame_index),
                )
            )
            frame_index += 1

    return LabRunResult(
        runtime_name="mock",
        joint_names=joint_names,
        joint_state_records=tuple(joint_records),
        captured_frames=tuple(frames),
        metadata={
            "mock_runtime": True,
            "robot_prim_path": config.scene.robot.prim_path,
            "camera_prim_path": config.scene.camera.prim_path,
        },
    )


def _make_mock_frame(width: int, height: int, frame_index: int) -> bytes:
    """Generate a deterministic RGB gradient frame."""
    buffer = bytearray(width * height * 3)
    cursor = 0
    width_scale = max(width - 1, 1)
    height_scale = max(height - 1, 1)
    for row in range(height):
        green = (row * 255) // height_scale
        for col in range(width):
            buffer[cursor] = (col * 255) // width_scale
            buffer[cursor + 1] = green
            buffer[cursor + 2] = (frame_index * 80) % 256
            cursor += 3
    return bytes(buffer)
