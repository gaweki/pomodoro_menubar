# Pomodoro Menu Bar Timer - Documentation

## Overview

Aplikasi menu bar macOS yang menampilkan Pomodoro timer di taskbar atas dengan real-time countdown dan visual indicators.

## Features

✅ **Real-time Countdown**: Timer ditampilkan di menu bar dengan format `🔴 25:00`
✅ **Visual Indicators**: Emoji berbeda untuk setiap jenis aktivitas
- 🔴 WORK session
- 🟡 SHORT BREAK 
- 🟢 LONG BREAK
- 🍽️ LUNCH
- 🏖️ Weekend
- ⏸️ Idle (outside work hours)

✅ **Menu Dropdown**: Klik icon untuk melihat:
- Session info (Morning/Afternoon, Session #, Type)
- Time range (start - end)
- Progress bar dengan percentage
- Next activity preview
- Quick access ke Zen Mode
- Quit option

✅ **Auto Notifications**: 
- Notifikasi otomatis saat activity berubah
- Zen Mode dibuka otomatis saat break

✅ **Weekend Detection**: Otomatis mendeteksi weekend dan menampilkan 🏖️

## Installation

### 1. Install Dependencies

```bash
pip3 install rumps
```

### 2. Run the Application

**Manual Run:**
```bash
python3 /Users/developer/pomodoro_terminal/pomodoro_menubar.py
```

**Run as Background Service (Recommended):**

Create LaunchAgent plist file:

```bash
nano ~/Library/LaunchAgents/com.developer.pomodoro.menubar.plist
```

Paste this content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.developer.pomodoro.menubar</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/developer/pomodoro_terminal/pomodoro_menubar.py</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/developer/pomodoro_terminal/menubar_output.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/developer/pomodoro_terminal/menubar_error.log</string>
</dict>
</plist>
```

Load the service:

```bash
launchctl load ~/Library/LaunchAgents/com.developer.pomodoro.menubar.plist
```

Check status:

```bash
launchctl list | grep pomodoro
```

## Usage

1. **Timer Display**: Timer akan otomatis muncul di menu bar sesuai schedule
2. **View Details**: Klik icon di menu bar untuk melihat detail session
3. **Zen Mode**: Klik "Open Zen Mode" di menu untuk membuka halaman Zen Mode manual
4. **Quit**: Klik "Quit" untuk menutup aplikasi

## Schedule

Aplikasi menggunakan schedule yang sama dengan `pomodoro_timer.py`:

**Morning**: 09:00 - 12:00 (6 sessions)
**Lunch**: 12:00 - 13:00
**Afternoon**: 13:00 - 18:00 (10 sessions)

Setiap session:
- Work: 25 menit
- Short Break: 5 menit
- Long Break: 15 menit (setiap 4 session)

## Troubleshooting

### Menu bar tidak muncul
- Pastikan rumps sudah terinstal: `pip3 list | grep rumps`
- Check log file: `tail -f ~/pomodoro_terminal/menubar_error.log`

### Timer tidak update
- Restart aplikasi
- Atau restart LaunchAgent: 
  ```bash
  launchctl unload ~/Library/LaunchAgents/com.developer.pomodoro.menubar.plist
  launchctl load ~/Library/LaunchAgents/com.developer.pomodoro.menubar.plist
  ```

### Zen Mode tidak terbuka
- Pastikan file `index.html` ada di folder yang sama
- Check browser default settings

## Integration dengan pomodoro_timer.py

Kedua aplikasi bisa berjalan bersamaan:
- `pomodoro_timer.py`: Terminal-based dengan ASCII art
- `pomodoro_menubar.py`: Menu bar display

Atau jalankan salah satu sesuai preferensi.

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/com.developer.pomodoro.menubar.plist
rm ~/Library/LaunchAgents/com.developer.pomodoro.menubar.plist
```
