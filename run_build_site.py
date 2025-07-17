
import os
import glob
from pathlib import Path

def update_category_pages(images_per_page=20):
    base_dir = Path(__file__).resolve().parent
    exclude_dirs = {"generator", "images", "assets", "pages", "__pycache__"}
    print("📄 正在生成分类分页与图页...")

    for category_folder in sorted(base_dir.iterdir()):
        if not category_folder.is_dir() or category_folder.name in exclude_dirs:
            continue

        image_files = sorted(glob.glob(str(category_folder / "*.jpg")))
        if not image_files:
            continue

        total_pages = (len(image_files) + images_per_page - 1) // images_per_page
        for page_num in range(total_pages):
            start = page_num * images_per_page
            end = start + images_per_page
            images = image_files[start:end]
            page_html = "<html><head><meta charset='utf-8'><title>{}</title></head><body>".format(category_folder.name)
            page_html += f"<h2>{category_folder.name.capitalize()} - Page {page_num + 1}</h2>"

            for img_path in images:
                filename = os.path.basename(img_path)
                img_name = os.path.splitext(filename)[0]
                detail_page = f"{img_name}.html"
                page_html += f"<a href='{detail_page}'><img src='{filename}' style='width:200px;margin:10px;'></a>"

            page_html += "<div style='margin-top:20px;'>Pages: "
            for i in range(total_pages):
                link = "index.html" if i == 0 else f"page{i+1}.html"
                label = f"[{i+1}]"
                page_html += f"<a href='{link}' style='margin:5px;'>{label}</a>"
            page_html += "</div></body></html>"

            page_file = category_folder / ("index.html" if page_num == 0 else f"page{page_num+1}.html")
            with open(page_file, "w", encoding="utf-8") as f:
                f.write(page_html)

        for img_path in image_files:
            filename = os.path.basename(img_path)
            img_name = os.path.splitext(filename)[0]
            html_path = category_folder / f"{img_name}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(f"<html><head><meta charset='utf-8'><title>{img_name}</title></head><body>")
                f.write(f"<h2>{img_name}</h2><img src='{filename}' style='width:80%;'><br>")
                f.write(f"<a href='index.html'>&larr; Back</a></body></html>")

    print("✅ 分类图页与分页已完成")

def update_homepage():
    base_dir = Path(__file__).resolve().parent
    template_file = base_dir / "custom_homepage_template.html"
    output_file = base_dir / "index.html"
    images_per_category = 4
    exclude_dirs = {"generator", "pages", "single", "assets", "__pycache__"}

    if not template_file.exists():
        print("❌ 模板文件不存在：", template_file)
        return

    sections = []
    for folder in sorted(base_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith(".") or folder.name in exclude_dirs:
            continue
        images = sorted(glob.glob(str(folder / "*.jpg")))
        if images:
            thumbs = ""
            for img_path in images[:images_per_category]:
                filename = os.path.basename(img_path)
                thumbs += f'<a href="{folder.name}/{filename}" data-lightbox="{folder.name}"><img src="{folder.name}/{filename}" alt=""></a>\n'
            section = (
                f"<!-- {folder.name.capitalize()} Section -->\n"
                f"<div class='section'>\n"
                f"  <h2>{folder.name.capitalize()}</h2>\n"
                f"  <div class='gallery'>\n"
                f"    {thumbs.strip()}\n"
                f"  </div>\n"
                f"  <div class='more'><a href='{folder.name}.html'>&rarr; View More</a></div>\n"
                f"</div>\n"
            )
            sections.append(section)

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    final_output = template.replace("{category_blocks}", "\n".join(sections))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_output)

    print("✅ 首页 index.html 已更新")

def generate_sitemap(base_url="https://your-site-url.com"):
    base_dir = Path(__file__).resolve().parent
    sitemap_file = base_dir / "sitemap.xml"
    urls = []

    for path in base_dir.rglob("*.html"):
        rel_path = path.relative_to(base_dir).as_posix()
        urls.append(f"{base_url}/{rel_path}")

    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in urls:
            f.write(f"  <url><loc>{url}</loc></url>\n")
        f.write('</urlset>\n')

    print(f"✅ sitemap.xml 生成完成，共收录 {len(urls)} 页")

if __name__ == "__main__":
    update_category_pages()
    update_homepage()
    generate_sitemap()
