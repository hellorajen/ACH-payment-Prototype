import os
for root, dirs, files in os.walk('.'):
    if 'venv' in root or '__pycache__' in root:
        continue
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 4 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f'{subindent}{f}')