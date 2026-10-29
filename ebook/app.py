import io
import os
import sys
import tempfile
import tkinter as tk
import zipfile
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk
from ebook.core import chapters, cover_image, export_epub, read_text


def prepare_tcl():
    # Some Windows Python distributions ship the Tcl libraries as zip files.
    directory = Path(sys.base_prefix) / 'tcl'
    archives = sorted(directory.glob('libtcl*.zip')) + sorted(directory.glob('libtk*.zip'))
    if len(archives) != 2 or os.environ.get('TCL_LIBRARY'):
        return
    cache = Path(tempfile.gettempdir()) / ('ebook-tcl-' + sys.version.split()[0])
    for archive in archives:
        folder = 'tcl_library' if archive.name.startswith('libtcl') else 'tk_library'
        if not (cache / folder / 'init.tcl' if folder == 'tcl_library' else cache / folder / 'tk.tcl').exists():
            with zipfile.ZipFile(archive) as z:
                z.extractall(cache)
        os.environ['TCL_LIBRARY' if folder == 'tcl_library' else 'TK_LIBRARY'] = str(cache / folder)


class App(tk.Tk):
    def __init__(self):
        prepare_tcl()
        super().__init__()
        self.title('书卷 · eBook')
        self.geometry('1280x800')
        self.minsize(950, 650)
        self.configure(bg='#eee6d5')
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#eee6d5')
        style.configure('TLabel', background='#eee6d5', foreground='#463b2e', font=('Microsoft YaHei UI', 10))
        style.configure('TButton', background='#44554c', foreground='#f9f2df', borderwidth=0, padding=(14, 9), font=('Microsoft YaHei UI', 10))
        style.map('TButton', background=[('active', '#647668')])
        style.configure('TCombobox', padding=7, fieldbackground='#faf5ea')
        self.title_var = tk.StringVar(value='未命名')
        self.template = tk.StringVar(value='1')
        self.texture = tk.StringVar(value='素白')
        self.cover_path = None
        self.status = tk.StringVar(value='请选择 TXT 文件')
        header = tk.Frame(self, bg='#263e37', height=85)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text='書 卷', bg='#263e37', fg='#f2dfb7', font=('Microsoft YaHei UI', 22, 'bold')).pack(side='left', padx=(25, 14))
        tk.Label(header, text='一  方  书  案  ·  收  藏  万  千  故  事', bg='#263e37', fg='#c9b993', font=('Microsoft YaHei UI', 10)).pack(side='left')
        top = ttk.Frame(self, padding=(18, 12))
        top.pack(fill='x')
        ttk.Button(top, text='打开 TXT', command=self.open_file).pack(side='left')
        ttk.Label(top, text='书名').pack(side='left', padx=(16, 5))
        ttk.Entry(top, textvariable=self.title_var, width=32).pack(side='left')
        ttk.Button(top, text='重新识别章节', command=self.refresh).pack(side='left', padx=10)
        ttk.Button(top, text='导出 EPUB', command=self.export).pack(side='right')
        main = ttk.Panedwindow(self, orient='horizontal')
        main.pack(fill='both', expand=True, padx=10, pady=5)
        left, middle, right = ttk.Frame(main, padding=5), ttk.Frame(main, padding=5), ttk.Frame(main, padding=5)
        main.add(left, weight=1); main.add(middle, weight=4); main.add(right, weight=2)
        ttk.Label(left, text='章节目录').pack(anchor='w')
        self.list = tk.Listbox(left, width=23, bg='#f8f2e5', fg='#544637', selectbackground='#667668', selectforeground='white', relief='flat', highlightthickness=0, font=('Microsoft YaHei UI', 10), activestyle='none')
        self.list.pack(fill='both', expand=True)
        self.list.bind('<<ListboxSelect>>', self.go_to_chapter)
        ttk.Label(middle, text='原文编辑（修改章节标题后点击“重新识别章节”）').pack(anchor='w')
        self.text = tk.Text(middle, wrap='word', undo=True, bg='#fbf7ed', fg='#423b30', insertbackground='#423b30', relief='flat', padx=20, pady=16, spacing1=4, spacing3=5, font=('Microsoft YaHei UI', 11))
        scroll = ttk.Scrollbar(middle, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y'); self.text.pack(fill='both', expand=True)
        ttk.Label(right, text='二次元封面（5 幅插画 · 100 种组合）').pack(anchor='w')
        self.cover_select = ttk.Combobox(right, textvariable=self.template, values=[str(i) for i in range(1, 101)], state='readonly')
        self.cover_select.pack(fill='x', pady=5)
        self.cover_select.bind('<<ComboboxSelected>>', self.use_template)
        ttk.Button(right, text='上传封面图片', command=self.upload_cover).pack(fill='x')
        self.cover_label = ttk.Label(right)
        self.cover_label.pack(pady=10)
        ttk.Label(right, text='书页纹理').pack(anchor='w')
        ttk.Combobox(right, textvariable=self.texture, values=['素白', '暖纸', '羊皮纸', '护眼绿'], state='readonly').pack(fill='x', pady=5)
        ttk.Label(right, text='部分阅读器会覆盖书页样式。', wraplength=210).pack(anchor='w')
        ttk.Label(self, textvariable=self.status, padding=(20, 10)).pack(fill='x')
        self.title_var.trace_add('write', lambda *_: self.preview())
        self.preview()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('文本文件', '*.txt'), ('所有文件', '*.*')])
        if not path:
            return
        try:
            content, encoding = read_text(path)
            self.text.delete('1.0', 'end'); self.text.insert('1.0', content)
            self.title_var.set(Path(path).stem)
            self.refresh()
            self.status.set(f'已导入：{Path(path).name}（{encoding}），识别到 {self.list.size()} 章')
        except (OSError, ValueError) as exc:
            messagebox.showerror('打开失败', str(exc))

    def refresh(self):
        sections = chapters(self.text.get('1.0', 'end-1c'))
        self.list.delete(0, 'end')
        for name, _ in sections:
            self.list.insert('end', name)
        self.status.set(f'识别到 {len(sections)} 章；可在原文中调整标题后重新识别。')

    def go_to_chapter(self, _event):
        selection = self.list.curselection()
        if not selection:
            return
        name = self.list.get(selection[0])
        pos = self.text.search(name, '1.0', stopindex='end')
        if pos:
            self.text.see(pos)

    def preview(self):
        try:
            data = cover_image(self.title_var.get(), int(self.template.get()) - 1, self.cover_path)
            img = Image.open(io.BytesIO(data)); img.thumbnail ( (180, 270) )
            self.preview_image = ImageTk.PhotoImage(img)
            self.cover_label.configure(image=self.preview_image)
        except (OSError, ValueError) as exc:
            messagebox.showerror('封面错误', str(exc))

    def use_template(self, _event=None):
        self.cover_path = None
        self.preview()

    def upload_cover(self):
        path = filedialog.askopenfilename(filetypes=[('图片', '*.png *.jpg *.jpeg *.webp *.bmp')])
        if path:
            try:
                cover_image(self.title_var.get(), source=path)
                self.cover_path = path
                self.preview()
            except (OSError, ValueError) as exc:
                messagebox.showerror('封面错误', str(exc))

    def export(self):
        title = self.title_var.get().strip()
        sections = chapters(self.text.get('1.0', 'end-1c'))
        if not title or not sections:
            messagebox.showwarning('无法导出', '请填写书名并导入或输入正文。')
            return
        path = filedialog.asksaveasfilename(defaultextension='.epub', filetypes=[('EPUB 电子书', '*.epub')], initialfile='电子书.epub')
        if not path:
            return
        try:
            cover = cover_image(title, int(self.template.get()) - 1, self.cover_path)
            export_epub(path, title, sections, cover, self.texture.get())
            self.refresh()
            self.status.set(f'已导出 {len(sections)} 章：{path}')
            messagebox.showinfo('导出成功', f'已生成 EPUB：\n{path}')
        except (OSError, ValueError) as exc:
            messagebox.showerror('导出失败', str(exc))


if __name__ == '__main__':
    App().mainloop()

