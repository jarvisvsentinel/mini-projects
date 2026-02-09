#!/usr/bin/env python3
"""
Pomodoro Timer - A productivity CLI tool
Helps you focus with timed work/break cycles
"""

import time
import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Config and data file paths
CONFIG_DIR = Path.home() / '.pomodoro'
CONFIG_FILE = CONFIG_DIR / 'config.json'
HISTORY_FILE = CONFIG_DIR / 'history.json'

# Default settings
DEFAULT_CONFIG = {
    'work_minutes': 25,
    'short_break_minutes': 5,
    'long_break_minutes': 15,
    'cycles_before_long_break': 4,
    'sound_enabled': True,
    'notify_enabled': True
}


def init_config():
    """Initialize config directory and files"""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
    
    if not HISTORY_FILE.exists():
        save_history([])


def load_config():
    """Load configuration from file"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def load_history():
    """Load session history from file"""
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


def save_history(history):
    """Save session history to file"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def add_to_history(session_type, duration, task=''):
    """Add a completed session to history"""
    history = load_history()
    history.append({
        'type': session_type,
        'duration': duration,
        'task': task,
        'timestamp': datetime.now().isoformat(),
        'completed': True
    })
    save_history(history)


def notify(title, message):
    """Send desktop notification"""
    config = load_config()
    if not config.get('notify_enabled', True):
        return
    
    try:
        # Try notify-send (Linux)
        os.system(f'notify-send "{title}" "{message}" 2>/dev/null')
    except:
        pass


def play_sound():
    """Play completion sound"""
    config = load_config()
    if not config.get('sound_enabled', True):
        return
    
    try:
        # Simple beep
        os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || beep 2>/dev/null || printf "\\a"')
    except:
        print('\a', end='', flush=True)  # Terminal bell fallback


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')


def format_time(seconds):
    """Format seconds as MM:SS"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def print_banner(text, color=CYAN):
    """Print a fancy banner"""
    width = len(text) + 4
    print(f"\n{color}{BOLD}{'═' * width}")
    print(f"  {text}  ")
    print(f"{'═' * width}{RESET}\n")


def run_timer(duration_minutes, session_type, task=''):
    """Run a countdown timer"""
    total_seconds = duration_minutes * 60
    remaining = total_seconds
    
    try:
        while remaining > 0:
            clear_screen()
            
            # Display banner
            if session_type == 'work':
                color = GREEN
                icon = "🍅"
            elif session_type == 'short_break':
                color = YELLOW
                icon = "☕"
            else:  # long_break
                color = MAGENTA
                icon = "🎉"
            
            print_banner(f"{icon} {session_type.replace('_', ' ').title()}", color)
            
            # Display task
            if task:
                print(f"{CYAN}Task: {BOLD}{task}{RESET}\n")
            
            # Display time
            time_str = format_time(remaining)
            print(f"{color}{BOLD}{'█' * 40}")
            print(f"{'█' * 20} {time_str} {'█' * 20}")
            print(f"{'█' * 40}{RESET}\n")
            
            # Progress bar
            progress = 1 - (remaining / total_seconds)
            bar_width = 50
            filled = int(bar_width * progress)
            bar = '█' * filled + '░' * (bar_width - filled)
            print(f"{color}[{bar}] {int(progress * 100)}%{RESET}\n")
            
            print(f"{BLUE}Press Ctrl+C to pause/quit{RESET}")
            
            time.sleep(1)
            remaining -= 1
        
        # Timer complete!
        clear_screen()
        print_banner(f"✓ {session_type.replace('_', ' ').title()} Complete!", GREEN)
        play_sound()
        notify("Pomodoro Timer", f"{session_type.replace('_', ' ').title()} complete!")
        
        # Add to history
        add_to_history(session_type, duration_minutes, task)
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Timer paused.{RESET}")
        response = input(f"\n{CYAN}(Q)uit or (R)esume? {RESET}").strip().lower()
        
        if response == 'r':
            return run_timer(remaining // 60 + (1 if remaining % 60 > 0 else 0), session_type, task)
        else:
            print(f"{RED}Session abandoned.{RESET}")
            return False


def show_stats():
    """Display session statistics"""
    history = load_history()
    
    if not history:
        print(f"{YELLOW}No sessions completed yet. Start your first pomodoro!{RESET}")
        return
    
    clear_screen()
    print_banner("📊 Your Pomodoro Stats", CYAN)
    
    # Count sessions by type
    work_sessions = [s for s in history if s['type'] == 'work']
    break_sessions = [s for s in history if s['type'] in ('short_break', 'long_break')]
    
    # Calculate totals
    total_work_minutes = sum(s['duration'] for s in work_sessions)
    total_work_hours = total_work_minutes / 60
    
    print(f"{GREEN}🍅 Work Sessions: {BOLD}{len(work_sessions)}{RESET}")
    print(f"{GREEN}   Total Work Time: {BOLD}{total_work_hours:.1f} hours{RESET}")
    print()
    print(f"{YELLOW}☕ Break Sessions: {BOLD}{len(break_sessions)}{RESET}")
    print()
    
    # Recent sessions
    print(f"{CYAN}{BOLD}Recent Sessions:{RESET}")
    recent = history[-10:][::-1]  # Last 10, reversed
    
    for session in recent:
        timestamp = datetime.fromisoformat(session['timestamp'])
        date_str = timestamp.strftime('%Y-%m-%d %H:%M')
        
        if session['type'] == 'work':
            icon = '🍅'
            color = GREEN
        else:
            icon = '☕'
            color = YELLOW
        
        task_str = f" - {session['task']}" if session.get('task') else ''
        print(f"{color}{icon} {date_str} - {session['type'].replace('_', ' ').title()} ({session['duration']}m){task_str}{RESET}")
    
    print()


def configure():
    """Interactive configuration"""
    clear_screen()
    print_banner("⚙️  Configuration", BLUE)
    
    config = load_config()
    
    print(f"{CYAN}Current Settings:{RESET}")
    print(f"  Work duration: {config['work_minutes']} minutes")
    print(f"  Short break: {config['short_break_minutes']} minutes")
    print(f"  Long break: {config['long_break_minutes']} minutes")
    print(f"  Cycles before long break: {config['cycles_before_long_break']}")
    print(f"  Sound: {'enabled' if config['sound_enabled'] else 'disabled'}")
    print(f"  Notifications: {'enabled' if config['notify_enabled'] else 'disabled'}")
    print()
    
    if input(f"{CYAN}Change settings? (y/N): {RESET}").lower() != 'y':
        return
    
    try:
        config['work_minutes'] = int(input(f"{CYAN}Work duration (minutes): {RESET}") or config['work_minutes'])
        config['short_break_minutes'] = int(input(f"{CYAN}Short break (minutes): {RESET}") or config['short_break_minutes'])
        config['long_break_minutes'] = int(input(f"{CYAN}Long break (minutes): {RESET}") or config['long_break_minutes'])
        config['cycles_before_long_break'] = int(input(f"{CYAN}Cycles before long break: {RESET}") or config['cycles_before_long_break'])
        
        sound = input(f"{CYAN}Enable sound? (y/n): {RESET}").lower()
        if sound in ('y', 'n'):
            config['sound_enabled'] = (sound == 'y')
        
        notify_input = input(f"{CYAN}Enable notifications? (y/n): {RESET}").lower()
        if notify_input in ('y', 'n'):
            config['notify_enabled'] = (notify_input == 'y')
        
        save_config(config)
        print(f"\n{GREEN}✓ Configuration saved!{RESET}")
        time.sleep(1)
    except ValueError:
        print(f"{RED}Invalid input. Configuration unchanged.{RESET}")
        time.sleep(2)


def start_session(task=''):
    """Start a pomodoro session with automatic breaks"""
    config = load_config()
    cycle_count = 0
    
    clear_screen()
    print_banner("🍅 Pomodoro Timer", GREEN)
    
    if not task:
        task = input(f"{CYAN}What are you working on? (optional): {RESET}").strip()
    
    try:
        while True:
            cycle_count += 1
            
            # Work session
            print(f"\n{GREEN}Starting work session {cycle_count}...{RESET}")
            time.sleep(2)
            
            if not run_timer(config['work_minutes'], 'work', task):
                break
            
            # Determine break type
            if cycle_count % config['cycles_before_long_break'] == 0:
                break_type = 'long_break'
                break_minutes = config['long_break_minutes']
            else:
                break_type = 'short_break'
                break_minutes = config['short_break_minutes']
            
            # Ask if user wants a break
            print(f"\n{YELLOW}Ready for a {break_minutes}-minute break?{RESET}")
            response = input(f"{CYAN}(Y)es, (S)kip, or (Q)uit: {RESET}").strip().lower()
            
            if response == 'q':
                break
            elif response == 's':
                continue
            
            # Break session
            run_timer(break_minutes, break_type)
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Session ended.{RESET}")


def main():
    """Main entry point"""
    init_config()
    
    parser = argparse.ArgumentParser(
        description='Pomodoro Timer - Stay focused and productive',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pomodoro.py              Start a pomodoro session
  pomodoro.py -t "Code"    Start with a task
  pomodoro.py --stats      View statistics
  pomodoro.py --config     Configure settings
        """
    )
    
    parser.add_argument('-t', '--task', help='Task description')
    parser.add_argument('-s', '--stats', action='store_true', help='Show statistics')
    parser.add_argument('-c', '--config', action='store_true', help='Configure settings')
    parser.add_argument('-w', '--work', type=int, help='Quick work session (minutes)')
    
    args = parser.parse_args()
    
    if args.stats:
        show_stats()
    elif args.config:
        configure()
    elif args.work:
        run_timer(args.work, 'work', args.task or '')
    else:
        start_session(args.task or '')


if __name__ == '__main__':
    main()
