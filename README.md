<p align="center"><strong>北邮 AI 学生个人实践项目</strong> · 欢迎关注项目更新与共建进展</p>

<h1 align="center">书卷 · eBook</h1>

<p align="center"><strong>让故事，成为一本书。</strong></p>
<p align="center">一款 Windows 桌面电子书制作工具：导入 TXT 小说，整理章节，挑选封面，再导出带目录的 EPUB。</p>
<p align="center"><img alt="Windows" src="https://img.shields.io/badge/platform-Windows-0078D4"> <img alt="Version 0.2.0" src="https://img.shields.io/badge/version-0.2.0-628570"> <img alt="EPUB 3" src="https://img.shields.io/badge/export-EPUB%203-bb9670"></p>

如果书卷让你更方便地整理自己的故事，欢迎点亮 ⭐ Star，也欢迎 Follow 关注后续更新。

一份 TXT 里可能有几百个章节，也可能只有一段尚未整理的文字。书卷会尝试识别常见的章节标题，把目录、正文和封面放在同一个工作台；你可以修改书名和正文，查看目录，再将它们制作成电子书。

当前是 **0.2.0 Windows 开发版**。处理与导出在本机进行；封面样式由五幅独立的二次元插画、色调与边框组合而成，也可以上传自己的封面。

## 它能帮你做什么

| 你想做的事 | 书卷目前支持 |
| --- | --- |
| 导入小说 | 打开 UTF-8 或 GB18030 编码的 TXT，也可以直接在编辑区输入或粘贴文字 |
| 整理章节 | 自动识别常见的“第一章”“第十回”、序言、后记和 `Chapter 1` 等标题；修改正文后更新目录 |
| 调整书名 | 修改书名后更新内置封面预览，并写入导出书籍的信息 |
| 选择封面 | 五幅不同的二次元插画，配合色调和边框提供 100 种组合；也可上传图片 |
| 装帧与导出 | 选择素白、暖纸、羊皮纸或护眼绿书页样式，导出带章节目录和封面的 EPUB 3 |

章节识别依赖标题格式。若目录不符合预期，可以在正文里调整标题；没有识别到章节时，全文会作为一章导出。

## 选择一张封面

| 樱花与剑 | 云上之旅 | 霓虹雨夜 | 秋日书斋 | 极光之境 |
| --- | --- | --- | --- | --- |
| ![樱花与剑封面插画](ebook/frontend/src/thumbs/anime-1.jpg) | ![云上之旅封面插画](ebook/frontend/src/thumbs/anime-2.jpg) | ![霓虹雨夜封面插画](ebook/frontend/src/thumbs/anime-3.jpg) | ![秋日书斋封面插画](ebook/frontend/src/thumbs/anime-4.jpg) | ![极光之境封面插画](ebook/frontend/src/thumbs/anime-5.jpg) |

上面展示的是五幅内置插画的缩略图。程序会在内置插画上组合书名、色调与边框；上传的图片会居中裁剪为竖版封面。

## 快速开始

### 直接使用 Windows 版本

1. 从 [v0.2.0 发布页面](https://github.com/yifanchen12/ebook/releases/tag/v0.2.0)下载 **`eBook-studio-fixed.exe`**。
2. 双击运行。程序使用 Windows WebView2 显示界面；如果系统缺少运行时，需要先安装 [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/)。
3. 选择“导入小说”，或直接在正文区输入文字。

### 从源码运行

需要 Python、Node.js、npm 和 Windows WebView2 Runtime。下面在 PowerShell 中从仓库根目录执行：

```powershell
git clone https://github.com/yifanchen12/ebook.git
cd ebook
python -m pip install -r ebook/requirements.txt
cd ebook/frontend
npm ci
npm run build
cd ../..
python -m ebook.desktop
```

安装依赖并构建前端后，也可以双击 `ebook/启动eBook.bat`。仓库保留旧的 Tk 界面，可用 `python -m ebook.app` 启动。

## 制作第一本书

1. 点击 **“导入小说”**，选择 TXT 文件；程序会读取文本并尝试识别章节。
2. 检查左侧目录，在中间编辑正文或章节标题；修改后目录会自动更新。
3. 修改书名，在右侧选择插画和样式组合，或点击 **“上传自己的封面”**。
4. 选择书页纹理，点击 **“导出 EPUB”** 并选择保存位置。
5. 用自己的阅读器打开生成文件，检查目录、封面和排版。

书页纹理使用 EPUB 内的样式实现；阅读器可能忽略或覆盖书籍样式。请在目标设备上检查最终效果。

## 开发与验证

桌面窗口通过 pywebview 将界面操作交给本地 Python 代码。TXT 解码、章节划分、封面处理和 EPUB 生成集中在 `ebook/core.py`；React 界面负责编辑和展示。

```text
ebook/core.py              TXT、章节、封面和 EPUB 生成
ebook/desktop.py           Windows 桌面窗口与本地桥接
ebook/frontend/            React 界面、缩略图及构建配置
ebook/assets/              五幅封面原图与程序图标
tests/                     章节、导出与桌面桥接测试
build-windows.bat          构建前端并打包 Windows 程序
```

在仓库根目录运行：

```powershell
python -m unittest discover -s tests -v
cd ebook/frontend
npm ci
npm run build
```

本机 Windows 已检查修复版窗口启动、桌面桥接与 EPUB 文件结构；电子书相关 4 项测试及前端构建通过。不同阅读器和其他电脑的完整兼容性尚未验证。

## 当前边界与素材来源

- 当前输入为 TXT，导出为 EPUB；PDF、MOBI 等格式尚未实现。
- 支持的章节标题取决于当前识别规则，复杂格式、误识别和漏识别仍需人工检查。
- 自定义封面会裁剪以适配竖版；内置封面书名过长时只绘制前 36 个字符。
- 内置封面是 5 幅 AI 生成插画加样式组合，并非 100 幅独立插画。界面布局参考 [Grain](https://github.com/jeasoncc/grain)，按钮组件改编自 [shadcn/ui](https://github.com/shadcn-ui/ui)，第三方许可说明见 [`ebook/frontend/THIRD_PARTY_NOTICES.md`](ebook/frontend/THIRD_PARTY_NOTICES.md)。
- 请只导入和使用你有权处理的小说与封面。反馈问题时，建议提供系统版本、操作步骤和不含个人内容的示例。

欢迎通过 [Issues](https://github.com/yifanchen12/ebook/issues)反馈章节识别、阅读器兼容性或界面使用问题。
