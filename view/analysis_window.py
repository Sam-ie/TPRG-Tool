import tkinter as tk
from tkinter import ttk
import re
from collections import Counter
import os

try:
    import jieba
    from wordcloud import WordCloud
    from PIL import Image, ImageTk
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    jieba = None

DICTIONARY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dictionary")
STOPWORD_FILES = {
    'zh_CN': os.path.join(DICTIONARY_DIR, "Simplified_Chinese_stopwords.txt"),
    'zh_TW': os.path.join(DICTIONARY_DIR, "Traditional_Chinese_stopwords.txt"),
    'en': os.path.join(DICTIONARY_DIR, "English_stopwords.txt"),
    'ja': os.path.join(DICTIONARY_DIR, "Japanese_stopwords.txt"),
}

def load_stopwords(language: str) -> set:
    filepath = STOPWORD_FILES.get(language)
    if not filepath or not os.path.exists(filepath):
        return set()
    stopwords = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word and not word.startswith('#'):
                    stopwords.add(word)
    except Exception as e:
        print(f"加载停用词文件失败 {filepath}: {e}")
    return stopwords

class AnalysisWindow:
    def __init__(self, parent, controller, language_manager):
        self.window = tk.Toplevel(parent)
        self.controller = controller
        self.language_manager = language_manager

        self.normal_geometry = "400x300"
        self.expanded_geometry = "900x700"

        model = self.controller.model
        self.entries = model.entries if hasattr(model, 'entries') else []
        self.full_content = "\n".join([entry.content for entry in self.entries if entry.content.strip()])

        self.detected_language = getattr(model, 'detected_language', 'zh_CN')
        self.stopwords = load_stopwords(self.detected_language)

        self.setup_ui()
        self._bind_events()

    def setup_ui(self):
        self.window.title(self.language_manager.get_text("analysis_window_title"))
        self.window.geometry(self.normal_geometry)

        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text=self.language_manager.get_text("word_count_stats"))
        self.setup_stats_tab(stats_frame)

        self.wordcloud_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.wordcloud_frame, text=self.language_manager.get_text("wordcloud_analysis"))
        self.setup_wordcloud_tab(self.wordcloud_frame)

        punctuation_frame = ttk.Frame(self.notebook)
        self.notebook.add(punctuation_frame, text=self.language_manager.get_text("punctuation_analysis"))
        self.setup_punctuation_tab(punctuation_frame)

        todo_frame = ttk.Frame(self.notebook)
        self.notebook.add(todo_frame, text=self.language_manager.get_text("more_analysis"))
        self.setup_todo_tab(todo_frame)

    def _bind_events(self):
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    def _on_tab_changed(self, event):
        current_tab = self.notebook.index(self.notebook.select())
        wordcloud_index = self.notebook.index(self.wordcloud_frame)
        if current_tab != wordcloud_index:
            self.window.geometry(self.normal_geometry)

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
            stats_lines = [self.language_manager.get_text("no_content_stats")]
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
                f"{self.language_manager.get_text('total_chars')}: {total_chars}",
                f"{self.language_manager.get_text('chinese_chars')}: {chinese_chars}",
                f"{self.language_manager.get_text('english_letters')}: {english_letters}",
                f"{self.language_manager.get_text('digits')}: {digits}",
                f"{self.language_manager.get_text('punctuation_chars')}: {punctuation_chars}",
                f"{self.language_manager.get_text('line_count')}: {line_count}",
                f"{self.language_manager.get_text('avg_line_length')}: {round(total_chars/line_count, 1)}",
            ]

        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        for line in stats_lines:
            self.stats_text.insert(tk.END, line + "\n")
        self.stats_text.config(state=tk.DISABLED)

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
            self.punctuation_tree.insert("", tk.END, values=(self.language_manager.get_text("no_data"), "-", "-"))
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
            self.punctuation_tree.insert("", tk.END, values=(self.language_manager.get_text("no_punctuation"), "0", "0.00%"))

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
                message = self.language_manager.get_text("wordcloud_lib_missing")
            elif not self.full_content.strip():
                message = self.language_manager.get_text("no_content_wordcloud")
            else:
                message = self.language_manager.get_text("wordcloud_display_area")
        self.wordcloud_canvas.create_text(
            self.wordcloud_canvas.winfo_width() // 2 or 200,
            self.wordcloud_canvas.winfo_height() // 2 or 150,
            text=message, font=("Microsoft YaHei", 12), fill="gray"
        )

    def generate_wordcloud(self):
        self.window.geometry(self.expanded_geometry)
        self.window.update()

        if not WORDCLOUD_AVAILABLE:
            self._show_wordcloud_placeholder(self.language_manager.get_text("wordcloud_missing_lib"))
            return

        if not self.full_content.strip():
            self._show_wordcloud_placeholder(self.language_manager.get_text("no_content_wordcloud"))
            return

        try:
            max_words = int(self.max_words_entry.get())
        except ValueError:
            max_words = 100

        canvas_width = self.wordcloud_canvas.winfo_width()
        canvas_height = self.wordcloud_canvas.winfo_height()
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500

        lang = self.detected_language
        if lang.startswith('zh'):
            filtered_text = ''.join(re.findall(r'[\u4e00-\u9fff]', self.full_content))
            words = jieba.cut(filtered_text)
            word_list = [w for w in words if w not in self.stopwords]
        elif lang == 'en':
            filtered_text = ''.join(re.findall(r'[a-zA-Z\s]', self.full_content))
            words = filtered_text.lower().split()
            word_list = [w for w in words if w not in self.stopwords]
        elif lang == 'ja':
            filtered_text = ''.join(re.findall(r'[\u3040-\u30FF\u4e00-\u9fff\s]', self.full_content))
            words = jieba.cut(filtered_text)
            word_list = [w for w in words if w not in self.stopwords]
        else:
            filtered_text = ''.join(re.findall(r'[\u4e00-\u9fff]', self.full_content))
            words = jieba.cut(filtered_text)
            word_list = [w for w in words if w not in self.stopwords]

        word_freq = Counter(word_list)
        if not word_freq:
            self._show_wordcloud_placeholder(self.language_manager.get_text("wordcloud_empty_result"))
            return

        wc = WordCloud(
            font_path="simhei.ttf",
            width=canvas_width,
            height=canvas_height,
            max_words=max_words,
            background_color="white"
        )
        wc.generate_from_frequencies(word_freq)

        image = wc.to_image()
        photo = ImageTk.PhotoImage(image)

        self.wordcloud_canvas.delete("all")
        self.wordcloud_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.wordcloud_canvas.image = photo

    def setup_todo_tab(self, parent):
        label = ttk.Label(parent, text=self.language_manager.get_text("more_analysis_placeholder"),
                          font=("Microsoft YaHei", 12))
        label.pack(expand=True)

        todo_text = tk.Text(parent, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        todo_text.insert(tk.END, self.language_manager.get_text("more_analysis_content"))
        todo_text.config(state=tk.DISABLED)
        todo_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
