import os

# Folder where your comic images live
COMIC_DIR = "comics"
OUTPUT_DIR = "site"

# Template for each comic page
PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Comic {num}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="nav">
        <a href="comic{prev}.html">Previous</a> |
        <a href="index.html">Latest</a> |
        <a href="comic{next}.html">Next</a>
    </div>
    <h1>Comic {num}</h1>
    <img src="../comics/{filename}" alt="Comic {num}">
    <p>{caption}</p>
</body>
</html>
"""

def generate_site():
    files = sorted(os.listdir(COMIC_DIR))
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, filename in enumerate(files, start=1):
        prev_num = i - 1 if i > 1 else 1
        next_num = i + 1 if i < len(files) else i
        caption = f"This is comic {i}!"
        
        page_html = PAGE_TEMPLATE.format(
            num=i,
            prev=prev_num,
            next=next_num,
            filename=filename,
            caption=caption
        )
        
        with open(os.path.join(OUTPUT_DIR, f"comic{i}.html"), "w") as f:
            f.write(page_html)

    # Generate index.html (latest comic)
    latest = len(files)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(PAGE_TEMPLATE.format(
            num=latest,
            prev=latest-1 if latest > 1 else 1,
            next=latest,
            filename=files[-1],
            caption=f"This is comic {latest}!"
        ))

if __name__ == "__main__":
    generate_site()