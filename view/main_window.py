import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


class MainWindow(Observer):
    def __init__(self, root, controller, language_manager):
        self.root = root
        self.controller = controller
        self.language_manager = language_manager
        self.current_file_path = ""  # 保存当前文件路径

        # 设置通用字体
        self.setup_fonts()
        self.setup_ui()

    def setup_fonts(self):
        """设置通用字体"""
        # 尝试使用系统通用字体，确保清晰度
        self.default_font = ("Microsoft YaHei", 10)  # 微软雅黑，适合中文显示
        self.label_font = ("Microsoft YaHei", 9)  # 标签字体
        self.text_font = ("Consolas", 11)  # 等宽字体，适合代码和文本显示

        # 设置全局字体
        self.root.option_add("*Font", self.default_font)

    def setup_ui(self):
        self.root.title("文本处理工具")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)  # 设置最小大小为400x300
        self.update_ui_text()

        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧面板
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # 文件选择区域
        self.setup_file_selection(left_frame)

        # 处理按钮区域
        self.setup_processing_buttons(left_frame)

        # 右侧面板
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 顶部工具栏
        self.setup_toolbar(right_frame)

        # 文本显示区域
        self.setup_text_display(right_frame)

        # 底部导航
        self.setup_navigation(right_frame)

    def setup_file_selection(self, parent):
        self.file_frame = ttk.LabelFrame(parent, text=self.language_manager.get_text("file_selection"))
        self.file_frame.pack(fill=tk.X, pady=(0, 10))

        # 文件路径显示标签 - 使用Frame包装实现多行显示
        path_frame = ttk.Frame(self.file_frame)
        path_frame.pack(fill=tk.X, padx=5, pady=5)

        # 创建三行标签用于显示文件路径
        self.file_path_labels = []
        for i in range(3):
            label = ttk.Label(path_frame, text="", font=self.label_font)
            label.pack(anchor=tk.W)
            self.file_path_labels.append(label)

        # 选择文件按钮
        self.select_file_button = ttk.Button(
            self.file_frame,
            text=self.language_manager.get_text("select_file"),
            command=self.controller.select_file
        )
        self.select_file_button.pack(padx=5, pady=5)

    def setup_processing_buttons(self, parent):
        self.button_frame = ttk.LabelFrame(parent, text=self.language_manager.get_text("text_processing"))
        self.button_frame.pack(fill=tk.X)

        self.buttons = {}
        button_configs = [
            ("deduplicate", self.controller.deduplicate),
            ("spell_check", self.controller.spell_check),
            ("correct_symbols", self.controller.correct_symbols),
            ("smart_auto_process", self.controller.smart_auto_process),
            ("smart_analysis", self.controller.show_analysis),
            ("export", self.controller.export_file)
        ]

        for key, command in button_configs:
            btn = ttk.Button(self.button_frame, text=self.language_manager.get_text(key), command=command)
            btn.pack(fill=tk.X, padx=5, pady=2)
            self.buttons[key] = btn

    def setup_toolbar(self, parent):
        self.toolbar = ttk.Frame(parent)
        self.toolbar.pack(fill=tk.X, pady=(0, 10))

        # 语言选择标签 - 使用多语言支持
        self.language_label = ttk.Label(self.toolbar, text=self.language_manager.get_text("language_label"))
        self.language_label.pack(side=tk.LEFT, padx=(0, 5))

        # 语言选择下拉框 - 设置为只读模式
        self.language_var = tk.StringVar(value="简体中文")
        self.language_combo = ttk.Combobox(
            self.toolbar,
            textvariable=self.language_var,
            values=["简体中文", "繁体中文", "English", "日本語"],
            state="readonly",  # 设置为只读，用户不能输入文字
            width=12
        )
        self.language_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.language_combo.bind('<<ComboboxSelected>>', self.controller.change_language)

        # 右侧按钮区域
        self.right_buttons_frame = ttk.Frame(self.toolbar)
        self.right_buttons_frame.pack(side=tk.RIGHT)

        # 帮助按钮
        self.help_button = ttk.Button(
            self.right_buttons_frame,
            text=self.language_manager.get_text("help"),
            command=self.controller.show_help
        )
        self.help_button.pack(side=tk.LEFT, padx=(5, 5))

        # 支持作者按钮
        self.support_button = ttk.Button(
            self.right_buttons_frame,
            text=self.language_manager.get_text("support_author"),
            command=self.controller.show_support
        )
        self.support_button.pack(side=tk.LEFT)

    def setup_text_display(self, parent):
        self.text_frame = ttk.LabelFrame(parent, text=self.language_manager.get_text("document_content"))
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # 创建文本显示区域，使用等宽字体
        self.text_display = tk.Text(self.text_frame, wrap=tk.WORD, font=self.text_font)
        scrollbar = ttk.Scrollbar(self.text_frame, command=self.text_display.yview)
        self.text_display.config(yscrollcommand=scrollbar.set)

        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_navigation(self, parent):
        self.nav_frame = ttk.Frame(parent)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0))

        # 暂时禁用导航按钮
        self.prev_button = ttk.Button(self.nav_frame,
                                      text=self.language_manager.get_text("previous_modification"),
                                      command=self.controller.previous_modification,
                                      state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=(0, 5))

        self.next_button = ttk.Button(self.nav_frame,
                                      text=self.language_manager.get_text("next_modification"),
                                      command=self.controller.next_modification,
                                      state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT)

    def format_file_path(self, file_path: str) -> list:
        """格式化文件路径，返回三行文本列表"""
        if not file_path:
            return [self.language_manager.get_text("no_file_selected"), "", ""]

        # 如果路径长度小于等于90个字符，直接显示在一行
        if len(file_path) <= 90:
            lines = [file_path, "", ""]
        else:
            # 保留最后90个字符，前面加省略号
            truncated_path = "..." + file_path[-87:]
            # 每行最多30个字符
            lines = []
            for i in range(0, min(len(truncated_path), 90), 30):
                end_index = min(i + 30, len(truncated_path))
                lines.append(truncated_path[i:end_index])

            # 补足三行
            while len(lines) < 3:
                lines.append("")

        return lines

    def update_ui_text(self):
        """更新UI文本"""
        # 更新文件选择区域
        if hasattr(self, 'file_frame'):
            self.file_frame.config(text=self.language_manager.get_text("file_selection"))

            # 更新选择文件按钮文本
            if hasattr(self, 'select_file_button'):
                self.select_file_button.config(text=self.language_manager.get_text("select_file"))

            # 更新文件路径显示
            self.update_file_path_display()

        # 更新处理按钮区域
        if hasattr(self, 'button_frame'):
            self.button_frame.config(text=self.language_manager.get_text("text_processing"))

            for key, button in self.buttons.items():
                button.config(text=self.language_manager.get_text(key))

        # 更新工具栏文本
        if hasattr(self, 'language_label'):
            self.language_label.config(text=self.language_manager.get_text("language_label"))

        if hasattr(self, 'help_button'):
            self.help_button.config(text=self.language_manager.get_text("help"))

        if hasattr(self, 'support_button'):
            self.support_button.config(text=self.language_manager.get_text("support_author"))

        # 更新文本显示区域
        if hasattr(self, 'text_frame'):
            self.text_frame.config(text=self.language_manager.get_text("document_content"))

        # 更新导航按钮
        if hasattr(self, 'prev_button'):
            self.prev_button.config(text=self.language_manager.get_text("previous_modification"))
            self.next_button.config(text=self.language_manager.get_text("next_modification"))

    def set_file_path(self, file_path: str):
        """设置当前文件路径并更新显示"""
        self.current_file_path = file_path
        self.update_file_path_display()

    def update_file_path_display(self):
        """更新文件路径显示"""
        if hasattr(self, 'file_path_labels'):
            lines = self.format_file_path(self.current_file_path)
            for i, label in enumerate(self.file_path_labels):
                if i < len(lines):
                    label.config(text=lines[i])
                else:
                    label.config(text="")

    def update(self):
        """观察者更新方法"""
        # 当model发生变化时调用
        pass

    def show_error(self, message: str):
        messagebox.showerror(self.language_manager.get_text("error"), message)

    def show_info(self, message: str):
        messagebox.showinfo(self.language_manager.get_text("info"), message)