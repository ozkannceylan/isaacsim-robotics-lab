# Lab 3: Sensor Simulation and Synthetic Data

## Objective

Master Isaac Sim's RTX-powered sensor simulation and Replicator-based synthetic data generation. This is the capability that justifies Isaac Sim over MuJoCo: physically accurate cameras, LiDAR, and automated dataset creation.

## Why This Lab Exists

Sim-to-real transfer in manipulation and navigation depends on realistic sensor data. Isaac Sim's RTX rendering produces camera outputs that closely match real cameras. Replicator generates annotated datasets at scale. These are differentiating skills for robotics AI engineering roles.

## Prerequisites

- Lab 2 complete (custom G1 environment running)
- Understanding of computer vision basics (RGB, depth, segmentation)
- Familiarity with COCO/KITTI annotation formats

## Deliverables

1. RTX camera mounted on G1 with RGB + depth + segmentation outputs
2. LiDAR simulation on G1 with point cloud visualization
3. Contact sensor integration for grasp detection
4. Synthetic dataset (1000+ annotated frames) using Replicator
5. Data quality analysis: synthetic vs real-world comparison

## Tasks

### 3.1 RTX Camera Setup

Mount and configure cameras on the G1:

- Wrist camera: attached to G1's end-effector for manipulation
- Head camera: forward-facing for navigation
- Configure resolution, FOV, near/far planes
- Capture RGB, depth, instance segmentation, semantic segmentation
- Verify RTX ray-traced rendering quality (vs rasterized)

### 3.2 Depth and Point Cloud Processing

Work with depth sensor outputs:

- Extract depth images from camera
- Convert depth to point cloud (camera intrinsics)
- Visualize point clouds in Isaac Sim
- Explore noise models: add realistic depth noise patterns

### 3.3 LiDAR Simulation

Configure LiDAR sensor on G1:

- Spinning LiDAR (e.g., Velodyne-style) configuration
- Point cloud output format and processing
- Compare LiDAR vs depth camera for different scenarios
- Measure simulation performance impact of LiDAR

### 3.4 Contact and Force Sensors

Integrate contact sensors for manipulation tasks:

- Contact sensor on G1's gripper/fingers
- Force/torque readings at key joints
- Use contact data as observation for RL (extends Lab 2 pick-and-place)
- IMU sensor for body state estimation

### 3.5 Replicator: Synthetic Data at Scale

Use NVIDIA Replicator to generate training datasets:

- Define randomization: object textures, lighting, camera pose, backgrounds
- Annotator setup: bounding boxes, segmentation masks, keypoints
- Generate 1000+ frames with full annotations
- Export in COCO format for downstream training
- Measure generation throughput (frames/second)

### 3.6 Data Quality Assessment

Evaluate the synthetic data:

- Visual inspection: do synthetic images look plausible?
- Train a simple object detector on synthetic data only
- Test on real images (if available) or held-out synthetic data
- Document the domain gap observations

## Key Isaac Sim Sensor Capabilities to Explore

| Sensor | Output | Use Case |
|--------|--------|----------|
| RTX Camera | RGB, depth, normals | Manipulation, navigation |
| Segmentation | Instance, semantic masks | Object detection training |
| LiDAR | 3D point cloud | SLAM, obstacle avoidance |
| Contact | Force vectors, contact points | Grasp detection |
| IMU | Acceleration, angular velocity | State estimation |
| Ray caster | Distance measurements | Custom proximity sensing |

## Performance Considerations

RTX sensor rendering is expensive. Document:
- FPS with 0, 1, 2, 4 cameras active
- Impact of resolution on performance
- Headless rendering for data generation (no display overhead)
- Batch rendering strategies for Replicator

## Success Criteria

- Camera outputs are visually correct (no artifacts, correct depth scale)
- LiDAR produces plausible point clouds
- Replicator generates 1000+ annotated frames without errors
- Performance impact of each sensor type is documented
- At least one downstream ML task uses the synthetic data

## Estimated Cloud Cost

8-10 hours at ~$0.30/hr = ~$2.40-3.00

## Notes

- This lab requires GUI mode for visual validation. Budget for higher VNC usage.
- RTX rendering is the main reason we need RT Core GPUs (RTX 4090). This lab would not work on A100/H100.
- Synthetic data generation is a highly marketable skill. Document thoroughly for portfolio.
