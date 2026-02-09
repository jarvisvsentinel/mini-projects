#!/usr/bin/env python3
"""
System Monitor - Live system stats dashboard
Shows CPU, Memory, Disk, and Network usage in real-time
"""

import psutil
import time
import sys
from datetime import datetime

try:
    from rich.console import Console
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.progress import BarColumn, Progress
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def get_size(bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"


def get_cpu_info():
    """Get CPU information"""
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_freq = psutil.cpu_freq()
    cpu_count = psutil.cpu_count()
    
    return {
        'percent': cpu_percent,
        'avg_percent': sum(cpu_percent) / len(cpu_percent),
        'freq': cpu_freq.current if cpu_freq else 0,
        'count': cpu_count
    }


def get_memory_info():
    """Get memory information"""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'percent': mem.percent,
        'swap_total': swap.total,
        'swap_used': swap.used,
        'swap_percent': swap.percent
    }


def get_disk_info():
    """Get disk information"""
    partitions = psutil.disk_partitions()
    disk_info = []
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
        except PermissionError:
            continue
    
    return disk_info


def get_network_info():
    """Get network information"""
    net_io = psutil.net_io_counters()
    
    return {
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv,
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv
    }


def get_process_info(limit=10):
    """Get top processes by CPU usage"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU percent
    processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
    return processes[:limit]


def create_rich_dashboard():
    """Create a rich dashboard layout"""
    console = Console()
    
    # Store previous network stats for delta calculation
    prev_net = get_network_info()
    
    def generate_table():
        """Generate the dashboard table"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Header
        header = Panel(
            f"[bold cyan]System Monitor[/bold cyan] | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            style="bold white on blue"
        )
        layout["header"].update(header)
        
        # Body - split into sections
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        layout["body"]["left"].split_column(
            Layout(name="cpu"),
            Layout(name="memory")
        )
        
        layout["body"]["right"].split_column(
            Layout(name="disk"),
            Layout(name="network")
        )
        
        # CPU Info
        cpu = get_cpu_info()
        cpu_table = Table(title="CPU", show_header=True, header_style="bold magenta")
        cpu_table.add_column("Core", style="cyan")
        cpu_table.add_column("Usage", justify="right")
        
        for i, percent in enumerate(cpu['percent']):
            color = "green" if percent < 50 else "yellow" if percent < 80 else "red"
            cpu_table.add_row(f"Core {i}", f"[{color}]{percent:.1f}%[/{color}]")
        
        cpu_table.add_row("", "")
        cpu_table.add_row("[bold]Average[/bold]", f"[bold]{cpu['avg_percent']:.1f}%[/bold]")
        cpu_table.add_row("[bold]Frequency[/bold]", f"[bold]{cpu['freq']:.0f} MHz[/bold]")
        
        layout["body"]["left"]["cpu"].update(Panel(cpu_table, border_style="magenta"))
        
        # Memory Info
        mem = get_memory_info()
        mem_table = Table(title="Memory", show_header=True, header_style="bold cyan")
        mem_table.add_column("Type", style="cyan")
        mem_table.add_column("Used", justify="right")
        mem_table.add_column("Total", justify="right")
        mem_table.add_column("Percent", justify="right")
        
        mem_color = "green" if mem['percent'] < 50 else "yellow" if mem['percent'] < 80 else "red"
        mem_table.add_row(
            "RAM",
            get_size(mem['used']),
            get_size(mem['total']),
            f"[{mem_color}]{mem['percent']:.1f}%[/{mem_color}]"
        )
        
        if mem['swap_total'] > 0:
            swap_color = "green" if mem['swap_percent'] < 50 else "yellow" if mem['swap_percent'] < 80 else "red"
            mem_table.add_row(
                "Swap",
                get_size(mem['swap_used']),
                get_size(mem['swap_total']),
                f"[{swap_color}]{mem['swap_percent']:.1f}%[/{swap_color}]"
            )
        
        layout["body"]["left"]["memory"].update(Panel(mem_table, border_style="cyan"))
        
        # Disk Info
        disks = get_disk_info()
        disk_table = Table(title="Disk", show_header=True, header_style="bold yellow")
        disk_table.add_column("Mount", style="cyan", no_wrap=True)
        disk_table.add_column("Used", justify="right")
        disk_table.add_column("Total", justify="right")
        disk_table.add_column("Percent", justify="right")
        
        for disk in disks[:5]:  # Show top 5 disks
            disk_color = "green" if disk['percent'] < 50 else "yellow" if disk['percent'] < 80 else "red"
            disk_table.add_row(
                disk['mountpoint'][:20],
                get_size(disk['used']),
                get_size(disk['total']),
                f"[{disk_color}]{disk['percent']:.1f}%[/{disk_color}]"
            )
        
        layout["body"]["right"]["disk"].update(Panel(disk_table, border_style="yellow"))
        
        # Network Info
        nonlocal prev_net
        net = get_network_info()
        
        # Calculate deltas
        sent_delta = net['bytes_sent'] - prev_net['bytes_sent']
        recv_delta = net['bytes_recv'] - prev_net['bytes_recv']
        prev_net = net
        
        net_table = Table(title="Network", show_header=True, header_style="bold green")
        net_table.add_column("Metric", style="cyan")
        net_table.add_column("Value", justify="right")
        
        net_table.add_row("Sent (Total)", get_size(net['bytes_sent']))
        net_table.add_row("Recv (Total)", get_size(net['bytes_recv']))
        net_table.add_row("", "")
        net_table.add_row("[bold]Sent/sec[/bold]", f"[bold green]{get_size(sent_delta)}[/bold green]")
        net_table.add_row("[bold]Recv/sec[/bold]", f"[bold green]{get_size(recv_delta)}[/bold green]")
        
        layout["body"]["right"]["network"].update(Panel(net_table, border_style="green"))
        
        # Footer with top processes
        processes = get_process_info(5)
        footer_text = "[bold]Top Processes:[/bold] "
        footer_text += " | ".join([
            f"{p['name'][:15]}: {p['cpu_percent']:.1f}%" 
            for p in processes[:5]
        ])
        footer = Panel(footer_text, style="bold white on black")
        layout["footer"].update(footer)
        
        return layout
    
    # Live display
    with Live(generate_table(), refresh_per_second=1, console=console) as live:
        try:
            while True:
                time.sleep(1)
                live.update(generate_table())
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Monitoring stopped.[/bold yellow]")


def create_simple_dashboard():
    """Create a simple text dashboard for when rich is not available"""
    print("System Monitor (Simple Mode - install 'rich' for better display)")
    print("=" * 60)
    
    try:
        while True:
            print("\n" + "=" * 60)
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            # CPU
            cpu = get_cpu_info()
            print(f"\nCPU: {cpu['avg_percent']:.1f}% | Cores: {cpu['count']} | Freq: {cpu['freq']:.0f} MHz")
            
            # Memory
            mem = get_memory_info()
            print(f"Memory: {mem['percent']:.1f}% ({get_size(mem['used'])} / {get_size(mem['total'])})")
            
            if mem['swap_total'] > 0:
                print(f"Swap: {mem['swap_percent']:.1f}% ({get_size(mem['swap_used'])} / {get_size(mem['swap_total'])})")
            
            # Disk
            print("\nDisk Usage:")
            disks = get_disk_info()
            for disk in disks[:3]:
                print(f"  {disk['mountpoint']}: {disk['percent']:.1f}% ({get_size(disk['used'])} / {get_size(disk['total'])})")
            
            # Network
            net = get_network_info()
            print(f"\nNetwork: Sent: {get_size(net['bytes_sent'])} | Recv: {get_size(net['bytes_recv'])}")
            
            # Top Processes
            print("\nTop 5 Processes:")
            processes = get_process_info(5)
            for proc in processes:
                print(f"  {proc['name'][:20]:20} CPU: {proc['cpu_percent']:.1f}% | Mem: {proc['memory_percent']:.1f}%")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


def main():
    """Main entry point"""
    if RICH_AVAILABLE:
        create_rich_dashboard()
    else:
        print("Note: Install 'rich' for a better dashboard experience:")
        print("  pip install rich")
        print()
        create_simple_dashboard()


if __name__ == "__main__":
    main()
