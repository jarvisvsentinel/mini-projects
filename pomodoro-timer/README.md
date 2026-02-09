# 🍅 Pomodoro Timer

A beautiful, feature-rich command-line Pomodoro timer to boost your productivity!

## Features

- **🎯 Classic Pomodoro Technique**: 25-minute work sessions with 5-minute breaks
- **📊 Session Tracking**: Automatic history of all your completed pomodoros
- **🎨 Beautiful CLI Interface**: Colorful progress bars and clear time display
- **🔔 Desktop Notifications**: Get notified when sessions complete
- **🔊 Sound Alerts**: Audible completion beeps (customizable)
- **⚙️ Fully Customizable**: Configure work/break durations to fit your workflow
- **📝 Task Labels**: Track what you're working on during each session
- **📈 Statistics**: View your productivity stats and session history
- **⏸️ Pause/Resume**: Interrupt and continue sessions as needed
- **🔄 Auto-cycling**: Automatically alternate between work and breaks

## Installation

No installation required! Just make sure you have Python 3.6+ installed:

```bash
python3 --version
```

## Usage

### Start a Basic Session

```bash
./pomodoro.py
```

This will:
1. Prompt for an optional task description
2. Start a 25-minute work session
3. Follow with a 5-minute break
4. Continue cycling until you quit

### Start with a Task

```bash
./pomodoro.py -t "Write documentation"
```

### Quick Work Session

Start a custom-length work session:

```bash
./pomodoro.py -w 45  # 45-minute work session
```

### View Statistics

See your productivity stats and recent sessions:

```bash
./pomodoro.py --stats
```

Example output:
```
╔════════════════════════════════════╗
║  📊 Your Pomodoro Stats            ║
╚════════════════════════════════════╝

🍅 Work Sessions: 12
   Total Work Time: 5.0 hours

☕ Break Sessions: 10

Recent Sessions:
🍅 2026-02-08 20:15 - Work (25m) - Write documentation
☕ 2026-02-08 20:40 - Short Break (5m)
🍅 2026-02-08 20:45 - Work (25m) - Code review
```

### Configure Settings

Customize the timer to your preferences:

```bash
./pomodoro.py --config
```

Configurable options:
- Work session duration (default: 25 minutes)
- Short break duration (default: 5 minutes)
- Long break duration (default: 15 minutes)
- Cycles before long break (default: 4)
- Sound alerts (enabled/disabled)
- Desktop notifications (enabled/disabled)

## The Pomodoro Technique

The Pomodoro Technique is a time management method developed by Francesco Cirillo:

1. **Choose a task** you want to work on
2. **Set the timer** for 25 minutes (one "pomodoro")
3. **Work** on the task with full focus until the timer rings
4. **Take a 5-minute break**
5. **Repeat** steps 2-4
6. After **4 pomodoros**, take a longer break (15-30 minutes)

## Keyboard Controls

- **Ctrl+C during timer**: Pause the session
  - Press **R** to resume
  - Press **Q** to quit
- **After work session**: Choose to take break, skip, or quit

## Data Storage

All configuration and history is stored in `~/.pomodoro/`:
- `config.json` - Your personal settings
- `history.json` - Complete session history

## Tips for Success

1. **Eliminate distractions** before starting a session
2. **Use task labels** to track what you accomplish
3. **Honor the breaks** - they're essential for sustained focus
4. **Review your stats** weekly to see your progress
5. **Adjust durations** to find what works best for you

## Requirements

- Python 3.6 or higher
- Terminal with ANSI color support (most modern terminals)
- Optional: `notify-send` for desktop notifications (Linux)
- Optional: `paplay` or `beep` for sound alerts

## Examples

**Full day workflow:**
```bash
# Morning coding sprint
./pomodoro.py -t "Implement authentication"

# After lunch, shorter focused work
./pomodoro.py -w 15

# Check your progress
./pomodoro.py --stats

# Evening session with custom settings
./pomodoro.py --config  # Set to 50-minute sessions
./pomodoro.py -t "Deep work: architecture design"
```

## Why Use This?

- **No web browser needed** - stays in your terminal
- **Lightweight** - minimal system resources
- **Private** - all data stored locally
- **Customizable** - adapt to your workflow
- **Distraction-free** - full-screen focus timer

## License

MIT License - Feel free to use and modify!

## Credits

Built with ❤️ by Jarvis for productive humans everywhere.

Based on the Pomodoro Technique® by Francesco Cirillo.
