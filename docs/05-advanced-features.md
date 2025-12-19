# Phase 5: Advanced Features

## 🎉 End of Workday (Go Home Page)

When the last session in your `SCHEDULE` concludes, the app automatically opens `go_home.html` – a celebratory page that:

- Displays the current time
- Shows your total sessions and focus minutes for the day
- Plays a "go home" message

This is your cue to **stop working** and enjoy your evening!

---

## 🕐 Manual Mode (Off-Hours)

Outside of the fixed schedule defined in `main.py` (before the first session, after the last session, or on weekends), you can still use the app:

1. Click **▶️ Start Pomodoro**.
2. A dynamic schedule is generated:
   - 4 work sessions (25m each)
   - Short breaks (5m) between sessions
   - Long break (15m) after the 4th session
3. Click **⏹️ Stop Pomodoro** to end early.

> **Note:** If you're in Manual Mode and enter fixed schedule hours (based on your `SCHEDULE` definition), the dynamic schedule is automatically cleared to follow the fixed routine.

---

## 😴 Sleep/Wake Handling

If your Mac goes to sleep or the screen locks:

1. The current session is **immediately saved** with the reflection: *"Session ended due to system sleep/lock."*
2. The timer is paused.
3. When you wake/unlock, the timer **resets to 0** for the current session.

> **Important Fix (v1.0.1):** The app no longer logs "ghost sessions" that occurred while your Mac was asleep.

---

**Next:** [Phase 6: Statistics & Customization →](06-statistics-customization.md)
