#!/usr/bin/env bash
set -euo pipefail

SSH_HOST="${VAST_SSH_HOST:-${PUBLIC_IPADDR:-${VAST_IP:-<VAST_IP>}}}"
SSH_PORT="${VAST_TCP_PORT_22:-${VAST_PORT:-<VAST_PORT>}}"

FORWARD_ARGS=("-L" "8200:localhost:8200")

for ((port=47995; port<=48012; port++)); do
    FORWARD_ARGS+=("-L" "${port}:localhost:${port}")
done

printf 'ssh -p %s' "$SSH_PORT"
for arg in "${FORWARD_ARGS[@]}"; do
    printf ' %s' "$arg"
done
printf ' root@%s\n' "$SSH_HOST"
