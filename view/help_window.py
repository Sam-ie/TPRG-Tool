import tkinter as tk
from tkinter import ttk


class HelpWindow:
    def __init__(self, parent, language_manager):
        self.window = tk.Toplevel(parent)
        self.language_manager = language_manager
        self.setup_ui()

    def setup_ui(self):
        self.window.title(self.language_manager.get_text("help_window_title"))
        self.window.geometry("600x500")

        # 主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 使用Notebook实现标签页
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # 功能介绍标签页
        functions_frame = ttk.Frame(notebook)
        notebook.add(functions_frame, text=self.language_manager.get_text("function_intro"))
        self.setup_functions_tab(functions_frame)

        # 使用说明标签页
        usage_frame = ttk.Frame(notebook)
        notebook.add(usage_frame, text=self.language_manager.get_text("usage_instructions"))
        self.setup_usage_tab(usage_frame)

        # 关于标签页
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text=self.language_manager.get_text("about"))
        self.setup_about_tab(about_frame)

    def setup_functions_tab(self, parent):
        """设置功能介绍标签页"""
        # 创建滚动文本框
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        # 功能介绍内容（根据当前功能更新）
        content = f"""
{self.language_manager.get_text('function_intro')}
{'=' * 20}

主要功能说明：

1. 【按时间戳排序】
   • 将多个团的日志混合在一起时，自动按时间顺序整理
   • 帮助海豹骰整合多群信息，方便回顾

2. 【去重】
   • 去除因骰娘不能识别撤回等原因产生的重复内容
   • 可调节相似度阈值，智能识别近似重复行

3. 【错别字修正】
   • 自动修正常见错别字（支持简中、繁中、英文）
   • 解决pl发错别字，结团后忘记修改的问题

4. 【符号修正】
   • 自动补全句末缺失的句号
   • 修正左右引号颠倒、引号配对错误
   • 统一中英文标点格式

5. 【智能自动处理】
   • 一键执行去重、错别字修正、符号修正
   • 快速优化整个文档

6. 【统计分析】
   • 字数统计：中文字符、英文字母、数字、标点等
   • 平均RP长度：计算平均每行字符数
   • 词云分析：根据文档语言智能生成词云（中文/英文/日文）
   • 标点符号使用统计

7. 【多格式导入导出】
   • 支持从 .txt、.doc、.docx 文件导入
   • 支持直接复制QQ聊天内容到编辑器
   • 可导出为 .txt 或 .docx 格式

8. 【多语言界面】
   • 支持简体中文、繁体中文、英文、日文
   • 一键切换界面语言

更多功能持续开发中...
"""
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_usage_tab(self, parent):
        """设置使用说明标签页"""
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        content = f"""
{self.language_manager.get_text('usage_instructions')}
{'=' * 10}

基本操作流程：

1. 导入文本
   • 点击“选择文件”按钮，导入 .txt/.doc/.docx 文件
   • 或直接将聊天记录复制粘贴到编辑器中

2. 调整顺序（可选）
   • 点击“按时间戳排序”按钮，自动将多个团的日志按时间整理

3. 处理文本
   • 单独处理：点击“去重”、“错别字修正”、“符号修正”分别执行
   • 批量处理：点击“智能自动处理”一键完成所有优化

4. 查看分析
   • 点击“智能分析”打开分析窗口，查看字数统计、词云、标点统计
   • 词云支持中/英/日文，自动过滤停用词和无意义字符

5. 导出结果
   • 点击“导出”按钮，默认以“文本处理记录.txt”为名保存
   • 若重名自动添加编号，可另选 .docx 格式

注意事项：

• 时间戳排序需文本中包含标准时间格式（如 2023-01-01 12:34:56）
如果时间缺损，如缺失日期，或跨年的记录缺失年份，可能导致排序错误，遇到这种情况请分日期或年份分别导入
• 错别字修正依赖百万级语料库，修正时间较长（200字/秒），请耐心等待
• 文本框中的修改支持撤销/重做（Ctrl+Z / Ctrl+Y）

快捷键：

• Ctrl+Z: 撤销
• Ctrl+Y: 重做
• F1: 显示帮助

更多使用技巧请关注后续版本。
"""
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_about_tab(self, parent):
        """设置关于标签页"""
        about_text = f"""
文本处理工具 v1.0

一款专为跑团日志优化设计的文本处理软件。

主要特点：
• 智能去重、错别字修正、符号补全
• 多团日志按时间戳自动排序
• 支持简中/繁中/英文/日文界面
• 词云与字数统计可视化分析
• 直接复制粘贴或导入 txt/doc/docx

开发者：小雨
版本号：1.0.0
发布日期：2026年

感谢使用！您的支持是持续改进的动力。
"""
        label = ttk.Label(parent, text=about_text, font=("Microsoft YaHei", 10), justify=tk.LEFT)
        label.pack(expand=True, padx=20, pady=20)