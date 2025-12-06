import os
from datetime import date

# Folder where your comic images live
COMIC_DIR = "comics"
OUTPUT_DIR = "content"

# Markdown template for each comic
MD_TEMPLATE = """Title: Comic {num}
Date: {date}
Category: Comics
Slug: comic{num}

![Comic {num}](images/{filename})

{caption}
"""

def generate_markdown():
    files = sorted(os.listdir(COMIC_DIR))
    os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)

    for i, filename in enumerate(files, start=1):
        caption = f"This is comic {i}!"
        today = date.today().isoformat()

        md_content = MD_TEMPLATE.format(
            num=i,
            date=today,
            filename=filename,
            caption=caption
        )

        md_filename = os.path.join(OUTPUT_DIR, f"comic{i}.md")
        with open(md_filename, "w") as f:
            f.write(md_content)

        # Copy images into Pelican's content/images folder
        src = os.path.join(COMIC_DIR, filename)
        dst = os.path.join(OUTPUT_DIR, "images", filename)
        if not os.path.exists(dst):
            with open(src, "rb") as s, open(dst, "wb") as d:
                d.write(s.read())

if __name__ == "__main__":
    generate_markdown()