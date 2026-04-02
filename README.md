# Isaac Sim Robotics Lab

GPU-accelerated robotics with NVIDIA Isaac Sim and Isaac Lab. A structured 5-lab curriculum covering RL fundamentals, custom task engineering, sensor simulation, synthetic data, and sim-to-real transfer with the Unitree G1 humanoid.

## Quick Start

```bash
# SSH into your Vast.ai RTX 4090 instance, then:
bash labs/lab_0/scripts/setup_instance.sh    # one-time setup (~15 min)
conda activate isaaclab
bash labs/lab_0/scripts/validate_setup.sh    # verify everything works
```

See [plan/README.md](plan/README.md) for the full curriculum and lab details.

## Lab Status

| Lab | Topic | Status |
|-----|-------|--------|
| 0 | Cloud Setup and Validation | In Progress |
| 1 | Isaac Lab RL Fundamentals | Not Started |
| 2 | Custom Task and Reward Engineering | Not Started |
| 3 | Sensor Simulation and Synthetic Data | Not Started |
| 4 | Sim-to-Real Pipeline | Not Started |

## Stack

- **Isaac Sim 5.1** + **Isaac Lab 2.3.x** on Vast.ai RTX 4090
- **PyTorch 2.7** with CUDA 12.8
- **RL Games** (primary) / **SKRL** (secondary)
- Target robot: **Unitree G1** humanoid (Labs 2-4)

## Related Projects

- [mujoco-robotics-lab](https://github.com/ozkannceylan/mujoco-robotics-lab) - Foundational robotics: FK, IK, dynamics, motion planning
- [humanoid_vla](https://github.com/ozkannceylan/humanoid_vla) - Unitree G1, ACT imitation learning, ROS2 deployment
