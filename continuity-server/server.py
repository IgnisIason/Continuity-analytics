from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

def init_database():
    """Initialize the database and create signals table if it doesn't exist."""
    db_path = 'continuity.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create signals table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    # Initialize with a single row if table is empty
    cursor.execute("SELECT COUNT(*) FROM signals")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO signals (id, count) VALUES (1, 0)")
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

@app.route('/')
def index():
    conn = sqlite3.connect('continuity.db')
    cursor = conn.cursor()
    
    # Read current count from signals table
    cursor.execute("SELECT count FROM signals WHERE id = 1")
    result = cursor.fetchone()
    heartbeat_count = result[0] if result else 0
    
    conn.close()
    
    # Return simple HTML string with the count
    return f'Total continuity signals received: {heartbeat_count}'

@app.route('/v1/heartbeat', methods=['POST'])
def heartbeat():
    conn = sqlite3.connect('continuity.db')
    cursor = conn.cursor()
    
    # Read current count
    cursor.execute("SELECT count FROM signals WHERE id = 1")
    current_count = cursor.fetchone()[0]
    
    # Increment count
    new_count = current_count + 1
    cursor.execute("UPDATE signals SET count = ? WHERE id = 1", (new_count,))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'received', 'total_signals': new_count})

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files from the static directory."""
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
