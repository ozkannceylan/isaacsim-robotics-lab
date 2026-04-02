# Lab 4: Sim-to-Real Pipeline

## Objective

Build an end-to-end sim-to-real pipeline: train a policy in Isaac Lab, export it, and deploy via ROS2. This capstone lab connects Isaac Lab expertise to real-world robotics deployment and ties back to the humanoid_vla project.

## Why This Lab Exists

Training in simulation is only valuable if policies transfer to real robots. This lab covers the full pipeline: policy training with transfer-friendly techniques, ONNX/TorchScript export, ROS2 integration, and deployment considerations. It demonstrates production-level thinking, not just research prototyping.

## Prerequisites

- Labs 0-3 complete
- ROS2 Humble installed (local Ubuntu machine for ROS2 side)
- humanoid_vla project context (G1 + ROS2 pipeline)
- Understanding of sim-to-real gap from literature

## Deliverables

1. Trained policy exported as ONNX and TorchScript
2. ROS2 node that loads exported policy and publishes joint commands
3. Isaac Sim ROS2 bridge demo: policy running in sim via ROS2
4. Sim-to-real transfer analysis document
5. Capstone demo video: full pipeline from training to deployment

## Tasks

### 4.1 Transfer-Friendly Training

Revisit Lab 2's policies with sim-to-real in mind:

- Aggressive domain randomization (physics, visual, dynamics)
- Observation noise injection (simulating real sensor noise)
- Action smoothing / rate limiting (real actuators have delays)
- Asymmetric actor-critic: privileged info in critic, only real-observable in actor

Document which techniques are used and their expected impact.

### 4.2 Policy Export

Export trained policy for deployment:

- **ONNX export:** Standard format, framework-agnostic
- **TorchScript export:** PyTorch-native, preserves more features
- Verify exported model produces identical outputs to training model
- Measure inference latency of exported model (target: <10ms per step)

### 4.3 ROS2 Bridge in Isaac Sim

Connect Isaac Sim to ROS2:

- Enable Isaac Sim's built-in ROS2 bridge
- Publish: joint states, camera images, IMU data
- Subscribe: joint commands from external policy node
- Verify bidirectional communication with `ros2 topic list/echo`

This creates a software-in-the-loop (SIL) testing environment.

### 4.4 ROS2 Policy Deployment Node

Build a ROS2 node (Python) that:

- Loads the exported ONNX/TorchScript model
- Subscribes to observation topics (joint states, sensor data)
- Runs inference at control frequency (e.g., 50Hz)
- Publishes joint position commands
- Handles latency, missing data, and error states

This node architecture should be reusable for real robot deployment.

### 4.5 cuRobo Integration (Optional/Stretch)

Isaac Lab 2.3.0 integrates cuRobo for GPU-accelerated motion planning:

- Use cuRobo for collision-free trajectory generation
- Compare RL policy vs cuRobo planner for reach/manipulation tasks
- Hybrid approach: RL for high-level decisions, cuRobo for motion execution

This is a stretch goal. Valuable if time permits, not required for lab completion.

### 4.6 Capstone Integration

Tie everything together:

- Train policy (Lab 2 task) with transfer-friendly settings (4.1)
- Export model (4.2)
- Run in Isaac Sim via ROS2 bridge (4.3 + 4.4)
- Record demo video showing the full pipeline
- Write capstone blog post connecting to humanoid_vla narrative

## Sim-to-Real Gap Mitigation Checklist

| Technique | Lab Reference | Purpose |
|-----------|--------------|---------|
| Domain randomization | Lab 2.5, 4.1 | Robustness to physics variation |
| Observation noise | 4.1 | Robustness to sensor noise |
| Action rate limiting | 4.1 | Realistic actuator behavior |
| Asymmetric actor-critic | 4.1 | Privileged training, real deployment |
| Visual randomization | Lab 3.5, 4.1 | Camera-based policy transfer |
| System identification | 4.6 | Match sim parameters to real robot |

## Architecture: Deployment Pipeline

```
[Isaac Lab Training] --> [ONNX Export] --> [ROS2 Inference Node]
                                                  |
                                          [Joint Commands]
                                                  |
                                     [Isaac Sim via ROS2 Bridge]
                                            or
                                        [Real G1 Robot]
```

The ROS2 node is identical whether driving the sim or the real robot. Only the ROS2 topic namespaces change.

## Success Criteria

- Exported ONNX model matches training model outputs (within floating point tolerance)
- ROS2 bridge connects Isaac Sim and external policy node
- Policy runs in SIL loop at >20Hz
- Demo video shows training, export, and ROS2 deployment
- Blog-ready writeup documents the full pipeline

## Estimated Cloud Cost

10-12 hours at ~$0.30/hr = ~$3.00-3.60

## Notes

- ROS2 bridge work can partially be done on local machine (Ubuntu) without GPU.
- The ROS2 node itself is lightweight. Cloud GPU is only needed for Isaac Sim side.
- This lab's deliverables directly strengthen the NEURA Robotics application narrative.
- Consider recording a LinkedIn video demo of the capstone.
