# main_window.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from lang_manager import LangManager


class MainWindow:
    def __init__(self, master, model, controller):
        self.master = master
        self.model = model
        self.controller = controller
        self._create_layout()
        self._bind_events()

    def _create_layout(self):
        """创建布局"""
        # 设置窗口标题和大小
        self.master.title("文本处理与分析工具")
        self.master.geometry("1000x700")

        # 创建主框架
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建左侧框架（控制面板）
        self.left_frame = ttk.LabelFrame(main_frame, text="控制面板", width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.left_frame.pack_propagate(False)  # 固定宽度

        # 创建文件路径显示
        file_frame = ttk.Frame(self.left_frame)
        file_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(file_frame, text="已选文件:").pack(anchor=tk.W)
        self.file_path_label = tk.Label(file_frame, justify=tk.LEFT, wraplength=180,
                                        bg='white', relief=tk.SUNKEN, height=4)
        self.file_path_label.pack(fill=tk.X, pady=5)

        # 创建文件选择按钮
        self.browse_button = tk.Button(self.left_frame, text="浏览文件",
                                       bg='#4CAF50', fg='white', font=('Arial', 10))
        self.browse_button.pack(fill=tk.X, padx=5, pady=5)

        # 创建处理功能按钮框架
        process_frame = ttk.LabelFrame(self.left_frame, text="文本处理")
        process_frame.pack(fill=tk.X, padx=5, pady=5)

        self.process_buttons = {
            'deduplicate': tk.Button(process_frame, text='去重'),
            'correct_spelling': tk.Button(process_frame, text='去错别字'),
            'correct_punctuation': tk.Button(process_frame, text='修正符号'),
            'auto_process': tk.Button(process_frame, text='智能自动处理'),
            'analyze': tk.Button(process_frame, text='智能分析'),
            'export': tk.Button(process_frame, text='导出结果')
        }

        for button in self.process_buttons.values():
            button.pack(fill=tk.X, pady=2)
            button.config(state=tk.DISABLED)

        # 创建右侧框架（文本显示区域）
        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 创建顶部功能按钮框架
        self.top_right_frame = ttk.Frame(self.right_frame)
        self.top_right_frame.pack(fill=tk.X, pady=(0, 10))

        # 创建帮助按钮
        self.help_button = tk.Button(self.top_right_frame, text="帮助", width=8)
        self.help_button.pack(side=tk.LEFT, padx=2)

        # 创建语言切换按钮
        self.langswitch_button = tk.Button(self.top_right_frame, text="切换语言", width=10)
        self.langswitch_button.pack(side=tk.LEFT, padx=2)

        # 创建支持作者按钮
        self.donate_button = tk.Button(self.top_right_frame, text="支持作者", width=10)
        self.donate_button.pack(side=tk.LEFT, padx=2)

        # 创建文本区域框架
        text_frame = ttk.LabelFrame(self.right_frame, text="文本内容")
        text_frame.pack(fill=tk.BOTH, expand=True)

        # 创建文本区域和滚动条
        text_container = ttk.Frame(text_frame)
        text_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(text_container)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # 文本区域
        self.text_area = tk.Text(text_container, wrap=tk.WORD,
                                 yscrollcommand=v_scrollbar.set,
                                 xscrollcommand=h_scrollbar.set,
                                 font=('Arial', 11))
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 配置滚动条
        v_scrollbar.config(command=self.text_area.yview)
        h_scrollbar.config(command=self.text_area.xview)

        # 创建导航按钮框架
        self.navigation_frame = ttk.Frame(self.right_frame)
        self.navigation_frame.pack(fill=tk.X, pady=(10, 0))

        # 创建导航按钮
        self.prev_button = tk.Button(self.navigation_frame, text="上一页", width=10)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(self.navigation_frame, text="第 1 页")
        self.page_label.pack(side=tk.LEFT, expand=True)

        self.next_button = tk.Button(self.navigation_frame, text="下一页", width=10)
        self.next_button.pack(side=tk.RIGHT, padx=5)

        # 初始禁用导航按钮
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)

        # 更新界面文本
        self._update_ui_text()

    def _bind_events(self):
        """绑定事件"""
        # 绑定浏览按钮事件
        self.browse_button.config(command=self.controller.handle_browse)

        # 绑定处理按钮事件
        button_operations = {
            'deduplicate': '去重',
            'correct_spelling': '去错别字',
            'correct_punctuation': '修正符号',
            'auto_process': '智能自动处理',
            'analyze': '智能分析',
            'export': '导出结果'
        }

        for key, button in self.process_buttons.items():
            operation = button_operations[key]
            button.config(command=lambda op=operation: self.controller.handle_process(op))

        # 绑定语言切换按钮事件
        self.langswitch_button.config(command=self._switch_language)

        # 绑定帮助按钮事件
        self.help_button.config(command=self._show_help)

        # 绑定支持作者按钮事件
        self.donate_button.config(command=self._show_donate_info)

    def _switch_language(self):
        """切换语言"""
        # 简单的语言切换逻辑（中英文切换）
        current_lang = self.model.lang_config.get('_current_lang', 'zh-cn')
        new_lang = 'en' if current_lang == 'zh-cn' else 'zh-cn'
        self.controller.handle_lang_switch(new_lang)

    def _show_help(self):
        """显示帮助信息"""
        messagebox.showinfo("帮助",
                            "文本处理与分析工具使用说明：\n\n"
                            "1. 点击'浏览文件'选择要处理的文本文件\n"
                            "2. 选择相应的处理功能\n"
                            "3. 查看处理结果并导出")

    def _show_donate_info(self):
        """显示支持信息"""
        messagebox.showinfo("支持作者",
                            "如果这个工具对您有帮助，请考虑支持作者。\n\n"
                            "感谢您的使用！")

    def _update_ui_text(self):
        """根据语言配置更新界面文本"""
        config = self.model.lang_config

        # 更新按钮文本
        self.browse_button.config(text=config.get('browse', '浏览文件'))
        self.help_button.config(text=config.get('help', '帮助'))
        self.langswitch_button.config(text=config.get('switch_language', '切换语言'))
        self.donate_button.config(text=config.get('donate', '支持作者'))
        self.prev_button.config(text=config.get('prev', '上一页'))
        self.next_button.config(text=config.get('next', '下一页'))

        # 更新处理按钮文本
        button_texts = {
            'deduplicate': 'deduplicate',
            'correct_spelling': 'correct_spelling',
            'correct_punctuation': 'correct_punctuation',
            'auto_process': 'auto_process',
            'analyze': 'analyze',
            'export': 'export'
        }

        for key, button in self.process_buttons.items():
            text_key = button_texts[key]
            button.config(text=config.get(text_key, key))

    def update_file_display(self, file_paths):
        """更新文件路径显示"""
        if file_paths:
            file_text = "\n".join([os.path.basename(path) for path in file_paths])
            self.file_path_label.config(text=file_text)
        else:
            self.file_path_label.config(text=self.model.lang_config.get('no_files_selected', '未选择文件'))

    def update_text_display(self, text_content):
        """更新文本内容显示"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete('1.0', tk.END)

        if text_content:
            for line in text_content:
                self.text_area.insert(tk.END, line + '\n')

        self.text_area.config(state=tk.NORMAL)  # 保持可编辑以便复制

    def update_button_states(self, has_files):
        """更新按钮状态"""
        state = tk.NORMAL if has_files else tk.DISABLED
        for button in self.process_buttons.values():
            button.config(state=state)