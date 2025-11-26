#!/usr/bin/env python3
"""
Pomodoro Timer - Menu Bar Application with Task Management
Displays Pomodoro timer in macOS menu bar with comprehensive task tracking
"""

import rumps
import subprocess
from datetime import datetime, timedelta
import time
import os
import webbrowser
import json
import uuid

# HARDCODED SCHEDULE (same as pomodoro_timer.py)
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


class TaskManager:
    """Manages tasks with CRUD operations"""
    
    def __init__(self, tasks_file):
        self.tasks_file = tasks_file
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    data = json.load(f)
                    return data.get('tasks', [])
            except:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump({'tasks': self.tasks}, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def add_task(self, name, priority="Medium"):
        """Add a new task"""
        task = {
            'id': str(uuid.uuid4()),
            'name': name,
            'priority': priority,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def edit_task(self, task_id, name=None, priority=None):
        """Edit an existing task"""
        for task in self.tasks:
            if task['id'] == task_id:
                if name:
                    task['name'] = name
                if priority:
                    task['priority'] = priority
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id):
        """Delete a task"""
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self.save_tasks()
        return True
    
    def get_task(self, task_id):
        """Get a specific task"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def get_all_active_tasks(self):
        """Get all active tasks"""
        return [t for t in self.tasks if t['status'] == 'active']


class SessionLogger:
    """Logs Pomodoro sessions with details"""
    
    def __init__(self, logs_file):
        self.logs_file = logs_file
        self.sessions = self.load_sessions()
    
    def load_sessions(self):
        """Load sessions from JSON file"""
        if os.path.exists(self.logs_file):
            try:
                with open(self.logs_file, 'r') as f:
                    data = json.load(f)
                    return data.get('sessions', [])
            except:
                return []
        return []
    
    def save_sessions(self):
        """Save sessions to JSON file"""
        try:
            with open(self.logs_file, 'w') as f:
                json.dump({'sessions': self.sessions}, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving sessions: {e}")
            return False
    
    def log_session(self, session_data):
        """Log a new session"""
        session = {
            'id': str(uuid.uuid4()),
            **session_data,
            'logged_at': datetime.now().isoformat()
        }
        self.sessions.append(session)
        self.save_sessions()
        return session
    
    def get_today_sessions(self):
        """Get today's sessions"""
        today = datetime.now().date()
        return [s for s in self.sessions 
                if datetime.fromisoformat(s['start_time']).date() == today]
    
    def get_week_sessions(self):
        """Get this week's sessions"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        return [s for s in self.sessions 
                if datetime.fromisoformat(s['start_time']).date() >= week_start]
    
    def get_sessions_by_task(self, task_id):
        """Get sessions for a specific task"""
        return [s for s in self.sessions if s.get('task_id') == task_id]
    
    def calculate_time_per_task(self):
        """Calculate total time spent per task"""
        task_times = {}
        for session in self.sessions:
            task_id = session.get('task_id')
            if task_id:
                duration = session.get('duration_minutes', 0)
                if task_id in task_times:
                    task_times[task_id]['minutes'] += duration
                    task_times[task_id]['sessions'] += 1
                else:
                    task_times[task_id] = {
                        'task_name': session.get('task_name', 'Unknown'),
                        'priority': session.get('priority', 'Medium'),
                        'minutes': duration,
                        'sessions': 1
                    }
        return task_times
    
    def get_mood_distribution(self):
        """Get mood distribution from sessions"""
        moods = {}
        for session in self.sessions:
            mood = session.get('mood')
            if mood:
                moods[mood] = moods.get(mood, 0) + 1
        return moods


class Analytics:
    """Generate analytics and reports"""
    
    def __init__(self, session_logger, task_manager):
        self.logger = session_logger
        self.task_manager = task_manager
    
    def generate_daily_summary(self):
        """Generate today's summary"""
        sessions = self.logger.get_today_sessions()
        work_sessions = [s for s in sessions if s.get('session_type') == 'WORK']
        
        total_minutes = sum(s.get('duration_minutes', 0) for s in work_sessions)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        # Get tasks worked on
        task_ids = set(s.get('task_id') for s in work_sessions if s.get('task_id'))
        
        # Find top task
        task_times = {}
        for session in work_sessions:
            tid = session.get('task_id')
            if tid:
                task_times[tid] = task_times.get(tid, 0) + session.get('duration_minutes', 0)
        
        top_task = None
        if task_times:
            top_task_id = max(task_times, key=task_times.get)
            top_task_mins = task_times[top_task_id]
            top_task_obj = self.task_manager.get_task(top_task_id)
            if top_task_obj:
                top_task = f"{top_task_obj['name']} ({top_task_mins // 60}h {top_task_mins % 60}m)"
        
        # Mood summary
        moods = [s.get('mood', '') for s in work_sessions if s.get('mood')]
        mood_str = ''.join(moods) if moods else 'No data'
        
        today_str = datetime.now().strftime("%b %d, %Y")
        
        summary = f"""📊 Today's Summary ({today_str})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sessions completed: {len(work_sessions)}
⏱️  Total focus time: {hours}h {minutes}m
📝 Tasks worked on: {len(task_ids)}

Top Task: {top_task or 'None'}
Mood: {mood_str}"""
        
        return summary
    
    def generate_weekly_summary(self):
        """Generate this week's summary"""
        sessions = self.logger.get_week_sessions()
        work_sessions = [s for s in sessions if s.get('session_type') == 'WORK']
        
        total_minutes = sum(s.get('duration_minutes', 0) for s in work_sessions)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        # Calculate scheduled sessions (rough estimate: 10 sessions/day * 5 days)
        scheduled = 50
        completion_rate = int((len(work_sessions) / scheduled) * 100) if scheduled > 0 else 0
        
        # Find most productive day
        day_times = {}
        for session in work_sessions:
            day = datetime.fromisoformat(session['start_time']).strftime("%A")
            day_times[day] = day_times.get(day, 0) + session.get('duration_minutes', 0)
        
        most_productive_day = "N/A"
        if day_times:
            top_day = max(day_times, key=day_times.get)
            top_mins = day_times[top_day]
            most_productive_day = f"{top_day} ({top_mins // 60}h {top_mins % 60}m)"
        
        # Top task
        task_times = self.logger.calculate_time_per_task()
        top_task = "None"
        if task_times:
            top_id = max(task_times, key=lambda x: task_times[x]['minutes'])
            top_data = task_times[top_id]
            mins = top_data['minutes']
            top_task = f"{top_data['task_name']} ({mins // 60}h {mins % 60}m)"
        
        # Overall mood
        mood_dist = self.logger.get_mood_distribution()
        overall_mood = "😊 Good" if mood_dist else "No data"
        
        today = datetime.now()
        week_start = (today - timedelta(days=today.weekday())).strftime("%b %d")
        week_end = today.strftime("%b %d, %Y")
        
        summary = f"""📊 This Week ({week_start} - {week_end})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sessions: {len(work_sessions)} / {scheduled} scheduled
⏱️  Focus time: {hours}h {minutes}m
📈 Completion rate: {completion_rate}%

Most productive day: {most_productive_day}
Top task: {top_task}
Overall mood: {overall_mood}"""
        
        return summary
    
    def get_task_time_breakdown(self):
        """Get time breakdown per task"""
        task_times = self.logger.calculate_time_per_task()
        
        if not task_times:
            return "📊 Time per Task\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nNo tasks tracked yet."
        
        # Sort by time spent (descending)
        sorted_tasks = sorted(task_times.items(), 
                            key=lambda x: x[1]['minutes'], 
                            reverse=True)
        
        lines = ["📊 Time per Task", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        
        for task_id, data in sorted_tasks:
            priority_badge = data['priority'][0]  # H, M, L
            name = data['task_name']
            mins = data['minutes']
            hours = mins // 60
            minutes = mins % 60
            sessions = data['sessions']
            
            line = f"[{priority_badge}] {name:20} {hours}h {minutes:02d}m  ({sessions} sessions)"
            lines.append(line)
        
        return '\n'.join(lines)
    
    def get_mood_analysis(self):
        """Get mood distribution analysis"""
        mood_dist = self.logger.get_mood_distribution()
        
        if not mood_dist:
            return "📊 Mood Analysis\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nNo mood data yet."
        
        total = sum(mood_dist.values())
        
        lines = ["📊 Mood Analysis", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        
        mood_names = {
            '😊': 'Good/Productive',
            '😓': 'Struggling',
            '🔥': 'Amazing/On Fire'
        }
        
        for mood, count in sorted(mood_dist.items(), key=lambda x: x[1], reverse=True):
            percentage = int((count / total) * 100)
            name = mood_names.get(mood, 'Unknown')
            line = f"{mood} {name:20} {count:3} sessions ({percentage}%)"
            lines.append(line)
        
        return '\n'.join(lines)


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


def send_notification(title, message, sound="Glass"):
    """Send macOS notification"""
    script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
    try:
        subprocess.run(['osascript', '-e', script], timeout=5)
    except:
        pass


def open_zen_mode():
    """Open the Zen Mode animation (index.html)"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(current_dir, "index.html")
        
        if os.path.exists(index_path):
            url = f"file://{index_path}"
            webbrowser.open(url)
    except Exception as e:
        print(f"Error opening Zen Mode: {e}")


class PomodoroMenuBarApp(rumps.App):
    def __init__(self):
        super(PomodoroMenuBarApp, self).__init__("🍅", quit_button=None)
        
        # Hide Dock icon (menu bar only app)
        try:
            from AppKit import NSApplication, NSApplicationActivationPolicyAccessory
            # Get the shared NSApplication instance
            app = NSApplication.sharedApplication()
            # Set activation policy to hide dock icon
            app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        except Exception as e:
            print(f"Could not hide Dock icon: {e}")
        
        # Initialize managers
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.task_manager = TaskManager(os.path.join(current_dir, "tasks.json"))
        self.session_logger = SessionLogger(os.path.join(current_dir, "session_logs.json"))
        self.analytics = Analytics(self.session_logger, self.task_manager)
        
        self.current_activity = None
        self.break_shown = False
        self.current_task = None
        self.session_start_time = None
        self.pending_feedback_session = None  # Store session data for later feedback
        self.break_start_time = None  # Track when break started
        self.feedback_shown_this_break = False  # Prevent showing feedback multiple times
        self.pulang_shown_today = False  # Track if pulang page shown today
        self.last_pulang_date = None  # Track date of last pulang page
        
        # Menu items - Session Info (with no-op callback to appear enabled)
        self.session_info = rumps.MenuItem("Not in session", callback=self.no_op)
        self.task_info = rumps.MenuItem("No task selected", callback=self.no_op)
        self.time_info = rumps.MenuItem("--:--", callback=self.no_op)
        self.progress_info = rumps.MenuItem("Progress: --", callback=self.no_op)
        self.next_info = rumps.MenuItem("Next: --", callback=self.no_op)
        
        # Build menu
        self.menu = [
            self.session_info,
            self.task_info,
            self.time_info,
            self.progress_info,
            None,  # Separator
            self.next_info,
            None,  # Separator
            self._build_tasks_menu(),
            None,  # Separator
            self._build_statistics_menu(),
            None,  # Separator
            rumps.MenuItem("Open Zen Mode", callback=self.open_zen),
            None,  # Separator
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
        
        # Start timer
        self.timer = rumps.Timer(self.update_timer, 1)
        self.timer.start()

    def _build_tasks_menu(self):
        """Build tasks submenu"""
        tasks_menu = rumps.MenuItem("📝 Tasks")
        tasks_menu.add(rumps.MenuItem("Select Task", callback=self.select_task))
        tasks_menu.add(rumps.MenuItem("Add New Task", callback=self.add_task))
        tasks_menu.add(rumps.MenuItem("Edit Task", callback=self.edit_task))
        tasks_menu.add(rumps.MenuItem("Delete Task", callback=self.delete_task))
        tasks_menu.add(rumps.MenuItem("View All Tasks", callback=self.view_all_tasks))
        return tasks_menu

    def _build_statistics_menu(self):
        """Build statistics submenu"""
        stats_menu = rumps.MenuItem("📊 Statistics")
        stats_menu.add(rumps.MenuItem("Today's Summary", callback=self.show_daily_summary))
        stats_menu.add(rumps.MenuItem("This Week", callback=self.show_weekly_summary))
        stats_menu.add(rumps.MenuItem("Time per Task", callback=self.show_time_per_task))
        stats_menu.add(rumps.MenuItem("Mood Analysis", callback=self.show_mood_analysis))
        return stats_menu

    def open_zen(self, _):
        """Callback to open Zen Mode"""
        open_zen_mode()
    
    def open_pulang_page(self):
        """Open PULANG SEKARANG page at 18:00"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pulang_path = os.path.join(current_dir, "pulang.html")
        
        if os.path.exists(pulang_path):
            webbrowser.open(f"file://{pulang_path}")
            send_notification(
                "PULANG SEKARANG! 🎉",
                "Saatnya istirahat, kerja hari ini sudah selesai!",
                "Glass"
            )
        else:
            print(f"Warning: pulang.html not found at {pulang_path}")
    
    def no_op(self, _):
        """Empty callback for info-only menu items"""
        pass

    def quit_app(self, _):
        """Quit the application"""
        rumps.quit_application()

    def get_emoji_and_label(self, type_str):
        """Get emoji and label based on activity type"""
        if type_str == "WORK":
            return "🔴", "WORK"
        elif "LONG" in type_str:
            return "🟢", "LONG BREAK"
        elif "SHORT" in type_str:
            return "🟡", "SHORT BREAK"
        elif type_str == "LUNCH":
            return "🍽️", "LUNCH"
        else:
            return "⏸️", "IDLE"

    def create_progress_bar(self, percentage, width=10):
        """Create visual progress bar with colored emoji blocks"""
        filled = int(width * percentage / 100)
        empty = width - filled
        # Use colored emoji blocks for better visual distinction
        # 🟦 = filled (blue), ⬜ = empty (light gray)
        return "🟦" * filled + "⬜" * empty

    def find_next_activity(self):
        """Find the next scheduled activity"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        for item in SCHEDULE:
            if item["start"] > current_time:
                period = "Morning" if item["start"] < "12:00" else ("Lunch" if item["type"] == "LUNCH" else "Afternoon")
                emoji, label = self.get_emoji_and_label(item["type"])
                return f"{emoji} {label} at {item['start']} ({period})"
        
        return "No more sessions today"

    # Task Management Callbacks
    def select_task(self, _):
        """Select a task from the list"""
        tasks = self.task_manager.get_all_active_tasks()
        
        if not tasks:
            rumps.alert("No Tasks", "Please create a task first!")
            return
        
        # Directly show task selection with numbered list
        self.show_task_selection_alert(tasks)

    def show_task_selection_alert(self, tasks):
        """Show task selection by task number input, grouped by priority"""
        if len(tasks) == 0:
            return
        
        # Group tasks by priority
        high_priority = [t for t in tasks if t['priority'] == 'High']
        medium_priority = [t for t in tasks if t['priority'] == 'Medium']
        low_priority = [t for t in tasks if t['priority'] == 'Low']
        
        # Create sorted array matching display order
        sorted_tasks = high_priority + medium_priority + low_priority
        
        # Build task list display grouped by priority with left padding
        task_displays = []
        numbered_index = 1
        
        if high_priority:
            task_displays.append("  === HIGH PRIORITY ===")  # Left padding
            for task in high_priority:
                task_displays.append(f"  {numbered_index}. [H] {task['name']}")  # Left padding
                numbered_index += 1
        
        if medium_priority:
            if task_displays:  # Add blank line between sections
                task_displays.append("")
            task_displays.append("  === MEDIUM PRIORITY ===")  # Left padding
            for task in medium_priority:
                task_displays.append(f"  {numbered_index}. [M] {task['name']}")  # Left padding
                numbered_index += 1
        
        if low_priority:
            if task_displays:  # Add blank line between sections
                task_displays.append("")
            task_displays.append("  === LOW PRIORITY ===")  # Left padding
            for task in low_priority:
                task_displays.append(f"  {numbered_index}. [L] {task['name']}")  # Left padding
                numbered_index += 1
        
        # Join with newlines for clean left-aligned text
        # Add invisible left-padding character to force left alignment
        message = "\n".join(task_displays)
        
        # Ask user to enter task number
        window = rumps.Window(
            message=f"Enter task number (1-{len(tasks)}):\n\n{message}\u200E",  # Added LTR mark
            title="Select Task",
            dimensions=(400, 24)  # Wider window for better display
        )
        
        response = window.run()
        if response.clicked and response.text:
            try:
                task_num = int(response.text)
                if 1 <= task_num <= len(sorted_tasks):
                    self.current_task = sorted_tasks[task_num - 1]  # Use sorted array!
                    self.update_task_display()
                    rumps.notification(
                        title="Task Selected",
                        subtitle=self.current_task['name'],
                        message=f"Priority: {self.current_task['priority']}"
                    )
                else:
                    rumps.alert("Invalid Number", f"Please enter a number between 1 and {len(tasks)}")
            except ValueError:
                rumps.alert("Invalid Input", "Please enter a valid number")

    def add_task(self, _):
        """Add a new task"""
        window = rumps.Window(
            message="Enter task name:",
            title="New Task",
            dimensions=(320, 24)
        )
        
        response = window.run()
        if response.clicked and response.text:
            # Ask for priority
            priority_response = rumps.alert(
                title="Select Priority",
                message=f"Task: {response.text}\n\nSelect priority level:",
                ok="High",
                cancel="Medium",
                other="Low"
            )
            
            if priority_response == 1:
                priority = "High"
            elif priority_response == 0:
                priority = "Medium"
            else:
                priority = "Low"
            
            task = self.task_manager.add_task(response.text, priority)
            rumps.notification(
                title="Task Created",
                subtitle=f"Priority: {priority}",
                message=response.text
            )

    def edit_task(self, _):
        """Edit an existing task"""
        tasks = self.task_manager.get_all_active_tasks()
        
        if not tasks:
            rumps.alert("No Tasks", "No tasks to edit!")
            return
        
        # Simple implementation: edit first task
        # In real app, you'd want a selection dialog
        rumps.alert("Edit Task", "Feature coming soon! For now, delete and recreate the task.")

    def delete_task(self, _):
        """Delete a task"""
        tasks = self.task_manager.get_all_active_tasks()
        
        if not tasks:
            rumps.alert("No Tasks", "No tasks to delete!")
            return
        
        # Simple implementation
        rumps.alert("Delete Task", "Feature coming soon!")

    def view_all_tasks(self, _):
        """View all tasks grouped by priority"""
        tasks = self.task_manager.get_all_active_tasks()
        
        if not tasks:
            rumps.alert("No Tasks", "You don't have any tasks yet!\n\nCreate one using 'Add New Task'.")
            return
        
        # Group tasks by priority
        high_priority = [t for t in tasks if t['priority'] == 'High']
        medium_priority = [t for t in tasks if t['priority'] == 'Medium']
        low_priority = [t for t in tasks if t['priority'] == 'Low']
        
        # Build task list display grouped by priority with left padding
        task_list = []
        numbered_index = 1
        
        if high_priority:
            task_list.append("  === HIGH PRIORITY ===")  # Left padding
            for task in high_priority:
                task_list.append(f"  {numbered_index}. [H] {task['name']}")  # Left padding
                numbered_index += 1
        
        if medium_priority:
            if task_list:  # Add blank line between sections
                task_list.append("")
            task_list.append("  === MEDIUM PRIORITY ===")  # Left padding
            for task in medium_priority:
                task_list.append(f"  {numbered_index}. [M] {task['name']}")  # Left padding
                numbered_index += 1
        
        if low_priority:
            if task_list:  # Add blank line between sections
                task_list.append("")
            task_list.append("  === LOW PRIORITY ===")  # Left padding
            for task in low_priority:
                task_list.append(f"  {numbered_index}. [L] {task['name']}")  # Left padding
                numbered_index += 1
        
        # Join with newlines for clean left-aligned text
        message = "\n".join(task_list)
        # Add LTR mark for left alignment
        rumps.alert(title="All Tasks", message=message + "\u200E")

    # Statistics Callbacks
    def show_daily_summary(self, _):
        """Show today's summary"""
        summary = self.analytics.generate_daily_summary()
        rumps.alert(title="Daily Summary", message=summary)

    def show_weekly_summary(self, _):
        """Show weekly summary"""
        summary = self.analytics.generate_weekly_summary()
        rumps.alert(title="Weekly Summary", message=summary)

    def show_time_per_task(self, _):
        """Show time breakdown per task"""
        breakdown = self.analytics.get_task_time_breakdown()
        rumps.alert(title="Time per Task", message=breakdown)

    def show_mood_analysis(self, _):
        """Show mood analysis"""
        analysis = self.analytics.get_mood_analysis()
        rumps.alert(title="Mood Analysis", message=analysis)

    def update_task_display(self):
        """Update task info in menu"""
        if self.current_task:
            priority_badge = f"[{self.current_task['priority'][0]}]"
            self.task_info.title = f"Task: {self.current_task['name']} {priority_badge}"
        else:
            self.task_info.title = "No task selected"

    def prompt_task_selection(self):
        """Prompt user to select a task at start of work session"""
        # If task already selected, don't prompt again
        if self.current_task:
            return
        
        tasks = self.task_manager.get_all_active_tasks()
        
        if not tasks:
            response = rumps.alert(
                title="No Tasks",
                message="You don't have any tasks!\n\nWould you like to create one?",
                ok="Create Task",
                cancel="Skip (Not Recommended)"
            )
            if response == 1:
                self.add_task(None)
                # After creating, try to select it
                tasks = self.task_manager.get_all_active_tasks()
                if tasks:
                    self.current_task = tasks[-1]  # Select the newly created task
                    self.update_task_display()
        else:
            # Show task selection dialog
            self.show_task_selection_alert(tasks)
            # If still no task after dialog, show reminder
            if not self.current_task:
                rumps.notification(
                    title="No Task Selected",
                    subtitle="Work session started",
                    message="⚠️ Please select a task from menu for tracking"
                )

    def prompt_session_feedback(self):
        """Save session immediately and optionally prompt for feedback later (non-blocking)"""
        if not self.session_start_time:
            return  # No session to log
        
        # Calculate actual duration
        end_time = datetime.now()
        actual_duration = int((end_time - self.session_start_time).total_seconds() / 60)
        duration = min(actual_duration, 25)  # Cap at 25 minutes
        
        # Prepare session data
        if self.current_task:
            # Session with task
            session_data = {
                'task_id': self.current_task['id'],
                'task_name': self.current_task['name'],
                'priority': self.current_task['priority'],
                'session_type': 'WORK',
                'session_number': self.current_activity.get('session', 0) if self.current_activity else 0,
                'start_time': self.session_start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_minutes': duration,
                'mood': '',  # Will be filled later
                'reflection': '',  # Will be filled later
                'blockers': '',  # Will be filled later
                'completed': True
            }
        else:
            # Session without task - still log it!
            session_data = {
                'task_id': 'no-task',
                'task_name': '(No Task Selected)',
                'priority': 'None',
                'session_type': 'WORK',
                'session_number': self.current_activity.get('session', 0) if self.current_activity else 0,
                'start_time': self.session_start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_minutes': duration,
                'mood': '',
                'reflection': '',
                'blockers': 'No task was selected for this session',
                'completed': True
            }
        
        # Log session immediately
        logged_session = self.session_logger.log_session(session_data)
        
        # Store for potential feedback update later
        self.pending_feedback_session = {
            'session_id': logged_session['id'],
            'task_name': self.current_task['name']
        }
        
        # Show simple notification - break can start immediately!
        rumps.notification(
            title="Session Complete!",
            subtitle=f"{duration}min on {self.current_task['name']}",
            message="Enjoy your break! ☕"
        )
    
    def prompt_feedback_during_break(self):
        """Show feedback dialogs during break time (optional, non-blocking)"""
        if not self.pending_feedback_session:
            return
        
        task_name = self.pending_feedback_session['task_name']
        
        # Mood tracker
        mood_response = rumps.alert(
            title="How was your session?",
            message=f"Task: {task_name}\n\n(Optional - you can skip this)",
            ok="😊 Good",
            cancel="Skip",
            other="🔥 Amazing"
        )
        
        if mood_response == 0:  # User clicked Skip
            self.pending_feedback_session = None
            return
        
        mood_map = {1: "😊", -1: "🔥"}
        mood = mood_map.get(mood_response, "😊")
        
        # Reflection (optional)
        reflection_window = rumps.Window(
            message="What did you accomplish? (optional)",
            title="Quick Reflection",
            dimensions=(320, 60)
        )
        reflection_response = reflection_window.run()
        reflection = reflection_response.text if reflection_response.clicked else ""
        
        # Blockers (optional)
        blocker_window = rumps.Window(
            message="Any blockers or issues? (optional)",
            title="Blocker Tracking",
            dimensions=(320, 60)
        )
        blocker_response = blocker_window.run()
        blockers = blocker_response.text if blocker_response.clicked else ""
        
        # Update the logged session with feedback
        session_id = self.pending_feedback_session['session_id']
        for session in self.session_logger.sessions:
            if session['id'] == session_id:
                session['mood'] = mood
                session['reflection'] = reflection
                session['blockers'] = blockers
                break
        
        self.session_logger.save_sessions()
        self.pending_feedback_session = None
        
        # Show confirmation
        rumps.notification(
            title="Feedback Saved",
            subtitle=f"Mood: {mood}",
            message="Thanks for the feedback!"
        )

    @rumps.timer(1)
    def update_timer(self, _):
        """Update timer every second"""
        now = datetime.now()
        activity = get_current_activity()

        # Check for activity change
        if activity != self.current_activity:
            # Session ended - save immediately, don't block for feedback
            if self.current_activity and self.current_activity.get('type') == 'WORK':
                self.prompt_session_feedback()  # Non-blocking now!
            
            self.current_activity = activity
            self.break_shown = False
            
            # New work session started
            if activity and activity.get('type') == 'WORK':
                self.session_start_time = now
                self.prompt_task_selection()
                self.feedback_shown_this_break = False  # Reset for next break
            
            # Break started - track start time for feedback timing
            if activity and ('BREAK' in activity.get('type', '') or activity.get('type') == 'LUNCH'):
                self.break_start_time = now
                self.feedback_shown_this_break = False
            
            # Send notification on activity change
            if activity:
                type_str = activity["type"]
                session = activity["session"]
                
                if type_str == "WORK":
                    send_notification("Pomodoro", f"Session {session}: Work time!", "Glass")
                elif "BREAK" in type_str:
                    send_notification("Break", f"Session {session}: {type_str}", "Crystal")
                    # Open Zen Mode for breaks
                    if not self.break_shown:
                        open_zen_mode()
                        self.break_shown = True
                elif type_str == "LUNCH":
                    send_notification("Lunch", "Enjoy your lunch!", "Submarine")
        
        # Show feedback dialog after 1 minute into break (non-blocking)
        if self.current_activity and ('BREAK' in self.current_activity.get('type', '') or self.current_activity.get('type') == 'LUNCH'):
            if self.break_start_time and not self.feedback_shown_this_break:
                elapsed_in_break = (now - self.break_start_time).total_seconds()
                # Show feedback after 60 seconds (1 minute) into break
                if elapsed_in_break >= 60:
                    self.prompt_feedback_during_break()
                    self.feedback_shown_this_break = True
        
        # Check for end of work day (18:00) - open PULANG page
        if now.hour == 18 and now.minute == 0:
            today_date = now.date()
            if self.last_pulang_date != today_date:
                self.last_pulang_date = today_date
                self.open_pulang_page()

        # Update display
        if activity is None:
            # Weekend or outside work hours
            if now.weekday() >= 5:
                self.title = "🏖️"
                self.session_info.title = "Weekend - Enjoy!"
            else:
                self.title = "⏸️"
                self.session_info.title = "Outside work hours"
            
            self.time_info.title = "No active session"
            self.progress_info.title = "Progress: --"
            self.next_info.title = f"Next: {self.find_next_activity()}"
            self.task_info.title = "No task selected"
        else:
            # Calculate ELAPSED time (count UP)
            start_time = datetime.strptime(activity["start"], "%H:%M").time()
            end_time = datetime.strptime(activity["end"], "%H:%M").time()

            start_dt = now.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
            end_dt = now.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)

            total_timedelta = end_dt - start_dt
            elapsed_timedelta = now - start_dt
            remaining_timedelta = end_dt - now

            total_seconds = total_timedelta.total_seconds()
            elapsed_seconds = elapsed_timedelta.total_seconds()
            remaining_seconds = remaining_timedelta.total_seconds()

            if remaining_seconds >= 0:
                # Calculate percentage based on ELAPSED time (count up)
                percentage = (elapsed_seconds / total_seconds) * 100 if total_seconds > 0 else 0
                
                # Display ELAPSED time (count up)
                mins = int(elapsed_seconds) // 60
                secs = int(elapsed_seconds) % 60

                # Get emoji and label
                type_str = activity["type"]
                session = activity["session"]
                emoji, label = self.get_emoji_and_label(type_str)

                # Update menu bar title with task name
                if self.current_task and type_str == "WORK":
                    priority_badge = f"[{self.current_task['priority'][0]}]"
                    task_name = self.current_task['name']
                    # Truncate task name if too long
                    if len(task_name) > 15:
                        task_name = task_name[:12] + "..."
                    self.title = f"{emoji} {mins:02d}:{secs:02d} - {priority_badge} {task_name}"
                else:
                    self.title = f"{emoji} {mins:02d}:{secs:02d}"

                # Update menu items
                period = "Morning" if activity["start"] < "12:00" else ("Lunch" if type_str == "LUNCH" else "Afternoon")
                self.session_info.title = f"[{period}] Session {session} - {label}"
                self.time_info.title = f"Time: {activity['start']} - {activity['end']}"
                
                # Progress bar (count up)
                progress_bar = self.create_progress_bar(percentage)
                self.progress_info.title = f"Progress: {progress_bar} {percentage:.0f}%"
                
                # Next activity
                self.next_info.title = f"Next: {self.find_next_activity()}"
                
                # Update task display
                self.update_task_display()


if __name__ == "__main__":
    app = PomodoroMenuBarApp()
    app.run()
