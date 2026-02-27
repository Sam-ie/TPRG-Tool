import tkinter as tk
from controller.base_controller import BaseController


class TextEditController(BaseController):
    """文本编辑控制器 - 负责处理用户键盘输入和命令管理"""

    def __init__(self, main_controller):
        super().__init__(main_controller)
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

            # 绑定Backspace和Delete按键
            text_widget.bind('<KeyPress-BackSpace>', self._on_backspace_press)
            text_widget.bind('<KeyPress-Delete>', self._on_delete_press)

            # 绑定粘贴事件
            text_widget.bind('<<Paste>>', self._on_paste)

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
        if len(event.char) == 1 and event.char.isprintable():
            if not self.command_manager.current_insert_command:
                self.command_manager.start_insert_command()

            position = self.view.text_display.index(tk.INSERT)
            self.command_manager.add_insert_operation(position, event.char)

    def _on_enter_key(self, event):
        """Enter键释放事件"""
        self.command_manager.start_insert_command()
        position = self.view.text_display.index(tk.INSERT)
        self.command_manager.add_insert_operation(position, '\n')
        self.command_manager.commit_current_commands()
        self.main_controller.update_button_states()

    def _on_tab_key(self, event):
        """Tab键释放事件"""
        self.command_manager.start_insert_command()
        position = self.view.text_display.index(tk.INSERT)
        self.command_manager.add_insert_operation(position, '\t')
        self.command_manager.commit_current_commands()
        self.main_controller.update_button_states()

    def _on_backspace_press(self, event):
        """Backspace按键按下事件"""
        # 先检查是否有选中文本
        if self._handle_selection_delete(event):
            return "break"
        # 无选中，处理单个字符删除
        cursor_pos = self.view.text_display.index(tk.INSERT)
        if self.view.text_display.compare(cursor_pos, ">", "1.0"):
            prev_pos = self.view.text_display.index(f"{cursor_pos} - 1c")
            deleted_text = self.view.text_display.get(prev_pos, cursor_pos)

            if not self.command_manager.current_delete_command:
                self.command_manager.start_delete_command(is_backspace=True)

            self.command_manager.add_delete_operation(prev_pos, deleted_text, is_backspace=True)

    def _on_delete_press(self, event):
        """Delete按键按下事件"""
        # 先检查是否有选中文本
        if self._handle_selection_delete(event):
            return "break"
        # 无选中，处理单个字符删除
        cursor_pos = self.view.text_display.index(tk.INSERT)
        next_pos = self.view.text_display.index(f"{cursor_pos} + 1c")
        if self.view.text_display.compare(next_pos, "<=", "end-1c"):
            deleted_text = self.view.text_display.get(cursor_pos, next_pos)

            if not self.command_manager.current_delete_command:
                self.command_manager.start_delete_command(is_backspace=False)

            self.command_manager.add_delete_operation(cursor_pos, deleted_text, is_backspace=False)

    def _handle_selection_delete(self, event) -> bool:
        """处理选中文本的删除（Backspace/Delete）。返回True表示已处理，应阻止默认行为。"""
        text_widget = self.view.text_display
        try:
            # 检查是否有选中文本
            sel_start = text_widget.index(tk.SEL_FIRST)
            sel_end = text_widget.index(tk.SEL_LAST)
        except tk.TclError:
            # 没有选中文本
            return False

        # 有选中文本，提交当前可能正在进行的连续命令
        self.command_manager.commit_current_commands()

        # 记录被删除的文本和位置
        deleted_text = text_widget.get(sel_start, sel_end)

        # 开始新的删除命令
        self.command_manager.start_delete_command(is_backspace=False)  # is_backspace 无实际影响
        self.command_manager.add_delete_operation(sel_start, deleted_text, is_backspace=False)

        # 执行实际删除
        text_widget.delete(sel_start, sel_end)
        # 提交命令
        self.command_manager.commit_current_commands()
        return True

    def _on_paste(self, event):
        """粘贴事件处理"""
        text_widget = self.view.text_display
        # 提交当前正在进行的连续命令
        self.command_manager.commit_current_commands()

        # 获取剪贴板内容
        try:
            clipboard_text = text_widget.clipboard_get()
        except tk.TclError:
            # 剪贴板为空或无法获取
            return "break"

        # 检查是否有选中文本（粘贴会先删除选中内容）
        try:
            sel_start = text_widget.index(tk.SEL_FIRST)
            sel_end = text_widget.index(tk.SEL_LAST)
            has_selection = True
        except tk.TclError:
            has_selection = False
            sel_start = None

        if has_selection:
            # 先记录删除选中内容的操作
            deleted_text = text_widget.get(sel_start, sel_end)
            # 执行删除
            text_widget.delete(sel_start, sel_end)
            # 记录删除命令
            self.command_manager.start_delete_command(is_backspace=False)
            self.command_manager.add_delete_operation(sel_start, deleted_text, is_backspace=False)
            self.command_manager.commit_current_commands()

        # 获取插入位置（现在是原选中区域的起始位置，如果没有选中就是当前光标位置）
        insert_pos = text_widget.index(tk.INSERT)

        # 开始插入命令
        self.command_manager.start_insert_command()
        # 执行插入
        text_widget.insert(insert_pos, clipboard_text)
        # 记录插入操作（一次性记录整个粘贴文本）
        self.command_manager.add_insert_operation(insert_pos, clipboard_text)
        # 提交插入命令
        self.command_manager.commit_current_commands()

        # 阻止默认粘贴行为，因为已经手动处理
        return "break"

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
        if self.main_controller.undo():
            return "break"
        return None

    def _on_redo(self, event):
        """处理重做快捷键"""
        if self.main_controller.redo():
            return "break"
        return None

    def on_text_edited(self, content: str):
        """当文本被编辑时调用 - 手动编辑不更新模型，只更新按钮状态"""
        self.main_controller.update_button_states()
