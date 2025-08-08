#!/usr/bin/env python3
import os

def upgrade_server_with_sqlite():
    server_file_path = 'continuity-server/server.py'
    
    # Check if the file exists
    if not os.path.exists(server_file_path):
        print(f"Error: {server_file_path} does not exist!")
        print("Please run setup_server.py first to create the initial structure.")
        return
    
    # Server.py content with SQLite persistence
    upgraded_content = '''from flask import Flask, request, jsonify
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

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    # Write the upgraded content to server.py
    with open(server_file_path, 'w') as f:
        f.write(upgraded_content)
    
    print(f"Successfully upgraded {server_file_path}")
    print("Added SQLite persistence with the following features:")
    print("  - sqlite3 library imported")
    print("  - init_database() function creates continuity.db and signals table")
    print("  - heartbeat() function uses database for persistent count storage")

if __name__ == '__main__':
    upgrade_server_with_sqlite()