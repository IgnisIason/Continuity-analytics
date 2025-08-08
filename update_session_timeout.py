#!/usr/bin/env python3
"""
Script to update sessionTimeout property in continuity.js file.
"""

import os
import re

def update_session_timeout():
    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), 'continuity.js')
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False
    
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Find and replace the sessionTimeout line
    modified = False
    for i, line in enumerate(lines):
        if 'sessionTimeout' in line:
            # Replace the entire line with the new value
            lines[i] = '  sessionTimeout: 15 * 60 * 1000, // 15 minutes\n'
            modified = True
            print(f"Updated line {i+1}: sessionTimeout property set to 15 minutes")
            break
    
    if not modified:
        print("Warning: sessionTimeout property not found in the file.")
        return False
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
    
    print(f"Successfully updated '{file_path}'")
    return True

if __name__ == "__main__":
    success = update_session_timeout()
    exit(0 if success else 1)