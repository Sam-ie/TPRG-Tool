# controller.py
import tkinter as tk
from tkinter import filedialog, messagebox
from Language.lang_manager import LangManager


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def handle_browse(self):
        # 处理文件浏览事件
        file_types = [
            ('Word 文档', '*.docx'),
            ('旧版Word文档', '*.doc'),
            ('文本文件', '*.txt'),
            ('所有文件', '*.*')
        ]

        paths = filedialog.askopenfilenames(
            title=self.model.lang_config.get('select_files', '选择文件'),
            filetypes=file_types
        )

        if paths:
            self.model.set_files(list(paths))
        else:
            messagebox.showwarning(
                self.model.lang_config.get('warning', '警告'),
                self.model.lang_config.get('no_files_selected', '未选择文件')
            )

    def handle_process(self, operation_type):
        # 处理文本处理事件
        if not self.model.file_paths:
            messagebox.showerror(
                self.model.lang_config.get('error', '错误'),
                self.model.lang_config.get('no_files_selected', '未选择文件')
            )
            return

        try:
            self.model.process_text(operation_type)
            self.view.update(self.model)
        except Exception as e:
            messagebox.showerror(
                self.model.lang_config.get('error', '错误'),
                f"{self.model.lang_config.get('processing_error', '处理错误')}: {str(e)}"
            )

    def handle_lang_switch(self, lang_code):
        # 处理语言切换事件
        if lang_code in LangManager.SUPPORTED_LANGS:
            self.model.lang_config = LangManager.get_config(lang_code)
            self.view.update(self.model)
        else:
            messagebox.showerror(
                self.model.lang_config.get('error', '错误'),
                self.model.lang_config.get('invalid_lang', '不支持的语言')
            )