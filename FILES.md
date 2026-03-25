# 📂 Files Created & What Each Does

## Core Application Files

### 1. **app.py** (Flask Backend - Core)
- SQLite database management
- REST API endpoints for storing/retrieving progress
- Records: tasks, time, streak, concepts
- Auto-syncs every 30 seconds
- **What it does:** Stores all your learning data

### 2. **ML_GenAI_Roadmap.html** (Frontend - Updated)
- Your study tracker interface
- Communicates with Flask backend
- Saves to database if server is running
- Falls back to browser storage if server offline
- **What it does:** Your daily tracking dashboard

### 3. **requirements.txt** (Dependencies)
- Flask 2.3.2 - Web framework
- Flask-CORS 4.0.0 - API cross-origin support
- Install with: `pip install -r requirements.txt`

## Utility Files

### 4. **start_server.bat** (Easy Start ⭐ USE THIS)
- Double-click to start backend
- Auto-installs dependencies if needed
- Keeps terminal open (don't close this!)
- Shows server status

### 5. **backup_database.bat** (Backup Tool)
- Backs up your database with timestamp
- Creates `backups/` folder
- Use before major updates
- Double-click to backup

## Documentation Files

### 6. **README.md** (Complete Guide)
- Full setup instructions
- API endpoints documentation
- Troubleshooting tips
- Database inspection methods

### 7. **QUICKSTART.md** (Fast Guide)
- 3-step setup
- How to verify it's working
- Most important info only

### 8. **FILES.md** (This File)
- What each file does
- File descriptions

## Database File (Auto-Created)

### 9. **progress_tracker.db**
- Created automatically on first run
- SQLite database file
- Stores all your tracking data
- Backup this file regularly!

---

# 🚀 HOW TO USE

## First Time Setup (One-Time Only)

```powershell
cd "C:\Ashwath-VH\Projects\progress tracker"
pip install -r requirements.txt
```

## Daily Usage (Every Study Session)

### Option 1: Easy Way (Recommended) ⭐
```
1. Double-click: start_server.bat
2. Wait for "✅ Ready!" message
3. Open: ML_GenAI_Roadmap.html in browser
4. Start studying!
```

### Option 2: Manual Way
```powershell
# Terminal 1 (Keep Open):
cd "C:\Ashwath-VH\Projects\progress tracker"
python app.py

# Browser:
Open ML_GenAI_Roadmap.html
```

---

# ✅ Verification Checklist

After opening the tracker in browser:

- [ ] Green status "✅ Database Connected" in top-right
- [ ] Can click checkboxes to mark tasks
- [ ] Timer works (Start/Pause buttons)
- [ ] Data displays in dashboard

If you see red "💾 Local Storage Only":
- Make sure start_server.bat is still running
- Check if terminal closed accidentally

---

# 📊 Data Storage

**While Backend is Running:**
- ✅ Saves to SQLite (progress_tracker.db)
- ✅ Also backs up to localStorage
- ✅ Auto-syncs every 30 seconds

**If Backend Goes Offline:**
- ✅ Automatically uses localStorage
- ✅ Data not lost
- ✅ Syncs to database when backend restarts

---

# 🔍 Viewing Your Data

### Database File Location:
```
C:\Ashwath-VH\Projects\progress tracker\progress_tracker.db
```

### View Data:
1. Download SQLite Browser: https://sqlitebrowser.org/
2. Open `progress_tracker.db`
3. Click tabs to browse tables:
   - `tasks` - Completed tasks
   - `time_tracking` - Hours spent
   - `study_streak` - Consecutive days
   - `concepts` - Learned concepts

### Or SQL Query:
```sql
-- See all tasks
SELECT * FROM tasks;

-- See time spent
SELECT date, hours_spent FROM time_tracking;

-- See streak
SELECT streak_count FROM study_streak;
```

---

# 🛠️ Common Tasks

## Backup Your Data
```
Double-click: backup_database.bat
# Creates timestamped backup in backups/ folder
```

## Reset All Data
**⚠️ WARNING: This cannot be undone!**

```powershell
curl -X POST http://localhost:5000/api/reset
```

## Check Backend Status
Visit in browser:
```
http://localhost:5000/api/health
```

Should return:
```json
{"status":"ok","timestamp":"2026-03-24T..."}
```

---

# 📱 Architecture Overview

```
Browser (ML_GenAI_Roadmap.html)
         ↓ (Send/Receive Data)
    Flask API (app.py)
         ↓
    SQLite Database (progress_tracker.db)
         ↓
    Stored on Your Computer
```

- No cloud upload
- No internet required (except initial setup)
- All data stays on your machine
- Fully offline capable

---

# 🎯 Next Steps

1. **Double-click** `start_server.bat`
2. **Open** `ML_GenAI_Roadmap.html` 
3. **Verify** green status indicator
4. **Start** your ML journey! 🎓

---

**All files are in:** `C:\Ashwath-VH\Projects\progress tracker\`

Happy learning! 🚀
