import json
import os
from pathlib import Path

# Config
DATA_FILE = "errors.json"
OUTPUT_DIR = "public"
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fix {manufacturer} {model} Error {code} | The Error DB</title>
    <meta name="description" content="How to fix {manufacturer} {model} error code {code}: {title}. Step-by-step troubleshooting guide.">
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #d32f2f; }}
        .warning {{ background: #fff3e0; padding: 15px; border-left: 5px solid #ff9800; }}
        .fix-steps {{ background: #e8f5e9; padding: 20px; border-radius: 5px; }}
        a.button {{ display: inline-block; background: #1976d2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
    </style>
</head>
<body>
    <nav><a href="index.html">← Back to Error Database</a></nav>
    
    <h1>{manufacturer} {model} Error: {code}</h1>
    <h2>{title}</h2>
    
    <div class="warning">
        <strong>Potential Cause:</strong><br>
        {cause}
    </div>

    <h3>How to Fix It:</h3>
    <div class="fix-steps">
        <pre>{fix}</pre>
    </div>

    <a href="{parts_link}" class="button" target="_blank">Find Replacement Parts</a>
    
    <footer>
        <p><small>Disclaimer: We are not affiliated with {manufacturer}. Always unplug equipment before servicing.</small></p>
    </footer>
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Commercial Kitchen Error Codes | The Error DB</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        a {{ text-decoration: none; color: #1976d2; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>🔧 The Commercial Kitchen Error Database</h1>
    <p>Search our database of error codes for Hobart, Vulcan, and more.</p>
    <ul>
        {links}
    </ul>
</body>
</html>
"""

def slugify(text):
    return text.lower().replace(" ", "-").replace("/", "-")

def build():
    # Load Data
    with open(DATA_FILE) as f:
        errors = json.load(f)
    
    # Create Output Dir
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    links = []
    
    # Generate Pages
    for e in errors:
        filename = f"{slugify(e['manufacturer'])}-{slugify(e['code'])}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Fill Template
        content = TEMPLATE.format(
            manufacturer=e['manufacturer'],
            model=e['model'],
            code=e['code'],
            title=e['title'],
            cause=e['cause'],
            fix=e['fix'],
            parts_link=e.get('parts_link', '#')
        )
        
        with open(filepath, "w") as f:
            f.write(content)
            
        print(f"✅ Generated {filename}")
        links.append(f"<li><a href='{filename}'><strong>{e['code']}</strong> - {e['manufacturer']} {e['model']} ({e['title']})</a></li>")
    
    # Generate Index
    index_content = INDEX_TEMPLATE.format(links="\n".join(links))
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(index_content)
    print("✅ Generated index.html")

if __name__ == "__main__":
    build()
