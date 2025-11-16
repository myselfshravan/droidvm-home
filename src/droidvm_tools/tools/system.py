"""System monitoring and information utilities."""

import json
import os
import platform
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional

import psutil


def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information."""
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time()).isoformat()
    except (PermissionError, OSError):
        boot_time = "N/A"

    return {
        "hostname": platform.node(),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "boot_time": boot_time,
    }


def get_cpu_info() -> Dict[str, Any]:
    """Get CPU usage and information."""
    try:
        cpu_freq = psutil.cpu_freq()
    except (PermissionError, OSError):
        cpu_freq = None

    try:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        cpu_usage_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    except (PermissionError, OSError):
        cpu_usage = 0
        cpu_usage_per_core = []

    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": f"{cpu_freq.max:.2f}Mhz" if cpu_freq else "N/A",
        "min_frequency": f"{cpu_freq.min:.2f}Mhz" if cpu_freq else "N/A",
        "current_frequency": f"{cpu_freq.current:.2f}Mhz" if cpu_freq else "N/A",
        "cpu_usage_percent": cpu_usage,
        "cpu_usage_per_core": cpu_usage_per_core,
    }


def get_memory_info() -> Dict[str, Any]:
    """Get memory usage information."""
    try:
        svmem = psutil.virtual_memory()
    except (PermissionError, OSError):
        return {
            "total": "N/A",
            "available": "N/A",
            "used": "N/A",
            "percentage": 0,
            "swap_total": "N/A",
            "swap_used": "N/A",
            "swap_percentage": 0,
            "error": "Permission denied"
        }

    try:
        swap = psutil.swap_memory()
    except (PermissionError, OSError):
        swap = None

    return {
        "total": _bytes_to_human_readable(svmem.total),
        "available": _bytes_to_human_readable(svmem.available),
        "used": _bytes_to_human_readable(svmem.used),
        "percentage": svmem.percent,
        "swap_total": _bytes_to_human_readable(swap.total) if swap else "N/A",
        "swap_used": _bytes_to_human_readable(swap.used) if swap else "N/A",
        "swap_percentage": swap.percent if swap else 0,
    }


def get_disk_info() -> Dict[str, Any]:
    """Get disk usage information."""
    partitions = []

    try:
        disk_partitions = psutil.disk_partitions(all=True)
    except (PermissionError, OSError) as e:
        # Termux/Android may restrict access to /proc/filesystems
        # Try to get at least the root partition
        try:
            root_usage = psutil.disk_usage('/')
            return {
                "partitions": [{
                    "device": "rootfs",
                    "mountpoint": "/",
                    "filesystem": "unknown",
                    "total": _bytes_to_human_readable(root_usage.total),
                    "used": _bytes_to_human_readable(root_usage.used),
                    "free": _bytes_to_human_readable(root_usage.free),
                    "percentage": root_usage.percent,
                }],
                "note": "Limited access due to system permissions"
            }
        except Exception:
            return {
                "partitions": [],
                "error": "Unable to access disk information"
            }

    for partition in disk_partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            partitions.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "total": _bytes_to_human_readable(partition_usage.total),
                "used": _bytes_to_human_readable(partition_usage.used),
                "free": _bytes_to_human_readable(partition_usage.free),
                "percentage": partition_usage.percent,
            })
        except (PermissionError, OSError):
            # Skip partitions that can't be accessed
            continue

    return {"partitions": partitions}


def get_battery_info() -> Optional[Dict[str, Any]]:
    """Get battery information (if available).

    Tries Termux:API first (termux-battery-status), falls back to psutil.
    """
    # Try Termux:API first (works on Android/Termux)
    termux_battery = _get_termux_battery_status()
    if termux_battery:
        return termux_battery

    # Fallback to psutil (usually fails on Termux due to permissions)
    try:
        battery = psutil.sensors_battery()
    except (PermissionError, OSError, NotImplementedError):
        # Termux/Android may restrict access to /sys/class/power_supply
        # or battery info may not be available via standard Linux APIs
        return None

    if battery is None:
        return None

    return {
        "percentage": battery.percent,
        "power_plugged": battery.power_plugged,
        "time_left": str(battery.secsleft) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited",
    }


def _get_termux_battery_status() -> Optional[Dict[str, Any]]:
    """Get battery status using Termux:API.

    Requires: pkg install termux-api && install Termux:API app from F-Droid
    """
    try:
        result = subprocess.run(
            ["termux-battery-status"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )

        data = json.loads(result.stdout)

        return {
            "percentage": data.get("percentage", 0),
            "power_plugged": data.get("plugged") != "UNPLUGGED",
            "status": data.get("status", "UNKNOWN"),
            "health": data.get("health", "UNKNOWN"),
            "temperature": data.get("temperature", 0),
            "current": data.get("current", 0),
        }
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            FileNotFoundError, json.JSONDecodeError, KeyError):
        # Termux:API not installed or not available
        return None


def get_termux_wifi_info() -> Optional[Dict[str, Any]]:
    """Get WiFi connection info using Termux:API.

    Requires: pkg install termux-api && install Termux:API app from F-Droid
    """
    try:
        result = subprocess.run(
            ["termux-wifi-connectioninfo"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )

        data = json.loads(result.stdout)

        return {
            "ssid": data.get("ssid", "Unknown"),
            "bssid": data.get("bssid", "Unknown"),
            "ip": data.get("ip", "Unknown"),
            "link_speed_mbps": data.get("link_speed_mbps", 0),
            "rssi": data.get("rssi", 0),
            "frequency_mhz": data.get("frequency_mhz", 0),
            "network_id": data.get("network_id", -1),
        }
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            FileNotFoundError, json.JSONDecodeError, KeyError):
        # Termux:API not installed or not available
        return None


def get_termux_device_info() -> Optional[Dict[str, Any]]:
    """Get device telephony info using Termux:API.

    Requires: pkg install termux-api && install Termux:API app from F-Droid
    """
    try:
        result = subprocess.run(
            ["termux-telephony-deviceinfo"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )

        data = json.loads(result.stdout)

        return {
            "device_id": data.get("device_id", "Unknown"),
            "device_software_version": data.get("device_software_version", "Unknown"),
            "phone_count": data.get("phone_count", 0),
            "phone_type": data.get("phone_type", "Unknown"),
            "network_operator": data.get("network_operator", "Unknown"),
            "network_operator_name": data.get("network_operator_name", "Unknown"),
            "network_country_iso": data.get("network_country_iso", "Unknown"),
            "network_type": data.get("network_type", "Unknown"),
            "sim_state": data.get("sim_state", "Unknown"),
        }
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            FileNotFoundError, json.JSONDecodeError, KeyError):
        # Termux:API not installed or not available
        return None


def get_tmux_sessions() -> list[Dict[str, str]]:
    """Get list of running tmux sessions."""
    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}:#{session_created}:#{session_attached}"],
            capture_output=True,
            text=True,
            check=True
        )

        sessions = []
        for line in result.stdout.strip().split("\n"):
            if line:
                name, created, attached = line.split(":")
                sessions.append({
                    "name": name,
                    "created": datetime.fromtimestamp(int(created)).isoformat(),
                    "attached": attached == "1",
                })
        return sessions
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def get_process_count() -> Dict[str, int]:
    """Get count of running processes by status."""
    statuses = {}

    try:
        for proc in psutil.process_iter(['status']):
            try:
                status = proc.info['status']
                statuses[status] = statuses.get(status, 0) + 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        total = len(psutil.pids())
    except (PermissionError, OSError):
        return {
            "total": 0,
            "by_status": {},
            "error": "Permission denied"
        }

    return {
        "total": total,
        "by_status": statuses,
    }


def _bytes_to_human_readable(bytes_value: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f}{unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f}PB"
