# Stop (bootout)
launchctl bootout gui/$(id -u)/com.developer.pomodoro

# Start (bootstrap)
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.developer.pomodoro.plist

# Restart
launchctl bootout gui/$(id -u)/com.developer.pomodoro
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.developer.pomodoro.plist

# Cek status
launchctl list | grep pomodoro

# Lihat log
tail -f /Users/developer/pomodoro_terminal/pomodoro_output.log

brew install python-tk@3.13