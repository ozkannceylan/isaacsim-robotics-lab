#!/usr/bin/env bash
# =============================================================================
# build_and_push.sh — Build and push the Isaac Sim Docker image
#
# Usage:
#   bash build_and_push.sh                  # default: ozkanceylan
#   bash build_and_push.sh myuser           # custom Docker Hub username
#   bash build_and_push.sh myuser mytag     # custom tag
# =============================================================================
set -euo pipefail

DOCKER_USER="${1:-ozkanceylan}"
TAG="${2:-latest}"
IMAGE="${DOCKER_USER}/isaacsim-robotics-lab:${TAG}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Building Docker image ==="
echo "  Image: $IMAGE"
echo "  Context: $SCRIPT_DIR"
echo ""

docker build -t "$IMAGE" "$SCRIPT_DIR"

echo ""
echo "=== Build complete ==="
echo ""

read -p "Push to Docker Hub? (y/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing $IMAGE..."
    docker push "$IMAGE"
    echo ""
    echo "=== Push complete ==="
    echo "  Image: $IMAGE"
    echo ""
    echo "  On Vast.ai, use this as your Docker image:"
    echo "  $IMAGE"
else
    echo "Skipped push. To push later:"
    echo "  docker push $IMAGE"
fi
