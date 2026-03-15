"""Isaac Lab-backed runtime for the Lab 01 foundations capstone."""

from __future__ import annotations

from lab_01_foundations.config.sim_cfg import Lab01Config

from .control import compute_capture_steps, generate_joint_targets
from .models import CapturedFrame, JointStateRecord, LabRunResult


class RuntimeUnavailableError(RuntimeError):
    """Raised when the Isaac Lab runtime cannot be used."""


def run_isaaclab_foundations(config: Lab01Config, device: str) -> LabRunResult:
    """Launch the actual Lab 01 scene in Isaac Lab and collect artifacts."""
    try:
        import isaaclab.sim as sim_utils
        import torch
        from isaaclab.actuators import ImplicitActuatorCfg
        from isaaclab.assets import AssetBaseCfg
        from isaaclab.assets.articulation import ArticulationCfg
        from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
        from isaaclab.sensors.camera import CameraCfg
        from isaaclab.utils import configclass
        from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
    except ImportError as exc:
        raise RuntimeUnavailableError(
            "Isaac Lab is not available. Run this script inside the Isaac Lab environment with `isaaclab -p`."
        ) from exc

    environment_usd = _expand_nucleus_path(config.scene.environment.usd_path, ISAAC_NUCLEUS_DIR)
    robot_usd = _expand_nucleus_path(config.scene.robot.usd_path, ISAAC_NUCLEUS_DIR)

    robot_cfg = ArticulationCfg(
        prim_path=config.scene.robot.prim_path,
        spawn=sim_utils.UsdFileCfg(
            usd_path=robot_usd,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(disable_gravity=False, max_depenetration_velocity=5.0),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(
                enabled_self_collisions=False,
                solver_position_iteration_count=8,
                solver_velocity_iteration_count=0,
            ),
        ),
        init_state=ArticulationCfg.InitialStateCfg(
            pos=config.scene.robot.base_position,
            rot=config.scene.robot.base_orientation,
            joint_pos={".*": 0.0},
            joint_vel={".*": 0.0},
        ),
        actuators={"arm": ImplicitActuatorCfg(joint_names_expr=[".*"], stiffness=None, damping=None)},
    )

    @configclass
    class FoundationsSceneCfg(InteractiveSceneCfg):
        ground = AssetBaseCfg(prim_path="/World/defaultGroundPlane", spawn=sim_utils.GroundPlaneCfg())
        dome_light = AssetBaseCfg(
            prim_path="/World/Light",
            spawn=sim_utils.DomeLightCfg(intensity=3000.0, color=(0.75, 0.75, 0.75)),
        )
        warehouse = AssetBaseCfg(
            prim_path=config.scene.environment.prim_path,
            spawn=sim_utils.UsdFileCfg(usd_path=environment_usd),
            init_state=AssetBaseCfg.InitialStateCfg(
                pos=config.scene.environment.translation,
                rot=config.scene.environment.orientation,
            ),
        )
        table = AssetBaseCfg(
            prim_path=config.scene.table.prim_path,
            spawn=sim_utils.CuboidCfg(
                size=config.scene.table.size,
                rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
                collision_props=sim_utils.CollisionPropertiesCfg(),
                visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=config.scene.table.color),
            ),
            init_state=AssetBaseCfg.InitialStateCfg(pos=config.scene.table.position),
        )
        robot = robot_cfg
        camera = CameraCfg(
            prim_path=config.scene.camera.prim_path,
            update_period=0.0,
            width=config.scene.camera.width,
            height=config.scene.camera.height,
            data_types=["rgb"],
            spawn=sim_utils.PinholeCameraCfg(
                focal_length=24.0,
                focus_distance=400.0,
                horizontal_aperture=20.955,
                clipping_range=(0.1, 1.0e5),
            ),
            offset=CameraCfg.OffsetCfg(
                pos=config.scene.camera.position,
                rot=config.scene.camera.orientation,
                convention=config.scene.camera.convention,
            ),
        )

    sim = sim_utils.SimulationContext(
        sim_utils.SimulationCfg(
            device=device,
            dt=config.runtime.physics_dt,
            render_interval=config.runtime.render_interval,
        )
    )
    sim.set_camera_view([2.5, -2.0, 1.8], [0.55, 0.0, 0.9])
    scene = InteractiveScene(FoundationsSceneCfg(num_envs=1, env_spacing=2.0))
    sim.reset()
    scene.update(config.runtime.physics_dt)

    robot = scene["robot"]
    camera = scene["camera"]
    arm_joint_count = len(config.scene.robot.joint_names)
    base_joint_positions = tuple(float(value) for value in robot.data.default_joint_pos[0, :arm_joint_count].tolist())
    capture_steps = set(compute_capture_steps(config.runtime.step_count, config.scene.camera.frame_count))

    joint_records: list[JointStateRecord] = []
    frames: list[CapturedFrame] = []
    for step in range(config.runtime.step_count):
        sim_time_s = (step + 1) * config.runtime.physics_dt
        joint_targets = generate_joint_targets(
            base_joint_positions,
            config.scene.robot.joint_amplitudes_rad,
            config.scene.robot.joint_phase_offsets_rad,
            config.scene.robot.trajectory_frequency_hz,
            sim_time_s,
        )
        target_tensor = robot.data.default_joint_pos.clone()
        target_tensor[:, :arm_joint_count] = torch.tensor(joint_targets, device=target_tensor.device).unsqueeze(0)
        robot.set_joint_position_target(target_tensor)
        scene.write_data_to_sim()
        sim.step()
        scene.update(config.runtime.physics_dt)

        joint_records.append(
            JointStateRecord(
                step=step,
                sim_time_s=round(sim_time_s, 6),
                joint_targets_rad=joint_targets,
                joint_positions_rad=tuple(float(value) for value in robot.data.joint_pos[0, :arm_joint_count].tolist()),
                joint_velocities_rad_s=tuple(float(value) for value in robot.data.joint_vel[0, :arm_joint_count].tolist()),
            )
        )
        if step in capture_steps:
            frames.append(
                CapturedFrame(
                    frame_index=len(frames),
                    step=step,
                    width=config.scene.camera.width,
                    height=config.scene.camera.height,
                    rgb_bytes=_tensor_to_rgb_bytes(camera.data.output["rgb"][0], torch),
                )
            )

    return LabRunResult(
        runtime_name="isaaclab",
        joint_names=config.scene.robot.joint_names,
        joint_state_records=tuple(joint_records),
        captured_frames=tuple(frames),
        metadata={
            "mock_runtime": False,
            "device": device,
            "robot_prim_path": config.scene.robot.prim_path,
            "camera_prim_path": config.scene.camera.prim_path,
        },
    )


def _expand_nucleus_path(asset_path: str, nucleus_root: str) -> str:
    """Expand `${ISAAC_NUCLEUS_DIR}` placeholders when present."""
    return asset_path.replace("${ISAAC_NUCLEUS_DIR}", nucleus_root)


def _tensor_to_rgb_bytes(rgb_tensor: object, torch_module: object) -> bytes:
    """Convert Isaac Lab camera output into packed RGB bytes."""
    tensor = rgb_tensor.detach().to(device="cpu")  # type: ignore[union-attr]
    if tensor.shape[-1] > 3:  # type: ignore[index]
        tensor = tensor[..., :3]
    tensor = tensor.clamp(0, 255).to(dtype=torch_module.uint8).contiguous()  # type: ignore[attr-defined]
    try:
        return tensor.numpy().tobytes()
    except AttributeError:
        return bytes(tensor.view(-1).tolist())
