# Lab 04 Domain Randomization — Architecture

## Module Map
- `main.py`: orchestrates config loading, training, evaluation, and artifact writing.
- `config_loader.py`: parses the Lab 04 YAML config into typed dataclasses.
- `models.py`: shared runtime dataclasses for episode parameters, policy profiles, ADR history, and evaluation results.
- `artifact_writers.py`: writes summary JSON, curriculum CSV, evaluation CSV, and comparison SVG.
- `agents/skrl_ppo_cfg.py`: local PPO config scaffold matching the headless local profile.
- `robust_grasp/robust_grasp_env_cfg.py`: typed Lab 04 environment config.
- `robust_grasp/training.py`: deterministic vanilla and DR training loops plus ADR.
- `robust_grasp/mdp/events.py`: reset-time and evaluation-time randomization sampling.
- `robust_grasp/mdp/observations.py`: clean observation assembly plus configurable noise injection.
- `robust_grasp/mdp/rewards.py`: deterministic grasp success/reward model.
- `eval/eval_robustness.py`: loads YAML evaluation configs and compares DR vs vanilla.

## Data Flow
1. Load `configs/local.yaml`.
2. Train the vanilla baseline and ADR-enabled DR profile.
3. Load `eval/eval_configs/*.yaml`.
4. Evaluate both policies over 100 fixed-seed episodes per config.
5. Persist summary/report artifacts under `outputs/lab_04/`.

## Expected Artifacts
- `summary.json`
- `curriculum_history.csv`
- `evaluation_results.csv`
- `robustness_comparison.svg`
