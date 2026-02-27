import tkinter as tk
from tkinter import ttk
import re
from collections import Counter

# 尝试导入词云相关库，若缺失则降级显示提示
try:
    import jieba
    from wordcloud import WordCloud
    from PIL import Image, ImageTk
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    jieba = None


class AnalysisWindow:
    def __init__(self, parent, controller, language_manager):
        self.window = tk.Toplevel(parent)
        self.controller = controller
        self.language_manager = language_manager

        # 窗口尺寸定义
        self.normal_geometry = "400x300"
        self.expanded_geometry = "900x700"

        # 从模型中获取所有 LogEntry 的 content，合并为完整文本
        model = self.controller.model
        self.entries = model.entries if hasattr(model, 'entries') else []
        self.full_content = "\n".join([entry.content for entry in self.entries if entry.content.strip()])

        # 文档语言（由模型检测）
        self.detected_language = getattr(model, 'detected_language', 'zh_CN')

        # 中文停用词
        self.stopwords = {
            '的', '了', '在', '是', '我', '你', '他', '她', '它', '我们', '你们', '他们',
            '这个', '那个', '这些', '那些', '和', '与', '或', '就', '都', '而', '而且',
            '但是', '不过', '因为', '所以', '如果', '那么', '虽然', '然而', '着', '过',
            '把', '被', '让', '给', '对', '对于', '关于', '由于', '除了', '之外', '等',
            '没有', '还是', '不能', '可以', '一下', '它们', '仿佛', '似乎', '如同', '像是',
            '可能', '开始', '再见', '看看', '进行', '查看', '一点', '回合', '她们', '突然',
            '如何', '什么', '一个', '自己', '这里', '出来', '现在', '已经', '时间', '故事',
            '东西', '设置', '玩家', '游戏', '日志', '记录', '检定', '理智', '侦查', '聆听',
            '看见', '发现', '一声', '一块', '看起来', '一只', '一条', '结果', '成功', '失败'
        }

        # 英文停用词
        self.english_stopwords = {
            'a', 'about', 'against', 'all', 'an', 'and', 'any', 'are', 'at', 'be',
            'been', 'being', 'both', 'but', 'by', 'can', 'don', 'each', 'else', 'end',
            'few', 'for', 'game', 'he', 'her', 'hers', 'him', 'his', 'how', 'hp', 'i',
            'if', 'in', 'into', 'is', 'it', 'its', 'join', 'just', 'log', 'me', 'mine',
            'more', 'most', 'mp', 'my', 'new', 'nn', 'no', 'nor', 'not', 'now', 'off',
            'on', 'only', 'or', 'other', 'our', 'ours', 'sc', 'set', 'should', 'so',
            'some', 'st', 'such', 't', 'than', 'that', 'the', 'their', 'theirs', 'them',
            'then', 'there', 'these', 'they', 'this', 'those', 'to', 'too', 'us', 'very',
            'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who',
            'whom', 'why', 'will', 'with', 'you', 'your', 'yours'
        }

        self.setup_ui()
        self._bind_events()

    def setup_ui(self):
        self.window.title(self.language_manager.get_text("analysis_window_title"))
        self.window.geometry(self.normal_geometry)  # 初始大小

        # 主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 使用Notebook实现标签页
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 字数统计标签页
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text=self.language_manager.get_text("word_count_stats"))
        self.setup_stats_tab(stats_frame)

        # 词云标签页
        self.wordcloud_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.wordcloud_frame, text=self.language_manager.get_text("wordcloud_analysis"))
        self.setup_wordcloud_tab(self.wordcloud_frame)

        # 标点符号标签页
        punctuation_frame = ttk.Frame(self.notebook)
        self.notebook.add(punctuation_frame, text=self.language_manager.get_text("punctuation_analysis"))
        self.setup_punctuation_tab(punctuation_frame)

        # 预留拓展标签页
        todo_frame = ttk.Frame(self.notebook)
        self.notebook.add(todo_frame, text=self.language_manager.get_text("more_analysis"))
        self.setup_todo_tab(todo_frame)

    def _bind_events(self):
        """绑定标签页切换事件，用于恢复窗口大小"""
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    def _on_tab_changed(self, event):
        """当切换标签页时，如果离开词云标签页，恢复窗口大小"""
        current_tab = self.notebook.index(self.notebook.select())
        wordcloud_index = self.notebook.index(self.wordcloud_frame)
        if current_tab != wordcloud_index:
            self.window.geometry(self.normal_geometry)

    # ---------- 字数统计标签页 ----------
    def setup_stats_tab(self, parent):
        stats_frame = ttk.LabelFrame(parent, text=self.language_manager.get_text("basic_stats"))
        stats_frame.pack(fill=tk.X, padx=10, pady=10)

        self.stats_text = tk.Text(stats_frame, height=8, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(stats_frame, command=self.stats_text.yview)
        self.stats_text.config(yscrollcommand=scrollbar.set)

        self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._update_stats()

    def _update_stats(self):
        if not self.full_content.strip():
            stats_lines = ["暂无内容可统计"]
        else:
            content = self.full_content
            total_chars = len(content)
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
            english_letters = len(re.findall(r'[a-zA-Z]', content))
            digits = len(re.findall(r'\d', content))
            punctuation_chars = len(re.findall(r'[，。！？；：“”‘’——……（）【】《》,.!?;:\'"()\[\]{}<>]', content))

            lines = content.splitlines()
            paragraphs = 0
            in_paragraph = False
            for line in lines:
                if line.strip():
                    if not in_paragraph:
                        paragraphs += 1
                        in_paragraph = True
                else:
                    in_paragraph = False
            line_count = len(lines)

            stats_lines = [
                f"总字符数: {total_chars}",
                f"中文字符数: {chinese_chars}",
                f"英文字母数: {english_letters}",
                f"数字数: {digits}",
                f"标点符号数: {punctuation_chars}",
                f"行数: {line_count}",
                f"平均行长度: {round(total_chars/line_count, 1)}",
            ]

        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        for line in stats_lines:
            self.stats_text.insert(tk.END, line + "\n")
        self.stats_text.config(state=tk.DISABLED)

    # ---------- 标点符号标签页 ----------
    def setup_punctuation_tab(self, parent):
        table_frame = ttk.LabelFrame(parent, text=self.language_manager.get_text("punctuation_stats"))
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = (
            self.language_manager.get_text("punctuation_symbol"),
            self.language_manager.get_text("occurrence_count"),
            self.language_manager.get_text("percentage")
        )
        self.punctuation_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.punctuation_tree.heading(col, text=col)
            self.punctuation_tree.column(col, width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.punctuation_tree.yview)
        self.punctuation_tree.configure(yscrollcommand=scrollbar.set)

        self.punctuation_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._update_punctuation()

    def _update_punctuation(self):
        if not self.full_content.strip():
            self.punctuation_tree.delete(*self.punctuation_tree.get_children())
            self.punctuation_tree.insert("", tk.END, values=("无数据", "-", "-"))
            return

        content = self.full_content
        punctuation_list = [
            '，', '。', '！', '？', '；', '：', '“', '”', '‘', '’',
            '——', '……', '（', '）', '【', '】', '《', '》',
            ',', '.', '!', '?', ';', ':', '"', "'", '(', ')', '[', ']',
            '{', '}', '<', '>', '「', '」', '『', '』'
        ]

        total_chars = len(content)
        counts = {p: content.count(p) for p in punctuation_list}
        valid_items = [(p, cnt) for p, cnt in counts.items() if cnt > 0]
        valid_items.sort(key=lambda x: x[1], reverse=True)

        self.punctuation_tree.delete(*self.punctuation_tree.get_children())
        for symbol, count in valid_items:
            percentage = (count / total_chars) * 100
            self.punctuation_tree.insert("", tk.END, values=(symbol, count, f"{percentage:.2f}%"))

        if not valid_items:
            self.punctuation_tree.insert("", tk.END, values=("无标点符号", "0", "0.00%"))

    # ---------- 词云标签页 ----------
    def setup_wordcloud_tab(self, parent):
        params_frame = ttk.LabelFrame(parent, text=self.language_manager.get_text("wordcloud_params"))
        params_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(params_frame, text=f"{self.language_manager.get_text('max_words')}:").pack(side=tk.LEFT, padx=5)
        self.max_words_entry = ttk.Entry(params_frame, width=10)
        self.max_words_entry.insert(0, "100")
        self.max_words_entry.pack(side=tk.LEFT, padx=5)

        self.generate_btn = ttk.Button(
            params_frame,
            text=self.language_manager.get_text("generate_wordcloud"),
            command=self.generate_wordcloud
        )
        self.generate_btn.pack(side=tk.RIGHT, padx=5)

        display_frame = ttk.Frame(parent)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.wordcloud_canvas = tk.Canvas(display_frame, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.wordcloud_canvas.pack(fill=tk.BOTH, expand=True)

        self._show_wordcloud_placeholder()

    def _show_wordcloud_placeholder(self, message=None):
        self.wordcloud_canvas.delete("all")
        if message is None:
            if not WORDCLOUD_AVAILABLE:
                message = "词云库未安装，无法生成\n请安装：jieba, wordcloud, pillow"
            elif not self.full_content.strip():
                message = "无内容可生成词云"
            else:
                message = f"{self.language_manager.get_text('wordcloud_analysis')}显示区域\n点击生成按钮"
        self.wordcloud_canvas.create_text(
            self.wordcloud_canvas.winfo_width() // 2 or 200,
            self.wordcloud_canvas.winfo_height() // 2 or 150,
            text=message, font=("Microsoft YaHei", 12), fill="gray"
        )

    def generate_wordcloud(self):
        # 扩大窗口并强制更新布局
        self.window.geometry(self.expanded_geometry)
        self.window.update()  # 确保画布已调整大小

        if not WORDCLOUD_AVAILABLE:
            self._show_wordcloud_placeholder("缺少词云库，无法生成")
            return

        if not self.full_content.strip():
            self._show_wordcloud_placeholder("无内容可生成词云")
            return

        try:
            max_words = int(self.max_words_entry.get())
        except ValueError:
            max_words = 100

        # 获取画布当前实际尺寸
        canvas_width = self.wordcloud_canvas.winfo_width()
        canvas_height = self.wordcloud_canvas.winfo_height()
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500

        # 根据语言预处理
        lang = self.detected_language
        if lang.startswith('zh'):  # 中文
            filtered_text = ''.join(re.findall(r'[\u4e00-\u9fff]', self.full_content))
            words = jieba.cut(filtered_text)
            word_list = [w for w in words if len(w) > 1 and w not in self.stopwords]
        elif lang == 'en':  # 英文
            filtered_text = ''.join(re.findall(r'[a-zA-Z\s]', self.full_content))
            words = filtered_text.lower().split()
            word_list = [w for w in words if len(w) > 1 and w not in self.english_stopwords]
        elif lang == 'ja':  # 日文
            filtered_text = ''.join(re.findall(r'[\u3040-\u30FF\u4e00-\u9fff\s]', self.full_content))
            words = jieba.cut(filtered_text)
            word_list = [w for w in words if len(w) > 1]
        else:
            filtered_text = ''.join(re.findall(r'[\u4e00-\u9fff]', self.full_content))
            words = jieba.cut(filtered_text)
            word_list = [w for w in words if len(w) > 1 and w not in self.stopwords]

        word_freq = Counter(word_list)
        if not word_freq:
            self._show_wordcloud_placeholder("分词结果为空或全部被过滤")
            return

        # 生成词云
        wc = WordCloud(
            font_path="simhei.ttf",  # 若无此字体可改为其他中文字体或留空
            width=canvas_width,
            height=canvas_height,
            max_words=max_words,
            background_color="white"
        )
        wc.generate_from_frequencies(word_freq)

        image = wc.to_image()
        photo = ImageTk.PhotoImage(image)

        # 在画布上显示，从左上角开始填满
        self.wordcloud_canvas.delete("all")
        self.wordcloud_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.wordcloud_canvas.image = photo  # 保持引用

    # ---------- 更多分析标签页（保留 TODO） ----------
    def setup_todo_tab(self, parent):
        label = ttk.Label(parent, text=f"{self.language_manager.get_text('more_analysis')}功能待拓展",
                          font=("Microsoft YaHei", 12))
        label.pack(expand=True)

        todo_text = tk.Text(parent, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        todo_text.insert(tk.END, f"{self.language_manager.get_text('expansion_features')}:\n\n")
        todo_text.insert(tk.END, "• 文本复杂度分析\n")
        todo_text.insert(tk.END, "• 关键词提取\n")
        todo_text.insert(tk.END, "• 情感分析\n")
        todo_text.insert(tk.END, "• 可读性分析\n")
        todo_text.insert(tk.END, "• 语言风格分析\n")
        todo_text.config(state=tk.DISABLED)
        todo_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)