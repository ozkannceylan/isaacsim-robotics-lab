"""Compare reward experiment results from TensorBoard logs.

Reads TensorBoard event files from multiple training runs and generates
comparison charts for reward components.

Usage:
    python compare_rewards.py --logdirs run_default run_high_energy run_no_alive
    python compare_rewards.py --logdirs outputs/Isaac-Ant-v0/*
"""

import argparse
from pathlib import Path


def find_event_files(logdir: Path) -> list[Path]:
    """Find TensorBoard event files in a directory tree.

    Args:
        logdir: Root directory to search.

    Returns:
        List of paths to event files.
    """
    return sorted(logdir.rglob("events.out.tfevents.*"))


def load_scalar_events(event_file: Path, tag: str) -> list[tuple[int, float]]:
    """Load scalar values for a specific tag from a TensorBoard event file.

    Args:
        event_file: Path to the event file.
        tag: The scalar tag to extract (e.g., "rewards/total").

    Returns:
        List of (step, value) tuples.
    """
    try:
        from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
    except ImportError:
        print("tensorboard not available. Install with: pip install tensorboard")
        return []

    ea = EventAccumulator(str(event_file.parent))
    ea.Reload()

    if tag not in ea.Tags().get("scalars", []):
        return []

    return [(e.step, e.value) for e in ea.Scalars(tag)]


def plot_comparison(
    data: dict[str, list[tuple[int, float]]],
    title: str,
    output_path: Path,
) -> None:
    """Plot reward comparison across experiments.

    Args:
        data: Dict mapping run name to list of (step, value) pairs.
        title: Chart title.
        output_path: Where to save the chart.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available. Skipping chart.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    for name, points in data.items():
        if points:
            steps, values = zip(*points)
            ax.plot(steps, values, label=name, linewidth=1.5)

    ax.set_xlabel("Training Step", fontsize=12)
    ax.set_ylabel("Reward", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Chart saved to: {output_path}")
    plt.close(fig)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Compare reward experiments")
    parser.add_argument(
        "--logdirs", nargs="+", type=Path, required=True,
        help="Directories containing TensorBoard logs for each run",
    )
    parser.add_argument(
        "--tag", default="rewards/episode_reward",
        help="Scalar tag to compare",
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parent.parent / "media" / "reward_comparison.png",
        help="Output chart path",
    )
    args = parser.parse_args()

    data = {}
    for logdir in args.logdirs:
        if not logdir.exists():
            print(f"Warning: {logdir} not found, skipping")
            continue
        events = find_event_files(logdir)
        if not events:
            print(f"Warning: No event files in {logdir}")
            continue
        points = load_scalar_events(events[0], args.tag)
        data[logdir.name] = points

    if not data:
        print("No data loaded. Check log directories and tag name.")
        return

    print(f"Loaded data from {len(data)} runs: {', '.join(data.keys())}")
    plot_comparison(data, f"Reward Comparison: {args.tag}", args.output)


if __name__ == "__main__":
    main()
