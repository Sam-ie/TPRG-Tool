import tkinter as tk
from tkinter import filedialog
from model.document_model import DocumentModel
from view.main_window import MainWindow
from view.analysis_window import AnalysisWindow
from view.help_window import HelpWindow
from view.support_window import SupportWindow
from utils.file_manager import FileManager
from languages.language_factory import LanguageFactory


class MainController:
    def __init__(self, root, similarity_threshold: float = 0.8):
        self.root = root
        self.model = DocumentModel(similarity_threshold)
        self.language_manager = LanguageFactory.create_language("zh_CN")  # 默认简体中文
        self.view = MainWindow(root, self, self.language_manager)

        # 注册观察者
        self.model.add_observer(self.view)

        # 初始化按钮状态
        self.update_button_states()

    def select_file(self):
        """选择文件"""
        file_path = filedialog.askopenfilename(
            title=self.language_manager.get_text("select_file"),
            filetypes=FileManager.get_file_filters(import_filter=True)
        )

        if file_path:
            if not FileManager.is_supported_import_file(file_path):
                self.view.show_error(self.language_manager.get_text("unsupported_format"))
                return

            success, message_key = self.model.load_file(file_path)
            if success:
                # 使用view的方法设置文件路径，确保语言切换时不会丢失
                self.view.set_file_path(file_path)
                self.view.show_info(self.language_manager.get_text(message_key))
                # 更新文本显示
                self.display_file_content()
            else:
                self.view.show_error(self.language_manager.get_text(message_key))

            self.update_button_states()

    def export_file(self):
        """导出文件"""
        if not self.model.modified_content:
            self.view.show_error(self.language_manager.get_text("no_content_to_export"))
            return

        file_path = filedialog.asksaveasfilename(
            title=self.language_manager.get_text("export"),
            defaultextension=".docx",
            filetypes=FileManager.get_file_filters(import_filter=False)
        )

        if file_path:
            if not FileManager.is_supported_export_file(file_path):
                self.view.show_error(self.language_manager.get_text("unsupported_export_format"))
                return

            # 确定文件类型
            ext = file_path.lower()[-4:]
            if ext == '.txt':
                file_type = 'txt'
            elif ext == '.docx':
                file_type = 'docx'
            elif ext == '.pdf':
                file_type = 'pdf'
            else:
                file_type = 'docx'  # 默认

            success, message_key = self.model.save_file(file_path, file_type)
            if success:
                self.view.show_info(self.language_manager.get_text(message_key))
            else:
                self.view.show_error(self.language_manager.get_text(message_key))

    def display_file_content(self):
        """显示文件内容"""
        if hasattr(self.view, 'text_display') and self.model.original_content:
            self.view.text_display.delete(1.0, tk.END)
            self.view.text_display.insert(1.0, self.model.original_content)

    def update_button_states(self):
        """更新按钮状态（根据是否有文件内容）"""
        has_content = bool(self.model.original_content)

        # 更新处理按钮的状态
        if hasattr(self.view, 'buttons'):
            for button_key, button in self.view.buttons.items():
                if button_key not in ['smart_analysis', 'export']:  # 分析和导出按钮单独处理
                    button.config(state=tk.NORMAL if has_content else tk.DISABLED)

        # 更新导出按钮状态
        if hasattr(self.view, 'buttons') and 'export' in self.view.buttons:
            has_modified_content = bool(self.model.modified_content)
            self.view.buttons['export'].config(
                state=tk.NORMAL if has_modified_content else tk.DISABLED
            )

        # 智能分析按钮始终可用（即使没有文件内容）
        if hasattr(self.view, 'buttons') and 'smart_analysis' in self.view.buttons:
            self.view.buttons['smart_analysis'].config(state=tk.NORMAL)

    def deduplicate(self):
        success, message_key = self.model.process_text('deduplicate')
        if success:
            self.view.show_info(self.language_manager.get_text(message_key))
            self.display_modified_content()
            self.update_button_states()
        else:
            self.view.show_error(self.language_manager.get_text(message_key))

    def spell_check(self):
        success, message_key = self.model.process_text('spell_check')
        if success:
            self.view.show_info(self.language_manager.get_text(message_key))
            self.display_modified_content()
            self.update_button_states()
        else:
            self.view.show_error(self.language_manager.get_text(message_key))

    def correct_symbols(self):
        success, message_key = self.model.process_text('correct_symbols')
        if success:
            self.view.show_info(self.language_manager.get_text(message_key))
            self.display_modified_content()
            self.update_button_states()
        else:
            self.view.show_error(self.language_manager.get_text(message_key))

    def smart_auto_process(self):
        success, message_key = self.model.smart_auto_process()
        if success:
            self.view.show_info(self.language_manager.get_text(message_key))
            self.display_modified_content()
            self.update_button_states()
        else:
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

    def display_modified_content(self):
        """显示修改后的内容"""
        if hasattr(self.view, 'text_display') and self.model.modified_content:
            self.view.text_display.delete(1.0, tk.END)
            self.view.text_display.insert(1.0, self.model.modified_content)
            # TODO: 实现审阅模式的高亮显示

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

        # 创建新的语言实例并更新视图
        self.language_manager = LanguageFactory.create_language(language_code)
        self.view.language_manager = self.language_manager  # 更新视图的语言管理器
        self.view.update_ui_text()

    def previous_modification(self):
        # TODO: 实现跳转到前一处修改
        pass

    def next_modification(self):
        # TODO: 实现跳转到后一处修改
        pass