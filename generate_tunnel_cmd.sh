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
#   8211           — WebRTC web client (--livestream 2)
#   8899           — WebSocket streaming (--livestream 1, optional)
#   47995-48012    — Omniverse native streaming media ports
# ---------------------------------------------------------------------------
echo "============================================================"
echo "  SSH Tunnel for Isaac Sim WebRTC Streaming"
echo "============================================================"
echo ""
echo "Run one of these on your LOCAL machine:"
echo ""
echo "--- Minimal (WebRTC browser streaming only) ---------------"
echo ""
echo "  ssh -p ${SSH_PORT} -L 8211:localhost:8211 root@${PUBLIC_IP}"
echo ""
echo "--- Full (includes native streaming ports) -----------------"
echo ""
printf "  ssh -p %s \\\\\n" "$SSH_PORT"
printf "    -L 8211:localhost:8211 \\\\\n"
printf "    -L 8899:localhost:8899 \\\\\n"

for port in $(seq 47995 48012); do
    printf "    -L %s:localhost:%s \\\\\n" "$port" "$port"
done

printf "    root@%s\n" "$PUBLIC_IP"

echo ""
echo "------------------------------------------------------------"
echo "After the tunnel is active, open in your browser:"
echo ""
echo "  http://localhost:8211/streaming/webrtc-client"
echo ""
echo "------------------------------------------------------------"

if [[ "$SSH_PORT" == "<VAST_PORT>" || "$PUBLIC_IP" == "<VAST_IP>" ]]; then
    echo ""
    echo "NOTE: Could not auto-detect SSH port or IP."
    echo "      Find them in the Vast.ai dashboard under your instance."
    echo "      Re-run:  bash generate_tunnel_cmd.sh <SSH_PORT>"
fi
