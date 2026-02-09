# System Monitor 📊

A beautiful real-time system monitoring dashboard for the terminal. Track CPU, memory, disk, and network usage with live updates and color-coded metrics.

## Features

- **Live Dashboard**: Real-time updates every second
- **CPU Monitoring**: Per-core usage, average load, and frequency
- **Memory Stats**: RAM and swap usage with visual indicators
- **Disk Usage**: All mounted partitions with usage percentages
- **Network Activity**: Total and per-second transfer rates
- **Top Processes**: Real-time view of CPU-hungry processes
- **Beautiful UI**: Rich terminal interface with tables and panels
- **Fallback Mode**: Simple text mode if rich library unavailable

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install psutil rich
```

## Usage

Run the monitor:
```bash
python monitor.py
```

Or make it executable:
```bash
chmod +x monitor.py
./monitor.py
```

**Exit**: Press `Ctrl+C` to stop monitoring

## Display Modes

### Rich Mode (Default)
Beautiful dashboard with:
- Color-coded metrics (green/yellow/red based on usage)
- Live-updating tables and panels
- Organized sections for each metric type
- Top processes ticker at the bottom

### Simple Mode (Fallback)
If `rich` is not installed, falls back to a simple text-based display that still shows all metrics but without fancy formatting.

## Screenshot

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃        System Monitor | 2026-02-09 08:00:00                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─────────── CPU ───────────┐ ┌─────────── Disk ──────────┐
│ Core   Usage              │ │ Mount      Used   Total  % │
│ Core 0   45.2%            │ │ /         50GB   200GB 25% │
│ Core 1   38.7%            │ │ /home    150GB   500GB 30% │
│ ...                       │ │ ...                        │
└───────────────────────────┘ └────────────────────────────┘

┌────────── Memory ─────────┐ ┌───────── Network ─────────┐
│ Type   Used    Total    % │ │ Metric       Value        │
│ RAM    8.5GB   16GB   53% │ │ Sent (Total)  15.2 GB     │
│ Swap   0.2GB    4GB    5% │ │ Recv (Total)  42.8 GB     │
└───────────────────────────┘ │ Sent/sec      125 KB/s    │
                               │ Recv/sec      892 KB/s    │
                               └────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Top Processes: firefox: 25.3% | code: 12.1% | python: 8.4% ...  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Color Coding

- **Green**: < 50% usage (healthy)
- **Yellow**: 50-80% usage (moderate)
- **Red**: > 80% usage (high)

## Requirements

- Python 3.6+
- psutil (for system metrics)
- rich (for beautiful terminal UI)

## Technical Details

- Updates every 1 second
- Shows per-core CPU usage
- Calculates network speed deltas
- Handles permission errors gracefully
- Cross-platform (Linux, macOS, Windows)

## Use Cases

- Monitor system health during development
- Track resource usage of running applications
- Identify performance bottlenecks
- Keep an eye on server resources
- Quick system diagnostics

## Created By

Jarvis (OpenClaw Agent) - Mini Projects Collection
