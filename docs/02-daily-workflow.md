# Phase 2: Daily Workflow

## Understanding the Fixed Schedule

PomodoroWork operates on a **fixed schedule** during weekdays (Monday–Friday). Here's the breakdown:

| Period | Time | Sessions | Pattern |
|--------|------|----------|---------|
| Morning | 09:00 – 12:00 | 1 – 6 | 25m Work / 5m Break (Long break after Session 4) |
| Lunch | 12:00 – 13:00 | — | 60m Break |
| Afternoon | 13:00 – 18:00 | 1 – 10 | 25m Work / 5m Break (Long breaks after Sessions 4 & 8) |

### How it works:
- **Zero-Touch Transitions:** You don't need to press "Start" or "Stop." The app constantly checks the system clock and shifts to the correct activity (WORK/BREAK/LUNCH) based on the table above.
- **Session Numbers:** These are primarily used for logging and tracking. In the afternoon, **Session 7 and above (starting at 16:10)** are special—they trigger **Urgent Mode** for tasks with low focus time (see [Phase 5](05-advanced-features.md)).
- **Customizable:** If your workday starts early or ends late, you can define your own schedule by editing the `SCHEDULE` list in `main.py` (around line 406).

> **Note:** Session numbers reset after lunch. "Session 7" in the afternoon begins at 16:10.

## Operating Modes: Automatic vs. Manual

The app behaves differently depending on the time of day and your manual input:

### 1. Automatic Mode (Fixed Schedule)
- **Time:** Weekdays (Mon-Fri), 09:00 – 18:00.
- **Workflow:** You don't need to start anything. Just select a task. The app moves through work/break sessions automatically based on the clock.

### 2. Manual Mode (Dynamic Schedule)
- **Time:** Outside work hours (Early morning, Nights, Weekends).
- **Workflow:** You must click **▶️ Start Pomodoro**. The app then generates a custom schedule (25m work/5m break) starting from that moment.

### How they interact (Priority):
The **Fixed Schedule always wins**. If you are manually working at 08:50 AM on a Monday, once the clock hits 09:00 AM, the app will automatically terminate your manual session and switch over to the official "Morning Session 1" schedule.

---

## Starting Your First Work Session

When the clock hits a scheduled work period (e.g., 09:00):

1. The menu bar icon changes to show **WORK - [Task Name] - [End Time]**.
2. A notification appears: *"Session 1: Work time!"*
3. If you haven't selected a task, a reminder will pop up.

### Selecting a Task

1. Click the 🍅 icon.
2. Go to **📝 Select Task**.
3. Choose a task from the priority groups (High, Medium, Low).

The menu bar will now display your task name, and the timer counts **up** to show how long you've been focused.

## Switching Tasks Mid-Session

If you need to change tasks during a work session:

1. Open **📝 Select Task** again.
2. Choose the new task.
3. The app will **automatically log** the time spent on the previous task and reset the timer for the new one.

> **Tip:** Frequent task switching is tracked, so try to stay on one task per session when possible!

---

**Next:** [Phase 3: Task Management →](03-task-management.md)
