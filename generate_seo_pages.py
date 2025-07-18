import os
import glob
import random
from pathlib import Path

# 读取关键词列表
def load_keywords(category):
    keywords_dir = Path(__file__).resolve().parent / "keywords"
    file_path = keywords_dir / f"{category}.txt"
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# 随机组合关键词生成SEO字段
def generate_seo_text(keywords, count=6):
    return ", ".join(random.sample(keywords, min(count, len(keywords))))

# 为每张图生成HTML页面
def make_html_for_image(img_path, category, keywords):
    filename = os.path.basename(img_path)
    name = os.path.splitext(filename)[0]
    title = f"{category.capitalize()} Photo - {name}"
    description = f"Explore {category} photography: {generate_seo_text(keywords, 3)}."
    keyword_str = generate_seo_text(keywords, 8)
    caption = f"A {category} themed photo titled {name}. Browse more: {keyword_str.split(',')[0]}."

    html = f"""<html><head>
<meta charset='utf-8'>
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keyword_str}">
</head><body>
<h2>{title}</h2>
<img src='{filename}' alt='{description}' style='width:80%;'><br>
<p>{caption}</p>
<a href='index.html'>&larr; Back</a>
</body></html>"""
    return html

# ✅ 为每个分类文件夹生成 index.html 展示页面
def generate_index_page(folder):
    html_files = sorted(folder.glob("*_seo.html"))
    if not html_files:
        return

    blocks = ""
    for file in html_files:
        img_name = file.name.replace("_seo.html", ".jpg")
        blocks += f"<div style='display:inline-block;margin:8px;text-align:center;'>"
        blocks += f"<a href='{file.name}'><img src='{img_name}' width='200'><br>{img_name}</a></div>\n"

    html = f"""<html><head>
<meta charset='utf-8'>
<title>{folder.name.capitalize()} Gallery</title>
</head><body>
<h1>{folder.name.capitalize()} Gallery</h1>
{blocks}
</body></html>"""

    with open(folder / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

# 主入口：生成所有分类的图页 + 索引页
def generate_image_pages():
    base = Path(__file__).resolve().parent
    exclude = {"images", "generator", "pages", "assets", "__pycache__", "keywords"}

    for folder in sorted(base.iterdir()):
        if not folder.is_dir() or folder.name in exclude:
            continue
        category = folder.name
        keywords = load_keywords(category)
        if not keywords:
            print(f"⚠️ 无关键词跳过：{category}")
            continue

        for img in glob.glob(str(folder / "*.jpg")):
            html_name = os.path.splitext(os.path.basename(img))[0] + "_seo.html"
            html_path = folder / html_name
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(make_html_for_image(img, category, keywords))

        generate_index_page(folder)  # ✅ 生成该分类的 index 页面

    print("✅ 所有 SEO 图页与分类索引页生成完毕！")

if __name__ == "__main__":
    generate_image_pages()
