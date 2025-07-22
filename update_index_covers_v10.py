import os
from bs4 import BeautifulSoup

# 分类文件夹名称
folders = ["dark", "soft", "office", "uniform", "shower", "boudoir"]
index_file = "index.html"

def find_latest_image(folder):
    exts = [".jpg", ".png", ".jpeg", ".webp"]
    files = [f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in exts]
    if not files:
        return None
    files.sort(reverse=True)
    return f"{folder}/{files[0]}"

# 读取并解析index.html
with open(index_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 替换每个分类的封面图
for folder in folders:
    latest_img = find_latest_image(folder)
    if not latest_img:
        continue
    # 查找img标签（src中包含该分类名）
    img_tag = soup.find("img", {"src": lambda x: x and folder in x})
    if img_tag:
        img_tag["src"] = latest_img

# 保存修改后的index.html
with open(index_file, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("✅ 封面图更新完毕，主页结构保持不变。")
