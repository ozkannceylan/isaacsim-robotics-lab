#!/usr/bin/env bash
# =============================================================================
# generate_tunnel_cmd.sh — Print the SSH tunnel command for WebRTC streaming
#
# Run this ON the Vast.ai instance. Copy the output and run it on your LOCAL
# machine to forward the Isaac Sim streaming ports.
#
# Usage:
#   bash generate_tunnel_cmd.sh              # auto-detect IP, prompt for port
#   bash generate_tunnel_cmd.sh 12345        # specify SSH port directly
#   SSH_PORT=12345 bash generate_tunnel_cmd.sh
# =============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Detect public IP
# ---------------------------------------------------------------------------
PUBLIC_IP=""

# Try Vast.ai env vars first
if [[ -n "${PUBLIC_IPADDR:-}" ]]; then
    PUBLIC_IP="$PUBLIC_IPADDR"
elif [[ -n "${VAST_SSH_HOST:-}" ]]; then
    PUBLIC_IP="$VAST_SSH_HOST"
fi

# Fall back to external IP lookup
if [[ -z "$PUBLIC_IP" ]]; then
    PUBLIC_IP=$(curl -s --max-time 5 ifconfig.me 2>/dev/null || true)
fi

if [[ -z "$PUBLIC_IP" ]]; then
    PUBLIC_IP="<VAST_IP>"
fi

# ---------------------------------------------------------------------------
# Detect SSH port
# ---------------------------------------------------------------------------
if [[ $# -ge 1 && "$1" =~ ^[0-9]+$ ]]; then
    SSH_PORT="$1"
elif [[ -n "${VAST_TCP_PORT_22:-}" ]]; then
    SSH_PORT="$VAST_TCP_PORT_22"
elif [[ -n "${VAST_PORT:-}" ]]; then
    SSH_PORT="$VAST_PORT"
else
    SSH_PORT="<VAST_PORT>"
fi

# ---------------------------------------------------------------------------
# Print tunnel commands
#
# Ports:
#   8011    — HTTP API (health check, Swagger docs)
#   49100   — WebRTC signaling (Kit Remote connects here)
# ---------------------------------------------------------------------------
echo "============================================================"
echo "  SSH Tunnel for Isaac Sim WebRTC Streaming"
echo "============================================================"
echo ""
echo "Run this on your LOCAL machine:"
echo ""
echo "  ssh -p ${SSH_PORT} -L 8011:localhost:8011 -L 49100:localhost:49100 root@${PUBLIC_IP}"
echo ""
echo "------------------------------------------------------------"
echo "After the tunnel is active:"
echo ""
echo "  1. Install 'Kit Remote' from NVIDIA Omniverse Launcher"
echo "     (Isaac Sim 5.1 pip install has no browser viewer)"
echo ""
echo "  2. In Kit Remote, connect to: localhost:49100"
echo ""
echo "  3. Health check (browser): http://localhost:8011/v1/streaming/ready"
echo "     API docs (Swagger):     http://localhost:8011/docs"
echo ""
echo "------------------------------------------------------------"

if [[ "$SSH_PORT" == "<VAST_PORT>" || "$PUBLIC_IP" == "<VAST_IP>" ]]; then
    echo ""
    echo "NOTE: Could not auto-detect SSH port or IP."
    echo "      Find them in the Vast.ai dashboard under your instance."
    echo "      Re-run:  bash generate_tunnel_cmd.sh <SSH_PORT>"
fi
