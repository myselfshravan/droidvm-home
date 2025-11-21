"""FastAPI server for DroidVM management and monitoring."""

import os
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from droidvm_tools.tools import system, network

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="DroidVM Tools API",
    description="API for managing and monitoring Android phone as a tiny home server",
    version="0.1.0",
)

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint - API information."""
    return {
        "name": "DroidVM Tools API",
        "version": "0.1.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/system/info")
async def system_info() -> Dict[str, Any]:
    """Get comprehensive system information."""
    try:
        info = system.get_system_info()
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/system/cpu")
async def cpu_info() -> Dict[str, Any]:
    """Get CPU information and usage."""
    try:
        info = system.get_cpu_info()
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/system/memory")
async def memory_info() -> Dict[str, Any]:
    """Get memory usage information."""
    try:
        info = system.get_memory_info()
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/system/disk")
async def disk_info() -> Dict[str, Any]:
    """Get disk usage information."""
    try:
        info = system.get_disk_info()
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/system/battery")
async def battery_info() -> Dict[str, Any]:
    """Get battery information (if available)."""
    try:
        info = system.get_battery_info()
        if info is None:
            return {"success": True, "data": None, "message": "Battery info not available"}
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/system/processes")
async def process_info() -> Dict[str, Any]:
    """Get process count information."""
    try:
        info = system.get_process_count()
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/system/tmux")
async def tmux_sessions() -> Dict[str, Any]:
    """Get list of running tmux sessions."""
    try:
        sessions = system.get_tmux_sessions()
        return {"success": True, "data": sessions, "count": len(sessions)}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/network/info")
async def network_info() -> Dict[str, Any]:
    """Get network interface information."""
    try:
        info = network.get_network_info()
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/network/stats")
async def network_stats() -> Dict[str, Any]:
    """Get network I/O statistics."""
    try:
        stats = network.get_network_stats()
        return {"success": True, "data": stats}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/network/connections")
async def network_connections() -> Dict[str, Any]:
    """Get active network connections."""
    try:
        connections = network.get_connections()
        return {"success": True, "data": connections, "count": len(connections)}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/network/tailscale")
async def tailscale_status() -> Dict[str, Any]:
    """Get Tailscale VPN status."""
    try:
        status = network.get_tailscale_status()
        tailscale_ip = network.get_tailscale_ip()

        if status is None:
            return {
                "success": True,
                "data": None,
                "message": "Tailscale not installed or not running"
            }

        status["tailscale_ip"] = tailscale_ip
        return {"success": True, "data": status}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/network/ip")
async def ip_info() -> Dict[str, Any]:
    """Get IP address information."""
    try:
        return {
            "success": True,
            "data": {
                "hostname": network.get_hostname(),
                "tailscale_ip": network.get_tailscale_ip(),
                "public_ip": network.get_public_ip(),
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/network/wifi")
async def wifi_info() -> Dict[str, Any]:
    """Get WiFi connection information via Termux:API."""
    try:
        info = system.get_termux_wifi_info()
        if info is None:
            return {
                "success": True,
                "data": None,
                "message": "WiFi info not available (Termux:API required)"
            }
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/device/info")
async def device_info() -> Dict[str, Any]:
    """Get Android device information via Termux:API."""
    try:
        info = system.get_termux_device_info()
        if info is None:
            return {
                "success": True,
                "data": None,
                "message": "Device info not available (Termux:API required)"
            }
        return {"success": True, "data": info}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/status")
async def full_status() -> Dict[str, Any]:
    """Get comprehensive system status."""
    try:
        # Get Termux:API info
        wifi_info = system.get_termux_wifi_info()
        device_info = system.get_termux_device_info()

        # Get network info
        public_ip = network.get_public_ip()
        net_stats = network.get_network_stats()

        return {
            "success": True,
            "data": {
                "timestamp": datetime.now().isoformat(),
                "system": system.get_system_info(),
                "cpu": system.get_cpu_info(),
                "memory": system.get_memory_info(),
                "battery": system.get_battery_info(),
                "network": {
                    "tailscale_ip": network.get_tailscale_ip(),
                    "public_ip": public_ip,
                    "hostname": network.get_hostname(),
                    "wifi": wifi_info,
                    "stats": net_stats,
                },
                "device": device_info,
                "tmux_sessions": system.get_tmux_sessions(),
                "processes": system.get_process_count(),
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


def start():
    """Start the FastAPI server using uvicorn."""
    import uvicorn

    host = os.getenv("DROIDVM_HOST", "0.0.0.0")
    port = int(os.getenv("DROIDVM_PORT", "8000"))
    reload = os.getenv("DROIDVM_RELOAD", "false").lower() == "true"

    print(f"Starting DroidVM Tools API on {host}:{port}")
    print(f"Docs available at http://{host}:{port}/docs")

    uvicorn.run(
        "droidvm_tools.server:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    start()
