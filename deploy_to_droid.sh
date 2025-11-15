#!/bin/bash
# Deploy DroidVM Tools to Android device

# Configuration
REMOTE_USER="u0_a315"
REMOTE_HOST="192.168.1.45"
REMOTE_PORT="8022"
REMOTE_PATH="/data/data/com.termux/files/home/droidvm-tools"

echo "DroidVM Tools Deployment Script"
echo "================================"
echo ""
echo "Deploying to: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PORT}"
echo "Remote path: ${REMOTE_PATH}"
echo ""

# Check if using Tailscale
if [ "$1" == "--tailscale" ]; then
    REMOTE_HOST="100.94.102.37"
    echo "Using Tailscale VPN address: ${REMOTE_HOST}"
    echo ""
fi

# Exclude unnecessary files and directories
EXCLUDE_DIRS=".git .venv .pytest_cache __pycache__ .DS_Store *.pyc .env"

RSYNC_EXCLUDE=""
for dir in $EXCLUDE_DIRS; do
    RSYNC_EXCLUDE="$RSYNC_EXCLUDE --exclude='$dir'"
done

echo "Syncing files to remote device..."
rsync -avz --progress \
    -e "ssh -p ${REMOTE_PORT}" \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='.pytest_cache' \
    --exclude='__pycache__' \
    --exclude='.DS_Store' \
    --exclude='*.pyc' \
    --exclude='.env' \
    ./ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Files synced successfully!"
    echo ""
    echo "Next steps:"
    echo "1. SSH into your device:"
    echo "   ssh -p ${REMOTE_PORT} ${REMOTE_USER}@${REMOTE_HOST}"
    echo ""
    echo "2. Navigate to project directory:"
    echo "   cd ${REMOTE_PATH}"
    echo ""
    echo "3. Install dependencies:"
    echo "   uv sync"
    echo ""
    echo "4. Start the server (in tmux for persistence):"
    echo "   tmux new -s droidvm-api"
    echo "   uv run start-server"
    echo "   # Press Ctrl+B then D to detach"
    echo ""
else
    echo ""
    echo "✗ Deployment failed!"
    exit 1
fi
