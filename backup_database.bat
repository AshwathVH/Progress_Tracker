@echo off
cd /d "%~dp0"
setlocal enabledelayedexpansion

REM Create backup folder if it doesn't exist
if not exist "backups" mkdir backups

REM Create timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set timestamp=!mydate!_!mytime!

REM Copy database to backup
if exist "progress_tracker.db" (
    copy "progress_tracker.db" "backups\progress_tracker_!timestamp!.db"
    echo ✅ Backup created: backups\progress_tracker_!timestamp!.db
) else (
    echo ⚠️  No database file found to backup
)

echo.
echo 📂 Backups folder: %CD%\backups
echo.
pause
