import sqlite3
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'progress_tracker.db')

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT UNIQUE NOT NULL,
            is_completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Time tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE DEFAULT CURRENT_DATE,
            hours_spent REAL DEFAULT 0,
            timer_seconds INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Study streak table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_streak (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            streak_count INTEGER DEFAULT 0,
            last_study_date DATE,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Concepts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_id TEXT NOT NULL,
            concept_name TEXT NOT NULL,
            is_learned BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# ==================== API ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/tasks/save', methods=['POST'])
def save_tasks():
    """Save task completion status"""
    try:
        data = request.json
        tasks = data.get('tasks', {})
        
        conn = get_db()
        cursor = conn.cursor()
        
        for task_id, is_completed in tasks.items():
            cursor.execute('''
                INSERT OR REPLACE INTO tasks (task_id, is_completed, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (task_id, is_completed))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Tasks saved'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/tasks/load', methods=['GET'])
def load_tasks():
    """Load all tasks"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT task_id, is_completed FROM tasks')
        
        tasks = {row['task_id']: row['is_completed'] for row in cursor.fetchall()}
        conn.close()
        
        return jsonify({'status': 'success', 'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/time/save', methods=['POST'])
def save_time():
    """Save time spent tracking"""
    try:
        data = request.json
        hours_spent = data.get('hours_spent', 0)
        timer_seconds = data.get('timer_seconds', 0)
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO time_tracking (hours_spent, timer_seconds)
            VALUES (?, ?)
        ''', (hours_spent, timer_seconds))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Time saved'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/time/today', methods=['GET'])
def get_today_time():
    """Get time spent today"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(hours_spent) as total_hours, SUM(timer_seconds) as total_seconds
            FROM time_tracking
            WHERE date = DATE('now')
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        total_hours = result['total_hours'] or 0
        total_seconds = result['total_seconds'] or 0
        
        return jsonify({
            'status': 'success',
            'hours': float(total_hours),
            'seconds': int(total_seconds)
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/streak/get', methods=['GET'])
def get_streak():
    """Get current study streak"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT streak_count, last_study_date FROM study_streak ORDER BY id DESC LIMIT 1')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                'status': 'success',
                'streak': result['streak_count'],
                'last_date': result['last_study_date']
            }), 200
        else:
            return jsonify({'status': 'success', 'streak': 0, 'last_date': None}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/streak/increment', methods=['POST'])
def increment_streak():
    """Increment study streak"""
    try:
        data = request.json
        new_streak = data.get('streak', 1)
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO study_streak (streak_count, last_study_date, updated_at)
            VALUES (?, DATE('now'), CURRENT_TIMESTAMP)
        ''', (new_streak,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'streak': new_streak}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/progress/summary', methods=['GET'])
def get_progress_summary():
    """Get overall progress summary"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Total tasks
        cursor.execute('SELECT COUNT(*) as total, SUM(is_completed) as completed FROM tasks')
        tasks = cursor.fetchone()
        
        # Total time
        cursor.execute('SELECT SUM(hours_spent) as total_hours FROM time_tracking')
        time_data = cursor.fetchone()
        
        # Current streak
        cursor.execute('SELECT streak_count FROM study_streak ORDER BY id DESC LIMIT 1')
        streak = cursor.fetchone()
        
        conn.close()
        
        total_tasks = tasks['total'] or 0
        completed_tasks = tasks['completed'] or 0
        total_hours = time_data['total_hours'] or 0
        streak_count = streak['streak_count'] if streak else 0
        progress_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return jsonify({
            'status': 'success',
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress_percent': round(progress_percent, 2),
            'total_hours': round(total_hours, 1),
            'streak': streak_count
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats/all', methods=['GET'])
def get_all_stats():
    """Get complete statistics"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Weekly stats
        cursor.execute('''
            SELECT 
                DATE(date) as week_date,
                COUNT(DISTINCT DATE(date)) as study_days,
                SUM(hours_spent) as total_hours
            FROM time_tracking
            WHERE date >= DATE('now', '-7 days')
            GROUP BY DATE(date)
        ''')
        weekly_stats = [dict(row) for row in cursor.fetchall()]
        
        # Overall stats
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT DATE(date)) as total_study_days,
                ROUND(SUM(hours_spent), 1) as total_hours,
                ROUND(AVG(hours_spent), 1) as avg_hours_per_day
            FROM time_tracking
        ''')
        overall = dict(cursor.fetchone())
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'overall': overall,
            'weekly': weekly_stats
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_data():
    """Reset all data (use with caution)"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM tasks')
        cursor.execute('DELETE FROM time_tracking')
        cursor.execute('DELETE FROM study_streak')
        cursor.execute('DELETE FROM concepts')
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'All data reset'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_file('ML_GenAI_Roadmap.html')

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ML/GenAI Progress Tracker Backend")
    print("=" * 60)
    print(f"📁 Database: {DB_PATH}")
    print(f"🌐 Server: http://localhost:5000")
    print("=" * 60)
    print("API Endpoints:")
    print("  GET  /api/health              - Health check")
    print("  POST /api/tasks/save          - Save tasks")
    print("  GET  /api/tasks/load          - Load tasks")
    print("  POST /api/time/save           - Save time")
    print("  GET  /api/time/today          - Get today's time")
    print("  GET  /api/streak/get          - Get streak")
    print("  POST /api/streak/increment    - Increment streak")
    print("  GET  /api/progress/summary    - Get summary")
    print("  GET  /api/stats/all           - Get all stats")
    print("  POST /api/reset               - Reset all data")
    print("=" * 60)
    app.run(debug=True, host='localhost', port=5000)
