# Phase 3: Task Management

## Adding Tasks

### Method 1: Web Interface

1. Click **⚙️ Manage Tasks** → **Add New Task**.
2. Your browser opens a form where you can enter:
   - **Task Name** (required)
   - **Priority** (High, Medium, Low)
   - **Repeat Schedule** (optional: daily, weekly, monthly, yearly)
   - **Allowed Days** (which days of the week this task should appear)
3. Click **Create Task**.

### Method 2: Quick Add (Paste)

If you have a list of tasks copied from another app (e.g., Notes, Slack):

1. Copy the text to your clipboard.
2. Click **⚙️ Manage Tasks** → **Quick Add (Paste)**.
3. The app will parse each line as a separate task.

## Editing Tasks

1. Click **⚙️ Manage Tasks** → **Edit Task**.
2. Select the priority group, then the specific task.
3. Your browser opens with the task's current details pre-filled.
4. Make changes and click **Save Changes**.

## Deleting Tasks

1. Click **⚙️ Manage Tasks** → **Delete Task**.
2. Select the task to delete.
3. Confirm the deletion.

> **Note:** Deleted tasks are "soft deleted" – their session history is preserved for statistics.

## Restoring or Permanently Deleting Tasks

If you accidentally deleted a task or want to permanently remove it from the system:

1. Click **⚙️ Manage Tasks** → **View Deleted Tasks**.
2. A window will appear listing all soft-deleted tasks grouped by priority.
3. **To Permanently Delete:** Enter the number of the task in the text field and click **OK**. You will be asked for a final confirmation.
4. **To Restore:** Currently, restoration is handled by creating the task again or manually editing the `tasks.json` file.

## Marking Tasks Complete

Use this feature when you have finished a task for the day, even if you spent less than the recommended 20 minutes.

1. Click **⚙️ Manage Tasks** → **Mark Complete for Today**.
2. Select the task from the list.
3. The task will be hidden from the "Select Task" menu until its next scheduled appearance (e.g., tomorrow for daily tasks).

### Smart Behavior:
- **Auto-Logging:** If you mark a task as complete **while it is currently active**, the app will automatically log your elapsed focus time as a finished session before clearing the task from the menu bar.
- **Urgent Mode Fix:** This is the primary way to remove the ⚡ icon early. If a task is flagged as "Urgent" but you've already finished it, marking it complete will hide the task and the icon immediately.
- **One-Time Tasks:** If a task has no repeat schedule, marking it complete will **permanently delete** it (since it's no longer needed).

---

---

**Next:** [Phase 4: Breaks & Feedback →](04-breaks-and-feedback.md)
