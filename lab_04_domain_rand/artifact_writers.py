"""Artifact writing for Lab 04 outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from lab_04_domain_rand.agents.skrl_ppo_cfg import SkrlPpoCfg
from lab_04_domain_rand.models import EvaluationResult, TrainingResult
from lab_04_domain_rand.robust_grasp.robust_grasp_env_cfg import RobustGraspEnvCfg


def write_artifacts(
    cfg: RobustGraspEnvCfg,
    agent_cfg: SkrlPpoCfg,
    dr_training: TrainingResult,
    vanilla_training: TrainingResult,
    evaluation_results: tuple[EvaluationResult, ...],
    output_dir: str | Path,
) -> dict[str, Path]:
    """Write the Lab 04 report artifacts and return their paths."""
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    summary_path = root / "summary.json"
    curriculum_path = root / "curriculum_history.csv"
    evaluation_path = root / "evaluation_results.csv"
    chart_path = root / cfg.evaluation.chart_filename

    _write_summary(summary_path, cfg, agent_cfg, dr_training, vanilla_training, evaluation_results)
    _write_curriculum_csv(curriculum_path, dr_training, vanilla_training)
    _write_evaluation_csv(evaluation_path, evaluation_results)
    _write_svg_chart(chart_path, evaluation_results, cfg.evaluation.dr_policy_name, cfg.evaluation.vanilla_policy_name)

    return {
        "summary": summary_path,
        "curriculum_csv": curriculum_path,
        "evaluation_csv": evaluation_path,
        "chart": chart_path,
    }


def _write_summary(
    path: Path,
    cfg: RobustGraspEnvCfg,
    agent_cfg: SkrlPpoCfg,
    dr_training: TrainingResult,
    vanilla_training: TrainingResult,
    evaluation_results: tuple[EvaluationResult, ...],
) -> None:
    payload = {
        "status": "success",
        "headless": cfg.training.headless,
        "num_envs": cfg.training.num_envs,
        "agent": agent_cfg.__dict__,
        "dr_training": {
            "policy_name": dr_training.policy_profile.name,
            "mean_success_rate": dr_training.mean_success_rate,
            "max_range_scale": dr_training.max_range_scale,
        },
        "vanilla_training": {
            "policy_name": vanilla_training.policy_profile.name,
            "mean_success_rate": vanilla_training.mean_success_rate,
            "max_range_scale": vanilla_training.max_range_scale,
        },
        "evaluation": [result.__dict__ for result in evaluation_results],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_curriculum_csv(path: Path, dr_training: TrainingResult, vanilla_training: TrainingResult) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["policy_name", "episode_index", "range_scale", "rolling_success_rate"],
        )
        writer.writeheader()
        for policy_name, result in (
            (dr_training.policy_profile.name, dr_training),
            (vanilla_training.policy_profile.name, vanilla_training),
        ):
            for snapshot in result.curriculum_history:
                writer.writerow(
                    {
                        "policy_name": policy_name,
                        "episode_index": snapshot.episode_index,
                        "range_scale": snapshot.range_scale,
                        "rolling_success_rate": snapshot.rolling_success_rate,
                    }
                )


def _write_evaluation_csv(path: Path, evaluation_results: tuple[EvaluationResult, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["config_name", "dr_success_rate", "vanilla_success_rate", "dr_mean_reward", "vanilla_mean_reward"],
        )
        writer.writeheader()
        for result in evaluation_results:
            writer.writerow(result.__dict__)


def _write_svg_chart(path: Path, evaluation_results: tuple[EvaluationResult, ...], dr_name: str, vanilla_name: str) -> None:
    width = 720
    height = 320
    bar_width = 48
    group_gap = 28
    baseline_y = 260
    scale = 180
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#faf7f0"/>',
        '<text x="24" y="36" font-size="20" font-family="monospace">Lab 04 Robustness Comparison</text>',
        f'<text x="24" y="58" font-size="12" font-family="monospace">{dr_name} vs {vanilla_name}</text>',
        '<line x1="24" y1="260" x2="696" y2="260" stroke="#222" stroke-width="2"/>',
    ]
    for index, result in enumerate(evaluation_results):
        origin_x = 70 + index * ((bar_width * 2) + group_gap)
        dr_height = result.dr_success_rate * scale
        vanilla_height = result.vanilla_success_rate * scale
        svg.extend(
            [
                f'<rect x="{origin_x}" y="{baseline_y - dr_height:.1f}" width="{bar_width}" height="{dr_height:.1f}" fill="#1f6f8b"/>',
                f'<rect x="{origin_x + bar_width + 8}" y="{baseline_y - vanilla_height:.1f}" width="{bar_width}" height="{vanilla_height:.1f}" fill="#d65a31"/>',
                f'<text x="{origin_x}" y="284" font-size="11" font-family="monospace">{result.config_name}</text>',
            ]
        )
    svg.extend(
        [
            '<rect x="520" y="34" width="16" height="16" fill="#1f6f8b"/>',
            f'<text x="544" y="47" font-size="12" font-family="monospace">{dr_name}</text>',
            '<rect x="520" y="58" width="16" height="16" fill="#d65a31"/>',
            f'<text x="544" y="71" font-size="12" font-family="monospace">{vanilla_name}</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(svg), encoding="utf-8")
