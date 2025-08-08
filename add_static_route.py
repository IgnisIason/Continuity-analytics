#!/usr/bin/env python3
"""
Script to modify server.py to add a static file serving route.
This adds a /static/<path:path> route that serves files from the static directory.
"""

import os
import re

def modify_server_file():
    """Modify the server.py file to add static file serving."""
    
    server_file = 'continuity-server/server.py'
    
    # Check if the file exists
    if not os.path.exists(server_file):
        print(f"Error: {server_file} not found!")
        return False
    
    # Read the current content
    with open(server_file, 'r') as f:
        content = f.read()
    
    # Check if the route already exists
    if '/static/<path:path>' in content or 'send_from_directory' in content:
        print("Static route already exists in server.py")
        return True
    
    # Find the import section and add send_from_directory import
    import_pattern = r'(from flask import .*)'
    import_match = re.search(import_pattern, content)
    
    if import_match:
        current_imports = import_match.group(1)
        # Check if send_from_directory is already imported
        if 'send_from_directory' not in current_imports:
            # Add send_from_directory to the imports
            new_imports = current_imports.replace('jsonify', 'jsonify, send_from_directory')
            content = content.replace(current_imports, new_imports)
            print("✓ Added send_from_directory to imports")
    else:
        print("Error: Could not find Flask imports!")
        return False
    
    # Find where to insert the new route (after the heartbeat route but before if __name__)
    # We'll insert it right before the if __name__ == '__main__': line
    main_pattern = r"(if __name__ == '__main__':)"
    main_match = re.search(main_pattern, content)
    
    if main_match:
        # Create the new route
        new_route = '''@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files from the static directory."""
    return send_from_directory('static', path)

'''
        
        # Insert the new route before the main block
        insert_position = main_match.start()
        modified_content = content[:insert_position] + new_route + content[insert_position:]
        
        # Write the modified content back to the file
        with open(server_file, 'w') as f:
            f.write(modified_content)
        
        print(f"✓ Successfully modified {server_file}")
        print("✓ Added route: /static/<path:path>")
        print("✓ This route will serve files from the 'static' directory")
        
        # Create the static directory if it doesn't exist
        static_dir = 'continuity-server/static'
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
            print(f"✓ Created {static_dir} directory")
        else:
            print(f"✓ Static directory already exists: {static_dir}")
        
        return True
    else:
        print("Error: Could not find the main block in server.py!")
        return False

if __name__ == '__main__':
    print("Modifying server.py to add static file serving...")
    print("-" * 50)
    
    if modify_server_file():
        print("-" * 50)
        print("Modification completed successfully!")
        print("\nThe server can now serve static files from:")
        print("  URL: /static/<filename>")
        print("  Directory: continuity-server/static/")
        print("\nExample: /static/style.css will serve continuity-server/static/style.css")
    else:
        print("-" * 50)
        print("Modification failed. Please check the errors above.")