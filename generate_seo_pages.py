import os
import glob
import random
from pathlib import Path

def load_keywords(category):
    keywords_dir = Path(__file__).resolve().parent / "keywords"
    file_path = keywords_dir / f"{category}.txt"
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def generate_seo_text(keywords, count=6):
    return ", ".join(random.sample(keywords, min(count, len(keywords))))

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
            # 用真实文件名 + _seo.html 生成 HTML 文件
            html_name = os.path.splitext(os.path.basename(img))[0] + "_seo.html"
            html_path = folder / html_name
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(make_html_for_image(img, category, keywords))
    print("✅ 带SEO的图片页面生成完成")

if __name__ == "__main__":
    generate_image_pages()
