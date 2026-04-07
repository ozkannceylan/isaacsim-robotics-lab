# Lab 0: Lessons Learned

Log bugs, fixes, and insights here as they occur during cloud setup.

Format: Symptom / Root Cause / Fix / Takeaway

---

### 2026-04-07 — isaaclab core package not installed in Docker image
**Symptom:** `from isaaclab.app import AppLauncher` fails with `ModuleNotFoundError: No module named 'isaaclab.app'`
**Root cause:** The Isaac Lab `./isaaclab.sh -i` installer installs sub-packages (isaaclab_tasks, isaaclab_assets, etc.) but NOT the core `isaaclab` package itself. The `/opt/IsaacLab/source` path in sys.path creates a namespace package that shadows the real module.
**Fix:** `cd /opt/IsaacLab/source/isaaclab && pip install -e . --no-build-isolation`
**Takeaway:** After Isaac Lab source install, always verify `from isaaclab.app import AppLauncher` works. Added this step to Dockerfile.

### 2026-04-07 — NVIDIA Omniverse EULA blocks non-interactive import
**Symptom:** `import isaacsim` hangs waiting for EULA acceptance, fails with `EOF when reading a line`
**Root cause:** Isaac Sim 5.1 requires Omniverse EULA acceptance on first import. Non-interactive SSH sessions can't provide input.
**Fix:** `echo 'Y' | python3 -c "import isaacsim"` to accept once. Added to Dockerfile.
**Takeaway:** Bake EULA acceptance into Docker image build.

### 2026-04-07 — rl_games batch_size assertion with low num_envs
**Symptom:** `AssertionError: self.batch_size % self.minibatch_size == 0` when running CartPole with num_envs < 512
**Root cause:** CartPole rl_games config has `minibatch_size: 8192` and `horizon_length: 16`. batch_size = num_envs * 16, so need num_envs >= 512 (512 * 16 = 8192).
**Fix:** Use num_envs >= 512 for CartPole with default rl_games config. For quick tests use 2048.
**Takeaway:** Always check minibatch_size in the RL config when choosing num_envs.

### 2026-04-07 — Vulkan ERROR_INCOMPATIBLE_DRIVER on RTX 5090
**Symptom:** `vkCreateInstance failed. Vulkan 1.1 is not supported` in Isaac Sim output
**Root cause:** RTX 5090 driver 570.x exposes Vulkan 1.4.303 ICD, but Ubuntu 22.04 system Vulkan loader (1.3.204) doesn't support it. Only affects rendering, NOT headless physics/training.
**Fix:** Not blocking for headless training. For GUI rendering, may need newer `libvulkan1` or the Vulkan SDK.
**Takeaway:** RTX 5090 headless training works fine despite Vulkan errors. Don't panic about Vulkan warnings in logs.

### 2026-04-07 — bash ((COUNT++)) exits with code 1 when COUNT is 0
**Symptom:** validate_setup.sh crashes on first `warn()` or `fail()` call under `set -e`
**Root cause:** `((0++))` evaluates to 0 (post-increment returns old value), which is falsy in bash arithmetic, returning exit code 1. Combined with `set -e`, this aborts the script.
**Fix:** Changed to `COUNT=$((COUNT + 1))` which always returns exit code 0.
**Takeaway:** Never use `((var++))` in bash scripts with `set -e`. Use `var=$((var + 1))` instead.

### 2026-04-07 — Isaac Sim redirects stdout to its logging system
**Symptom:** `print('HEADLESS_OK')` inside SimulationApp context doesn't appear in bash stdout pipe
**Root cause:** Isaac Sim's Kit runtime captures stdout for its own logging framework. Python `print()` output gets swallowed.
**Fix:** Use a marker file (`open('/tmp/marker', 'w').write('OK')`) instead of stdout for detecting success.
**Takeaway:** Don't rely on stdout for pass/fail detection when Isaac Sim is initialized. Use file-based markers or exit codes.

### 2026-04-07 — Windows line endings break bash scripts on Linux
**Symptom:** `set: pipefail: invalid option name` when running scripts copied from Windows
**Root cause:** Windows `\r\n` line endings cause bash to interpret `pipefail\r` as the option name.
**Fix:** `sed -i 's/\r$//' script.sh` or configure git: `git config core.autocrlf input`
**Takeaway:** Always ensure `.sh` files use LF line endings. Add `.gitattributes` or configure git autocrlf.

---

### 2026-04-07 — Validated stack versions on RTX 5090 instance
**Versions confirmed working together:**
| Component | Version |
|-----------|---------|
| GPU | NVIDIA GeForce RTX 5090 (32 GB VRAM) |
| Driver | 570.144 |
| CUDA | 12.8 |
| PyTorch | 2.7.0+cu128 |
| Isaac Sim | 5.1 (import OK, no `__version__` attr) |
| Isaac Lab | 2.3.0 |
| Python | 3.11.15 (system, no conda) |
| OS | Ubuntu 22.04 (Docker) |
| imageio | 2.37.0 |
| OpenCV | 4.11.0 |
| MoviePy | 2.1.2 |
| Gymnasium | 1.2.0 |
**Takeaway:** This stack is the validated baseline. Pin these versions in Docker image.

### 2026-04-07 — Headless video recording works on RTX 5090
**Symptom:** Feared Vulkan errors would block rendering (see earlier lesson).
**Root cause:** `--enable_cameras` flag uses Omniverse Replicator for offscreen rendering, which works despite Vulkan ICD version mismatch.
**Fix:** N/A — it just works. Use `--headless --enable_cameras` (or `--headless --video` for play.py).
**Takeaway:** RTX 5090 supports headless video recording via Replicator. Non-blocking warnings appear (GLFW init, Fabric, syntheticdata) but output is correct. Default resolution 1280x720 at 60 FPS.

### 2026-04-07 — isaaclab CLI not on PATH in Docker image
**Symptom:** `isaaclab` command not found when running commands.
**Root cause:** The Docker image installs Isaac Lab to `/opt/IsaacLab` but doesn't add `isaaclab.sh` to PATH.
**Fix:** Use `bash /opt/IsaacLab/isaaclab.sh -p <script>` instead of `isaaclab -p <script>`.
**Takeaway:** Always use full path to `isaaclab.sh` on this Docker image. Could add to PATH in Dockerfile.

### 2026-04-07 — CartPole trains to -1.57 reward in 50 iterations (expected)
**Symptom:** Negative reward values during training — looks like failure.
**Root cause:** CartPole reward config has penalty terms (angle=-1.0, cart_vel=-0.01, pole_vel=-0.005, termination=-2.0) with only alive bonus (+1.0). Negative total is normal; near-zero is the goal.
**Fix:** N/A — reward improved from -1.80 to -1.57 in 50 iterations. Need 200-500 iterations for convergence.
**Takeaway:** Don't panic at negative CartPole rewards with default Isaac Lab config. Check individual reward terms in TensorBoard.

### 2026-04-07 — Working commands for video recording
**Reference commands:**
```bash
# Train CartPole (min 512 envs for rl_games default config)
bash /opt/IsaacLab/isaaclab.sh -p /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 512 --max_iterations 50

# Play trained policy with video recording
bash /opt/IsaacLab/isaaclab.sh -p /opt/IsaacLab/scripts/reinforcement_learning/rl_games/play.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 4 --video --video_length 200

# Custom video recording scripts
cd /workspace/isaacsim-robotics-lab
bash /opt/IsaacLab/isaaclab.sh -p labs/lab_0/scripts/record_demo.py --headless --enable_cameras
bash /opt/IsaacLab/isaaclab.sh -p labs/lab_0/scripts/multi_env_demo.py --headless --enable_cameras
```
**Checkpoints:** Saved to `/root/logs/rl_games/cartpole/<timestamp>/nn/`
**Videos:** play.py saves to `.../videos/play/`, custom scripts save to `labs/lab_0/media/`
