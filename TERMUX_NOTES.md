# Termux-Specific Notes for DroidVM Tools

## ✅ Successfully Running on Android!

Your DroidVM Tools is now working on Termux/Android with optimized compatibility.

## 🔧 Key Fixes Applied

### 1. Dependency Compatibility
- **Pydantic v1.x** instead of v2 (no Rust compilation needed!)
- **FastAPI 0.103.2** compatible with Pydantic v1
- All packages now install without requiring Rust/compilation

### 2. Permission Handling
The app now gracefully handles Termux permission restrictions:
- CPU frequency: Falls back to "N/A" if `/proc/cpuinfo` is restricted
- CPU usage: Uses minimal interval (0.1s) to avoid permission issues
- Memory stats: Handles swap permission errors
- Boot time: Shows "N/A" if `/proc/uptime` is inaccessible

**These are expected on Android and the app works fine!**

## 📱 Android/Termux Limitations

### What Works Perfectly ✅
- ✅ Memory usage monitoring
- ✅ Disk usage for all mounted partitions
- ✅ Network interfaces and statistics
- ✅ Tailscale VPN integration
- ✅ Process counting
- ✅ Tmux session management
- ✅ FastAPI server on any port
- ✅ Battery monitoring (Android-specific)

### What Has Limitations ⚠️
- ⚠️ CPU frequency might show "N/A" (Android restricts `/proc/cpuinfo`)
- ⚠️ Some CPU stats may be limited
- ⚠️ Boot time might show "N/A"

**Note**: These limitations are Android OS restrictions, not bugs!

## 🚀 Usage on Termux

### Always Use `uv run` Prefix
```bash
# Run CLI commands
uv run droidvm-tools status
uv run droidvm-tools cpu
uv run droidvm-tools memory

# Or use the wrapper script
./droidvm-tools status
```

### Server is Working!
Your server at http://100.94.102.37:8000 is successfully:
- ✅ Serving API requests
- ✅ Accessible via Tailscale
- ✅ Handling permission errors gracefully
- ✅ Providing all available metrics

## 📊 Testing the Installation

### Test the Server
```bash
# From any device connected to Tailscale:
curl http://100.94.102.37:8000/health
curl http://100.94.102.37:8000/status | jq

# Check specific endpoints
curl http://100.94.102.37:8000/system/memory | jq
curl http://100.94.102.37:8000/system/battery | jq
curl http://100.94.102.37:8000/network/tailscale | jq
```

### Test the CLI
```bash
# On your Android device (via SSH):
cd ~/droidvm-tools

# Test various commands
uv run droidvm-tools status
uv run droidvm-tools memory
uv run droidvm-tools battery
uv run droidvm-tools tailscale

# Get JSON output
uv run droidvm-tools status --json | jq
```

## 🔄 Managing the Server on Termux

### Start Server in tmux (Recommended)
```bash
# Create persistent session
tmux new -s droidvm-api

# Start server (inside tmux)
cd ~/droidvm-tools
uv run start-server

# Detach: Ctrl+B, then D

# Reattach anytime
tmux attach -t droidvm-api
```

### Check if Server is Running
```bash
# From Android device
netstat -tuln | grep 8000

# Or check tmux sessions
tmux ls
```

### View Server Logs
```bash
# Attach to tmux session
tmux attach -t droidvm-api
```

## 🌐 Accessing from Other Devices

### Via Tailscale (Works Anywhere)
```bash
# Browser
http://100.94.102.37:8000/docs

# Command line
curl http://100.94.102.37:8000/status
```

### Via Local Network (Same WiFi)
```bash
# Browser
http://192.168.1.45:8000/docs

# Command line
curl http://192.168.1.45:8000/status
```

## 📦 Updating the Project

### Update Code
```bash
cd ~/droidvm-tools
git pull  # if using git

# Or re-deploy from your dev machine
# (see deploy_to_droid.sh)
```

### Update Dependencies
```bash
cd ~/droidvm-tools
uv sync
```

### Restart Server
```bash
# If running in tmux
tmux attach -t droidvm-api
# Press Ctrl+C to stop
# Then restart:
uv run start-server
```

## 🐛 Common Issues & Solutions

### Issue: "command not found: droidvm-tools"
**Solution**: Use `uv run droidvm-tools` or `./droidvm-tools`

### Issue: Permission denied errors in API responses
**Solution**: Normal on Android! The app handles these gracefully.

### Issue: CPU frequency shows "N/A"
**Solution**: Expected on Android due to `/proc` restrictions.

### Issue: Server stops when SSH disconnects
**Solution**: Use tmux! See "Managing the Server" section above.

### Issue: Can't access server remotely
**Solution**:
1. Check Tailscale: `tailscale status`
2. Verify server is running: `netstat -tuln | grep 8000`
3. Check `.env` has `DROIDVM_HOST=0.0.0.0`

## 🎉 You're All Set!

Your DroidVM Tools is production-ready on Android/Termux with:
- ✅ FastAPI server accessible anywhere via Tailscale
- ✅ Rich CLI tools for system monitoring
- ✅ Graceful handling of Android/Termux limitations
- ✅ Easy deployment and management

Enjoy your Android home server! 📱🚀
