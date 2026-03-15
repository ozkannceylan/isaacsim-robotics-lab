# Lessons Learned

## Context
Lab 01 needed a full correction pass because the original repo content was a generic scaffold rather than the actual Isaac Sim foundations capstone described in `plan/lab_01_foundations.md`.

## Step Log
1. Reviewed the existing Lab 01 implementation against the plan and identified that it never launched Isaac Sim or produced the required artifacts.
2. Replaced the placeholder loop with a real standalone Isaac Lab runner.
3. Added a mock backend so the artifact contract can still be tested in environments without Isaac Lab installed.
4. Switched the lab configs to YAML and encoded the real 300-step and 30-frame targets explicitly.

## What Worked
- Separating the real Isaac Lab backend from the mock backend kept the entrypoint clean and testable.
- Pure-stdlib PNG writing avoids adding image dependencies just to validate the frame output contract.
- Encoding Isaac Nucleus asset references in config is clearer than committing fake USD placeholders.

## What Didn't Work
- The previous placeholder implementation gave a false sense of completion while missing every capstone requirement that mattered.
- This workspace does not currently include the `isaaclab` command, so the real simulation path could not be executed here.

## Open Questions
- Does the local Isaac Lab environment already expose the UR5e Nucleus asset exactly at `${ISAAC_NUCLEUS_DIR}/Robots/UniversalRobots/ur5e/ur5e.usd`?
- Does the chosen UR5e USD expose only the six arm joints, or is a narrower actuator regex needed after the first live run?

## Follow-up Actions
- Run `bash lab_01_foundations/scripts/run_lab.sh` inside the real Isaac Lab environment and inspect the generated CSV/PNG artifacts.
- If the UR5e USD layout differs locally, update only the asset path and arm-joint targeting logic in `configs/local.yaml` and `src/isaaclab_runtime.py`.
