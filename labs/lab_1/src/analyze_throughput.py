"""Analyze num_envs benchmark results and generate throughput chart.

Reads benchmark_results.csv produced by benchmark_num_envs.sh and creates
a throughput scaling chart showing steps/sec vs num_envs.

Usage:
    python analyze_throughput.py                          # default paths
    python analyze_throughput.py --csv path/to/results.csv --output chart.png
"""

import argparse
import csv
from pathlib import Path


def load_benchmark_data(csv_path: Path) -> list[dict]:
    """Load benchmark results from CSV file.

    Args:
        csv_path: Path to benchmark_results.csv

    Returns:
        List of dicts with num_envs, wall_time_sec, iterations, steps_per_sec.
    """
    results = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            num_envs = int(row["num_envs"])
            wall_time = float(row["wall_time_sec"])
            iterations = int(row["iterations"])
            total_steps = num_envs * iterations
            steps_per_sec = total_steps / wall_time if wall_time > 0 else 0
            results.append({
                "num_envs": num_envs,
                "wall_time_sec": wall_time,
                "iterations": iterations,
                "total_steps": total_steps,
                "steps_per_sec": steps_per_sec,
            })
    return results


def print_table(results: list[dict]) -> None:
    """Print results as a formatted table.

    Args:
        results: List of benchmark result dicts.
    """
    print(f"{'num_envs':>10} {'wall_time':>12} {'total_steps':>14} {'steps/sec':>14}")
    print("-" * 54)
    for r in results:
        print(
            f"{r['num_envs']:>10} "
            f"{r['wall_time_sec']:>11.1f}s "
            f"{r['total_steps']:>14,} "
            f"{r['steps_per_sec']:>13,.0f}"
        )


def generate_chart(results: list[dict], output_path: Path) -> None:
    """Generate throughput scaling chart.

    Args:
        results: List of benchmark result dicts.
        output_path: Path to save the chart image.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available. Install with: pip install matplotlib")
        print("Skipping chart generation. Table output above.")
        return

    num_envs = [r["num_envs"] for r in results]
    steps_per_sec = [r["steps_per_sec"] for r in results]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(num_envs, steps_per_sec, "o-", linewidth=2, markersize=8, color="#76b900")
    ax.set_xlabel("num_envs", fontsize=12)
    ax.set_ylabel("Steps / Second", fontsize=12)
    ax.set_title("Isaac Lab CartPole: GPU Parallelism Scaling", fontsize=14)
    ax.set_xscale("log", base=2)
    ax.grid(True, alpha=0.3)

    # Annotate each point
    for n, s in zip(num_envs, steps_per_sec):
        ax.annotate(f"{s:,.0f}", (n, s), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Chart saved to: {output_path}")
    plt.close(fig)


def main() -> None:
    """Main entry point."""
    lab_dir = Path(__file__).resolve().parent.parent
    default_csv = lab_dir / "src" / "benchmark_results.csv"
    default_output = lab_dir / "media" / "throughput_scaling.png"

    parser = argparse.ArgumentParser(description="Analyze num_envs benchmark results")
    parser.add_argument("--csv", type=Path, default=default_csv, help="Path to benchmark CSV")
    parser.add_argument("--output", type=Path, default=default_output, help="Output chart path")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"CSV not found: {args.csv}")
        print("Run benchmark_num_envs.sh first to generate data.")
        return

    results = load_benchmark_data(args.csv)
    print_table(results)
    print()
    generate_chart(results, args.output)


if __name__ == "__main__":
    main()
