"""Command-line interface for DroidVM Tools."""

import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from droidvm_tools.tools import system
from droidvm_tools.tools import network as network_tools

app = typer.Typer(
    name="droidvm-tools",
    help="Tools for managing Android phone as a tiny home server via Termux",
    add_completion=False,
)
console = Console()


@app.command()
def info():
    """Display comprehensive system information."""
    console.print("\n[bold cyan]System Information[/bold cyan]")

    sys_info = system.get_system_info()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    for key, value in sys_info.items():
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


@app.command()
def cpu():
    """Display CPU information and usage."""
    console.print("\n[bold cyan]CPU Information[/bold cyan]")

    cpu_info = system.get_cpu_info()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    for key, value in cpu_info.items():
        if key != "cpu_usage_per_core":
            table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)

    if "cpu_usage_per_core" in cpu_info:
        console.print("\n[bold yellow]Per-Core Usage:[/bold yellow]")
        for i, usage in enumerate(cpu_info["cpu_usage_per_core"]):
            console.print(f"  Core {i}: {usage}%")


@app.command()
def memory():
    """Display memory usage information."""
    console.print("\n[bold cyan]Memory Information[/bold cyan]")

    mem_info = system.get_memory_info()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    for key, value in mem_info.items():
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


@app.command()
def disk():
    """Display disk usage information."""
    console.print("\n[bold cyan]Disk Information[/bold cyan]")

    disk_info = system.get_disk_info()

    for partition in disk_info["partitions"]:
        console.print(f"\n[bold yellow]{partition['mountpoint']}[/bold yellow] ({partition['device']})")
        table = Table(show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        for key, value in partition.items():
            if key not in ["mountpoint", "device"]:
                table.add_row(key.replace("_", " ").title(), str(value))

        console.print(table)


@app.command()
def battery():
    """Display battery information (if available)."""
    console.print("\n[bold cyan]Battery Information[/bold cyan]")

    battery_info = system.get_battery_info()

    if battery_info is None:
        console.print("[yellow]Battery information not available on this device[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    for key, value in battery_info.items():
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


@app.command()
def network():
    """Display network information."""
    console.print("\n[bold cyan]Network Information[/bold cyan]")

    net_info = network_tools.get_network_info()

    for iface_name, iface_data in net_info["interfaces"].items():
        console.print(f"\n[bold yellow]{iface_name}[/bold yellow]")
        console.print(f"  Status: {'UP' if iface_data['is_up'] else 'DOWN'}")
        console.print(f"  Speed: {iface_data['speed']} Mbps")

        if iface_data["addresses"]:
            console.print("  Addresses:")
            for addr in iface_data["addresses"]:
                console.print(f"    - {addr['address']} ({addr['family']})")


@app.command()
def netstat():
    """Display network statistics."""
    console.print("\n[bold cyan]Network Statistics[/bold cyan]")

    stats = network.get_network_stats()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    for key, value in stats.items():
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


@app.command()
def tailscale():
    """Display Tailscale VPN status."""
    console.print("\n[bold cyan]Tailscale Status[/bold cyan]")

    ts_status = network.get_tailscale_status()
    ts_ip = network.get_tailscale_ip()

    if ts_status is None:
        console.print("[yellow]Tailscale is not installed or not running[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Status", "Connected" if ts_status.get("connected") else "Disconnected")
    table.add_row("Backend State", str(ts_status.get("backend_state", "Unknown")))
    table.add_row("Peers", str(ts_status.get("peers", 0)))
    table.add_row("Tailscale IP", ts_ip or "N/A")

    console.print(table)

    if ts_status.get("health"):
        console.print("\n[bold yellow]Health Issues:[/bold yellow]")
        for issue in ts_status["health"]:
            console.print(f"  - {issue}")


@app.command()
def tmux():
    """Display running tmux sessions."""
    console.print("\n[bold cyan]Tmux Sessions[/bold cyan]")

    sessions = system.get_tmux_sessions()

    if not sessions:
        console.print("[yellow]No tmux sessions found[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Session Name", style="cyan")
    table.add_column("Created", style="green")
    table.add_column("Attached", style="yellow")

    for session in sessions:
        table.add_row(
            session["name"],
            session["created"],
            "Yes" if session["attached"] else "No"
        )

    console.print(table)


@app.command()
def status(json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")):
    """Display comprehensive system status."""
    status_data = {
        "system": system.get_system_info(),
        "cpu": system.get_cpu_info(),
        "memory": system.get_memory_info(),
        "disk": system.get_disk_info(),
        "battery": system.get_battery_info(),
        "network": {
            "stats": network.get_network_stats(),
            "tailscale_ip": network.get_tailscale_ip(),
            "hostname": network.get_hostname(),
        },
        "tmux_sessions": system.get_tmux_sessions(),
        "processes": system.get_process_count(),
    }

    if json_output:
        print(json.dumps(status_data, indent=2))
    else:
        console.print("\n[bold cyan]Comprehensive System Status[/bold cyan]\n")

        console.print("[bold yellow]Hostname:[/bold yellow]", status_data["network"]["hostname"])
        console.print("[bold yellow]CPU Usage:[/bold yellow]", f"{status_data['cpu']['cpu_usage_percent']}%")
        console.print("[bold yellow]Memory Usage:[/bold yellow]", f"{status_data['memory']['percentage']}%")
        console.print("[bold yellow]Tmux Sessions:[/bold yellow]", len(status_data["tmux_sessions"]))
        console.print("[bold yellow]Total Processes:[/bold yellow]", status_data["processes"]["total"])

        if status_data["battery"]:
            console.print("[bold yellow]Battery:[/bold yellow]", f"{status_data['battery']['percentage']}%")

        if status_data["network"]["tailscale_ip"]:
            console.print("[bold yellow]Tailscale IP:[/bold yellow]", status_data["network"]["tailscale_ip"])

        console.print("\n[dim]Use --json flag for full JSON output[/dim]")


@app.command()
def version():
    """Display version information."""
    from droidvm_tools import __version__
    console.print(f"\n[bold cyan]DroidVM Tools[/bold cyan] version [green]{__version__}[/green]\n")


if __name__ == "__main__":
    app()
