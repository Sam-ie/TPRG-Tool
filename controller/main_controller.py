import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional
import threading
import time

from model.document_model import DocumentModel
from model.commands import CommandManager
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

        # 命令管理器
        self.command_manager = CommandManager()

        # 注册观察者
        self.model.add_observer(self.view)

        # 进度窗口引用
        self.progress_window = None

        # 初始化FileManager
        self._update_file_manager()

        # 绑定键盘事件
        self._bind_keyboard_events()

    def _bind_keyboard_events(self):
        """绑定键盘事件"""
        if hasattr(self.view, 'text_display'):
            text_widget = self.view.text_display

            # 设置文本组件到命令管理器
            self.command_manager.set_text_widget(text_widget)

            # 启用Text组件的内置undo/redo功能用于正常输入
            text_widget.configure(undo=True)

            # 绑定普通按键（不中断连续操作）
            text_widget.bind('<KeyPress>', self._on_key_press)

            # 绑定Backspace和Delete按键（不中断连续操作）
            text_widget.bind('<KeyPress-BackSpace>', self._on_backspace_press)
            text_widget.bind('<KeyPress-Delete>', self._on_delete_press)

            # 绑定特殊按键（Enter和Tab作为独立操作）
            text_widget.bind('<KeyRelease-Return>', self._on_enter_key)
            text_widget.bind('<KeyRelease-Tab>', self._on_tab_key)

            # 绑定方向键（中断连续操作）
            text_widget.bind('<KeyPress-Up>', self._on_arrow_key)
            text_widget.bind('<KeyPress-Down>', self._on_arrow_key)
            text_widget.bind('<KeyPress-Left>', self._on_arrow_key)
            text_widget.bind('<KeyPress-Right>', self._on_arrow_key)
            text_widget.bind('<KeyPress-Prior>', self._on_arrow_key)  # Page Up
            text_widget.bind('<KeyPress-Next>', self._on_arrow_key)  # Page Down
            text_widget.bind('<KeyPress-Home>', self._on_arrow_key)
            text_widget.bind('<KeyPress-End>', self._on_arrow_key)

            # 绑定鼠标点击（中断连续操作）
            text_widget.bind('<Button-1>', self._on_mouse_click)
            text_widget.bind('<Button-2>', self._on_mouse_click)
            text_widget.bind('<Button-3>', self._on_mouse_click)

            # 绑定鼠标拖动选择（中断连续操作）
            text_widget.bind('<B1-Motion>', self._on_mouse_drag)

            # 绑定焦点事件（失去焦点时提交）
            text_widget.bind('<FocusOut>', self._on_focus_out)

            # 绑定撤销重做快捷键 - 由我们自己处理
            text_widget.bind('<Control-z>', self._on_undo)
            text_widget.bind('<Control-y>', self._on_redo)
            text_widget.bind('<Control-Z>', self._on_undo)
            text_widget.bind('<Control-Y>', self._on_redo)

    def _on_key_press(self, event):
        """普通按键按下事件"""
        # 不中断连续操作，只记录插入
        if len(event.char) == 1 and event.char.isprintable():
            # 开始新的插入命令（如果还没有的话）
            if not self.command_manager.current_insert_command:
                self.command_manager.start_insert_command()

            # 获取插入位置并添加操作
            position = self.view.text_display.index(tk.INSERT)
            self.command_manager.add_insert_operation(position, event.char)

            # 不阻止默认处理，让Text组件自动处理显示

    def _on_enter_key(self, event):
        """Enter键释放事件"""
        # Enter键作为独立操作，不与其他插入合并
        self.command_manager.start_insert_command()

        # 获取插入位置并添加操作
        position = self.view.text_display.index(tk.INSERT)
        self.command_manager.add_insert_operation(position, '\n')

        # 提交命令
        self.command_manager.commit_current_commands()

        # 不阻止默认处理，让Text组件自动处理显示

    def _on_tab_key(self, event):
        """Tab键释放事件"""
        # Tab键作为独立操作，不与其他插入合并
        self.command_manager.start_insert_command()

        # 获取插入位置并添加操作
        position = self.view.text_display.index(tk.INSERT)
        self.command_manager.add_insert_operation(position, '\t')

        # 提交命令
        self.command_manager.commit_current_commands()

        # 不阻止默认处理，让Text组件自动处理显示

    def _on_backspace_press(self, event):
        """Backspace按键按下事件"""
        # 不中断连续操作，只记录删除
        # 获取删除位置和被删除的文本
        cursor_pos = self.view.text_display.index(tk.INSERT)
        if self.view.text_display.compare(cursor_pos, ">", "1.0"):
            # 计算前一个字符的位置
            prev_pos = self.view.text_display.index(f"{cursor_pos} - 1c")
            deleted_text = self.view.text_display.get(prev_pos, cursor_pos)

            # 开始新的删除命令（如果还没有的话）
            if not self.command_manager.current_delete_command:
                self.command_manager.start_delete_command(is_backspace=True)

            # 添加删除操作
            self.command_manager.add_delete_operation(prev_pos, deleted_text, is_backspace=True)

            # 不阻止默认处理，让Text组件自动处理删除

    def _on_delete_press(self, event):
        """Delete按键按下事件"""
        # 不中断连续操作，只记录删除
        # 获取删除位置和被删除的文本
        cursor_pos = self.view.text_display.index(tk.INSERT)
        next_pos = self.view.text_display.index(f"{cursor_pos} + 1c")
        if self.view.text_display.compare(next_pos, "<=", "end-1c"):
            deleted_text = self.view.text_display.get(cursor_pos, next_pos)

            # 开始新的删除命令（如果还没有的话）
            if not self.command_manager.current_delete_command:
                self.command_manager.start_delete_command(is_backspace=False)

            # 添加删除操作
            self.command_manager.add_delete_operation(cursor_pos, deleted_text, is_backspace=False)

            # 不阻止默认处理，让Text组件自动处理删除

    def _on_arrow_key(self, event):
        """方向键按下事件 - 中断连续操作"""
        self.command_manager.interrupt_by_user_action()

    def _on_mouse_click(self, event):
        """鼠标点击事件 - 中断连续操作"""
        self.command_manager.interrupt_by_user_action()

    def _on_mouse_drag(self, event):
        """鼠标拖动选择事件 - 中断连续操作"""
        self.command_manager.interrupt_by_user_action()

    def _on_focus_out(self, event):
        """失去焦点事件 - 提交当前命令"""
        self.command_manager.commit_current_commands()

    def _on_undo(self, event):
        """处理撤销快捷键"""
        if self.undo():
            return "break"  # 阻止事件继续传播，避免Text组件处理
        return None

    def _on_redo(self, event):
        """处理重做快捷键"""
        if self.redo():
            return "break"  # 阻止事件继续传播，避免Text组件处理
        return None

    def on_text_edited(self, content: str):
        """当文本被编辑时调用"""
        # 更新模型的修改内容
        self.model.modified_content = content
        # 更新按钮状态
        self.update_button_states()

    def update_button_states(self):
        """更新按钮状态"""
        has_content = bool(self.model.original_content)
        has_modified_content = bool(self.model.modified_content)

        # 更新处理按钮状态
        if hasattr(self.view, 'buttons'):
            for button_key, button in self.view.buttons.items():
                if button_key not in ['smart_analysis', 'export']:
                    button.config(state=tk.NORMAL if has_content else tk.DISABLED)

        # 更新导出按钮状态
        if hasattr(self.view, 'buttons') and 'export' in self.view.buttons:
            self.view.buttons['export'].config(
                state=tk.NORMAL if has_modified_content else tk.DISABLED
            )

        # 智能分析按钮始终可用
        if hasattr(self.view, 'buttons') and 'smart_analysis' in self.view.buttons:
            self.view.buttons['smart_analysis'].config(state=tk.NORMAL)

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

    def undo(self):
        """撤销操作"""
        if self.command_manager.undo():
            # 更新模型内容
            content = self.view.text_display.get(1.0, tk.END).strip()
            self.model.modified_content = content
            return True
        return False

    def redo(self):
        """重做操作"""
        if self.command_manager.redo():
            # 更新模型内容
            content = self.view.text_display.get(1.0, tk.END).strip()
            self.model.modified_content = content
            return True
        return False

    def can_undo(self) -> bool:
        """检查是否可以撤销"""
        return self.command_manager.can_undo()

    def can_redo(self) -> bool:
        """检查是否可以重做"""
        return self.command_manager.can_redo()

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
