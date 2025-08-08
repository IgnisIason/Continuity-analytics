#!/usr/bin/env python3
import os

def add_root_route_to_server():
    server_file_path = 'continuity-server/server.py'
    
    # Check if the file exists
    if not os.path.exists(server_file_path):
        print(f"Error: {server_file_path} does not exist!")
        print("Please run upgrade_server.py first to create the server with database support.")
        return
    
    # Read the current content
    with open(server_file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the position to insert the new route (after init_database function)
    insert_position = None
    for i, line in enumerate(lines):
        if line.strip().startswith("@app.route('/v1/heartbeat'"):
            insert_position = i
            break
    
    if insert_position is None:
        print("Error: Could not find the heartbeat route to insert before")
        return
    
    # Create the new route code
    root_route_code = """@app.route('/')
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

"""
    
    # Insert the new route before the heartbeat route
    lines.insert(insert_position, root_route_code)
    
    # Write the modified content back
    with open(server_file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"Successfully modified {server_file_path}")
    print("Added root route (/) that:")
    print("  - Connects to continuity.db database")
    print("  - Reads heartbeat_count from signals table")
    print("  - Returns HTML showing 'Total continuity signals received: [count]'")

if __name__ == '__main__':
    add_root_route_to_server()