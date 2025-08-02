#!/usr/bin/env python3
"""
Script to fix web_app.py to use get_project_manager() in all routes
"""
import re

def fix_web_app():
    with open('web_app.py', 'r') as f:
        content = f.read()
    
    # Find all routes that use pm. but don't have pm = get_project_manager()
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Check if this is a function definition that will need pm
        if line.strip().startswith('def ') and '@app.route' in new_lines[-2] if len(new_lines) >= 2 else False:
            # Look ahead to see if this function uses pm. and doesn't already have get_project_manager()
            func_lines = []
            j = i + 1
            while j < len(lines) and not (lines[j].startswith('def ') or lines[j].startswith('@app.')):
                func_lines.append(lines[j])
                j += 1
            
            func_content = '\n'.join(func_lines)
            if 'pm.' in func_content and 'get_project_manager()' not in func_content:
                # Find the first 'try:' line and add pm = get_project_manager() after it
                for k, func_line in enumerate(func_lines):
                    if 'try:' in func_line:
                        # Add the line after try:
                        new_lines.append(func_lines[k])
                        new_lines.append('        pm = get_project_manager()  # Get fresh data')
                        # Add the rest of the function
                        for remaining_line in func_lines[k+1:]:
                            new_lines.append(remaining_line)
                        i = j - 1
                        break
                else:
                    # No try: found, add normally
                    for func_line in func_lines:
                        new_lines.append(func_line)
                    i = j - 1
            else:
                # Add function normally
                for func_line in func_lines:
                    new_lines.append(func_line)
                i = j - 1
        
        i += 1
    
    # Write the fixed content
    with open('web_app_fixed.py', 'w') as f:
        f.write('\n'.join(new_lines))
    
    print("Fixed web_app.py saved as web_app_fixed.py")
    print("You can review and then replace the original file")

if __name__ == '__main__':
    fix_web_app()