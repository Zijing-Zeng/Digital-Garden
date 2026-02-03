# 1 Hugo + Hextra 个人网站搭建

这份笔记涵盖了从零开始搭建 Hugo + Hextra 个人网站的核心流程。

## 1.1 环境准备

- **Git**: 版本控制。
- **Go**: 用于管理 Hugo 主题模块。
- **Hugo (Extended 版本)**: 必须安装 Extended 版以支持高级功能。
- **Python 3**: 用于运行同步脚本。

## 1.2 初始化项目

**目标**：在 Git 仓库根目录直接建立 Hugo 站点，避免多层文件夹嵌套。

```bash
# 1. 克隆 GitHub 仓库
git clone https://github.com/yourname/your-repo.git
cd your-repo

# 2. 强制在当前目录初始化 Hugo (关键步骤)
hugo new site . --force --format yaml

# 3. 初始化 Go Module (用于安装主题)
# 路径建议格式: github.com/用户名/仓库名
hugo mod init github.com/yourusername/your-repo
```

## 1.3 安装 Hextra 主题

使用 Go Modules 方式安装，便于后续更新和管理。

```bash
# 下载主题
hugo mod get github.com/imfing/hextra
# 整理依赖
hugo mod tidy
```

## 1.4 配置文件 (`hugo.yaml`)

新建或覆盖根目录下的 `hugo.yaml`。此配置已包含 **Obsidian 兼容性** 和 **Latex 公式修复**。

```yaml
baseURL: "https://yourusername.github.io/" # 部署时修改
languageCode: "zh-cn"
title: "My Digital Garden"

# 核心渲染配置
markup:
  goldmark:
    renderer:
      unsafe: true # 必须开启，支持 Mermaid 和 HTML
    extensions:
      passthrough: # 关键：修复 Latex 公式不渲染的问题
        enable: true
        delimiters:
          block:
            - - $$
              - $$
            - - \\[
              - \\]
          inline:
            - - $
              - $
            - - \\(
              - \\)
  highlight:
    noClasses: false

# 引入主题
module:
  imports:
    - path: github.com/imfing/hextra

# 主题参数
params:
  math:
    enable: true # 全局开启数学公式
  search:
    enable: true
    type: flexsearch
  navbar:
    displayTitle: true
    displayLogo: true
  blog:
    list:
      displayTags: true

# 菜单配置
menu:
  main:
    - identifier: notes
      name: "笔记"
      url: "/posts/"
      weight: 1
```

## 1.5 自动化同步脚本 (`sync_obsidian.py`)

在根目录创建 `sync_obsidian.py`。

**功能**：读取 Obsidian 笔记 -> 处理图片路径 -> 转换链接 -> 写入 Hugo 目录。

```python
import os
import shutil
import re
from pathlib import Path

# ================= 配置区域 =================
# 修改为你的 Obsidian 仓库绝对路径
OBSIDIAN_VAULT_PATH = r"/Users/username/Documents/MyVault" 
HUGO_CONTENT_PATH = "./content/posts"
HUGO_STATIC_IMG_PATH = "./static/images"
PUBLISH_TAG = "#publish" # 只发布包含此标签的笔记
# ===========================================

def clean_hugo_dirs():
    if os.path.exists(HUGO_CONTENT_PATH):
        shutil.rmtree(HUGO_CONTENT_PATH)
    os.makedirs(HUGO_CONTENT_PATH, exist_ok=True)
    os.makedirs(HUGO_STATIC_IMG_PATH, exist_ok=True)

def process_markdown(content, file_path):
    # 替换 Obsidian 图片语法 ![](/images/xxx.png) 为 Markdown 标准 ![xxx](/images/xxx.png)
    def img_replacer(match):
        full_str = match.group(1)
        if '|' in full_str: filename, caption = full_str.split('|', 1)
        else: filename, caption = full_str, ""
        
        # 复制图片到 static/images
        # 依次查找：assets文件夹 -> 笔记同级目录
        possible_paths = [
            Path(OBSIDIAN_VAULT_PATH) / "assets" / filename,
            Path(file_path).parent / filename
        ]
        
        for src_img in possible_paths:
            if src_img.exists():
                shutil.copy2(src_img, Path(HUGO_STATIC_IMG_PATH) / filename)
                break
                
        return f"![{caption}](/images/{filename})"

    return re.sub(r'!\[\[(.*?)\]\]', img_replacer, content)

def main():
    clean_hugo_dirs()
    print("🚀 Syncing Obsidian notes...")
    vault = Path(OBSIDIAN_VAULT_PATH)
    
    for md_file in vault.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if PUBLISH_TAG in content:
                print(f"Processing: {md_file.name}")
                new_content = process_markdown(content, md_file)
                
                with open(Path(HUGO_CONTENT_PATH) / md_file.name, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Error {md_file}: {e}")

if __name__ == "__main__":
    main()
```

## 1.6 运行与预览

1. **准备目录**：确保存在 `content/posts` 目录。

```bash
mkdir -p content/posts
```

2. **同步笔记**：

```bash
python3 sync_obsidian.py
```

3. **启动服务**：

```bash
hugo server
```

4. **访问**：打开浏览器访问 `http://localhost:1313`。

---

## 1.7 常用命令速查

- **本地预览**：`hugo server`
- **构建静态文件**：`hugo --minify` (生成到 `public/` 目录)
- **更新主题**：`hugo mod get -u`
- **清理缓存**：`hugo mod clean`
