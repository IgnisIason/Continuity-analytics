#!/usr/bin/env python3
import os

def modify_server_file():
    server_file_path = 'continuity-server/server.py'
    
    # Check if the file exists
    if not os.path.exists(server_file_path):
        print(f"Error: {server_file_path} does not exist!")
        print("Please run setup_server.py first to create the initial structure.")
        return
    
    # Modified server.py content with heartbeat counter
    modified_content = '''from flask import Flask, request, jsonify

app = Flask(__name__)

heartbeat_count = 0

@app.route('/v1/heartbeat', methods=['POST'])
def heartbeat():
    global heartbeat_count
    heartbeat_count += 1
    return jsonify({'status': 'received', 'total_signals': heartbeat_count})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    # Write the modified content to server.py
    with open(server_file_path, 'w') as f:
        f.write(modified_content)
    
    print(f"Successfully modified {server_file_path}")
    print("Added heartbeat_count global variable and updated response to include total_signals")

if __name__ == '__main__':
    modify_server_file()