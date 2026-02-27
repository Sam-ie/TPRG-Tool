import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional
import threading
import time

from utils.file_manager import FileManager
from view.progress_window import ProgressWindow


class FileOperationController:
    """文件操作控制器"""

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.file_manager = None
        self.progress_window = None
        self._update_file_manager()

    def _update_file_manager(self):
        """更新FileManager的语言设置"""
        self.file_manager = FileManager(self.main_controller.language_manager)

    def select_file(self):
        """选择文件"""
        self._update_file_manager()

        file_path = filedialog.askopenfilename(
            title=self.main_controller.language_manager.get_text("select_file"),
            filetypes=self.file_manager.get_file_filters(import_filter=True)
        )

        if file_path:
            if not self.file_manager.is_supported_import_file(file_path):
                self.main_controller.view.show_error(
                    self.main_controller.language_manager.get_text("unsupported_format")
                )
                return

            thread = threading.Thread(target=self._load_file_with_progress, args=(file_path,))
            thread.daemon = True
            thread.start()

    def _load_file_with_progress(self, file_path: str):
        """带进度条的文件读取"""
        self.main_controller.root.after(0, self._create_progress_window, file_path)
        time.sleep(0.1)

        def progress_callback(current, total, status):
            if self.progress_window and self.progress_window.window.winfo_exists():
                self.main_controller.root.after(
                    0, self.progress_window.update_progress, current, total, status
                )

        try:
            self._update_file_manager()
            content, error = self.file_manager.read_file(file_path, progress_callback)
            self.main_controller.root.after(
                0, self._handle_file_load_result, file_path, content, error
            )
        except Exception as e:
            self.main_controller.root.after(
                0, self._handle_file_load_result, file_path, None, str(e)
            )

    def _create_progress_window(self, file_path: str):
        """创建进度窗口"""
        file_name = os.path.basename(file_path)
        title = f"{self.main_controller.language_manager.get_text('reading_file')} - {file_name}"

        self.progress_window = ProgressWindow(
            self.main_controller.root,
            self.main_controller.language_manager,
            title,
            100
        )

    def _handle_file_load_result(self, file_path: str, content: Optional[str], error: Optional[str]):
        """处理文件读取结果"""
        if self.progress_window and self.progress_window.window.winfo_exists():
            if content and not error:
                complete_message = self.main_controller.language_manager.get_text("file_read_complete")
                self.progress_window.complete(complete_message)
                self.main_controller.root.after(
                    600, lambda: self._finalize_file_load(file_path, content, error)
                )
            else:
                self.progress_window.close()
                if error:
                    self.main_controller.view.show_error(error)
        else:
            self._finalize_file_load(file_path, content, error)

    def _finalize_file_load(self, file_path: str, content: Optional[str], error: Optional[str]):
        """最终处理文件加载"""
        if error:
            self.main_controller.view.show_error(error)
            return

        if not content:
            self.main_controller.view.show_error("文件内容为空")
            return

        success, message_key = self.main_controller.model.load_file_with_content(file_path, content)
        if not success:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text(message_key)
            )

        if self.progress_window and self.progress_window.window.winfo_exists():
            self.progress_window.close()
        self.progress_window = None

    def export_file(self):
        """导出文件 - 直接保存视图编辑器中的内容"""
        # 获取编辑器内容
        editor_content = self.main_controller.view.text_display.get(1.0, tk.END).strip()
        if not editor_content:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text("no_content_to_export")
            )
            return

        self._update_file_manager()

        file_path = filedialog.asksaveasfilename(
            title=self.main_controller.language_manager.get_text("export"),
            defaultextension=".txt",
            filetypes=self.file_manager.get_file_filters(import_filter=False)
        )

        if file_path:
            if not self.file_manager.is_supported_export_file(file_path):
                self.main_controller.view.show_error(
                    self.main_controller.language_manager.get_text("unsupported_export_format")
                )
                return

            ext = file_path.lower()[-4:]
            file_type = 'txt' if ext == '.txt' else 'docx'

            error = self.file_manager.write_file(
                file_path, editor_content, file_type
            )
            if error:
                self.main_controller.view.show_error(error)
            else:
                self.main_controller.view.show_info(
                    self.main_controller.language_manager.get_text("file_save_success")
                )
