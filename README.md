# DroidVM Tools

A modern Python toolkit for managing an Android phone (vivo V2158) running Termux as a tiny home server.

## About DroidVM

This is a folder in the "DroidVM" - an old Android 14 phone (vivo V2158) running Termux as a tiny home server.

**Device Details:**
- SSH server on port `8022` | user: `u0_a315`
- Python 3.12 installed
- Termux home folder: `/data/data/com.termux/files/home`
- Project folder: `/data/data/com.termux/files/home/droidvm-tools`

**Access Methods:**
- Local network: `ssh -p 8022 u0_a315@192.168.1.45`
- Via Tailscale VPN: `ssh -p 8022 u0_a315@100.94.102.37` (account: droidvmtailscale@gmail.com)

I use tmux for long-running processes (FastAPI / scripts) and Tailscale for VPN to access the phone from other devices on different networks.

## Features

### FastAPI Server
- RESTful API for remote system monitoring and management
- Health checks and status endpoints
- System resource monitoring (CPU, memory, disk, battery)
- Network information and Tailscale status
- Tmux session management
- Auto-generated API docs at `/docs`

### CLI Tools
- `droidvm-tools info` - System information
- `droidvm-tools cpu` - CPU usage and details
- `droidvm-tools memory` - Memory usage
- `droidvm-tools disk` - Disk usage
- `droidvm-tools battery` - Battery status
- `droidvm-tools network` - Network interfaces
- `droidvm-tools netstat` - Network statistics
- `droidvm-tools tailscale` - Tailscale VPN status
- `droidvm-tools tmux` - List tmux sessions
- `droidvm-tools status` - Comprehensive status (use `--json` for JSON output)
- `droidvm-tools version` - Version information

## Installation

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Clone and Setup
```bash
# Clone the repository (or sync to your device)
git clone <repository-url> droidvm-tools
cd droidvm-tools

# Install dependencies using uv
uv sync
```

### Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env to customize settings (optional)
nano .env
```

## Usage

### Starting the FastAPI Server

**Development mode (with auto-reload):**
```bash
uv run start-server
```

Or set `DROIDVM_RELOAD=true` in `.env` for persistent development mode.

**Production mode (in tmux for long-running):**
```bash
# Start a new tmux session
tmux new -s droidvm-server

# Inside tmux, start the server
uv run start-server

# Detach from tmux: Ctrl+B, then D
```

The server will be available at:
- Local: `http://localhost:8000`
- Network: `http://192.168.1.45:8000`
- Tailscale: `http://100.94.102.37:8000`
- API Docs: `http://<host>:8000/docs`

### Using CLI Tools

```bash
# Show comprehensive system status
uv run droidvm-tools status

# Show CPU information
uv run droidvm-tools cpu

# Show memory usage
uv run droidvm-tools memory

# Show battery status (Android-specific)
uv run droidvm-tools battery

# Show Tailscale VPN status
uv run droidvm-tools tailscale

# List tmux sessions
uv run droidvm-tools tmux

# Get status as JSON
uv run droidvm-tools status --json
```

## API Endpoints

### System Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /status` - Comprehensive system status
- `GET /system/info` - System information
- `GET /system/cpu` - CPU usage and details
- `GET /system/memory` - Memory usage
- `GET /system/disk` - Disk usage
- `GET /system/battery` - Battery status (if available)
- `GET /system/processes` - Process counts
- `GET /system/tmux` - List tmux sessions

### Network Endpoints
- `GET /network/info` - Network interface information
- `GET /network/stats` - Network I/O statistics
- `GET /network/connections` - Active connections
- `GET /network/tailscale` - Tailscale VPN status
- `GET /network/ip` - IP addresses (hostname, Tailscale, public)

### Example API Calls
```bash
# Health check
curl http://localhost:8000/health

# Get full system status
curl http://localhost:8000/status | jq

# Get CPU info
curl http://localhost:8000/system/cpu | jq

# Get Tailscale status
curl http://localhost:8000/network/tailscale | jq
```

## Deployment to Android Device

### Option 1: Clone via Git (Recommended)
```bash
# SSH into your Android device
ssh -p 8022 u0_a315@192.168.1.45

# Navigate to home directory
cd /data/data/com.termux/files/home

# Clone the repository
git clone <repository-url> droidvm-tools
cd droidvm-tools

# Install dependencies
uv sync
```

### Option 2: Copy via SCP
```bash
# From your local machine, copy the project
scp -P 8022 -r droidvm-tools u0_a315@192.168.1.45:/data/data/com.termux/files/home/

# SSH into the device and install
ssh -p 8022 u0_a315@192.168.1.45
cd /data/data/com.termux/files/home/droidvm-tools
uv sync
```

## Running in Production

### Using tmux for Persistent Server
```bash
# SSH into device
ssh -p 8022 u0_a315@192.168.1.45

# Create a new tmux session for the server
tmux new -s droidvm-api

# Start the server
cd /data/data/com.termux/files/home/droidvm-tools
uv run start-server

# Detach from tmux: Ctrl+B, then D

# Later, reattach to check on the server
tmux attach -t droidvm-api

# List all tmux sessions
tmux ls
```

### Access Server from Other Devices
```bash
# Via local network
curl http://192.168.1.45:8000/status

# Via Tailscale VPN (from anywhere)
curl http://100.94.102.37:8000/status

# Open in browser for interactive API docs
# http://100.94.102.37:8000/docs
```

## Development

### Project Structure
```
droidvm-tools/
├── src/
│   └── droidvm_tools/
│       ├── __init__.py
│       ├── server.py          # FastAPI server
│       ├── cli.py             # CLI interface
│       └── tools/
│           ├── __init__.py
│           ├── system.py      # System monitoring
│           └── network.py     # Network tools
├── tests/
├── pyproject.toml             # uv configuration
├── .env.example               # Example configuration
├── .gitignore
└── README.md
```

### Adding New Features

1. **Add system monitoring functions** in `src/droidvm_tools/tools/system.py`
2. **Add network utilities** in `src/droidvm_tools/tools/network.py`
3. **Add API endpoints** in `src/droidvm_tools/server.py`
4. **Add CLI commands** in `src/droidvm_tools/cli.py`

### Running Tests
```bash
# Install dev dependencies
uv sync

# Run tests
uv run pytest
```

## Configuration Options

Environment variables (set in `.env`):

- `DROIDVM_HOST` - Server host (default: `0.0.0.0`)
- `DROIDVM_PORT` - Server port (default: `8000`)
- `DROIDVM_RELOAD` - Enable auto-reload for development (default: `false`)

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use: `lsof -i :8000` or `netstat -tuln | grep 8000`
- Try a different port: `DROIDVM_PORT=8001 uv run start-server`

### Can't access server from network
- Ensure `DROIDVM_HOST=0.0.0.0` in `.env`
- Check firewall settings on Termux
- Verify network connectivity

### Tailscale status shows nothing
- Ensure Tailscale is installed and running on the device
- Check Tailscale status: `tailscale status`
- Authenticate if needed: `tailscale up`

### CLI commands not found
**Always use `uv run` prefix on Termux:**
```bash
# Correct
uv run droidvm-tools status

# Alternative: use the wrapper script
./droidvm-tools status
```

### Permission denied errors (Termux-specific)
Some system metrics may show "Permission denied" or "N/A" on Android/Termux due to restricted `/proc` access. This is normal and the app handles these gracefully:
- CPU frequency might not be available
- Some system stats may be limited
- Battery info works via Android-specific APIs
- Most features still work fine!

**Note**: The app is designed to gracefully handle Termux permission restrictions.

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
