# Lab 1: Lessons Learned

Log bugs, fixes, and insights here as they occur during RL training.

Format: Symptom / Root Cause / Fix / Takeaway

---

## L1-001: HEADLESS env var conflicts with --headless CLI flag

- **Symptom:** `ValueError: invalid literal for int() with base 10: '--headless'` when running training scripts on Vast.ai Docker instance.
- **Root Cause:** The Docker `vastai_onstart.sh` sets `HEADLESS=1` as an environment variable. Isaac Lab's `AppLauncher._config_resolution()` reads this env var with `int(os.environ.get("HEADLESS", 0))`. Separately, our shell scripts were passing `--headless` as a CLI argument. When the env var is already set to the string `"1"`, the CLI `--headless` flag caused the env var to be overwritten to the string `"--headless"` somewhere in the arg parsing chain, which then failed `int()` conversion.
- **Fix:** Check if `HEADLESS` env var is already set before passing the `--headless` CLI flag. If env var is set (as it is on our Docker images), skip the CLI flag entirely. Applied to all 5 training/benchmark/evaluate scripts.
- **Takeaway:** Isaac Lab has two headless modes: env var (`HEADLESS=1`) and CLI flag (`--headless`). They should not be mixed. On Docker instances where the env var is pre-configured, do not pass the CLI flag. Always check `${HEADLESS:-}` before adding `--headless` to command lines.

## L1-002: CartPole reward saturates around 4.93, not a clean convergence

- **Symptom:** After 300 iterations with 2048 envs, the best reward was 4.93 (at epoch 141). Reward oscillates between 3.4 and 4.9 throughout training -- no stable plateau.
- **Root Cause:** This is expected behavior for CartPole with the default Isaac Lab reward function. The reward consists of: alive (+1.0), terminating (-2.0), pole_pos (-1.0), cart_vel (-0.01), pole_vel (-0.005). The theoretical max is ~5.0 per step (alive=1.0, all penalties near zero). Achieving 4.93 means the pole is nearly perfectly balanced. The oscillation is because RL Games' PPO has stochastic exploration and the policy occasionally enters states where episodes terminate early.
- **Takeaway:** A reward of ~4.9/5.0 indicates successful convergence for CartPole. The oscillation is normal for on-policy RL -- do not interpret it as instability.

## L1-003: RTX 5090 throughput scaling is sub-linear for CartPole

- **Symptom:** Doubling num_envs from 512 to 1024 increases fps_step by ~1.5x (90K to 135K), but from 4096 to 8192 it increases by ~2x (440K to 870K). However, wall time increases because there are more total samples to process.
- **Root Cause:** CartPole is extremely lightweight (4 obs, 1 action). At small num_envs, GPU compute is underutilized and overhead dominates. At larger num_envs, the GPU becomes better utilized. The fps_total metric (which includes policy network training) scales less aggressively because the training computation per iteration also grows with batch size.
- **Takeaway:** For lightweight envs, use num_envs >= 4096 to saturate the GPU. The RTX 5090 can handle 8192 CartPole envs at ~870K fps_step using only 3.9 GB of its 32 GB VRAM.
