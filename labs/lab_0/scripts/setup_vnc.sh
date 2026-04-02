#!/usr/bin/env bash
# =============================================================================
# setup_vnc.sh - Optional VNC/noVNC Setup for GUI Access on Vast.ai
#
# Usage: bash setup_vnc.sh [--novnc]
#
# Installs TurboVNC + VirtualGL for GPU-accelerated remote desktop.
# Optionally installs noVNC for browser-based access.
#
# After running, connect via:
#   VNC:   ssh -L 5901:localhost:5901 root@<vast-ip> -p <port>
#          Then open VNC viewer -> localhost:5901
#   noVNC: ssh -L 6080:localhost:6080 root@<vast-ip> -p <port>
#          Then open browser -> http://localhost:6080/vnc.html
# =============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
VNC_DISPLAY=":1"
VNC_PORT="5901"
NOVNC_PORT="6080"
INSTALL_NOVNC=false
TURBOVNC_VERSION="3.1.2"
VIRTUALGL_VERSION="3.1.1"

# Parse args
for arg in "$@"; do
    case "$arg" in
        --novnc) INSTALL_NOVNC=true ;;
        *) echo "Unknown argument: $arg"; exit 1 ;;
    esac
done

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()   { echo -e "${GREEN}[OK]${NC}    $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail() { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

# Check root
if [[ $EUID -ne 0 ]]; then
    fail "This script must be run as root (sudo bash setup_vnc.sh)"
fi

# ---------------------------------------------------------------------------
# Step 1: Install dependencies
# ---------------------------------------------------------------------------
log "Installing system dependencies..."
apt-get update -qq
apt-get install -y -qq \
    wget \
    xorg \
    xfce4 \
    xfce4-terminal \
    dbus-x11 \
    x11-xserver-utils \
    libglu1-mesa \
    2>/dev/null
ok "System dependencies installed"

# ---------------------------------------------------------------------------
# Step 2: Install VirtualGL
# ---------------------------------------------------------------------------
if command -v vglrun &>/dev/null; then
    ok "VirtualGL already installed"
else
    log "Installing VirtualGL $VIRTUALGL_VERSION..."
    VGL_DEB="/tmp/virtualgl_${VIRTUALGL_VERSION}_amd64.deb"
    wget -q "https://github.com/VirtualGL/virtualgl/releases/download/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb" \
        -O "$VGL_DEB"
    dpkg -i "$VGL_DEB" 2>/dev/null || apt-get -f install -y -qq
    rm -f "$VGL_DEB"
    ok "VirtualGL installed"
fi

# Configure VirtualGL
log "Configuring VirtualGL..."
/opt/VirtualGL/bin/vglserver_config -config +s +f -t 2>/dev/null || true
ok "VirtualGL configured"

# ---------------------------------------------------------------------------
# Step 3: Install TurboVNC
# ---------------------------------------------------------------------------
if command -v /opt/TurboVNC/bin/vncserver &>/dev/null; then
    ok "TurboVNC already installed"
else
    log "Installing TurboVNC $TURBOVNC_VERSION..."
    TVNC_DEB="/tmp/turbovnc_${TURBOVNC_VERSION}_amd64.deb"
    wget -q "https://github.com/TurboVNC/turbovnc/releases/download/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb" \
        -O "$TVNC_DEB"
    dpkg -i "$TVNC_DEB" 2>/dev/null || apt-get -f install -y -qq
    rm -f "$TVNC_DEB"
    ok "TurboVNC installed"
fi

# ---------------------------------------------------------------------------
# Step 4: Start VNC server
# ---------------------------------------------------------------------------
log "Starting VNC server on display $VNC_DISPLAY (port $VNC_PORT)..."

# Kill existing VNC server on this display (idempotent)
/opt/TurboVNC/bin/vncserver -kill "$VNC_DISPLAY" 2>/dev/null || true

# Set VNC password (default: "isaac" - change this!)
mkdir -p "$HOME/.vnc"
echo "isaac" | /opt/TurboVNC/bin/vncpasswd -f > "$HOME/.vnc/passwd"
chmod 600 "$HOME/.vnc/passwd"

# Create xstartup for XFCE
cat > "$HOME/.vnc/xstartup" << 'XSTARTUP'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XDG_SESSION_TYPE=x11
exec startxfce4
XSTARTUP
chmod +x "$HOME/.vnc/xstartup"

# Start VNC server with VirtualGL support
/opt/TurboVNC/bin/vncserver "$VNC_DISPLAY" \
    -geometry 1920x1080 \
    -depth 24 \
    -securitytypes VncAuth
ok "VNC server running on port $VNC_PORT"

# ---------------------------------------------------------------------------
# Step 5: Install noVNC (optional)
# ---------------------------------------------------------------------------
if $INSTALL_NOVNC; then
    log "Installing noVNC for browser access..."
    NOVNC_DIR="/opt/noVNC"
    if [[ -d "$NOVNC_DIR" ]]; then
        ok "noVNC already installed"
    else
        git clone --depth 1 https://github.com/novnc/noVNC.git "$NOVNC_DIR"
        git clone --depth 1 https://github.com/novnc/websockify.git "$NOVNC_DIR/utils/websockify"
        ok "noVNC installed"
    fi

    # Kill existing noVNC (idempotent)
    pkill -f "websockify.*${NOVNC_PORT}" 2>/dev/null || true

    # Start noVNC
    log "Starting noVNC on port $NOVNC_PORT..."
    "$NOVNC_DIR/utils/novnc_proxy" \
        --vnc localhost:"$VNC_PORT" \
        --listen "$NOVNC_PORT" \
        &>/dev/null &
    disown
    ok "noVNC running on port $NOVNC_PORT"
fi

# ---------------------------------------------------------------------------
# Connection instructions
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo " VNC Connection Instructions"
echo "========================================"
echo ""
echo "  Default VNC password: isaac"
echo "  (Change it: /opt/TurboVNC/bin/vncpasswd)"
echo ""
echo "  Option A: VNC Viewer"
echo "  1. Create SSH tunnel from your local machine:"
echo "     ssh -L 5901:localhost:5901 root@<vast-ip> -p <port>"
echo "  2. Open VNC viewer and connect to: localhost:5901"
echo ""

if $INSTALL_NOVNC; then
    echo "  Option B: Browser (noVNC)"
    echo "  1. Create SSH tunnel from your local machine:"
    echo "     ssh -L 6080:localhost:6080 root@<vast-ip> -p <port>"
    echo "  2. Open browser: http://localhost:6080/vnc.html"
    echo ""
fi

echo "  To run Isaac Sim with GPU rendering through VNC:"
echo "     vglrun python <your_script>.py"
echo ""
echo "  To stop VNC server:"
echo "     /opt/TurboVNC/bin/vncserver -kill $VNC_DISPLAY"
echo ""
