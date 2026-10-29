# 书卷 · eBook

将 TXT 小说整理为带章节目录和封面的 EPUB 的 Windows 桌面工具。新界面参考 Grain 写作工作台，采用 React 与 pywebview。

## 功能

- 导入 UTF-8 或 GB18030 文本，自动识别常见中文章节标题；修改正文时自动更新目录。
- 自定义书名、上传封面；内置 5 幅不同的 AI 生成二次元插画，组合色调和边框提供 100 种封面样式。
- 选择书页背景并导出带目录的 EPUB。部分阅读器可能覆盖书页样式。

## 使用

已打包的 Windows 版本可从 [Releases](https://github.com/yifanchen12/ebook/releases) 下载。源码运行需要 Python、Node.js 和 Windows WebView2 运行时。在仓库根目录运行：

```powershell
python -m pip install -r ebook/requirements.txt
cd ebook/frontend
npm ci
npm run build
cd ../..
python -m ebook.desktop
```

也可以安装依赖并构建前端后双击 `ebook/启动eBook.bat`。打开 TXT，检查和调整章节，设置书名与封面，点击“导出 EPUB”。识别不到章节时全文作为一章；上传图片会居中裁剪为竖版。原 Tk 版本可通过 `python -m ebook.app` 启动。

## 验证与限制

```powershell
python -m unittest discover -s tests -v
```

本机 Windows 测试了程序窗口启动、桥接层和 EPUB 文件结构；尚未在其他电脑和各种阅读器上完成兼容性测试。生成的 5 幅二次元封面素材位于 `ebook/assets/`，源自 AI 图片生成。按钮组件改编自 shadcn/ui，许可证说明见 `ebook/frontend/THIRD_PARTY_NOTICES.md`。请仅处理有权使用的内容。

