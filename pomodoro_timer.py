#!/usr/bin/env python3
"""
Smart Pomodoro Timer - WITH PROGRESS BAR ANIMATION (DIALOG BUG FIXED)
Bug fix: Dialog timeout calculation was truncating seconds
"""

import subprocess
import time
from datetime import datetime
import os
import webbrowser
import sys

# HARDCODED SCHEDULE
SCHEDULE = [
    # Morning sessions
    {"session": 1, "type": "WORK", "start": "09:00", "end": "09:25"},
    {"session": 1, "type": "SHORT_BREAK", "start": "09:25", "end": "09:30"},
    {"session": 2, "type": "WORK", "start": "09:30", "end": "09:55"},
    {"session": 2, "type": "SHORT_BREAK", "start": "09:55", "end": "10:00"},
    {"session": 3, "type": "WORK", "start": "10:00", "end": "10:25"},
    {"session": 3, "type": "SHORT_BREAK", "start": "10:25", "end": "10:30"},
    {"session": 4, "type": "WORK", "start": "10:30", "end": "10:55"},
    {"session": 4, "type": "LONG_BREAK", "start": "10:55", "end": "11:10"},
    {"session": 5, "type": "WORK", "start": "11:10", "end": "11:35"},
    {"session": 5, "type": "SHORT_BREAK", "start": "11:35", "end": "11:40"},
    {"session": 6, "type": "WORK", "start": "11:40", "end": "12:00"},

    # Lunch
    {"session": "-", "type": "LUNCH", "start": "12:00", "end": "13:00"},

    # Afternoon sessions
    {"session": 1, "type": "WORK", "start": "13:00", "end": "13:25"},
    {"session": 1, "type": "SHORT_BREAK", "start": "13:25", "end": "13:30"},
    {"session": 2, "type": "WORK", "start": "13:30", "end": "13:55"},
    {"session": 2, "type": "SHORT_BREAK", "start": "13:55", "end": "14:00"},
    {"session": 3, "type": "WORK", "start": "14:00", "end": "14:25"},
    {"session": 3, "type": "SHORT_BREAK", "start": "14:25", "end": "14:30"},
    {"session": 4, "type": "WORK", "start": "14:30", "end": "14:55"},
    {"session": 4, "type": "LONG_BREAK", "start": "14:55", "end": "15:10"},
    {"session": 5, "type": "WORK", "start": "15:10", "end": "15:35"},
    {"session": 5, "type": "SHORT_BREAK", "start": "15:35", "end": "15:40"},
    {"session": 6, "type": "WORK", "start": "15:40", "end": "16:05"},
    {"session": 6, "type": "SHORT_BREAK", "start": "16:05", "end": "16:10"},
    {"session": 7, "type": "WORK", "start": "16:10", "end": "16:35"},
    {"session": 7, "type": "SHORT_BREAK", "start": "16:35", "end": "16:40"},
    {"session": 8, "type": "WORK", "start": "16:40", "end": "17:05"},
    {"session": 8, "type": "LONG_BREAK", "start": "17:05", "end": "17:20"},
    {"session": 9, "type": "WORK", "start": "17:20", "end": "17:45"},
    {"session": 9, "type": "SHORT_BREAK", "start": "17:45", "end": "17:50"},
    {"session": 10, "type": "WORK", "start": "17:50", "end": "18:00"},
]

# ASCII Art Digits (5 lines high)
ASCII_DIGITS = {
    '0': [
        "  ████  ",
        " █    █ ",
        " █    █ ",
        " █    █ ",
        "  ████  "
    ],
    '1': [
        "   ██   ",
        "  ███   ",
        "   ██   ",
        "   ██   ",
        "  ████  "
    ],
    '2': [
        "  ████  ",
        "      █ ",
        "  ████  ",
        " █      ",
        " ██████ "
    ],
    '3': [
        "  ████  ",
        "      █ ",
        "   ███  ",
        "      █ ",
        "  ████  "
    ],
    '4': [
        " █   █  ",
        " █   █  ",
        " █████  ",
        "     █  ",
        "     █  "
    ],
    '5': [
        " ██████ ",
        " █      ",
        " █████  ",
        "      █ ",
        " ██████ "
    ],
    '6': [
        "  ████  ",
        " █      ",
        " █████  ",
        " █    █ ",
        "  ████  "
    ],
    '7': [
        " ██████ ",
        "     █  ",
        "    █   ",
        "   █    ",
        "  █     "
    ],
    '8': [
        "  ████  ",
        " █    █ ",
        "  ████  ",
        " █    █ ",
        "  ████  "
    ],
    '9': [
        "  ████  ",
        " █    █ ",
        " ██████ ",
        "      █ ",
        "  ████  "
    ],
    ':': [
        "        ",
        "   ██   ",
        "        ",
        "   ██   ",
        "        "
    ]
}

def set_terminal_title(title):
    """Set the terminal window title"""
    print(f"\033]0;{title}\007", end="", flush=True)

def generate_ascii_art(time_str):
    """Generate ASCII art string for the time"""
    lines = [""] * 5
    for char in time_str:
        if char in ASCII_DIGITS:
            digit_lines = ASCII_DIGITS[char]
            for i in range(5):
                lines[i] += digit_lines[i]
    return "\n".join(lines)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def send_notification(title, message, sound="Glass"):
    script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
    try:
        subprocess.run(['osascript', '-e', script], timeout=5)
    except:
        pass

def is_screen_locked():
    """Check if screen locked"""
    try:
        result = subprocess.run(['pgrep', '-x', 'ScreenSaverEngine'], capture_output=True, timeout=2)
        return result.returncode == 0
    except:
        return False

def time_in_range(current, start, end):
    """Check if current time is in range [start, end)"""
    return start <= current < end

def get_current_activity():
    """Get what should be happening right now based on schedule"""
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    # Check if weekday
    if now.weekday() >= 5:  # Weekend
        return None

    # Check against schedule
    for item in SCHEDULE:
        if time_in_range(current_time, item["start"], item["end"]):
            return item

    # Not in any scheduled time
    return None

    # Visual Urgency: Red if < 5 minutes
    # 5 minutes = 300 seconds
    # We need to pass remaining_seconds to this function or calculate it outside
    # But to keep signature simple, let's assume we pass it or handle it differently.
    # Actually, let's modify the function signature to accept remaining_seconds optionally
    pass

def create_progress_bar(percentage, remaining_seconds=None, width=40):
    """Create animated progress bar"""
    filled = int(width * percentage / 100)
    empty = width - filled

    # Colors for rotation (every minute)
    colors = [
        "\033[92m",  # Green
        "\033[93m",  # Yellow
        "\033[94m",  # Blue
        "\033[95m",  # Magenta
        "\033[96m",  # Cyan
        "\033[91m",  # Red
    ]
    
    # Visual Urgency: Force Red and Bold if < 5 mins (300s)
    if remaining_seconds is not None and remaining_seconds < 300:
        color = "\033[91m\033[1m" # Bold Red
    else:
        # Select color based on current minute
        current_minute = datetime.now().minute
        color_index = current_minute % len(colors)
        color = colors[color_index]
    
    fill_char = "█"
    reset = "\033[0m"

    bar = color + fill_char * filled + "░" * empty + reset

    return f"[{bar}] {percentage:3.0f}%"

def open_zen_mode():
    """Open the Zen Mode animation (index.html)"""
    try:
        # Get absolute path to index.html in the same directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(current_dir, "index.html")
        
        if os.path.exists(index_path):
            url = f"file://{index_path}"
            log(f"Opening Zen Mode: {url}")
            webbrowser.open(url)
        else:
            log(f"Error: index.html not found at {index_path}")
    except Exception as e:
        log(f"Error opening Zen Mode: {e}")

def spawn_tkinter_dialog(index, message):
    """Spawn a tkinter dialog at a specific position"""
    # Calculate position (side-by-side)
    width = 300
    height = 150
    x = 50 + (index * 310) # Spacing
    y = 300 # Vertical position
    
    title = "POMODORO BREAK"
    
    # Escape message for python string
    safe_message = message.replace('"', '\\"').replace('\n', '\\n')
    
    # Python script to run in subprocess
    script = f"""
import tkinter as tk
try:
    root = tk.Tk()
    root.title("{title}")
    root.geometry("{width}x{height}+{x}+{y}")
    root.attributes('-topmost', True)
    label = tk.Label(root, text="{safe_message}", wraplength=280, justify="center", font=("Arial", 12))
    label.pack(pady=20)
    btn = tk.Button(root, text="OK", command=root.destroy)
    btn.pack(pady=10)
    # Force focus
    root.lift()
    root.focus_force()
    root.mainloop()
except Exception as e:
    print(e)
"""
    try:
        subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        log(f"Error spawning dialog: {e}")

def show_dialog(activity):
    """Show dialog for break"""
    session = activity["session"]
    type_str = activity["type"]

    if "BREAK" in type_str or type_str == "LUNCH":
        # Trigger Zen Mode
        open_zen_mode()
        
        msg = f"{type_str}\\n\\nSession: {session}\\n\\nWHAT TO DO:\\n• Stretch\\n• Rest eyes\\n• Drink water\\n• Move around"
        
        # Spawn 5 dialogs side-by-side
        for i in range(5):
            spawn_tkinter_dialog(i, msg)
            time.sleep(0.1)

def main():
    log("="*70)
    log("POMODORO TIMER - WITH PROGRESS BAR (BUG FIX)")
    log("="*70)
    log("Features: Animated progress bar, percentage display, FIXED dialog timeout")
    log("="*70)

    current_activity = None
    dialog_shown = False

    while True:
        now = datetime.now()
        activity = get_current_activity()

        # Activity changed
        if activity != current_activity:
            if activity is None:
                # Outside work hours
                if current_activity is not None:
                    print()  # New line
                    log(f"Outside work hours")
                current_activity = None
                dialog_shown = False
                time.sleep(60)
                continue

            # New activity started
            session = activity["session"]
            type_str = activity["type"]
            start = activity["start"]
            end = activity["end"]

            # Determine period
            period = "MORNING" if start < "12:00" else ("LUNCH" if type_str == "LUNCH" else "AFTERNOON")

            print()  # New line
            log(f"")
            log(f"[{period}] SESSION {session} - {type_str}")
            log(f"[{period}] SESSION {session} - {type_str}")
            log(f"Time: {start} - {end}")
            
            # Reserve space for the timer (print empty lines)
            print("\n" * 7)

            # Send notification
            if type_str == "WORK":
                send_notification("Pomodoro", f"Session {session}: Work time!", "Glass")
            elif "BREAK" in type_str:
                send_notification("Break", f"Session {session}: {type_str}", "Crystal")
            elif type_str == "LUNCH":
                send_notification("Lunch", "Enjoy your lunch!", "Submarine")

            current_activity = activity
            dialog_shown = False

        # During break, show dialog if not shown yet
        if current_activity and not dialog_shown:
            if "BREAK" in current_activity["type"] or current_activity["type"] == "LUNCH":
                # Check if screen unlocked
                if not is_screen_locked():
                    log("Showing break dialog...")
                    show_dialog(current_activity)
                    dialog_shown = True

        # Display countdown with progress bar
        if current_activity:
            # Calculate time
            start_time = datetime.strptime(current_activity["start"], "%H:%M").time()
            end_time = datetime.strptime(current_activity["end"], "%H:%M").time()

            start_dt = now.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
            end_dt = now.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)

            total_timedelta = end_dt - start_dt
            elapsed_timedelta = now - start_dt
            remaining_timedelta = end_dt - now

            total_seconds = total_timedelta.total_seconds()
            elapsed_seconds = elapsed_timedelta.total_seconds()
            remaining_seconds = remaining_timedelta.total_seconds()

            if remaining_seconds >= 0:
                # Calculate percentage REMAINING (100% = full time left, 0% = done)
                percentage = (remaining_seconds / total_seconds) * 100 if total_seconds > 0 else 0

                mins = int(remaining_seconds) // 60
                secs = int(remaining_seconds) % 60

                # Emoji based on type
                type_str = current_activity["type"]
                if type_str == "WORK":
                    emoji = "🔴"
                    label = "WORK"
                elif "LONG" in type_str:
                    emoji = "🟢"
                    label = "LONG BREAK"
                elif "SHORT" in type_str:
                    emoji = "🟡"
                    label = "SHORT BREAK"
                else:
                    emoji = "🍽️"
                    label = "LUNCH"

                # Create progress bar
                progress = create_progress_bar(percentage, remaining_seconds)

                # Dynamic Window Title
                set_terminal_title(f"{emoji} {mins:02d}:{secs:02d} - {label}")

                # ASCII Art
                time_str = f"{mins:02d}:{secs:02d}"
                ascii_art = generate_ascii_art(time_str)

                # Move cursor up 6 lines (5 for ASCII + 1 for progress bar) to overwrite
                # But only if we are not printing for the first time in this loop iteration?
                # Actually, \r only moves to start of line. We need \033[F (move up)
                # Let's clear screen or move cursor up.
                # Since we have log messages above, we don't want to clear entire screen.
                # We can print the ASCII art and progress bar, then move cursor up 6 lines.
                
                # Clear lines
                # \033[K clears to end of line
                # \033[A moves cursor up 1 line
                
                # Construct the full display string
                # ASCII Art (5 lines)
                # Gap (1 line)
                # Progress Bar (1 line)
                # Total height = 7 lines
                
                # We need to move up 7 lines to overwrite the previous frame
                # The first time we print, we are at the bottom, so we just print.
                # But subsequent times we need to move up.
                # To make it consistent, we can always print 7 lines.
                
                # Note: \033[K clears the line. We might need it if width changes.
                
                display = f"{ascii_art}\n\n{emoji} {label:12} | {mins:02d}:{secs:02d} | {progress}"
                
                # Move up 7 lines, print display, then flush.
                # We use \033[7A to move up 7 lines.
                # We use \r to move to the start of the line.
                # We use \033[J to clear from cursor to end of screen (cleans up any artifacts).
                print(f"\033[7A\r\033[J{display}", end="", flush=True)
                
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        log("\nStopped by user")
        os.system("pkill -f 'osascript' 2>/dev/null")
    except Exception as e:
        print()
        log(f"\nError: {e}")
        os.system("pkill -f 'osascript' 2>/dev/null")
        raise