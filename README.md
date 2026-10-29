# 书卷 · eBook

将 TXT 小说整理为带章节目录和封面的 EPUB 的 Windows 桌面工具。

## 功能

- 导入 UTF-8 或 GB18030 文本，识别常见中文章节标题；修改原文或标题后可重新识别。
- 自定义书名、上传封面；内置 5 幅不同的 AI 生成二次元插画，组合色调和边框提供 100 种封面样式。
- 选择书页背景并导出带目录的 EPUB。部分阅读器可能覆盖书页样式。

## 使用

需要 Windows、Python（含 Tkinter）及 Pillow。在仓库根目录运行：

```powershell
python -m pip install -r ebook/requirements.txt
python -m ebook.app
```

也可以安装依赖后双击 `ebook/启动eBook.bat`。打开 TXT，检查和调整章节，设置书名与封面，点击“导出 EPUB”。识别不到章节时全文作为一章；上传图片会居中裁剪为竖版。

## 验证与限制

```powershell
python -m unittest discover -s tests -v
```

本机 Windows 测试了程序窗口启动和 EPUB 文件结构；尚未在其他电脑和各种阅读器上完成兼容性测试。生成的 5 幅二次元封面素材位于 `ebook/assets/`，源自 AI 图片生成。请仅处理有权使用的内容。

