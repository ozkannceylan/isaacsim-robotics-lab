"""Main entrypoint for Lab 04."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from lab_04_domain_rand.agents.skrl_ppo_cfg import build_local_ppo_cfg
from lab_04_domain_rand.artifact_writers import write_artifacts
from lab_04_domain_rand.config_loader import load_config
from lab_04_domain_rand.eval.eval_robustness import evaluate_policies, load_evaluation_configs
from lab_04_domain_rand.robust_grasp.training import train_domain_randomized_policy, train_vanilla_policy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Lab 04 domain-randomization scaffold")
    parser.add_argument("--config", default="lab_04_domain_rand/configs/local.yaml")
    parser.add_argument("--eval-config-dir", default="lab_04_domain_rand/eval/eval_configs")
    parser.add_argument("--output-dir", default=None)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Execute training and evaluation for Lab 04."""
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config)
    output_dir = args.output_dir or cfg.training.output_dir
    agent_cfg = build_local_ppo_cfg(cfg.training)

    vanilla_training = train_vanilla_policy(cfg)
    dr_training = train_domain_randomized_policy(cfg)
    eval_configs = load_evaluation_configs(args.eval_config_dir)
    evaluation_results = evaluate_policies(
        cfg,
        dr_policy=dr_training.policy_profile,
        vanilla_policy=vanilla_training.policy_profile,
        eval_configs=eval_configs,
    )
    paths = write_artifacts(cfg, agent_cfg, dr_training, vanilla_training, evaluation_results, output_dir)
    print(f"Lab 04 completed. Summary: {paths['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
