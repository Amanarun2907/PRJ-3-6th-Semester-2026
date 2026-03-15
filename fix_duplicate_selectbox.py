"""
Fix duplicate selectbox error by removing old code
"""

with open('main_ultimate_final.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the duplicate section
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if i > 4000 and '# Category Selection' in line and start_idx is None:
        start_idx = i
        print(f"Found start at line {i}")
    
    if start_idx and i > start_idx and 'def show_portfolio_management():' in line:
        end_idx = i
        print(f"Found end at line {i}")
        break

if start_idx and end_idx:
    print(f"Removing lines {start_idx} to {end_idx-1}")
    new_lines = lines[:start_idx] + lines[end_idx:]
    
    with open('main_ultimate_final.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ Fixed! Duplicate code removed.")
else:
    print("❌ Could not find the duplicate section")
