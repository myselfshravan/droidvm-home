"""Network monitoring and Tailscale utilities."""

import socket
import subprocess
from typing import Dict, Any, Optional, List

import psutil


def get_network_info() -> Dict[str, Any]:
    """Get network interface information."""
    interfaces = {}

    # Get network interface addresses
    if_addrs = psutil.net_if_addrs()
    if_stats = psutil.net_if_stats()

    for interface_name, addresses in if_addrs.items():
        interface_info = {
            "addresses": [],
            "is_up": False,
            "speed": 0,
        }

        # Get interface stats
        if interface_name in if_stats:
            stats = if_stats[interface_name]
            interface_info["is_up"] = stats.isup
            interface_info["speed"] = stats.speed

        # Get addresses
        for addr in addresses:
            addr_info = {
                "family": str(addr.family),
                "address": addr.address,
            }
            if addr.netmask:
                addr_info["netmask"] = addr.netmask
            if addr.broadcast:
                addr_info["broadcast"] = addr.broadcast
            interface_info["addresses"].append(addr_info)

        interfaces[interface_name] = interface_info

    return {"interfaces": interfaces}


def get_network_stats() -> Dict[str, Any]:
    """Get network I/O statistics."""
    try:
        net_io = psutil.net_io_counters()
    except (PermissionError, OSError):
        return {
            "bytes_sent": "N/A",
            "bytes_recv": "N/A",
            "packets_sent": 0,
            "packets_recv": 0,
            "errors_in": 0,
            "errors_out": 0,
            "drop_in": 0,
            "drop_out": 0,
            "error": "Permission denied"
        }

    return {
        "bytes_sent": _bytes_to_human_readable(net_io.bytes_sent),
        "bytes_recv": _bytes_to_human_readable(net_io.bytes_recv),
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
        "errors_in": net_io.errin,
        "errors_out": net_io.errout,
        "drop_in": net_io.dropin,
        "drop_out": net_io.dropout,
    }


def get_connections() -> List[Dict[str, Any]]:
    """Get active network connections."""
    connections = []

    try:
        for conn in psutil.net_connections(kind='inet'):
            conn_info = {
                "family": str(conn.family),
                "type": str(conn.type),
                "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                "status": conn.status,
                "pid": conn.pid,
            }
            connections.append(conn_info)
    except psutil.AccessDenied:
        # Some systems require elevated permissions
        pass

    return connections


def get_tailscale_status() -> Optional[Dict[str, Any]]:
    """Get Tailscale VPN status and information."""
    try:
        # Check if tailscale is running
        result = subprocess.run(
            ["tailscale", "status", "--json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )

        import json
        status_data = json.loads(result.stdout)

        # Extract relevant information
        return {
            "connected": True,
            "backend_state": status_data.get("BackendState", "Unknown"),
            "self": status_data.get("Self", {}),
            "peers": len(status_data.get("Peer", {})),
            "health": status_data.get("Health", []),
        }

    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        # Tailscale not installed or not running
        return None


def get_tailscale_ip() -> Optional[str]:
    """Get the Tailscale IP address."""
    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None


def get_public_ip() -> Optional[str]:
    """Get the public IP address (best effort)."""
    try:
        import httpx
        response = httpx.get("https://api.ipify.org", timeout=5.0)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return None


def get_hostname() -> str:
    """Get the system hostname."""
    return socket.gethostname()


def _bytes_to_human_readable(bytes_value: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f}{unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f}PB"
