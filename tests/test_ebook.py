import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from ebook.core import chapters, cover_image, export_epub, read_text


class EbookTests(unittest.TestCase):
    def test_chapters_and_fallback(self):
        self.assertEqual([x[0] for x in chapters('前言内容\n第一章 开始\n正文\n第二章 结束\n完成')], ['正文', '第一章 开始', '第二章 结束'])
        self.assertEqual(chapters('没有章节标题'), [('正文', '没有章节标题')])

    def test_gbk_and_epub(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'book.txt'
            source.write_bytes('第一章 起始\n故事 & 内容'.encode('gb18030'))
            content, encoding = read_text(source)
            self.assertEqual(encoding, 'gb18030')
            target = Path(temp) / 'book.epub'
            export_epub(target, '书 & 名', chapters(content), cover_image('书名', 99), '暖纸')
            with zipfile.ZipFile(target) as z:
                self.assertEqual(z.infolist()[0].filename, 'mimetype')
                self.assertEqual(z.infolist()[0].compress_type, zipfile.ZIP_STORED)
                for name in ('META-INF/container.xml', 'OEBPS/content.opf', 'OEBPS/nav.xhtml', 'OEBPS/chapter0.xhtml'):
                    ElementTree.fromstring(z.read(name))
                self.assertIn('故事 &amp; 内容', z.read('OEBPS/chapter0.xhtml').decode())
                self.assertTrue(z.read('OEBPS/cover.png').startswith(b'\x89PNG'))


if __name__ == '__main__':
    unittest.main()

