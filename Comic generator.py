import os

INDEX_FILE = "comic_index.txt"
REGENERATE_ALL = True   # Set to True when you want to rebuild everything

PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
    <style>
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .nav button {{
            background: #444;
            color: white;
            padding: 10px 18px;
            border: none;
            border-radius: 6px;
            margin: 5px;
            cursor: pointer;
            font-size: 1rem;
        }}
        .nav button:hover {{
            background: #666;
        }}
    </style>
</head>
<body>
    <div class="nav">
        <button onclick="window.location.href='comic{prev}.html'">Previous</button>
        <button onclick="window.location.href='index.html'">Latest</button>
        <button onclick="window.location.href='comic{next}.html'">Next</button>
        <button onclick="window.location.href='comic' + Math.floor(Math.random() * {total} + 1) + '.html'">Random</button>
    </div>

    <h1>{title}</h1>

    <img src="{filename}" alt="{title}">
    <p>{caption}</p>
</body>
</html>
"""

def load_index():
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def save_index(index):
    with open(INDEX_FILE, "w") as f:
        f.write("\n".join(index))

def generate_site():
    index = load_index()

    # Find all image files
    files = sorted([
        f for f in os.listdir(".")
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ])

    # Detect new files
    new_files = [f for f in files if f not in index]

    # Add new files to index
    if new_files:
        index.extend(new_files)
        save_index(index)

    # Determine which pages to generate
    if REGENERATE_ALL:
        to_generate = index
    else:
        to_generate = new_files

    # Generate pages
    for filename in to_generate:
        num = index.index(filename) + 1
        title = os.path.splitext(filename)[0]

        prev_num = num - 1 if num > 1 else 1
        next_num = num + 1 if num < len(index) else num

        caption = ""#f"This is comic {num}!"

        html = PAGE_TEMPLATE.format(
            title=title,
            prev=prev_num,
            next=next_num,
            total=len(index),
            filename=filename,
            caption=caption
        )

        with open(f"comic{num}.html", "w") as f:
            f.write(html)

    # Always regenerate index.html
    latest = len(index)
    latest_file = index[-1]
    latest_title = os.path.splitext(latest_file)[0]

    with open("index.html", "w") as f:
        f.write(PAGE_TEMPLATE.format(
            title=latest_title,
            prev=latest-1 if latest > 1 else 1,
            next=latest,
            total=len(index),
            filename=latest_file,
            caption=""#f"This is comic {latest}!"
        ))

if __name__ == "__main__":
    generate_site()