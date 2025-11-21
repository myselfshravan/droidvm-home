"""Terminal command execution utilities."""

import subprocess
import time
from typing import Dict, Any


# Whitelist of safe commands for Termux mode
SAFE_COMMANDS = [
    "ls",
    "pwd",
    "whoami",
    "date",
    "uptime",
    "uname",
    "ps",
    "tmux",
    "cat",
    "grep",
    "head",
    "tail",
    "wc",
    "echo",
    "which",
    "file",
    "stat",
    "du",
    "df",
    "ping",
    "curl",
    "wget",
    "hostname",
    "getprop",
]

# Blocked patterns for security
BLOCKED_PATTERNS = [
    "rm",
    "dd",
    "mkfs",
    "mount",
    "umount",
    "sudo",
    "su",
    "passwd",
    "chmod",
    "chown",
]

# Maximum output lines to prevent huge responses
MAX_OUTPUT_LINES = 1000


def execute_termux_command(command: str, timeout: int = 30) -> Dict[str, Any]:
    """Execute a real shell command on the Termux system.

    Args:
        command: The shell command to execute
        timeout: Maximum execution time in seconds (default 30, max 60)

    Returns:
        Dict containing output, exit_code, and execution time
    """
    # Validate timeout
    timeout = min(timeout, 60)

    # Parse command to get the base command
    cmd_parts = command.strip().split()
    if not cmd_parts:
        return {
            "output": ["Error: Empty command"],
            "exit_code": 1,
            "error": "Empty command",
        }

    base_cmd = cmd_parts[0]

    # Check if command is in whitelist
    if base_cmd not in SAFE_COMMANDS:
        return {
            "output": [f"Command '{base_cmd}' is not allowed for security reasons."],
            "exit_code": 1,
            "error": f"Command not whitelisted: {base_cmd}",
        }

    # Check for blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if pattern in command.lower():
            return {
                "output": [f"Command contains blocked pattern: {pattern}"],
                "exit_code": 1,
                "error": f"Blocked pattern detected: {pattern}",
            }

    # Execute command
    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

        execution_time = int((time.time() - start_time) * 1000)

        # Split output into lines
        stdout_lines = result.stdout.strip().split("\n") if result.stdout else []
        stderr_lines = result.stderr.strip().split("\n") if result.stderr else []

        # Limit output size
        if len(stdout_lines) > MAX_OUTPUT_LINES:
            stdout_lines = stdout_lines[:MAX_OUTPUT_LINES]
            stdout_lines.append(
                f"... (output truncated, showing first {MAX_OUTPUT_LINES} lines)"
            )

        # Combine stdout and stderr
        output = stdout_lines
        if stderr_lines and result.returncode != 0:
            output.extend([f"Error: {line}" for line in stderr_lines if line])

        return {
            "output": output if output else [""],
            "exit_code": result.returncode,
            "execution_time_ms": execution_time,
        }

    except subprocess.TimeoutExpired:
        return {
            "output": [f"Command timed out after {timeout} seconds"],
            "exit_code": 124,
            "error": "Timeout",
        }
    except Exception as e:
        return {
            "output": [f"Error executing command: {str(e)}"],
            "exit_code": 1,
            "error": str(e),
        }


def execute_typescript_command(command: str) -> Dict[str, Any]:
    """Execute a command in TypeScript mode (hardcoded responses).

    Args:
        command: The command string

    Returns:
        Dict containing hardcoded output
    """
    cmd = command.strip().lower()

    # Command to output mapping
    responses = {
        "help": [
            "✔ Available commands:",
            "  help      - Show this help message",
            "  clear     - Clear terminal screen",
            "  whoami    - Display user info",
            "  about     - About this portfolio",
            "  projects  - List recent projects",
            "  contact   - Contact information",
            "  skills    - Technical skills",
            "  ls        - List directory contents",
            "  pwd       - Print working directory",
            "  cat       - Display file contents",
            "  exit      - Exit interactive mode",
            "",
        ],
        "?": [
            "✔ Available commands:",
            "  help      - Show this help message",
            "  Type 'help' for full command list",
            "",
        ],
        "clear": [""],
        "whoami": [
            "DroidVM Server - Android phone running as a tiny home server",
            "Powered by Termux and Python",
            "",
        ],
        "about": [
            "DroidVM Tools - System monitoring and management for Android devices",
            "Location: Termux Environment",
            "Platform: Android/Linux",
            "",
        ],
        "projects": [
            "✔ Active Services:",
            "  • DroidVM Tools API - System monitoring REST API",
            "  • Cloudflared Tunnel - Secure remote access",
            "  • Tmux Sessions - Background service management",
            "",
            "ℹ Use /status endpoint for detailed system information.",
            "",
        ],
        "contact": [
            "✔ API Endpoints:",
            "  📡 /status - System status",
            "  🖥️  /system/info - System information",
            "  🔋 /system/battery - Battery status",
            "  🌐 /network/info - Network details",
            "",
        ],
        "skills": [
            "✔ System Capabilities:",
            "  💻 Core: Python, FastAPI, psutil",
            "  🔧 Tools: Termux, tmux, bash",
            "  🌐 Network: Tailscale, Cloudflare Tunnel",
            "  📊 Monitoring: CPU, Memory, Battery, Network",
            "",
        ],
        "ls": [
            "api/          tools/        system/       network/",
            "status.json   config.env    logs/         docs/",
            "",
        ],
        "pwd": [
            "/data/data/com.termux/files/home/droidvm-tools",
            "",
        ],
        "cat": [
            "Usage: cat [filename]",
            "Available files: about.txt, status.json, config.env",
            "",
        ],
        "cat about.txt": [
            "DroidVM Tools - Turn your Android device into a home server",
            "Version: 0.1.0",
            "Platform: Termux/Android",
            "Features: System monitoring, API server, Remote access",
            "",
        ],
        "cat status.json": [
            '{ "status": "running", "uptime": "12h 34m", "api": "active" }',
            "",
        ],
        "exit": [
            "Goodbye! Terminal session ended.",
            "",
        ],
        "sudo": [
            "Nice try! 😄",
            "This is not a real terminal. Use Termux mode for actual commands.",
            "",
        ],
        "sudo rm -rf /": [
            "🚨 SYSTEM BREACH DETECTED! 🚨",
            "Just kidding! This is a safe environment 😉",
            "But I appreciate the classic hacker humor!",
            "",
        ],
    }

    # Check for exact match
    if cmd in responses:
        return {"output": responses[cmd], "exit_code": 0}

    # Check for partial matches
    if cmd.startswith("cat "):
        filename = cmd[4:].strip()
        if filename in ["about.txt", "status.json", "config.env"]:
            return responses.get(
                f"cat {filename}",
                {
                    "output": [f"File '{filename}' is empty or not readable.", ""],
                    "exit_code": 0,
                },
            )

    if "sudo" in cmd:
        return {
            "output": [
                "sudo: command not found (and you probably shouldn't try that here! 😅)",
                "",
            ],
            "exit_code": 127,
        }

    # Default response for unknown commands
    return {
        "output": [
            f"Command not found: {command}",
            "Type 'help' for available commands.",
            "",
        ],
        "exit_code": 127,
    }


def execute_command(
    command: str, mode: str = "typescript", timeout: int = 30
) -> Dict[str, Any]:
    """Execute a command in the specified mode.

    Args:
        command: The command to execute
        mode: Either 'termux' or 'typescript'
        timeout: Timeout for Termux mode (ignored in TypeScript mode)

    Returns:
        Dict with output, exit_code, and metadata
    """
    start_time = time.time()

    if mode.lower() == "termux":
        result = execute_termux_command(command, timeout)
    elif mode.lower() == "typescript":
        result = execute_typescript_command(command)
    else:
        return {
            "output": [f"Invalid mode: {mode}. Use 'termux' or 'typescript'."],
            "exit_code": 1,
            "error": "Invalid mode",
        }

    # Add execution time if not already present
    if "execution_time_ms" not in result:
        result["execution_time_ms"] = int((time.time() - start_time) * 1000)

    # Add mode to result
    result["mode"] = mode
    result["command"] = command

    return result
