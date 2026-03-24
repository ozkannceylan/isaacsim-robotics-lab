#!/usr/bin/env bash
set -euo pipefail

required=(
  "lab_04_domain_rand/main.py"
  "lab_04_domain_rand/config_loader.py"
  "lab_04_domain_rand/models.py"
  "lab_04_domain_rand/artifact_writers.py"
  "lab_04_domain_rand/agents/skrl_ppo_cfg.py"
  "lab_04_domain_rand/robust_grasp/robust_grasp_env_cfg.py"
  "lab_04_domain_rand/robust_grasp/training.py"
  "lab_04_domain_rand/robust_grasp/mdp/events.py"
  "lab_04_domain_rand/robust_grasp/mdp/observations.py"
  "lab_04_domain_rand/robust_grasp/mdp/rewards.py"
  "lab_04_domain_rand/eval/eval_robustness.py"
  "lab_04_domain_rand/configs/local.yaml"
  "lab_04_domain_rand/eval/eval_configs/nominal.yaml"
  "lab_04_domain_rand/eval/eval_configs/heavy_objects.yaml"
  "lab_04_domain_rand/eval/eval_configs/slippery.yaml"
  "lab_04_domain_rand/eval/eval_configs/noisy.yaml"
  "lab_04_domain_rand/tasks/PLAN.md"
  "lab_04_domain_rand/tasks/ARCHITECTURE.md"
  "lab_04_domain_rand/tasks/TODO.md"
  "lab_04_domain_rand/tasks/LESSONS.md"
)

for p in "${required[@]}"; do
  [[ -f "$p" ]] || { echo "Missing required file: $p"; exit 1; }
done

echo "Lab 4 structure validation passed."
