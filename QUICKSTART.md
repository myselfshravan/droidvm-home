# DroidVM Tools - Quick Start Guide

## ✅ Server is Running!

Your DroidVM Tools API is now live at:
- **Tailscale VPN**: http://100.94.102.37:8000
- **Local Network**: http://192.168.1.45:8000

## 📚 API Documentation

Visit the interactive API docs:
- **Swagger UI**: http://100.94.102.37:8000/docs
- **ReDoc**: http://100.94.102.37:8000/redoc

## 🔌 Available Endpoints

### Basic Endpoints
```bash
# Health check
curl http://100.94.102.37:8000/health

# Full system status
curl http://100.94.102.37:8000/status | jq
```

### System Information
```bash
# System info
curl http://100.94.102.37:8000/system/info | jq

# CPU usage
curl http://100.94.102.37:8000/system/cpu | jq

# Memory usage
curl http://100.94.102.37:8000/system/memory | jq

# Disk usage
curl http://100.94.102.37:8000/system/disk | jq

# Battery status (Android-specific)
curl http://100.94.102.37:8000/system/battery | jq

# Process counts
curl http://100.94.102.37:8000/system/processes | jq

# Tmux sessions
curl http://100.94.102.37:8000/system/tmux | jq
```

### Network Information
```bash
# Network interfaces
curl http://100.94.102.37:8000/network/info | jq

# Network I/O statistics
curl http://100.94.102.37:8000/network/stats | jq

# Active connections
curl http://100.94.102.37:8000/network/connections | jq

# Tailscale VPN status
curl http://100.94.102.37:8000/network/tailscale | jq

# IP addresses
curl http://100.94.102.37:8000/network/ip | jq
```

## 🖥️ CLI Commands (On Device)

SSH into your device and run:

```bash
# Show comprehensive status
uv run droidvm-tools status

# Show status as JSON
uv run droidvm-tools status --json

# CPU information
uv run droidvm-tools cpu

# Memory usage
uv run droidvm-tools memory

# Disk usage
uv run droidvm-tools disk

# Battery status
uv run droidvm-tools battery

# Network interfaces
uv run droidvm-tools network

# Network statistics
uv run droidvm-tools netstat

# Tailscale VPN status
uv run droidvm-tools tailscale

# List tmux sessions
uv run droidvm-tools tmux

# Version info
uv run droidvm-tools version
```

## 🔄 Managing the Server

### Running in tmux (Persistent)
```bash
# Create a new tmux session
tmux new -s droidvm-api

# Start the server (inside tmux)
uv run start-server

# Detach from tmux: Press Ctrl+B, then D

# Reattach to check on the server
tmux attach -t droidvm-api

# List all sessions
tmux ls
```

### Stopping the Server
```bash
# If running in foreground: Ctrl+C

# If running in tmux:
tmux attach -t droidvm-api
# Then press Ctrl+C
```

### Viewing Logs
```bash
# If running in tmux, attach to see logs
tmux attach -t droidvm-api
```

## 🌐 Access from Anywhere

### Via Tailscale (Recommended)
Connect to Tailscale VPN, then access:
- http://100.94.102.37:8000
- Works from any network!

### Via Local Network
Only works when on the same WiFi:
- http://192.168.1.45:8000

## 🛠️ Troubleshooting

### Server won't start
```bash
# Check if port is in use
netstat -tuln | grep 8000

# Use a different port
DROIDVM_PORT=8001 uv run start-server
```

### Can't access remotely
1. Ensure Tailscale is running: `tailscale status`
2. Check firewall settings in Termux
3. Verify server is listening on 0.0.0.0: check `.env` file

### Update dependencies
```bash
cd ~/droidvm-tools
uv sync
```

## 📊 Example API Response

```json
{
  "success": true,
  "data": {
    "timestamp": "2025-11-15T17:46:03.702307",
    "system": {
      "hostname": "localhost",
      "platform": "Linux",
      "python_version": "3.12.12"
    },
    "cpu": {
      "cpu_usage_percent": 15.2
    },
    "memory": {
      "percentage": 45.6
    },
    "battery": {
      "percentage": 85,
      "power_plugged": false
    }
  }
}
```

## 🚀 Next Steps

1. **Bookmark the API docs**: http://100.94.102.37:8000/docs
2. **Set up autostart**: Add to termux-boot if needed
3. **Monitor**: Use the CLI tools to check system health
4. **Extend**: Add custom endpoints in `src/droidvm_tools/server.py`

Enjoy your DroidVM home server! 🎉
