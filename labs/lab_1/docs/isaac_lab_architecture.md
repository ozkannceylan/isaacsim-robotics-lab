# Isaac Lab Architecture: Core Concepts

## 1. The Big Picture

Isaac Lab is a GPU-first RL framework built on top of NVIDIA Isaac Sim. The fundamental insight: instead of running N separate environment processes on CPU (like Gymnasium's `SubprocVecEnv`), Isaac Lab runs all N environments in a single GPU simulation. Observations, actions, and rewards are batched tensors that never leave the GPU.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Isaac Lab                                │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  ManagerBasedRLEnv (or DirectRLEnv)                        │  │
│  │                                                            │  │
│  │  ┌─────────────────────┐  ┌────────────────────────────┐  │  │
│  │  │  InteractiveScene    │  │  Managers                  │  │  │
│  │  │  ├─ Articulations    │  │  ├─ ObservationManager     │  │  │
│  │  │  ├─ Rigid Bodies     │  │  ├─ ActionManager          │  │  │
│  │  │  ├─ Deformable Bodies│  │  ├─ RewardManager          │  │  │
│  │  │  └─ Sensors          │  │  ├─ TerminationManager     │  │  │
│  │  └─────────────────────┘  │  ├─ EventManager (resets)   │  │  │
│  │                            │  └─ CurriculumManager      │  │  │
│  │                            └────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              v                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Isaac Sim (Omniverse Kit)                                 │  │
│  │  ├─ PhysX 5 GPU simulation (all envs in one scene)        │  │
│  │  ├─ USD scene graph (Universal Scene Description)          │  │
│  │  └─ RTX renderer (ray-tracing for cameras/video)          │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Two Workflow Styles

### Manager-Based (Recommended)
- Environment behavior is defined via `@configclass` configuration objects
- Each concern (observations, rewards, terminations) is a separate Manager
- Modular: swap reward terms without touching env code
- Used for: most tasks, especially when experimenting with reward engineering

### Direct
- More like traditional Gymnasium: override `_step()`, `_reset()`, `_get_observations()`
- Full control, less boilerplate for simple cases
- Used for: custom physics logic, unusual stepping patterns

**Rule of thumb:** Start with Manager-Based. Use Direct only if you need custom step logic.

## 3. The Four Core Managers

### ObservationManager
Assembles observation tensors from independent **terms** (functions).

```python
@configclass
class ObservationsCfg:
    @configclass
    class PolicyCfg(ObsGroup):
        joint_pos = ObsTerm(func=mdp.joint_pos_rel)     # (N, num_joints)
        joint_vel = ObsTerm(func=mdp.joint_vel_rel)      # (N, num_joints)
        base_ang_vel = ObsTerm(func=mdp.base_ang_vel)    # (N, 3)
    policy: PolicyCfg = PolicyCfg()
```

Each term is a function `f(env) -> Tensor(N, dim)`. Terms are concatenated into the final observation. Multiple observation groups can exist (e.g., `policy` for the actor, `critic` for asymmetric critic).

### ActionManager
Maps raw policy output to physical actuation.

```python
@configclass
class ActionsCfg:
    joint_effort = ActionTerm(
        class_type=JointEffortAction,
        asset_name="robot",
        joint_names=[".*"],
    )
```

Supports joint effort (torque), joint position (PD control), joint velocity, and custom action types. The action space dimension is automatically inferred.

### RewardManager
Computes per-environment scalar reward as a weighted sum of **terms**.

```python
@configclass
class RewardsCfg:
    alive = RewardTerm(func=mdp.is_alive, weight=1.0)
    pole_angle = RewardTerm(func=mdp.joint_pos_target_l2, weight=-1.0,
                            params={"target": 0.0, "asset_cfg": ...})
    energy = RewardTerm(func=mdp.action_l2, weight=-0.01)
```

Each term: `f(env) -> Tensor(N,)` scalar per env. Total reward = sum of (term * weight). This decomposition makes reward engineering transparent — inspect each component in TensorBoard.

### TerminationManager
Determines which environments should reset.

```python
@configclass
class TerminationsCfg:
    time_out = TermTerm(func=mdp.time_out, time_out=True)
    bad_state = TermTerm(func=mdp.bad_orientation, params={"limit_angle": 0.5})
```

Returns boolean masks `(N,)`. Time-limited terminations (`time_out=True`) are distinguished from failure terminations for proper value bootstrapping in RL.

## 4. InteractiveScene

The scene is the container for all simulation entities. It uses USD (Universal Scene Description) as the scene graph format.

```python
@configclass
class MySceneCfg(InteractiveSceneCfg):
    ground = AssetBaseCfg(prim_path="/World/ground", spawn=GroundPlaneCfg())
    robot = ArticulationCfg(
        prim_path="/World/envs/env_.*/Robot",
        spawn=UsdFileCfg(usd_path="path/to/robot.usd"),
        actuators={"joints": ImplicitActuatorCfg(...)},
    )
    camera = CameraCfg(...)  # optional, for rendering
```

Key pattern: `env_.*` in the prim path. Isaac Lab clones the scene N times (one per env), replacing `env_.*` with `env_0`, `env_1`, ..., `env_N-1`. All clones share the same PhysX simulation.

## 5. GPU Parallelism Model

```
Traditional (CPU):                    Isaac Lab (GPU):
┌──────┐ ┌──────┐ ┌──────┐           ┌──────────────────────┐
│ Env 0│ │ Env 1│ │ Env 2│  ...      │  PhysX GPU Simulation │
│(proc)│ │(proc)│ │(proc)│           │  ┌───┬───┬───┬─────┐ │
└──┬───┘ └──┬───┘ └──┬───┘           │  │ 0 │ 1 │ 2 │ ... │ │
   │        │        │                │  └───┴───┴───┴─────┘ │
   v        v        v                └──────────┬───────────┘
 CPU      CPU      CPU                           │ GPU
 step     step     step                      one batched step
```

- `num_envs` controls how many parallel environments
- All environments share one PhysX scene on GPU
- A single `env.step(actions)` advances ALL envs simultaneously
- Observation: `Tensor(num_envs, obs_dim)` on GPU
- Action: `Tensor(num_envs, act_dim)` on GPU
- Reward: `Tensor(num_envs,)` on GPU

**Scaling behavior** (RTX 5090, 32GB):
- CartPole: up to 8192 envs comfortably
- Ant: up to 4096 envs
- Complex humanoid: 1024-2048 envs
- Throughput scales near-linearly until GPU saturates, then diminishing returns

## 6. The Step Loop

```python
# Inside ManagerBasedRLEnv.step():
1. ActionManager.process(actions)     # decode raw -> joint commands
2. SimulationContext.step()            # advance PhysX (GPU)
3. Scene.update(dt)                    # read new state from PhysX
4. ObservationManager.compute()        # obs = concat(terms...)
5. RewardManager.compute()             # reward = sum(weight * term)
6. TerminationManager.compute()        # done mask
7. Auto-reset terminated envs          # selective per-env reset
```

Auto-reset is key: when env `i` terminates, only env `i` is reset. Other envs continue uninterrupted. No global `env.reset()` needed during training.

## 7. Configuration Pattern (@configclass)

Isaac Lab uses a decorator `@configclass` (similar to `@dataclass`) for all configuration:

```python
from isaaclab.utils import configclass

@configclass
class CartpoleEnvCfg(ManagerBasedRLEnvCfg):
    scene: CartpoleSceneCfg = CartpoleSceneCfg(num_envs=2048, env_spacing=4.0)
    observations: ObservationsCfg = ObservationsCfg()
    actions: ActionsCfg = ActionsCfg()
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()
    events: EventsCfg = EventsCfg()
```

Benefits:
- Entire env behavior is a single config object
- Override any field at runtime: `cfg.scene.num_envs = 4096`
- Serializable for experiment tracking
- No code changes needed to modify rewards, observations, etc.

## 8. RL Framework Integration

Isaac Lab environments are wrapped as Gymnasium envs, compatible with any RL library:

```python
import gymnasium as gym
env = gym.make("Isaac-Cartpole-v0", cfg=env_cfg)
```

Supported frameworks:
| Framework | Config Style | Strengths |
|-----------|-------------|-----------|
| RL Games | YAML | Fastest, NVIDIA-maintained, production-ready |
| SKRL | Python | Most Pythonic, easy to customize |
| RSL-RL | Python | ETH Zurich, legged locomotion focus |
| Stable Baselines3 | Python | Largest community, most algorithms |

## 9. Key Source Code Locations

| Component | Path (on Docker instance) |
|-----------|---------------------------|
| Env base classes | `/opt/IsaacLab/source/isaaclab/isaaclab/envs/` |
| Manager implementations | `/opt/IsaacLab/source/isaaclab/isaaclab/managers/` |
| MDP term functions | `/opt/IsaacLab/source/isaaclab/isaaclab/envs/mdp/` |
| Built-in task configs | `/opt/IsaacLab/source/isaaclab_tasks/isaaclab_tasks/` |
| RL training scripts | `/opt/IsaacLab/scripts/reinforcement_learning/` |
| Scene utilities | `/opt/IsaacLab/source/isaaclab/isaaclab/scene/` |
| Asset configs | `/opt/IsaacLab/source/isaaclab/isaaclab/assets/` |
