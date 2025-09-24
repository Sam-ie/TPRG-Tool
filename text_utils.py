# text_utils.py
import tkinter as tk
import re


class TextUtils:
    @staticmethod
    def apply_highlights(text_widget, processed_text, correction_map=None):
        """应用高亮和标记"""
        if correction_map is None:
            correction_map = {}

        text_widget.config(state=tk.NORMAL)
        text_widget.delete('1.0', tk.END)

        # 定义标记样式
        text_widget.tag_config('duplicate', background='#fffacd')  # 重复行背景色
        text_widget.tag_config('error', foreground='#ff0000')  # 错误文本红色
        text_widget.tag_config('correction', foreground='#008000')  # 修正文本绿色
        text_widget.tag_config('highlight', background='#ffffe0')  # 高亮背景

        # 插入文本并应用标记
        for i, line in enumerate(processed_text):
            # 检查是否为重复行
            if line.startswith("【重复】"):
                text_widget.insert(tk.END, line + '\n', 'duplicate')
            # 检查是否有修正信息
            elif i in correction_map:
                errors = correction_map[i]
                # 应用错误标记（简化处理）
                text_widget.insert(tk.END, line + '\n', 'correction')
            else:
                text_widget.insert(tk.END, line + '\n')

        text_widget.config(state=tk.NORMAL)

    @staticmethod
    def find_and_highlight_errors(text_widget, pattern, tag_name):
        """查找并高亮特定模式的文本"""
        text = text_widget.get('1.0', tk.END)

        # 清除现有标记
        text_widget.tag_remove(tag_name, '1.0', tk.END)

        # 查找匹配项并添加标记
        matches = list(re.finditer(pattern, text))
        for match in matches:
            start_pos = f"1.0+{match.start()}c"
            end_pos = f"1.0+{match.end()}c"
            text_widget.tag_add(tag_name, start_pos, end_pos)

    @staticmethod
    def setup_text_tags(text_widget):
        """设置文本标记样式"""
        # 错误标记（红色）
        text_widget.tag_config("error", foreground="red", background="#ffe6e6")

        # 警告标记（橙色）
        text_widget.tag_config("warning", foreground="orange", background="#fff0e6")

        # 成功标记（绿色）
        text_widget.tag_config("success", foreground="green", background="#e6ffe6")

        # 重复内容标记
        text_widget.tag_config("duplicate", background="#f0f0f0", relief="ridge")

        # 选中行高亮
        text_widget.tag_config("current_line", background="#e6f3ff")