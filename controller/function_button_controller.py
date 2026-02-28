import threading
import tkinter as tk
from view.analysis_window import AnalysisWindow
from view.help_window import HelpWindow
from view.support_window import SupportWindow
from view.progress_window import ProgressWindow


class FunctionButtonController:
    """功能按钮控制器"""

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.progress_window = None
        self._cancel_event = None  # 用于取消长时间操作

    def deduplicate(self):
        """去重功能"""
        self.main_controller.sync_model_with_editor_if_needed()
        success, message_key = self.main_controller.model.process_text('deduplicate')
        if not success:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text(message_key)
            )
        else:
            self.main_controller.view.display_file_content(
                self.main_controller.model.get_display_text()
            )

    def spell_check(self):
        """错别字修正（带进度条）"""
        self.main_controller.sync_model_with_editor_if_needed()
        if not self.main_controller.model.entries:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text("please_load_file_first")
            )
            return

        # 创建取消事件
        self._cancel_event = threading.Event()

        # 创建进度窗口
        self.progress_window = ProgressWindow(
            self.main_controller.root,
            self.main_controller.language_manager,
            self.main_controller.language_manager.get_text("spell_check") + "...",
            100
        )
        # 绑定关闭事件到取消方法
        self.progress_window.set_cancel_callback(self._cancel_processing)

        def run():
            def progress_cb(current, total, status):
                # 检查窗口是否仍然有效，如果无效则设置取消事件
                if self.progress_window is None or not self.progress_window.window.winfo_exists():
                    self._cancel_event.set()
                    return
                # 更新进度
                self.main_controller.root.after(
                    0, self.progress_window.update_progress, current, total, status
                )

            # 定义停止检查函数
            def stop_check():
                return self._cancel_event.is_set()

            success, message_key = self.main_controller.model.process_text(
                'spell_check', progress_cb, stop_check
            )
            self.main_controller.root.after(0, self._finish_processing, success, message_key)

        threading.Thread(target=run, daemon=True).start()

    def correct_symbols(self):
        """符号修正"""
        self.main_controller.sync_model_with_editor_if_needed()
        success, message_key = self.main_controller.model.process_text('correct_symbols')
        if not success:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text(message_key)
            )
        else:
            self.main_controller.view.display_file_content(
                self.main_controller.model.get_display_text()
            )

    def smart_auto_process(self):
        """智能自动处理（带进度条）"""
        self.main_controller.sync_model_with_editor_if_needed()
        if not self.main_controller.model.entries:
            self.main_controller.view.show_error(
                self.main_controller.language_manager.get_text("please_load_file_first")
            )
            return

        self._cancel_event = threading.Event()

        self.progress_window = ProgressWindow(
            self.main_controller.root,
            self.main_controller.language_manager,
            self.main_controller.language_manager.get_text("smart_auto_process") + "...",
            100
        )
        self.progress_window.set_cancel_callback(self._cancel_processing)

        def run():
            def progress_cb(current, total, status):
                if self.progress_window is None or not self.progress_window.window.winfo_exists():
                    self._cancel_event.set()
                    return
                self.main_controller.root.after(
                    0, self.progress_window.update_progress, current, total, status
                )

            def stop_check():
                return self._cancel_event.is_set()

            success, message_key = self.main_controller.model.smart_auto_process(progress_cb, stop_check)
            self.main_controller.root.after(0, self._finish_processing, success, message_key)

        threading.Thread(target=run, daemon=True).start()

    def _cancel_processing(self):
        """取消处理（由进度窗口关闭时调用）"""
        if self._cancel_event:
            self._cancel_event.set()

    def _finish_processing(self, success, message_key):
        """处理完成后的回调（在主线程中执行）"""
        # 清理取消事件
        self._cancel_event = None

        # 如果进度窗口还存在，则更新或关闭它
        if self.progress_window is not None:
            try:
                if self.progress_window.window.winfo_exists():
                    if success:
                        self.progress_window.complete(
                            self.main_controller.language_manager.get_text("process_completed")
                        )
                    else:
                        self.progress_window.close()
                        self.main_controller.view.show_error(
                            self.main_controller.language_manager.get_text(message_key)
                        )
                else:
                    self.progress_window = None
            except tk.TclError:
                self.progress_window = None

        self.progress_window = None

        # 无论窗口是否存在，都要刷新视图（模型已更新）
        self.main_controller.view.display_file_content(
            self.main_controller.model.get_display_text()
        )
        self.main_controller.update_button_states()

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
