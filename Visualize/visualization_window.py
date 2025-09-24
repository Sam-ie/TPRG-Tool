# visualization_window.py
import tkinter as tk
from tkinter import ttk
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tempfile
import os
import webbrowser


class VisualizationWindow:
    def __init__(self, master, model):
        self.model = model
        self.lang_config = model.lang_config
        self.root = tk.Toplevel(master)
        self.root.title(self.lang_config.get('analyze_title', '文本分析'))
        self.root.geometry("1000x700")

        # 创建可视化工厂
        from visualization_factory import VisualizationFactory
        self.visualization_factory = VisualizationFactory(self.lang_config)

        self._create_layout()
        self._update_visualization()

    def _create_layout(self):
        """创建布局"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建标签控件用于显示图表
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 创建三个标签页
        self.tab_wordcloud = ttk.Frame(self.notebook)
        self.tab_stats = ttk.Frame(self.notebook)
        self.tab_network = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_wordcloud, text=self.lang_config.get('wordcloud_title', '词频统计'))
        self.notebook.add(self.tab_stats, text=self.lang_config.get('stats_title', '文本统计'))
        self.notebook.add(self.tab_network, text=self.lang_config.get('network_title', '文本网络'))

        # 在每个标签页中创建Web视图框架
        self._create_web_view(self.tab_wordcloud, "wordcloud")
        self._create_web_view(self.tab_stats, "stats")
        self._create_web_view(self.tab_network, "network")

        # 创建控制按钮框架
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        self.export_button = tk.Button(control_frame,
                                       text=self.lang_config.get('export', '导出图表'),
                                       command=self._export_charts)
        self.export_button.pack(side=tk.RIGHT, padx=5)

        self.refresh_button = tk.Button(control_frame,
                                        text=self.lang_config.get('refresh', '刷新'),
                                        command=self._update_visualization)
        self.refresh_button.pack(side=tk.RIGHT, padx=5)

    def _create_web_view(self, parent, chart_type):
        """创建Web视图用于显示Plotly图表"""
        # 由于tkinter无法直接显示Plotly图表，我们使用HTML文件并在浏览器中打开
        label = tk.Label(parent, text=f"{chart_type}图表将在浏览器中显示",
                         font=("Arial", 12))
        label.pack(expand=True)

    def _update_visualization(self):
        """更新可视化内容"""
        text = self.model.text_content
        if not text:
            return

        try:
            # 创建临时目录存储HTML文件
            temp_dir = tempfile.mkdtemp()

            # 生成词云图表
            wordcloud_fig = self.visualization_factory.create_wordcloud_chart(text)
            wordcloud_file = os.path.join(temp_dir, "wordcloud.html")
            pyo.plot(wordcloud_fig, filename=wordcloud_file, auto_open=False)

            # 生成统计图表
            stats_fig = self.visualization_factory.create_stats_chart(text)
            stats_file = os.path.join(temp_dir, "stats.html")
            pyo.plot(stats_fig, filename=stats_file, auto_open=False)

            # 生成网络图
            network_fig = self.visualization_factory.create_network_chart(text)
            network_file = os.path.join(temp_dir, "network.html")
            pyo.plot(network_fig, filename=network_file, auto_open=False)

            # 存储文件路径供导出使用
            self.chart_files = {
                'wordcloud': wordcloud_file,
                'stats': stats_file,
                'network': network_file
            }

            # 显示成功消息
            success_label = tk.Label(self.root, text="图表已生成，点击标签页名称查看对应图表",
                                     fg="green", font=("Arial", 10))
            success_label.pack(pady=5)

            # 绑定标签页切换事件
            self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        except Exception as e:
            error_label = tk.Label(self.root, text=f"生成图表时出错: {str(e)}",
                                   fg="red", font=("Arial", 10))
            error_label.pack(pady=5)

    def _on_tab_changed(self, event):
        """当标签页切换时在浏览器中打开对应图表"""
        try:
            tab_index = self.notebook.index(self.notebook.select())
            tab_names = ['wordcloud', 'stats', 'network']
            current_tab = tab_names[tab_index]

            if hasattr(self, 'chart_files') and current_tab in self.chart_files:
                # 在默认浏览器中打开HTML文件
                webbrowser.open('file://' + os.path.abspath(self.chart_files[current_tab]))
        except Exception as e:
            print(f"打开图表时出错: {e}")

    def _export_charts(self):
        """导出图表到指定目录"""
        try:
            from tkinter import filedialog
            export_dir = filedialog.askdirectory(title="选择导出目录")
            if export_dir:
                for chart_type, file_path in self.chart_files.items():
                    if os.path.exists(file_path):
                        import shutil
                        dest_path = os.path.join(export_dir, f"{chart_type}.html")
                        shutil.copy2(file_path, dest_path)

                # 显示成功消息
                tk.messagebox.showinfo("导出成功", f"图表已导出到: {export_dir}")
        except Exception as e:
            tk.messagebox.showerror("导出错误", f"导出图表时出错: {str(e)}")