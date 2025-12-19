# Phase 6: Statistics & Customization

## Viewing Statistics

Click **📊 Statistics** in the menu to access productivity insights.

### Summary

- **Daily Summary:** Today's session count, total focus time, and a breakdown by priority.
- **Weekly Summary:** Aggregated data for the current week.

### Task Duration Stats

See how much time you've spent on each task:

- **Daily:** Last 7 days, broken down by day.
- **Weekly:** Aggregated by week.
- **Monthly:** Aggregated by month.

### Mood Analysis

Track your emotional patterns over time:

- **Today / This Week / This Month / All Time**
- See which moods are most common
- Correlate moods with specific tasks

---

## Customizing the Schedule

The fixed schedule is defined in `main.py` under the `SCHEDULE` list.

### Example: Changing Work Hours

If you start work at 08:00 instead of 09:00:

1. Open `main.py` in a text editor.
2. Find the `SCHEDULE = [...]` block (around line 406).
3. Modify the `start` and `end` times for each session.
4. Restart the app.

### Example: Adding More Sessions

To add an 11th afternoon session:

```python
{"session": 11, "type": "WORK", "start": "18:00", "end": "18:25"},
{"session": 11, "type": "SHORT_BREAK", "start": "18:25", "end": "18:30"},
```

> **Warning:** Ensure times do not overlap and are in chronological order.

---

## Customizing Emojis and Icons

The app uses default emojis for activities. To change them:

1. Open the app's **Settings** page via browser (if available), or
2. Edit `settings.json` in the project root.

---

## Tips for Power Users

1. **Use Statistics Weekly:** Review your mood and task data every Friday to spot patterns.
2. **Leverage Quick Add:** Copy task lists from project management tools and paste them directly.
3. **Trust the Breaks:** Zen Mode exists for a reason – don't skip it!
4. **Customize Aggressively:** The code is yours – adjust the schedule, emojis, and even break durations to fit your rhythm.

---

**← Back to:** [Tutorial Index](README.md)
