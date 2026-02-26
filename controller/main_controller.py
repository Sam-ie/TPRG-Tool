import tkinter as tk
from model.document_model import DocumentModel
from model.commands import CommandManager
from view.main_window import MainWindow
from languages.language_factory import LanguageFactory

from controller.text_edit_controller import TextEditController
from controller.file_operation_controller import FileOperationController
from controller.function_button_controller import FunctionButtonController


class MainController:
    def __init__(self, root, similarity_threshold: float = 0.8):
        self.root = root
        self.model = DocumentModel(similarity_threshold)
        self.language_manager = LanguageFactory.create_language("zh_CN")
        self.view = MainWindow(root, self, self.language_manager)

        self.command_manager = CommandManager()
        self.model.add_observer(self.view)

        self.text_edit_controller = TextEditController(self)
        self.file_operation_controller = FileOperationController(self)
        self.function_button_controller = FunctionButtonController(self)

        self.update_button_states()

    def on_text_edited(self, content: str):
        self.update_button_states()

    def undo(self):
        if self.command_manager.undo():
            self.update_button_states()
            return True
        return False

    def redo(self):
        if self.command_manager.redo():
            self.update_button_states()
            return True
        return False

    def can_undo(self) -> bool:
        return self.command_manager.can_undo()

    def can_redo(self) -> bool:
        return self.command_manager.can_redo()

    def select_file(self):
        self.file_operation_controller.select_file()

    def export_file(self):
        self.file_operation_controller.export_file()

    def deduplicate(self):
        self.function_button_controller.deduplicate()

    def spell_check(self):
        self.function_button_controller.spell_check()

    def correct_symbols(self):
        self.function_button_controller.correct_symbols()

    def smart_auto_process(self):
        self.function_button_controller.smart_auto_process()

    def show_analysis(self):
        self.function_button_controller.show_analysis()

    def show_help(self):
        self.function_button_controller.show_help()

    def show_support(self):
        self.function_button_controller.show_support()

    def sort_by_timestamp(self):
        """按时间戳排序"""
        if self.model.sort_by_timestamp():
            self.view.display_file_content(self.model.get_display_text())
            self.update_button_states()
        else:
            self.view.show_error(
                self.language_manager.get_text("no_timestamp_to_sort")
            )

    def reparse_from_editor(self):
        """使用编辑器中的文本重新解析为 LogEntry"""
        editor_content = self.view.text_display.get(1.0, tk.END).strip()
        if not editor_content:
            self.view.show_error(self.language_manager.get_text("no_content_to_reparse"))
            return
        self.model.reparse_entries(editor_content)

    def sync_model_with_editor_if_needed(self):
        """如果编辑器内容与模型显示文本不一致，则重新解析编辑器内容"""
        editor_content = self.view.text_display.get(1.0, tk.END).strip()
        model_display = self.model.get_display_text().strip()
        if editor_content != model_display:
            self.reparse_from_editor()

    def update_button_states(self):
        has_entries = len(self.model.entries) > 0
        editor_content = self.view.text_display.get(1.0, tk.END).strip()
        has_editor_content = bool(editor_content)

        if hasattr(self.view, 'buttons'):
            for button_key, button in self.view.buttons.items():
                if button_key not in ['smart_analysis', 'export', 'sort_by_timestamp', 'reparse']:
                    button.config(state=tk.NORMAL if has_entries else tk.DISABLED)

        if hasattr(self.view, 'buttons') and 'export' in self.view.buttons:
            self.view.buttons['export'].config(
                state=tk.NORMAL if has_editor_content else tk.DISABLED
            )

        if hasattr(self.view, 'buttons') and 'smart_analysis' in self.view.buttons:
            self.view.buttons['smart_analysis'].config(state=tk.NORMAL)

        if hasattr(self.view, 'buttons') and 'sort_by_timestamp' in self.view.buttons:
            has_timestamp = any(entry.timestamp for entry in self.model.entries)
            self.view.buttons['sort_by_timestamp'].config(
                state=tk.NORMAL if has_entries and has_timestamp else tk.DISABLED
            )

        if hasattr(self.view, 'buttons') and 'reparse' in self.view.buttons:
            self.view.buttons['reparse'].config(
                state=tk.NORMAL if has_editor_content else tk.DISABLED
            )

    def change_language(self, event):
        language_map = {
            "简体中文": "zh_CN",
            "繁体中文": "zh_TW",
            "English": "en",
            "日本語": "ja"
        }
        selected_language = self.view.language_var.get()
        language_code = language_map.get(selected_language, "zh_CN")

        self.language_manager = LanguageFactory.create_language(language_code)
        self.view.language_manager = self.language_manager
        self.view.update_ui_text()

    def previous_modification(self):
        pass

    def next_modification(self):
        pass
