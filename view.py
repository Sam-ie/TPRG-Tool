# view.py
import tkinter as tk
from tkinter import ttk, messagebox
from observer import Observer


class GUIView(Observer):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.lang_config = None
        self._create_layout()
        self._bind_events()

    def _create_layout(self):
        # 创建左侧文件选择区域
        self.left_frame = ttk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建右侧文本展示区域
        self.right_frame = ttk.Frame(self.master)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建文件路径标签
        self.file_path_label = tk.Label(self.left_frame, justify=tk.LEFT, wraplength=200)
        self.file_path_label.pack(padx=5, pady=5)

        # 创建浏览按钮
        self.browse_button = tk.Button(self.left_frame, text="浏览文件")
        self.browse_button.pack(padx=5, pady=5)

        # 创建处理按钮
        self.process_buttons = {
            '去重': tk.Button(self.left_frame, text='去重'),
            '去错别字': tk.Button(self.left_frame, text='去错别字'),
            '修正符号': tk.Button(self.left_frame, text='修正符号')
        }

        for button in self.process_buttons.values():
            button.pack(padx=5, pady=2)
            button.config(state=tk.DISABLED)

        # 创建主文本区域
        self.text_area = tk.Text(self.right_frame, wrap='word', height=20, width=60)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建导航按钮框架
        self.nav_frame = ttk.Frame(self.right_frame)
        self.nav_frame.pack(fill=tk.X, padx=5, pady=5)

        # 创建导航按钮
        self.nav_buttons = {
            'prev': tk.Button(self.nav_frame, text='上一页'),
            'next': tk.Button(self.nav_frame, text='下一页')
        }

        self.nav_buttons['prev'].pack(side=tk.LEFT)
        self.nav_buttons['next'].pack(side=tk.RIGHT)

        # 创建可视化分析窗口引用
        self.visualization_window = None

    def _bind_events(self):
        # 绑定文件选择按钮
        self.browse_button.config(command=self._on_browse)
        # 绑定处理按钮
        for key, button in self.process_buttons.items():
            button.config(command=lambda op=key: self._on_process(op))

    def _on_browse(self):
        # 触发浏览文件事件
        if hasattr(self, 'controller'):
            self.controller.handle_browse()

    def _on_process(self, operation_type):
        # 触发处理事件
        if hasattr(self, 'controller'):
            self.controller.handle_process(operation_type)

    def update(self, model):
        self.lang_config = model.lang_config
        # 更新界面文本
        self._update_ui_text()
        # 更新文件路径显示
        self._update_file_paths(model)
        # 更新文本内容展示
        self._update_text_content(model)
        # 更新按钮状态
        self._update_button_state(model)

    def _update_ui_text(self):
        if not self.lang_config:
            return

        # 根据语言配置更新所有UI元素的文本
        self.browse_button.config(text=self.lang_config.get('browse', '浏览文件'))

        for key, button in self.process_buttons.items():
            button_text = self.lang_config.get(key.lower().replace(' ', '_'), key)
            button.config(text=button_text)

        # 更新导航按钮
        self.nav_buttons['prev'].config(text=self.lang_config.get('prev', '上一页'))
        self.nav_buttons['next'].config(text=self.lang_config.get('next', '下一页'))

    def _update_file_paths(self, model):
        # 更新文件路径显示
        if model.file_paths:
            self.file_path_label.config(text='\n'.join(model.file_paths))
        else:
            self.file_path_label.config(text=self.lang_config.get('no_files_selected', '未选择文件'))

    def _update_text_content(self, model):
        # 清空文本区域
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete('1.0', tk.END)

        # 插入处理后的文本
        if hasattr(model, 'processed_text') and model.processed_text:
            for line in model.processed_text:
                self.text_area.insert(tk.END, line + '\n')

        self.text_area.config(state=tk.DISABLED)

    def _update_button_state(self, model):
        # 根据文件状态更新按钮
        if model.file_paths:
            for button in self.process_buttons.values():
                button.config(state=tk.NORMAL)
        else:
            for button in self.process_buttons.values():
                button.config(state=tk.DISABLED)

    def set_controller(self, controller):
        self.controller = controller