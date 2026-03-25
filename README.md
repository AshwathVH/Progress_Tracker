# 🚀 ML + GenAI Progress Tracker with SQLite Backend

A complete learning roadmap tracker with local database storage.

## 📋 Project Structure

```
progress tracker/
├── ML_GenAI_Roadmap.html      (Frontend - Open in browser)
├── app.py                      (Flask Backend API)
├── requirements.txt            (Python dependencies)
├── progress_tracker.db         (SQLite database - auto-created)
└── README.md                   (This file)
```

## 🛠️ Setup Instructions

### Step 1: Install Python Dependencies

Open PowerShell in the project folder and run:

```powershell
pip install -r requirements.txt
```

**What gets installed:**
- Flask (2.3.2) - Web framework
- Flask-CORS (4.0.0) - Cross-origin requests support

### Step 2: Start the Backend Server

Run in PowerShell:

```powershell
python app.py
```

You should see:
```
============================================================
🚀 ML/GenAI Progress Tracker Backend
============================================================
📁 Database: C:\Ashwath-VH\Projects\progress tracker\progress_tracker.db
🌐 Server: http://localhost:5000
============================================================
API Endpoints:
  GET  /api/health              - Health check
  POST /api/tasks/save          - Save tasks
  GET  /api/tasks/load          - Load tasks
  POST /api/time/save           - Save time
  GET  /api/time/today          - Get today's time
  GET  /api/streak/get          - Get streak
  POST /api/streak/increment    - Increment streak
  GET  /api/progress/summary    - Get summary
  GET  /api/stats/all           - Get all stats
  POST /api/reset               - Reset all data
============================================================
```

**Keep this terminal open!** The server needs to keep running.

### Step 3: Open the Frontend

Open `ML_GenAI_Roadmap.html` in your browser:

```
Right-click → Open With → Chrome/Firefox/Safari
```

Or paste in address bar:
```
file:///C:/Ashwath-VH/Projects/progress tracker/ML_GenAI_Roadmap.html
```

### Step 4: Check Connection Status

When the page loads, you'll see a status indicator in the top-right:
- ✅ **Green "Database Connected"** → Backend is running, data saves to SQLite
- 💾 **Red "Local Storage Only"** → Backend is offline, data saves to browser only

---

## 📊 What Gets Tracked

### Database Storage (SQLite):
- ✅ Task completion status
- ⏱️ Time spent per day
- 📈 Study streak count
- 🧠 Concepts learned
- 📊 Overall statistics

### Data Sync:
- Auto-saves every 30 seconds if backend is running
- Falls back to localStorage if backend goes offline
- Data persists even if you close the browser

---

## 🎯 Daily Workflow

1. **Start Server** → Open PowerShell, run `python app.py`
2. **Open Tracker** → Open HTML file in browser
3. **Begin Study** → Click "▶ Start" on timer
4. **Check Tasks** → Mark completed items
5. **Data Auto-Saves** → Every task checked + every 30 seconds
6. **Review Progress** → Check dashboard stats

---

## 📁 Database File

The SQLite database is created automatically at:
```
C:\Ashwath-VH\Projects\progress tracker\progress_tracker.db
```

To inspect the database, you can use:

**SQLite Browser (GUI):**
- Download: https://sqlitebrowser.org/
- Open `progress_tracker.db` to view/edit data visually

**PowerShell (Command Line):**
```powershell
sqlite3 progress_tracker.db
.tables
SELECT * FROM tasks;
```

---

## 🔧 Troubleshooting

### "Backend is offline" message?
**Solution:** Make sure `python app.py` is still running in PowerShell. Don't close that terminal!

### Changes not saving?
1. Check if backend is running (look for green status indicator)
2. Open browser DevTools (F12) → Console tab → look for errors
3. Restart the backend: Close PowerShell, run `python app.py` again

### Port 5000 already in use?
The backend uses port 5000. If it's already in use:
```python
# Edit app.py, line 239 (at bottom):
app.run(debug=True, host='localhost', port=5001)  # Change 5000 to 5001
```

Then update HTML API_URL:
```javascript
const API_URL = 'http://localhost:5001/api';  // Change in ML_GenAI_Roadmap.html
```

### Want to reset all data?
```powershell
# This will delete all tracked progress
curl -X POST http://localhost:5000/api/reset
```

---

## 📈 Viewing Statistics

The backend provides several stats endpoints:

**Summary (Overall Progress):**
```
GET http://localhost:5000/api/progress/summary
```

**Detailed Stats (Daily/Weekly):**
```
GET http://localhost:5000/api/stats/all
```

**Today's Time:**
```
GET http://localhost:5000/api/time/today
```

You can visit these in your browser or use tools like Postman/curl to see data.

---

## 🎓 Learning While Using This

This project teaches you:
- ✅ Flask REST APIs
- ✅ SQLite database design
- ✅ Frontend-backend communication
- ✅ CORS and API security basics
- ✅ Python async/await with fetch
- ✅ Data persistence patterns

---

## 🚀 Next Steps (Optional)

Want to extend this?

1. **Add Login System** - Track progress per user
2. **Deploy to Cloud** - AWS Lambda, Heroku, Railway
3. **Add Goals API** - Set weekly/monthly goals
4. **Mobile App** - React Native version
5. **Export Data** - CSV/PDF reports

---

## 📝 Notes

- All data saves locally - nothing goes to the cloud
- Backend must run on your machine for database features
- Works offline with localStorage fallback
- SQLite database is portable - copy `.db` file to backup

---

## ❓ Questions?

- Check console (F12) for error messages
- View database directly with SQLite Browser
- Review API responses at http://localhost:5000/api/progress/summary

**Happy Learning! 🎯**
