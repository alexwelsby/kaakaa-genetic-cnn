import re
from pathlib import Path


# Current directory
current_dir = Path(__file__).parent
index_html_path = current_dir.parent / "static" / "react" / "index.html"
output_template = current_dir.parent / "templates" / "index.html"
output_template.parent.mkdir(parents=True, exist_ok=True)

# Load HTML
with open(index_html_path, encoding="utf-8") as f:
    html = f.read()

# Replace /assets/... and assets/... links with {% static 'assets/...' %}
def replace_with_static(match):
    attr, quote, path = match.groups()
    path = path.lstrip("/")  # Remove leading slash if present
    return f'{attr}={quote}{{% static \'{path}\' %}}{quote}'

html = re.sub(r'(src|href)=(["\'])(/?assets/[^"\']+)\2', replace_with_static, html)

# Inject {% load static %} at the top if missing
if "{% load static %}" not in html:
    html = "{% load static %}\n" + html

# Save result
with open(output_template, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Converted index.html saved to {output_template}")