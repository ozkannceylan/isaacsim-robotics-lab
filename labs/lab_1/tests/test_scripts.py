"""Tests for Lab 1 script and file existence.

These tests verify that all required Lab 1 files exist and scripts
have correct structure. They run locally without Isaac Sim.
"""

from pathlib import Path

import pytest

LAB_DIR = Path(__file__).resolve().parent.parent


class TestLabStructure:
    """Verify Lab 1 directory structure and required files."""

    def test_tasks_plan_exists(self) -> None:
        assert (LAB_DIR / "tasks" / "PLAN.md").is_file()

    def test_tasks_architecture_exists(self) -> None:
        assert (LAB_DIR / "tasks" / "ARCHITECTURE.md").is_file()

    def test_tasks_todo_exists(self) -> None:
        assert (LAB_DIR / "tasks" / "TODO.md").is_file()

    def test_tasks_lessons_exists(self) -> None:
        assert (LAB_DIR / "tasks" / "LESSONS.md").is_file()

    def test_docs_directory_exists(self) -> None:
        assert (LAB_DIR / "docs").is_dir()

    def test_media_directory_exists(self) -> None:
        assert (LAB_DIR / "media").is_dir()


class TestScripts:
    """Verify training scripts exist and are executable."""

    SCRIPTS = [
        "train_cartpole.sh",
        "train_ant.sh",
        "benchmark_num_envs.sh",
        "compare_frameworks.sh",
        "evaluate.sh",
    ]

    @pytest.mark.parametrize("script_name", SCRIPTS)
    def test_script_exists(self, script_name: str) -> None:
        script_path = LAB_DIR / "scripts" / script_name
        assert script_path.is_file(), f"Script not found: {script_path}"

    @pytest.mark.parametrize("script_name", SCRIPTS)
    def test_script_is_executable(self, script_name: str) -> None:
        import os

        script_path = LAB_DIR / "scripts" / script_name
        assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"

    @pytest.mark.parametrize("script_name", SCRIPTS)
    def test_script_has_shebang(self, script_name: str) -> None:
        script_path = LAB_DIR / "scripts" / script_name
        first_line = script_path.read_text().splitlines()[0]
        assert first_line.startswith("#!/"), f"Missing shebang in {script_name}"

    @pytest.mark.parametrize("script_name", SCRIPTS)
    def test_script_has_set_euo_pipefail(self, script_name: str) -> None:
        script_path = LAB_DIR / "scripts" / script_name
        content = script_path.read_text()
        assert "set -euo pipefail" in content, f"Missing 'set -euo pipefail' in {script_name}"


class TestPythonModules:
    """Verify Python analysis scripts exist and are importable."""

    def test_analyze_throughput_exists(self) -> None:
        assert (LAB_DIR / "src" / "analyze_throughput.py").is_file()

    def test_compare_rewards_exists(self) -> None:
        assert (LAB_DIR / "src" / "compare_rewards.py").is_file()

    def test_analyze_throughput_has_main(self) -> None:
        content = (LAB_DIR / "src" / "analyze_throughput.py").read_text()
        assert "def main()" in content

    def test_compare_rewards_has_main(self) -> None:
        content = (LAB_DIR / "src" / "compare_rewards.py").read_text()
        assert "def main()" in content


class TestDocumentation:
    """Verify documentation files exist."""

    def test_comparison_doc_exists(self) -> None:
        assert (LAB_DIR / "docs" / "isaac_lab_vs_mujoco.md").is_file()

    def test_benchmark_doc_exists(self) -> None:
        assert (LAB_DIR / "docs" / "benchmark_results.md").is_file()
