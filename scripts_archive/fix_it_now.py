"""Fix by removing from line 4088"""

with open('main_ultimate_final.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where show_portfolio_management starts
for i, line in enumerate(lines[4088:], 4088):
    if 'def show_portfolio_management():' in line:
        print(f"Found show_portfolio_management at line {i}")
        # Keep everything before 4088 and from this line onwards
        new_lines = lines[:4088] + lines[i:]
        
        with open('main_ultimate_final.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"✅ Removed lines 4088 to {i-1}")
        break
