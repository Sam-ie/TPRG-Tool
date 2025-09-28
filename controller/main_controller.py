import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional
import threading
import time

from model.document_model import DocumentModel
from view.main_window import MainWindow
from view.analysis_window import AnalysisWindow
from view.help_window import HelpWindow
from view.support_window import SupportWindow
from view.progress_window import ProgressWindow
from utils.file_manager import FileManager
from languages.language_factory import LanguageFactory


class MainController:
    def __init__(self, root, similarity_threshold: float = 0.8):
        self.root = root
        self.model = DocumentModel(similarity_threshold)
        self.language_manager = LanguageFactory.create_language("zh_CN")
        self.file_manager = None
        self.view = MainWindow(root, self, self.language_manager)

        # 注册观察者
        self.model.add_observer(self.view)

        # 进度窗口引用
        self.progress_window = None

        # 初始化FileManager
        self._update_file_manager()

    def _update_file_manager(self):
        """更新FileManager的语言设置"""
        self.file_manager = FileManager(self.language_manager)

    def select_file(self):
        """选择文件"""
        # 确保FileManager使用当前语言
        self._update_file_manager()

        file_path = filedialog.askopenfilename(
            title=self.language_manager.get_text("select_file"),
            filetypes=self.file_manager.get_file_filters(import_filter=True)
        )

        if file_path:
            if not self.file_manager.is_supported_import_file(file_path):
                self.view.show_error(self.language_manager.get_text("unsupported_format"))
                return

            # 在新线程中读取文件
            thread = threading.Thread(target=self._load_file_with_progress, args=(file_path,))
            thread.daemon = True
            thread.start()

    def _load_file_with_progress(self, file_path: str):
        """带进度条的文件读取"""
        self.root.after(0, self._create_progress_window, file_path)
        time.sleep(0.1)

        def progress_callback(current, total, status):
            if self.progress_window and self.progress_window.window.winfo_exists():
                self.root.after(0, self.progress_window.update_progress, current, total, status)

        try:
            # 确保使用当前语言的FileManager
            self._update_file_manager()
            content, error = self.file_manager.read_file(file_path, progress_callback)
            self.root.after(0, self._handle_file_load_result, file_path, content, error)
        except Exception as e:
            self.root.after(0, self._handle_file_load_result, file_path, None, str(e))

    def _create_progress_window(self, file_path: str):
        """创建进度窗口"""
        file_name = os.path.basename(file_path)
        title = f"{self.language_manager.get_text('reading_file')} - {file_name}"

        self.progress_window = ProgressWindow(
            self.root,
            self.language_manager,
            title,
            100
        )

    def _handle_file_load_result(self, file_path: str, content: Optional[str], error: Optional[str]):
        """处理文件读取结果"""
        if self.progress_window and self.progress_window.window.winfo_exists():
            if content and not error:
                # 使用多语言完成消息
                complete_message = self.language_manager.get_text("file_read_complete")
                self.progress_window.complete(complete_message)
                self.root.after(600, lambda: self._finalize_file_load(file_path, content, error))
            else:
                self.progress_window.close()
                if error:
                    self.view.show_error(error)
        else:
            self._finalize_file_load(file_path, content, error)

    def _finalize_file_load(self, file_path: str, content: Optional[str], error: Optional[str]):
        """最终处理文件加载"""
        if error:
            self.view.show_error(error)
            return

        if not content:
            self.view.show_error("文件内容为空")
            return

        # 加载文件到模型（会自动通知观察者）
        success, message_key = self.model.load_file_with_content(file_path, content)
        if not success:
            # 只有在失败时才显示错误信息
            self.view.show_error(self.language_manager.get_text(message_key))

        # 清理进度窗口
        if self.progress_window and self.progress_window.window.winfo_exists():
            self.progress_window.close()
        self.progress_window = None

    def export_file(self):
        """导出文件"""
        if not self.model.modified_content:
            self.view.show_error(self.language_manager.get_text("no_content_to_export"))
            return

        # 确保FileManager使用当前语言
        self._update_file_manager()

        file_path = filedialog.asksaveasfilename(
            title=self.language_manager.get_text("export"),
            defaultextension=".docx",
            filetypes=self.file_manager.get_file_filters(import_filter=False)
        )

        if file_path:
            if not self.file_manager.is_supported_export_file(file_path):
                self.view.show_error(self.language_manager.get_text("unsupported_export_format"))
                return

            ext = file_path.lower()[-4:]
            file_type = 'txt' if ext == '.txt' else 'docx'

            error = self.file_manager.write_file(file_path, self.model.modified_content, file_type)
            if error:
                self.view.show_error(error)
            else:
                self.view.show_info(self.language_manager.get_text("file_save_success"))

    def deduplicate(self):
        success, message_key = self.model.process_text('deduplicate')
        if not success:
            self.view.show_error(self.language_manager.get_text(message_key))

    def spell_check(self):
        success, message_key = self.model.process_text('spell_check')
        if not success:
            self.view.show_error(self.language_manager.get_text(message_key))

    def correct_symbols(self):
        success, message_key = self.model.process_text('correct_symbols')
        if not success:
            self.view.show_error(self.language_manager.get_text(message_key))

    def smart_auto_process(self):
        success, message_key = self.model.smart_auto_process()
        if not success:
            self.view.show_error(self.language_manager.get_text(message_key))

    def show_analysis(self):
        """显示智能分析窗口"""
        AnalysisWindow(self.view.root, self, self.language_manager)

    def show_help(self):
        """显示帮助窗口"""
        HelpWindow(self.view.root, self.language_manager)

    def show_support(self):
        """显示支持作者窗口"""
        SupportWindow(self.view.root, self.language_manager)

    def change_language(self, event):
        """切换UI语言"""
        language_map = {
            "简体中文": "zh_CN",
            "繁体中文": "zh_TW",
            "English": "en",
            "日本語": "ja"
        }

        selected_language = self.view.language_var.get()
        language_code = language_map.get(selected_language, "zh_CN")

        # 更新语言管理器
        self.language_manager = LanguageFactory.create_language(language_code)
        self.view.language_manager = self.language_manager

        # 更新FileManager的语言设置
        self._update_file_manager()

        # 更新UI文本
        self.view.update_ui_text()

    def previous_modification(self):
        # TODO: 实现跳转到前一处修改
        pass

    def next_modification(self):
        # TODO: 实现跳转到后一处修改
        pass