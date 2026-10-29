import html
import io
import re
import uuid
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HEADING = re.compile(r'^\s*(?:第[零〇一二三四五六七八九十百千万两\d]+[章节回卷部篇][^\n]{0,60}|(?:序章|序言|楔子|引子|前言|尾声|后记|番外)(?:[ \t：:·-].{0,40})?|Chapter\s+\d+[^\n]{0,60})\s*$', re.I)
COLORS = ['#243b53', '#734b5e', '#315950', '#614f38', '#33304f', '#713c3c', '#38556a', '#53613b', '#775644', '#3e3b45']


def read_text(path):
    data = Path(path).read_bytes()
    for encoding in ('utf-8-sig', 'gb18030'):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            pass
    raise ValueError('无法识别文件编码，请将 TXT 保存为 UTF-8 或 GB18030。')


def chapters(text):
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    result, title, body = [], None, []
    for line in lines:
        if HEADING.fullmatch(line) and len(line.strip()) <= 80:
            if title is not None or any(x.strip() for x in body):
                result.append((title or '正文', '\n'.join(body).strip()))
            title, body = line.strip(), []
        else:
            body.append(line)
    if title is not None or any(x.strip() for x in body):
        result.append((title or '正文', '\n'.join(body).strip()))
    return result


def cover_image(title, template=0, source=None):
    if source:
        with Image.open(source) as img:
            img = ImageOps.fit(img.convert('RGB'), (600, 900))
    else:
        template = int(template) % 100
        artwork = Path(__file__).parent / 'assets' / f'anime-{template % 5 + 1}.png'
        if artwork.exists():
            with Image.open(artwork) as source_image:
                base = ImageOps.fit(source_image.convert('RGB'), (600, 900))
            tint = Image.new('RGB', base.size, COLORS[template // 10])
            img = Image.blend(base, tint, 0.08 + 0.035 * ((template // 5) % 4))
        else:
            img = Image.new('RGB', (600, 900), COLORS[template // 10])
        draw = ImageDraw.Draw(img)
        style = template % 10
        for i in range(style + 1):
            inset = 25 + i * 9
            draw.rectangle((inset, inset, 599-inset, 899-inset), outline='#d5bd90', width=2)
        try:
            font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 52)
        except OSError:
            font = ImageFont.load_default()
        lines = [title[i:i+9] for i in range(0, min(len(title), 36), 9)] or ['未命名']
        top = 840 - len(lines) * 65
        draw.rectangle((65, top - 25, 535, 860), fill='#263e37')
        for index, line in enumerate(lines):
            draw.text((300, top + 25 + index * 65), line, fill='#f6ead4', font=font, anchor='mm')
    out = io.BytesIO()
    img.save(out, 'PNG')
    return out.getvalue()


def export_epub(path, title, sections, cover, texture='素白'):
    if not title.strip() or not sections:
        raise ValueError('书名和正文不能为空。')
    identifier = str(uuid.uuid4())
    e = html.escape
    backgrounds = {'素白': '#ffffff', '暖纸': '#f5edda', '羊皮纸': '#eee0bd', '护眼绿': '#e4eddf'}
    color = backgrounds.get(texture, '#ffffff')
    pattern = 'background-image: repeating-linear-gradient(0deg, transparent 0, transparent 3px, rgba(100,80,45,.025) 4px);' if texture in ('暖纸', '羊皮纸') else ''
    css = f'body {{ background-color: {color}; {pattern} line-height: 1.8; }} p {{ text-indent: 2em; }}'
    nav = ''.join(f'<li><a href="chapter{i}.xhtml">{e(name)}</a></li>' for i, (name, _) in enumerate(sections))
    manifest = ''.join(f'<item id="c{i}" href="chapter{i}.xhtml" media-type="application/xhtml+xml"/>' for i in range(len(sections)))
    spine = ''.join(f'<itemref idref="c{i}"/>' for i in range(len(sections)))
    opf = f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="id">urn:uuid:{identifier}</dc:identifier><dc:title>{e(title)}</dc:title><dc:language>zh</dc:language><meta property="dcterms:modified">2020-01-01T00:00:00Z</meta></metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="cover" href="cover.png" media-type="image/png" properties="cover-image"/><item id="coverpage" href="cover.xhtml" media-type="application/xhtml+xml"/><item id="css" href="style.css" media-type="text/css"/>{manifest}</manifest><spine><itemref idref="coverpage"/>{spine}</spine></package>'''
    def page(name, content):
        return f'<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>{e(name)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head><body>{content}</body></html>'
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr('OEBPS/content.opf', opf)
        z.writestr('OEBPS/style.css', css)
        z.writestr('OEBPS/cover.png', cover)
        z.writestr('OEBPS/cover.xhtml', page('封面', '<div><img src="cover.png" alt="封面" style="max-width:100%; max-height:100%"/></div>'))
        z.writestr('OEBPS/nav.xhtml', page('目录', f'<nav epub:type="toc" id="toc"><h1>目录</h1><ol>{nav}</ol></nav>'))
        for i, (name, body) in enumerate(sections):
            paragraphs = ''.join(f'<p>{e(line.strip())}</p>' for line in body.splitlines() if line.strip())
            z.writestr(f'OEBPS/chapter{i}.xhtml', page(name, f'<h1>{e(name)}</h1>{paragraphs}'))

