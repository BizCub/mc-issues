import os
import re
import shutil

def generate_template_from_master(template_path, projects, output_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    options_lines = [f'        - "{p}"' for p in projects]

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^[ \t]*options:', line):
            new_lines.append(line)
            i += 1
            while i < len(lines) and re.match(r'^[ \t]*- ', lines[i]):
                i += 1
            for opt in options_lines:
                new_lines.append(opt + '\n')
            continue
        else:
            new_lines.append(line)
            i += 1

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Generated: {output_path}")

with open('.github/scripts/projects.txt', 'r', encoding='utf-8') as f:
    projects = [line.strip() for line in f if line.strip()]

templates = {
    '.github/scripts/bug-report.template.yml': '.github/ISSUE_TEMPLATE/bug-report.yml',
    '.github/scripts/new-feature.template.yml': '.github/ISSUE_TEMPLATE/new-feature.yml',
}

for template_path, output_path in templates.items():
    generate_template_from_master(template_path, projects, output_path)

print("All templates regenerated successfully.")