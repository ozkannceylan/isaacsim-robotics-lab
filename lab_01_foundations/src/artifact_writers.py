"""Artifact writers for Lab 01 foundations outputs."""

from __future__ import annotations

import csv
import json
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path

from lab_01_foundations.config.sim_cfg import Lab01Config

from .models import CapturedFrame, LabRunResult


@dataclass(frozen=True)
class ArtifactPaths:
    """Resolved artifact paths for a Lab 01 run."""

    output_dir: Path
    summary_path: Path
    joint_state_csv_path: Path
    frame_paths: tuple[Path, ...]


def write_run_artifacts(config: Lab01Config, result: LabRunResult) -> ArtifactPaths:
    """Write run summary, joint-state CSV, and PNG frames to disk."""
    output_dir = Path(config.output.root_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / config.output.summary_filename
    joint_state_csv_path = output_dir / config.output.joint_state_filename
    frame_dir = output_dir / config.output.frames_dirname
    frame_dir.mkdir(parents=True, exist_ok=True)

    frame_paths = write_frame_sequence(result.captured_frames, frame_dir)
    write_joint_state_csv(result, joint_state_csv_path)
    summary_path.write_text(
        json.dumps(build_summary_payload(config, result, joint_state_csv_path, frame_paths), indent=2),
        encoding="utf-8",
    )
    return ArtifactPaths(
        output_dir=output_dir,
        summary_path=summary_path,
        joint_state_csv_path=joint_state_csv_path,
        frame_paths=frame_paths,
    )


def write_joint_state_csv(result: LabRunResult, csv_path: Path) -> None:
    """Write per-step joint targets, positions, and velocities to CSV."""
    headers = ["step", "sim_time_s"]
    headers.extend(f"target_{name}" for name in result.joint_names)
    headers.extend(f"position_{name}" for name in result.joint_names)
    headers.extend(f"velocity_{name}" for name in result.joint_names)

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for record in result.joint_state_records:
            row = {"step": record.step, "sim_time_s": record.sim_time_s}
            row.update(
                {f"target_{name}": value for name, value in zip(result.joint_names, record.joint_targets_rad, strict=True)}
            )
            row.update(
                {
                    f"position_{name}": value
                    for name, value in zip(result.joint_names, record.joint_positions_rad, strict=True)
                }
            )
            row.update(
                {
                    f"velocity_{name}": value
                    for name, value in zip(result.joint_names, record.joint_velocities_rad_s, strict=True)
                }
            )
            writer.writerow(row)


def write_frame_sequence(frames: tuple[CapturedFrame, ...], frame_dir: Path) -> tuple[Path, ...]:
    """Write RGB frame captures as PNG files."""
    written_paths: list[Path] = []
    for frame in frames:
        frame_path = frame_dir / f"frame_{frame.frame_index:03d}.png"
        write_png_rgb(frame_path, frame.width, frame.height, frame.rgb_bytes)
        written_paths.append(frame_path)
    return tuple(written_paths)


def build_summary_payload(
    config: Lab01Config,
    result: LabRunResult,
    joint_state_csv_path: Path,
    frame_paths: tuple[Path, ...],
) -> dict[str, object]:
    """Create a JSON-serializable summary payload."""
    return {
        "status": "success",
        "runtime_name": result.runtime_name,
        "step_count": len(result.joint_state_records),
        "captured_frame_count": len(frame_paths),
        "physics_dt": config.runtime.physics_dt,
        "simulated_time_s": round(config.runtime.physics_dt * len(result.joint_state_records), 6),
        "joint_state_csv": str(joint_state_csv_path),
        "frames_dir": str(frame_paths[0].parent) if frame_paths else "",
        "robot_usd_path": config.scene.robot.usd_path,
        "environment_usd_path": config.scene.environment.usd_path,
        "headless": config.runtime.headless,
        "cartpole_verification_command": (
            "isaaclab -p scripts/reinforcement_learning/skrl/train.py "
            "--task Isaac-Cartpole-Direct-v0 --headless --num_envs 64 --max_iterations 100"
        ),
        "metadata": dict(result.metadata),
    }


def write_png_rgb(path: Path, width: int, height: int, rgb_bytes: bytes) -> None:
    """Write packed RGB bytes as an 8-bit PNG file using only the standard library."""
    expected_size = width * height * 3
    if len(rgb_bytes) != expected_size:
        raise ValueError(f"RGB byte payload has size {len(rgb_bytes)}, expected {expected_size}")

    row_size = width * 3
    raw_rows = bytearray()
    for row in range(height):
        start = row * row_size
        raw_rows.extend(b"\x00")
        raw_rows.extend(rgb_bytes[start : start + row_size])

    png_bytes = bytearray(b"\x89PNG\r\n\x1a\n")
    png_bytes.extend(_png_chunk(b"IHDR", struct.pack("!2I5B", width, height, 8, 2, 0, 0, 0)))
    png_bytes.extend(_png_chunk(b"IDAT", zlib.compress(bytes(raw_rows), level=9)))
    png_bytes.extend(_png_chunk(b"IEND", b""))
    path.write_bytes(bytes(png_bytes))


def _png_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    """Encode a PNG chunk."""
    checksum = zlib.crc32(chunk_type)
    checksum = zlib.crc32(payload, checksum)
    return struct.pack("!I", len(payload)) + chunk_type + payload + struct.pack("!I", checksum & 0xFFFFFFFF)
