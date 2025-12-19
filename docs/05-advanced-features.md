# Phase 5: Advanced Features

## ⚡ Urgent Mode

### What Is It?

Starting from **Session 7** (16:10 onwards), the app enters "Urgent Mode." A ⚡ icon appears next to any task that has **less than 20 minutes** of logged focus time today.

### Why Does It Exist?

The goal is to ensure you don't end the day with neglected tasks. By flagging under-worked tasks in the final stretch, you're reminded to give them attention before 18:00.

### Where Does It Appear?

1. **Menu Bar Title:** If any available task is "urgent," the title shows `⚡ WORK - [Task Name]`.
2. **Select Task Menu:** Each urgent task displays ⚡ next to its name.

### When Does It Disappear?

The ⚡ icon disappears automatically once a task accumulates 20 minutes of focus time (including the current session's elapsed time).

---

## 🎉 Go Home Now (18:00 Trigger)

At exactly **18:00**, the app opens `go_home.html` – a celebratory page that:

- Displays the current time
- Shows your total sessions and focus minutes for the day
- Plays a "go home" message

This is your cue to **stop working** and enjoy your evening!

---

## 🕐 Manual Mode (Off-Hours)

Outside of the fixed schedule (before 09:00, after 18:00, or on weekends), you can still use the app:

1. Click **▶️ Start Pomodoro**.
2. A dynamic schedule is generated:
   - 4 work sessions (25m each)
   - Short breaks (5m) between sessions
   - Long break (15m) after the 4th session
3. Click **⏹️ Stop Pomodoro** to end early.

> **Note:** If you're in Manual Mode and enter fixed schedule hours (e.g., it becomes 09:00 on a weekday), the dynamic schedule is automatically cleared.

---

## 😴 Sleep/Wake Handling

If your Mac goes to sleep or the screen locks:

1. The current session is **immediately saved** with the reflection: *"Session ended due to system sleep/lock."*
2. The timer is paused.
3. When you wake/unlock, the timer **resets to 0** for the current session.

> **Important Fix (v1.0.1):** The app no longer logs "ghost sessions" that occurred while your Mac was asleep.

---

**Next:** [Phase 6: Statistics & Customization →](06-statistics-customization.md)
