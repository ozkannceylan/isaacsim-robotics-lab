import unittest

from lab_01_foundations.src.control import compute_capture_steps, generate_joint_targets


class TestControl(unittest.TestCase):
    def test_capture_steps_cover_requested_frame_count(self) -> None:
        capture_steps = compute_capture_steps(300, 30)
        self.assertEqual(len(capture_steps), 30)
        self.assertEqual(capture_steps[0], 9)
        self.assertEqual(capture_steps[-1], 299)
        self.assertEqual(len(set(capture_steps)), 30)

    def test_generate_joint_targets_returns_one_value_per_joint(self) -> None:
        targets = generate_joint_targets(
            base_positions=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
            amplitudes_rad=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6),
            phase_offsets_rad=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5),
            frequency_hz=0.25,
            time_s=1.0,
        )
        self.assertEqual(len(targets), 6)
        self.assertTrue(all(isinstance(value, float) for value in targets))


if __name__ == "__main__":
    unittest.main()
