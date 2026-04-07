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

## L1-004: Positive reward magnitude matters more than penalty tuning

- **Symptom:** In Ant reward experiments, doubling the locomotion reward (+87%) far outperformed adjusting penalties (high_energy: -49%, no_alive: -28%).
- **Root Cause:** RL agents optimize for the signal with the largest magnitude. Increasing positive rewards gives a clearer gradient toward desired behavior. Increasing penalties can cause the agent to "freeze" and avoid action entirely (as seen in the high_energy experiment where the agent became "lazy").
- **Fix:** N/A — this is a design insight, not a bug.
- **Takeaway:** When engineering rewards: (1) Boost positive rewards for desired behavior before increasing penalties. (2) Over-penalizing energy creates lazy agents. (3) The alive bonus acts as a stabilizer — removing it causes training instability but not catastrophic failure. (4) Speed-efficiency trade-off is real: the fast agent (high_velocity) consumed 3.5x more energy.

## L1-005: SKRL logs only to TensorBoard, no stdout progress

- **Symptom:** Running SKRL training produced no per-epoch reward output to stdout. Only TensorBoard event files were written. Made it impossible to monitor training progress interactively.
- **Root Cause:** SKRL's `SequentialTrainer` writes metrics exclusively to TensorBoard via its logging system. Unlike RL Games, which prints epoch-by-epoch stats (reward, fps, loss) to stdout, SKRL's design philosophy is to use TensorBoard as the sole monitoring interface.
- **Fix:** After training completes, use Python's `tensorboard.backend.event_processing.EventAccumulator` to extract metrics programmatically. For live monitoring, launch a TensorBoard server (`tensorboard --logdir /opt/IsaacLab/logs/skrl/`).
- **Takeaway:** Always check the framework's logging behavior before training. For SKRL, prepare TensorBoard access or a post-hoc metric extraction script before starting long runs.

## L1-006: SKRL uses timesteps, RL Games uses epochs/iterations

- **Symptom:** SKRL config has `trainer.timesteps: 2400` instead of `max_epochs` or `max_iterations`. Confusing when trying to match training durations between frameworks.
- **Root Cause:** SKRL counts total environment interaction steps (timesteps = iterations * rollouts), while RL Games counts optimization epochs. The Isaac Lab wrapper script converts `--max_iterations` to timesteps via `timesteps = max_iterations * agent.rollouts`.
- **Fix:** N/A — understand the conversion: SKRL timesteps = iterations * rollouts_per_iteration. For CartPole with rollouts=16: 300 iters = 4800 timesteps.
- **Takeaway:** When comparing frameworks, always normalize to "total environment steps" (timesteps * num_envs) to get an apples-to-apples comparison. The `--max_iterations` CLI flag handles the conversion automatically.

## L1-007: RL Games achieves higher peak rewards but with more oscillation

- **Symptom:** On Ant, RL Games peaked at 90.35 (epoch 840) but dropped to 68.31 by epoch 1000. SKRL peaked at 72.63 at epoch 1000 and was still climbing steadily.
- **Root Cause:** RL Games uses a higher value loss coefficient (critic_coef=2.0 vs SKRL's value_loss_scale=1.0), mixed precision, and different minibatch strategies. The stronger value function fitting helps faster convergence but can lead to more reward oscillation as the policy overshoots optimal behavior.
- **Fix:** N/A — different training dynamics, not a bug.
- **Takeaway:** Higher peak reward does not mean better training. SKRL's steadier learning curve suggests it might converge to a higher final reward with more iterations. For practical deployment, consider using the best checkpoint (RL Games) rather than the final one, or train SKRL longer for more stable convergence.

## L1-008: RTX 5090 Vulkan ICD mismatch prevents GUI mode in Isaac Sim

- **Symptom:** Isaac Sim GUI mode fails on RTX 5090 with Vulkan ICD mismatch errors. The headless mode works perfectly.
- **Root Cause:** The RTX 5090 is a very new GPU (Blackwell architecture). The Vulkan ICD (Installable Client Driver) in the current Isaac Sim Docker container targets Ampere/Ada Lovelace GPUs. The driver expects certain Vulkan extensions that the 5090 handles differently in GUI mode. Headless mode uses a software Vulkan rasterizer that bypasses this issue.
- **Fix:** Skip GUI FPS comparison for now. Use headless mode exclusively. GUI mode will likely be fixed in a future Isaac Sim container update or NVIDIA driver release.
- **Takeaway:** When using bleeding-edge GPUs (RTX 5090, etc.), always verify GUI rendering works before planning GUI-dependent tasks. Headless training is the primary workflow anyway, so this is not a blocker for RL development. Video recording via `--video` flag works in headless mode.

## L1-009: Isaac Lab video recording uses gymnasium RecordVideo wrapper

- **Symptom:** Video files are saved with the naming pattern `rl-video-step-0.mp4` in a `videos/play/` subdirectory under the checkpoint's log directory.
- **Root Cause:** Isaac Lab wraps the environment with gymnasium's `RecordVideo` wrapper when `--video` is passed. The `step_trigger` is set to `lambda step: step == 0`, meaning it records the very first episode. The `video_length` parameter controls how many steps (frames) are captured.
- **Fix:** N/A -- this is normal behavior. Copy the video to a known location after recording.
- **Takeaway:** The `--video` flag produces 1280x720 at 60fps MP4 files. At 300 frames, this gives a 5-second clip. For longer portfolio videos, increase `--video_length`. The videos are rendered via Isaac Sim's camera system even in headless mode (using offscreen rendering).
