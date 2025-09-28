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

        # 添加功能介绍内容
        content = f"""
{self.language_manager.get_text('function_intro')}文档
{'=' * 20}

主要功能按钮说明：

1. {self.language_manager.get_text('select_file')}
   - 支持导入 .docx, .doc, .txt 格式文件
   - 自动检测文件编码和语言

2. {self.language_manager.get_text('deduplicate')}
   - 去除重复的文本内容
   - 支持设置相似度阈值

3. {self.language_manager.get_text('spell_check')}
   - 自动检测和修正错别字
   - 支持多种语言拼写检查

4. {self.language_manager.get_text('correct_symbols')}
   - 补全句号、括号、双引号
   - 英文半角符号转中文全角符号

5. {self.language_manager.get_text('smart_auto_process')}
   - 组合执行上述所有处理功能
   - 一键完成文本优化

6. {self.language_manager.get_text('smart_analysis')}
   - 生成文本统计报告
   - 可视化数据分析图表

7. {self.language_manager.get_text('export')}
   - 支持导出为 .docx, .txt 格式
   - 保留文本格式和修改记录

更多功能开发中...
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

1. 点击"{self.language_manager.get_text('select_file')}"按钮导入文本文件
2. 根据需要选择处理功能：
   - 单独处理：点击对应功能按钮
   - 批量处理：点击"{self.language_manager.get_text('smart_auto_process')}"
3. 查看处理结果，文本会以审阅模式显示
4. 使用导航按钮查看具体修改位置
5. 满意后点击"{self.language_manager.get_text('export')}"保存结果

注意事项：

• 支持简体中文、繁体中文、英文、日文文本
• 处理时会自动跳过空行和时间字符串
• 导出功能支持多种格式选择
• 所有修改都有记录，可随时撤销

快捷键说明：

• Ctrl+O: 打开文件
• Ctrl+S: 保存文件
• F1: 显示帮助

更多功能开发中...
"""
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_about_tab(self, parent):
        """设置关于标签页"""
        about_text = f"""
文本处理工具 v1.0

这是一个多功能文本处理软件，支持：

• 多语言文本处理
• 智能文本优化
• 可视化数据分析
• 多种格式导入导出

开发团队：TODO
版本号：1.0.0
发布日期：2024年

技术支持：TODO
反馈邮箱：TODO

感谢使用本软件！
"""
        label = ttk.Label(parent, text=about_text, font=("Microsoft YaHei", 10), justify=tk.LEFT)
        label.pack(expand=True, padx=20, pady=20)