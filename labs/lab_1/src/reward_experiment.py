# Copyright (c) 2024. Reward shaping experiment for Ant locomotion.
# Modifies reward weights and trains with RL-Games to compare against baseline.

"""Script to run Ant reward shaping experiments with RL-Games."""

"""Launch Isaac Sim Simulator first."""

import argparse
import sys

from isaaclab.app import AppLauncher

# -- CLI arguments --
parser = argparse.ArgumentParser(description="Ant reward shaping experiment.")
parser.add_argument("--experiment", type=str, required=True,
                    choices=["high_energy", "no_alive", "high_velocity"],
                    help="Name of the experiment to run.")
parser.add_argument("--num_envs", type=int, default=2048, help="Number of environments.")
parser.add_argument("--max_iterations", type=int, default=500, help="Training iterations.")
parser.add_argument("--seed", type=int, default=42, help="Random seed.")

# AppLauncher args (--headless handled via HEADLESS env var)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# Launch sim
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows after sim is launched."""

import gymnasium as gym
import math
import os
import time
from datetime import datetime

from rl_games.common import env_configurations, vecenv
from rl_games.common.algo_observer import IsaacAlgoObserver
from rl_games.torch_runner import Runner

from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.utils.dict import print_dict
from isaaclab.utils.io import dump_yaml

from isaaclab_rl.rl_games import RlGamesGpuEnv, RlGamesVecEnvWrapper

import isaaclab_tasks  # noqa: F401 -- registers all tasks
from isaaclab_tasks.utils.parse_cfg import load_cfg_from_registry


# Experiment definitions: maps experiment name -> reward weight overrides
EXPERIMENTS = {
    "high_energy": {
        "description": "Double energy penalties (action_l2: -0.005->-0.01, energy: -0.05->-0.1)",
        "overrides": {
            "action_l2": -0.01,
            "energy": -0.1,
        },
    },
    "no_alive": {
        "description": "Remove alive bonus (alive: 0.5->0.0)",
        "overrides": {
            "alive": 0.0,
        },
    },
    "high_velocity": {
        "description": "Double forward progress weight (progress: 1.0->2.0)",
        "overrides": {
            "progress": 2.0,
        },
    },
}


def apply_reward_overrides(env_cfg, overrides):
    """Modify reward term weights on the env config in-place.

    Args:
        env_cfg: The environment configuration object.
        overrides: Dict mapping reward term name -> new weight value.
    """
    rewards_cfg = env_cfg.rewards
    for term_name, new_weight in overrides.items():
        if not hasattr(rewards_cfg, term_name):
            available = [a for a in dir(rewards_cfg) if not a.startswith("_")]
            raise ValueError(
                "Reward term '{}' not found in config. Available: {}".format(term_name, available)
            )
        reward_term = getattr(rewards_cfg, term_name)
        old_weight = reward_term.weight
        reward_term.weight = new_weight
        print("  [OVERRIDE] {}: {} -> {}".format(term_name, old_weight, new_weight))


def main():
    """Run a single Ant reward experiment."""
    experiment_name = args_cli.experiment
    exp_info = EXPERIMENTS[experiment_name]

    print("=" * 70)
    print("EXPERIMENT: {}".format(experiment_name))
    print("DESCRIPTION: {}".format(exp_info["description"]))
    print("=" * 70)

    # 1. Load env config from registry
    task_name = "Isaac-Ant-v0"
    env_cfg = load_cfg_from_registry(task_name, "env_cfg_entry_point")
    agent_cfg = load_cfg_from_registry(task_name, "rl_games_cfg_entry_point")

    # 2. Override scene / sim settings
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = "cuda:0"
    env_cfg.seed = args_cli.seed

    # 3. Apply reward weight overrides
    print("\nApplying reward overrides:")
    apply_reward_overrides(env_cfg, exp_info["overrides"])

    # Print final reward weights for verification
    print("\nFinal reward weights:")
    for attr_name in dir(env_cfg.rewards):
        if attr_name.startswith("_"):
            continue
        term = getattr(env_cfg.rewards, attr_name)
        if hasattr(term, "weight"):
            print("  {}: weight={}".format(attr_name, term.weight))

    # 4. Configure agent
    agent_cfg["params"]["seed"] = args_cli.seed
    agent_cfg["params"]["config"]["max_epochs"] = args_cli.max_iterations
    agent_cfg["params"]["config"]["device"] = "cuda:0"
    agent_cfg["params"]["config"]["device_name"] = "cuda:0"

    # Logging directory
    log_root_path = os.path.join(
        "/workspace/isaacsim-robotics-lab/logs/rl_games", "ant_reward_experiments"
    )
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = experiment_name + "_" + timestamp

    agent_cfg["params"]["config"]["train_dir"] = log_root_path
    agent_cfg["params"]["config"]["full_experiment_name"] = log_dir
    agent_cfg["params"]["config"]["name"] = "ant_" + experiment_name

    full_log_path = os.path.join(log_root_path, log_dir)
    print("\n[INFO] Logging to: {}".format(full_log_path))

    # Dump configs
    dump_yaml(os.path.join(full_log_path, "params", "env.yaml"), env_cfg)
    dump_yaml(os.path.join(full_log_path, "params", "agent.yaml"), agent_cfg)

    # 5. Create environment
    rl_device = agent_cfg["params"]["config"]["device"]
    clip_obs = agent_cfg["params"]["env"].get("clip_observations", math.inf)
    clip_actions = agent_cfg["params"]["env"].get("clip_actions", math.inf)

    env = gym.make(task_name, cfg=env_cfg)

    # Wrap for rl-games
    env = RlGamesVecEnvWrapper(env, rl_device, clip_obs, clip_actions)

    # Register environment
    vecenv.register(
        "IsaacRlgWrapper",
        lambda config_name, num_actors, **kwargs: RlGamesGpuEnv(config_name, num_actors, **kwargs),
    )
    env_configurations.register(
        "rlgpu", {"vecenv_type": "IsaacRlgWrapper", "env_creator": lambda **kwargs: env}
    )

    # Set num_actors
    agent_cfg["params"]["config"]["num_actors"] = env.unwrapped.num_envs

    # 6. Train
    runner = Runner(IsaacAlgoObserver())
    runner.load(agent_cfg)
    runner.reset()

    wall_start = time.time()
    runner.run({"train": True, "play": False, "sigma": None})
    wall_elapsed = time.time() - wall_start

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE: {}".format(experiment_name))
    print("Wall clock time: {:.1f}s ({:.1f}min)".format(wall_elapsed, wall_elapsed / 60.0))
    print("Log directory: {}".format(full_log_path))
    print("=" * 70)

    env.close()


if __name__ == "__main__":
    main()
    simulation_app.close()
