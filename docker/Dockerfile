# =============================================================================
# Dockerfile - Isaac Sim 5.1 + Isaac Lab 2.3.0 for Vast.ai
#
# Base: NVIDIA CUDA runtime (Ubuntu 22.04)
# Produces: ozkanceylan/isaacsim-robotics-lab:latest
#
# Build:
#   docker build -t ozkanceylan/isaacsim-robotics-lab:latest .
#
# Note: Project code is NOT baked in -- it's cloned via vastai_onstart.sh
# =============================================================================

FROM nvidia/cuda:12.8.0-devel-ubuntu22.04

LABEL maintainer="ozkanceylan"
LABEL description="Isaac Sim 5.1 + Isaac Lab 2.3.0 development environment for Vast.ai"

# Prevent interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# ---------------------------------------------------------------------------
# System dependencies
# ---------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        curl \
        wget \
        vim \
        htop \
        tmux \
        openssh-server \
        ca-certificates \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libgl1-mesa-glx \
        libglu1-mesa \
        libx11-6 \
        libxt6 \
        libvulkan1 \
        xvfb \
        x11vnc \
        sudo \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Miniconda
# ---------------------------------------------------------------------------
ENV CONDA_DIR=/opt/conda
RUN curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
        -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p $CONDA_DIR \
    && rm /tmp/miniconda.sh \
    && $CONDA_DIR/bin/conda init bash

ENV PATH=$CONDA_DIR/bin:$PATH

# Accept Anaconda TOS (required since mid-2025)
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main 2>/dev/null || true \
    && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r 2>/dev/null || true

# ---------------------------------------------------------------------------
# Conda environment: isaaclab (Python 3.11)
# ---------------------------------------------------------------------------
RUN conda create -n isaaclab python=3.11 -y
SHELL ["conda", "run", "-n", "isaaclab", "/bin/bash", "-c"]

# ---------------------------------------------------------------------------
# Isaac Sim 5.1.0
# ---------------------------------------------------------------------------
RUN pip install --no-cache-dir \
        "isaacsim[all,extscache]==5.1.0" \
        --extra-index-url https://pypi.nvidia.com

# ---------------------------------------------------------------------------
# Isaac Lab 2.3.0 from source
# ---------------------------------------------------------------------------
ENV ISAACLAB_DIR=/opt/IsaacLab
RUN git clone --depth 1 --branch v2.3.0 \
        https://github.com/isaac-sim/IsaacLab.git $ISAACLAB_DIR \
    && cd $ISAACLAB_DIR \
    && ./isaaclab.sh -i

# ---------------------------------------------------------------------------
# Install isaaclab core package (editable, needed for isaaclab.app import)
# ---------------------------------------------------------------------------
RUN cd $ISAACLAB_DIR/source/isaaclab && pip install --no-cache-dir -e . --no-build-isolation

# ---------------------------------------------------------------------------
# Accept NVIDIA Omniverse EULA non-interactively
# ---------------------------------------------------------------------------
RUN echo 'Y' | python -c "import isaacsim" 2>/dev/null || true

# ---------------------------------------------------------------------------
# PyTorch 2.7.0 with CUDA 12.8
# ---------------------------------------------------------------------------
RUN pip install --no-cache-dir \
        "torch==2.7.0" "torchvision==0.22.0" \
        --index-url https://download.pytorch.org/whl/cu128

# ---------------------------------------------------------------------------
# Additional Python packages
# ---------------------------------------------------------------------------
RUN pip install --no-cache-dir \
        matplotlib \
        tensorboard \
        onnxruntime-gpu \
        pytest

# ---------------------------------------------------------------------------
# Workspace setup
# ---------------------------------------------------------------------------
WORKDIR /workspace

# Create /data mount point for Vast.ai persistent volume
RUN mkdir -p /data/outputs /data/checkpoints /data/logs

# Copy on-start script
COPY vastai_onstart.sh /opt/vastai_onstart.sh
RUN chmod +x /opt/vastai_onstart.sh

# ---------------------------------------------------------------------------
# Environment defaults
# ---------------------------------------------------------------------------
# Auto-activate isaaclab env on bash login
RUN echo "conda activate isaaclab" >> /root/.bashrc
ENV ISAACLAB_DIR=/opt/IsaacLab

# Headless rendering by default
ENV DISPLAY=""

ENTRYPOINT ["/bin/bash"]
