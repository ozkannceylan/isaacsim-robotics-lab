"""Record a demo video of a CartPole scene in Isaac Sim.

Creates a single CartPole environment, applies sinusoidal control inputs,
and saves the rendered frames as an MP4 video.

Usage:
    cd /workspace/isaacsim-robotics-lab
    bash /opt/IsaacLab/isaaclab.sh -p labs/lab_0/scripts/record_demo.py --headless --enable_cameras
"""

from __future__ import annotations

import argparse
import os

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Record a CartPole demo video.")
parser.add_argument("--num_steps", type=int, default=300, help="Number of simulation steps to record.")
parser.add_argument("--output", type=str, default="labs/lab_0/media/demo.mp4", help="Output video path.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
args_cli.enable_cameras = True
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# Post-launch imports (Isaac Sim must be initialized first)
import gymnasium as gym
import numpy as np
import torch
import imageio

import isaaclab_tasks  # noqa: F401 — registers Isaac Lab gym tasks
from isaaclab_tasks.utils import parse_env_cfg


def main() -> None:
    """Run CartPole with sinusoidal control and save video."""
    env_cfg = parse_env_cfg("Isaac-Cartpole-v0", device="cuda:0", num_envs=1)
    env = gym.make("Isaac-Cartpole-v0", cfg=env_cfg, render_mode="rgb_array")

    frames: list[np.ndarray] = []
    obs, info = env.reset()

    for step in range(args_cli.num_steps):
        # Sinusoidal control for visually interesting pole swinging
        t = step * 0.05
        action = torch.tensor([[np.sin(t) * 0.5]], device="cuda:0")
        obs, reward, terminated, truncated, info = env.step(action)

        frame = env.render()
        if frame is not None:
            frames.append(frame)

        # Reset if episode ends
        if terminated.any() or truncated.any():
            obs, info = env.reset()

    # Determine FPS from simulation timestep
    try:
        fps = max(1, int(1.0 / env.unwrapped.step_dt))
    except AttributeError:
        fps = 30

    env.close()

    # Write video
    if frames:
        output_path = os.path.abspath(args_cli.output)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        writer = imageio.get_writer(output_path, fps=fps)
        for f in frames:
            writer.append_data(f)
        writer.close()
        print(f"[INFO] Saved {len(frames)} frames to {output_path} @ {fps} FPS")
    else:
        print("[ERROR] No frames captured!")


if __name__ == "__main__":
    main()
    simulation_app.close()
