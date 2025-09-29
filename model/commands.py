from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    """命令基类"""

    @abstractmethod
    def execute(self) -> bool:
        """执行命令（正常输入时不修改文本，只记录）"""
        pass

    @abstractmethod
    def undo(self) -> bool:
        """撤销命令（实际修改文本）"""
        pass

    @abstractmethod
    def redo(self) -> bool:
        """重做命令（实际修改文本）"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """获取命令描述"""
        pass


class InsertTextCommand(Command):
    """插入文本命令 - 支持合并连续的插入操作"""

    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.insert_operations = []  # 存储连续的插入操作

    def add_insertion(self, position: str, text: str):
        """添加一个插入操作"""
        self.insert_operations.append({
            'position': position,
            'text': text
        })

    def execute(self) -> bool:
        """执行所有插入操作（正常输入时不修改文本，只记录）"""
        # 打印插入的字符串
        if self.insert_operations:
            all_text = ''.join(op['text'] for op in self.insert_operations)
            print(f"[插入] '{self._escape_text(all_text)}'")
        return True

    def undo(self) -> bool:
        """撤销所有插入操作（实际删除文本）"""
        try:
            # 打印撤销插入的字符串
            if self.insert_operations:
                all_text = ''.join(op['text'] for op in self.insert_operations)
                print(f"[撤销插入] '{self._escape_text(all_text)}'")

            # 从后往前撤销
            for op in reversed(self.insert_operations):
                start_index = self.text_widget.index(op['position'])
                end_index = self.text_widget.index(f"{start_index}+{len(op['text'])}c")
                self.text_widget.delete(start_index, end_index)

            return True
        except Exception as e:
            print(f"InsertTextCommand撤销失败: {e}")
            return False

    def redo(self) -> bool:
        """重做所有插入操作（实际插入文本）"""
        try:
            # 打印重做插入的字符串
            if self.insert_operations:
                all_text = ''.join(op['text'] for op in self.insert_operations)
                print(f"[重做插入] '{self._escape_text(all_text)}'")

            for op in self.insert_operations:
                self.text_widget.insert(op['position'], op['text'])

            return True
        except Exception as e:
            print(f"InsertTextCommand重做失败: {e}")
            return False

    def _escape_text(self, text: str) -> str:
        """转义特殊字符以便在控制台显示"""
        # 替换特殊字符为可读形式
        escaped = text.replace('\n', '\\n')
        escaped = escaped.replace('\t', '\\t')
        escaped = escaped.replace('\r', '\\r')
        return escaped

    def get_description(self) -> str:
        if not self.insert_operations:
            return "空插入命令"

        total_chars = sum(len(op['text']) for op in self.insert_operations)

        # 检查特殊字符
        special_chars = []
        for op in self.insert_operations:
            if '\n' in op['text']:
                special_chars.append("回车")
            if '\t' in op['text']:
                special_chars.append("制表符")

        desc = f"插入: {total_chars}个字符 ({len(self.insert_operations)}次操作)"
        if special_chars:
            desc += f" [包含: {', '.join(set(special_chars))}]"

        return desc

    def is_empty(self) -> bool:
        """检查命令是否为空"""
        return len(self.insert_operations) == 0


class DeleteTextCommand(Command):
    """删除文本命令 - 支持合并连续的删除操作"""

    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.delete_operations = []  # 存储连续的删除操作

    def add_deletion(self, position: str, deleted_text: str, is_backspace: bool = False):
        """添加一个删除操作"""
        self.delete_operations.append({
            'position': position,
            'deleted_text': deleted_text,
            'is_backspace': is_backspace
        })

    def execute(self) -> bool:
        """执行所有删除操作（正常输入时不修改文本，只记录）"""
        # 打印删除的字符串
        if self.delete_operations:
            all_text = ''.join(op['deleted_text'] for op in self.delete_operations)
            operation_type = "Backspace" if self.delete_operations[0]['is_backspace'] else "Delete"
            print(f"[{operation_type}] '{self._escape_text(all_text)}'")
        return True

    def undo(self) -> bool:
        """撤销所有删除操作（实际插入被删除的文本）"""
        try:
            # 打印撤销删除的字符串
            if self.delete_operations:
                all_text = ''.join(op['deleted_text'] for op in self.delete_operations)
                print(f"[撤销删除] '{self._escape_text(all_text)}'")

            # 按照删除的逆序插入文本
            for op in reversed(self.delete_operations):
                if op['is_backspace']:
                    # Backspace删除：在删除位置插入（删除位置就是插入位置）
                    self.text_widget.insert(op['position'], op['deleted_text'])
                else:
                    # Delete删除：在删除位置插入
                    self.text_widget.insert(op['position'], op['deleted_text'])

            return True
        except Exception as e:
            print(f"DeleteTextCommand撤销失败: {e}")
            return False

    def redo(self) -> bool:
        """重做所有删除操作（实际删除文本）"""
        try:
            # 打印重做删除的字符串
            if self.delete_operations:
                all_text = ''.join(op['deleted_text'] for op in self.delete_operations)
                operation_type = "Backspace" if self.delete_operations[0]['is_backspace'] else "Delete"
                print(f"[重做{operation_type}] '{self._escape_text(all_text)}'")

            for op in self.delete_operations:
                start_index = self.text_widget.index(op['position'])
                end_index = self.text_widget.index(f"{start_index}+{len(op['deleted_text'])}c")
                self.text_widget.delete(start_index, end_index)

            return True
        except Exception as e:
            print(f"DeleteTextCommand重做失败: {e}")
            return False

    def _escape_text(self, text: str) -> str:
        """转义特殊字符以便在控制台显示"""
        # 替换特殊字符为可读形式
        escaped = text.replace('\n', '\\n')
        escaped = escaped.replace('\t', '\\t')
        escaped = escaped.replace('\r', '\\r')
        return escaped

    def get_description(self) -> str:
        if not self.delete_operations:
            return "空删除命令"

        total_chars = sum(len(op['deleted_text']) for op in self.delete_operations)
        has_backspace = any(op['is_backspace'] for op in self.delete_operations)
        has_delete = any(not op['is_backspace'] for op in self.delete_operations)

        if has_backspace and has_delete:
            operation_type = "Backspace/Delete混合"
        elif has_backspace:
            operation_type = "Backspace"
        else:
            operation_type = "Delete"

        # 检查特殊字符
        special_chars = []
        for op in self.delete_operations:
            if '\n' in op['deleted_text']:
                special_chars.append("回车")
            if '\t' in op['deleted_text']:
                special_chars.append("制表符")

        desc = f"{operation_type}删除: {total_chars}个字符 ({len(self.delete_operations)}次操作)"
        if special_chars:
            desc += f" [包含: {', '.join(set(special_chars))}]"

        return desc

    def is_empty(self) -> bool:
        """检查命令是否为空"""
        return len(self.delete_operations) == 0


class CommandManager:
    """命令管理器"""

    def __init__(self, max_history_size=100):
        self.undo_stack = []
        self.redo_stack = []
        self.max_history_size = max_history_size

        # 当前未提交的命令
        self.current_insert_command = None
        self.current_delete_command = None
        self.text_widget = None

    def set_text_widget(self, text_widget):
        """设置文本组件"""
        self.text_widget = text_widget

    def start_insert_command(self):
        """开始新的插入命令"""
        self.commit_current_commands()
        if self.text_widget:
            self.current_insert_command = InsertTextCommand(self.text_widget)

    def add_insert_operation(self, position: str, text: str):
        """添加插入操作"""
        if not self.current_insert_command and self.text_widget:
            self.current_insert_command = InsertTextCommand(self.text_widget)

        if self.current_insert_command:
            self.current_insert_command.add_insertion(position, text)

    def start_delete_command(self, is_backspace: bool = False):
        """开始新的删除命令"""
        self.commit_current_commands()
        if self.text_widget:
            self.current_delete_command = DeleteTextCommand(self.text_widget)

    def add_delete_operation(self, position: str, deleted_text: str, is_backspace: bool = False):
        """添加删除操作"""
        if not self.current_delete_command and self.text_widget:
            self.current_delete_command = DeleteTextCommand(self.text_widget)

        if self.current_delete_command:
            self.current_delete_command.add_deletion(position, deleted_text, is_backspace)

    def commit_current_commands(self):
        """提交当前未完成的命令"""
        commands_committed = False

        if self.current_insert_command and not self.current_insert_command.is_empty():
            # 正常输入时不修改文本，只记录命令
            self.add_command(self.current_insert_command)
            commands_committed = True

        if self.current_delete_command and not self.current_delete_command.is_empty():
            # 正常输入时不修改文本，只记录命令
            self.add_command(self.current_delete_command)
            commands_committed = True

        self.current_insert_command = None
        self.current_delete_command = None

        return commands_committed

    def _escape_text(self, text: str) -> str:
        """转义特殊字符以便在控制台显示"""
        escaped = text.replace('\n', '\\n')
        escaped = escaped.replace('\t', '\\t')
        escaped = escaped.replace('\r', '\\r')
        return escaped

    def add_command(self, command: Command) -> bool:
        """添加命令到历史记录（正常输入时不修改文本）"""
        if command.execute():  # 只记录，不修改文本
            self.undo_stack.append(command)
            # 清空重做栈
            self.redo_stack.clear()
            # 限制历史记录大小
            if len(self.undo_stack) > self.max_history_size:
                self.undo_stack.pop(0)
            return True
        return False

    def interrupt_by_user_action(self):
        """用户主动中断连续操作（鼠标点击、方向键等）"""
        return self.commit_current_commands()

    def undo(self) -> bool:
        """撤销上一个命令（实际修改文本）"""
        # 先提交当前未完成的命令
        self.commit_current_commands()

        if self.undo_stack:
            command = self.undo_stack.pop()
            if command.undo():  # 实际修改文本
                self.redo_stack.append(command)
                return True
        return False

    def redo(self) -> bool:
        """重做上一个撤销的命令（实际修改文本）"""
        if self.redo_stack:
            command = self.redo_stack.pop()
            if command.redo():  # 实际修改文本
                self.undo_stack.append(command)
                return True
        return False

    def can_undo(self) -> bool:
        """检查是否可以撤销"""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """检查是否可以重做"""
        return len(self.redo_stack) > 0

    def clear_history(self):
        """清空命令历史"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.current_insert_command = None
        self.current_delete_command = None

    def get_undo_description(self) -> str:
        """获取下一个撤销操作的描述"""
        if self.undo_stack:
            return self.undo_stack[-1].get_description()
        return ""

    def get_redo_description(self) -> str:
        """获取下一个重做操作的描述"""
        if self.redo_stack:
            return self.redo_stack[-1].get_description()
        return ""