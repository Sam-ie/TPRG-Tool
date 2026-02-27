from view.analysis_window import AnalysisWindow
from view.help_window import HelpWindow
from view.support_window import SupportWindow


class FunctionButtonController:
    """功能按钮控制器"""

    def __init__(self, main_controller):
        self.main_controller = main_controller

    def deduplicate(self):
        """去重功能"""
        self.main_controller.sync_model_with_editor_if_needed()
        success, message_key = self.main_controller.model.process_text('deduplicate')
        if not success:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text(message_key)
            )

    def spell_check(self):
        """错别字修正"""
        self.main_controller.sync_model_with_editor_if_needed()
        success, message_key = self.main_controller.model.process_text('spell_check')
        if not success:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text(message_key)
            )

    def correct_symbols(self):
        """符号修正"""
        self.main_controller.sync_model_with_editor_if_needed()
        success, message_key = self.main_controller.model.process_text('correct_symbols')
        if not success:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text(message_key)
            )

    def smart_auto_process(self):
        """智能自动处理"""
        self.main_controller.sync_model_with_editor_if_needed()
        success, message_key = self.main_controller.model.smart_auto_process()
        if not success:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text(message_key)
            )

    def show_analysis(self):
        """显示智能分析窗口"""
        AnalysisWindow(
            self.main_controller.view.root,
            self.main_controller,
            self.main_controller.language_manager
        )

    def show_help(self):
        """显示帮助窗口"""
        HelpWindow(self.main_controller.view.root, self.main_controller.language_manager)

    def show_support(self):
        """显示支持作者窗口"""
        SupportWindow(self.main_controller.view.root, self.main_controller.language_manager)
