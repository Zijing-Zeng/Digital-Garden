import os
import shutil
import re
from pathlib import Path

# ================= 配置区域 =================
OBSIDIAN_VAULT_PATH = r"/Users/zzj/Desktop/ob" # 修改为你的 Vault 路径
HUGO_CONTENT_PATH = "./content/posts"
HUGO_STATIC_IMG_PATH = "./static/images"
# 只处理带有这个标签的笔记，防止把草稿发出去
PUBLISH_TAG = "#publish"
# ===========================================

# 配置路径
HUGO_STATIC_IMG_PATH = Path("./static/images")

# 确保目标图片目录存在
if not HUGO_STATIC_IMG_PATH.exists():
    HUGO_STATIC_IMG_PATH.mkdir(parents=True, exist_ok=True)

def process_images(content, md_file_path):
    """
    1. 扫描 content 中的图片链接。
    2. 在 static/images/ 下建立以【文章名为名】的子文件夹。
    3. 将图片复制进去，并修改 Markdown 链接指向该子文件夹。
    """

    # 正则：匹配 ![[image.png]] 和 ![desc](image.png)
    pattern = r'!\[(.*?)\]\((.*?)\)|!\[\[(.*?)\]\]'

    # 1. 获取文章的文件名作为子目录名 (例如: matlab)
    # 如果你文件名有中文，这里也会生成中文文件夹，Web服务器通常能支持，
    # 但如果你想更保险，可以用 slugify 处理，目前保持简单即可。
    article_subfolder_name = md_file_path.stem

    # 2. 设定该文章专属的图片目标目录 (static/images/matlab/)
    target_dir = HUGO_STATIC_IMG_PATH / article_subfolder_name

    # 如果该目录不存在，创建它
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)

    def image_replacer(match):
        # 获取图片路径
        raw_path = match.group(2) or match.group(3)
        if not raw_path:
            return match.group(0)

        img_filename = Path(raw_path).name
        clean_filename = img_filename.replace(" ", "_")

        # === 动作 A: 寻找源图片 ===
        md_stem = md_file_path.stem
        assets_folder_name = f"{md_stem}.assets"

        search_paths = [
            md_file_path.parent / assets_folder_name / img_filename,
            md_file_path.parent / img_filename,
            md_file_path.parent / "assets" / img_filename
        ]

        src_image = None
        for path in search_paths:
            if path.exists():
                src_image = path
                break

        # URL解码重试
        if not src_image:
            import urllib.parse
            decoded_name = urllib.parse.unquote(img_filename)
            decoded_paths = [
                md_file_path.parent / assets_folder_name / decoded_name,
                md_file_path.parent / decoded_name
            ]
            for path in decoded_paths:
                if path.exists():
                    src_image = path
                    break

        # === 动作 B: 复制图片 (复制到 target_dir 子目录中) ===
        if src_image and src_image.exists():
            target_image = target_dir / clean_filename # 注意这里变了
            try:
                if not target_image.exists() or \
                   (src_image.stat().st_mtime > target_image.stat().st_mtime):
                    shutil.copy2(src_image, target_image)
                    print(f"  [图片] 已搬运: {article_subfolder_name}/{clean_filename}")
            except Exception as e:
                print(f"  [图片] 复制失败: {e}")
        else:
            print(f"  [警告] 找不到图片: {img_filename}")

        # === 动作 C: 返回新的 Markdown 链接 (指向子目录) ===
        desc = match.group(1) or ""
        # 链接变成了 /images/文章名/文件名.png
        return f"![{desc}](/images/{article_subfolder_name}/{clean_filename})"

    # 执行正则替换
    new_content = re.sub(pattern, image_replacer, content)
    return new_content

def clean_hugo_dirs():
    """清理旧内容，保持环境纯净"""
    if os.path.exists(HUGO_CONTENT_PATH):
        shutil.rmtree(HUGO_CONTENT_PATH)
    os.makedirs(HUGO_CONTENT_PATH, exist_ok=True)
    os.makedirs(HUGO_STATIC_IMG_PATH, exist_ok=True)

def process_markdown(content, file_path):
    """
    处理 Markdown 内容：
    1. 转换 Obsidian 图片语法 ![[xxx.png]] -> ![xxx](/images/xxx.png)
    2. 处理 Latex 格式（如果需要）
    """

    # 正则：匹配 ![[image.png]] 或 ![[image.png|caption]]
    # 替换为标准 Markdown: ![caption](/images/image.png)
    def img_replacer(match):
        full_str = match.group(1) # image.png|caption
        if '|' in full_str:
            filename, caption = full_str.split('|', 1)
        else:
            filename, caption = full_str, ""

        # 复制图片到 static 目录
        src_img = Path(OBSIDIAN_VAULT_PATH) / "assets" / filename # 假设你的图片在 assets 文件夹
        dst_img = Path(HUGO_STATIC_IMG_PATH) / filename

        if src_img.exists():
            shutil.copy2(src_img, dst_img)
            print(f"  [IMG] Copied {filename}")
        else:
            # 尝试在当前目录查找（如果图片和笔记在一起）
            src_img_local = Path(file_path).parent / filename
            if src_img_local.exists():
                shutil.copy2(src_img_local, dst_img)
                print(f"  [IMG] Copied {filename} from local")
            else:
                print(f"  [WARN] Image not found: {filename}")

        return f"![{caption}](/images/{filename})"

    # 执行替换
    new_content = re.sub(r'!\[\[(.*?)\]\]', img_replacer, content)
    return new_content

def main():
    clean_hugo_dirs()
    print("🚀 开始同步 Obsidian 笔记...")

    vault = Path(OBSIDIAN_VAULT_PATH)

    for md_file in vault.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否有发布标签 (或者你可以检查 frontmatter 中的 published: true)
            if PUBLISH_TAG not in content:
                continue

            print(f"处理: {md_file.name}")

            # 处理内容
            processed_content = process_markdown(content, md_file)
            processed_content = process_images(processed_content, md_file)

            # 写入 Hugo 目录
            # 保持文件名不变，或者根据 title 变，这里简单起见保持文件名
            dest_path = Path(HUGO_CONTENT_PATH) / md_file.name
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)

        except Exception as e:
            print(f"出错 {md_file}: {e}")

    print("✅ 同步完成！请运行 'hugo server' 预览")

if __name__ == "__main__":
    main()
