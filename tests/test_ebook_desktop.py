import tempfile
import unittest
import zipfile
from pathlib import Path

from ebook.desktop import BookAPI


class FakeWindow:
    def __init__(self, path):
        self.path = path

    def create_file_dialog(self, *args, **kwargs):
        return (str(self.path),)


class DesktopBridgeTests(unittest.TestCase):
    def test_import_preview_and_export(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / '示例.txt'
            source.write_text('第一章 初见\n这是正文\n第二章 重逢\n故事继续', encoding='utf-8')
            api = BookAPI()
            api._window = FakeWindow(source)
            opened = api.open_text()
            self.assertEqual(opened['title'], '示例')
            self.assertEqual(api.chapter_list(opened['text']), ['第一章 初见', '第二章 重逢'])
            preview = api.preview_cover('示例', 1)
            self.assertTrue(preview.startswith('data:image/jpeg;base64,'))
            self.assertLess(len(preview), 200000)
            target = Path(folder) / 'result.epub'
            api._window = FakeWindow(target)
            result = api.export_book('示例', opened['text'], 1, False, '暖纸')
            self.assertEqual(result['chapters'], 2)
            with zipfile.ZipFile(target) as book:
                self.assertIn('OEBPS/chapter1.xhtml', book.namelist())

    def test_empty_book_is_rejected(self):
        with self.assertRaises(ValueError):
            BookAPI().export_book('书名', '', 0, False, '素白')


if __name__ == '__main__':
    unittest.main()
