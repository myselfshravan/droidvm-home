#!/bin/bash

# ----------------------------
# Startup script for DroidVM + Cloudflare Tunnel
# ----------------------------

# --- TMUX session names ---
API_SESSION="droidvm-tools"
TUNNEL_SESSION="cloudflared"
APP_SESSION="droidvm-demo"

# --- Paths to commands ---
# Adjust if your commands are in different locations
CLOUDFLARED="/usr/local/bin/cloudflared"
UVICORN="uvicorn"

# --- Ports ---
API_PORT=8000
APP_PORT=8090

# --- Docker / Python app paths ---
API_DIR="/data/data/com.termux/files/home/droidvm-tools"
APP_DIR="/data/data/com.termux/files/home/droidvm-demo"  # optional, if you have a second app

# --- Tunnel name ---
TUNNEL_NAME="shravan-tunnel"

# ----------------------------
# Function to create tmux session if not exists
# ----------------------------
function start_tmux_session() {
    local session_name=$1
    local command=$2

    tmux has-session -t "$session_name" 2>/dev/null
    if [ $? != 0 ]; then
        echo "Starting tmux session: $session_name"
        tmux new-session -d -s "$session_name" "$command"
    else
        echo "Tmux session $session_name already running"
    fi
}

# ----------------------------
# Start DroidVM Tools API
# ----------------------------
start_tmux_session "$API_SESSION" "cd $API_DIR && $UVICORN main:app --host 0.0.0.0 --port $API_PORT"

# Optional: start second app on 8090
# start_tmux_session "app-session" "cd $APP_DIR && $UVICORN main:app --host 0.0.0.0 --port $APP_PORT"

# ----------------------------
# Start Cloudflare Tunnel
# ----------------------------
start_tmux_session "$TUNNEL_SESSION" "$CLOUDFLARED tunnel run $TUNNEL_NAME"

# ----------------------------
echo "Startup script completed."
echo "Check sessions with: tmux ls"
echo "Attach to a session: tmux attach -t <session_name>"
