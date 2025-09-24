# file_handler.py
import os
import tkinter as tk
from tkinter import messagebox
from FileProcessor.docx_processor import DocxProcessor
from FileProcessor.text_processor_file import TextFileProcessor
from FileProcessor.doc_processor import DocProcessor

class FileHandler:
    def __init__(self):
        self._file_types = {
            '.docx': DocxProcessor(),
            '.txt': TextFileProcessor(),
            '.doc': DocProcessor()
        }

    def read_files(self, paths):
        text_content = []
        for path in paths:
            ext = os.path.splitext(path)[1].lower()
            if ext in self._file_types:
                try:
                    content = self._file_types[ext].read_file(path)
                    if isinstance(content, list):
                        text_content.extend(content)
                    else:
                        text_content.append(content)
                except Exception as e:
                    messagebox.showerror(
                        "错误",
                        f"读取文件失败: {path}\n错误信息: {str(e)}"
                    )
            else:
                messagebox.showwarning(
                    "警告",
                    f"不支持的文件格式: {ext}"
                )
        return text_content

    def export_files(self, text, output_path, format_type):
        ext = os.path.splitext(output_path)[1].lower()
        if ext in self._file_types:
            return self._file_types[ext].export_file(text, output_path)
        else:
            raise ValueError("不支持的输出格式")