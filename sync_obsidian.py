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
