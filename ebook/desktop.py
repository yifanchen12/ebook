"""Desktop window and local-only bridge for the eBook editor."""
import base64
import io
import sys
from pathlib import Path

from PIL import Image
from ebook.core import chapters, cover_image, export_epub, read_text


class BookAPI:
    def __init__(self):
        self._window = None
        self._cover_path = None

    def open_text(self):
        import webview
        paths = self._window.create_file_dialog(webview.OPEN_DIALOG, file_types=('文本文件 (*.txt)', '所有文件 (*.*)'))
        if not paths:
            return None
        text, encoding = read_text(paths[0])
        return {'title': Path(paths[0]).stem, 'text': text, 'encoding': encoding, 'name': Path(paths[0]).name}

    def chapter_list(self, text):
        return [name for name, _ in chapters(text)]

    def preview_cover(self, title, template, custom=False):
        data = cover_image(title or '未命名', int(template), self._cover_path if custom else None)
        with Image.open(io.BytesIO(data)) as image:
            image.thumbnail((240, 360))
            output = io.BytesIO()
            image.convert('RGB').save(output, format='JPEG', quality=85)
        return 'data:image/jpeg;base64,' + base64.b64encode(output.getvalue()).decode('ascii')

    def upload_cover(self):
        import webview
        paths = self._window.create_file_dialog(webview.OPEN_DIALOG, file_types=('图片文件 (*.png;*.jpg;*.jpeg;*.webp;*.bmp)', '所有文件 (*.*)'))
        if not paths:
            return False
        cover_image('未命名', source=paths[0])
        self._cover_path = paths[0]
        return True

    def export_book(self, title, text, template, custom, texture):
        import webview
        sections = chapters(text)
        if not title.strip() or not sections:
            raise ValueError('请填写书名并导入或输入正文。')
        if custom and not self._cover_path:
            raise ValueError('请先上传封面。')
        path = self._window.create_file_dialog(webview.SAVE_DIALOG, save_filename='电子书.epub', file_types=('EPUB 电子书 (*.epub)',))
        if not path:
            return None
        if isinstance(path, (tuple, list)):
            path = path[0]
        if not path.lower().endswith('.epub'):
            path += '.epub'
        export_epub(path, title.strip(), sections, cover_image(title, int(template), self._cover_path if custom else None), texture)
        return {'path': path, 'chapters': len(sections)}


def main():
    import webview
    api = BookAPI()
    package_dir = Path(sys._MEIPASS) / 'ebook' if getattr(sys, 'frozen', False) else Path(__file__).parent
    page = package_dir / 'frontend' / 'dist' / 'index.html'
    if not page.exists():
        raise RuntimeError('前端尚未构建，请先在 ebook/frontend 中运行 npm install 和 npm run build。')
    api._window = webview.create_window('书卷 · eBook', str(page), js_api=api, width=1440, height=900, min_size=(1000, 650))
    webview.start()


if __name__ == '__main__':
    main()
