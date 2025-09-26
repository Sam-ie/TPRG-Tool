from abc import ABC, abstractmethod


class BaseLanguage(ABC):
    """语言基类"""

    @property
    @abstractmethod
    def language_code(self) -> str:
        """返回语言代码"""
        pass

    @property
    @abstractmethod
    def language_name(self) -> str:
        """返回语言名称"""
        pass

    @abstractmethod
    def get_text(self, key: str) -> str:
        """获取翻译文本"""
        pass

    def get_ui_texts(self) -> dict:
        """获取所有UI文本"""
        return {
            # 界面文本
            "file_selection": self.get_text("file_selection"),
            "text_processing": self.get_text("text_processing"),
            "document_content": self.get_text("document_content"),
            "select_file": self.get_text("select_file"),
            "no_file_selected": self.get_text("no_file_selected"),
            "deduplicate": self.get_text("deduplicate"),
            "spell_check": self.get_text("spell_check"),
            "correct_symbols": self.get_text("correct_symbols"),
            "smart_auto_process": self.get_text("smart_auto_process"),
            "smart_analysis": self.get_text("smart_analysis"),
            "export": self.get_text("export"),
            "help": self.get_text("help"),
            "support_author": self.get_text("support_author"),
            "previous_modification": self.get_text("previous_modification"),
            "next_modification": self.get_text("next_modification"),
            "language_label": self.get_text("language_label"),

            # 弹窗标题
            "error": self.get_text("error"),
            "info": self.get_text("info"),
            "analysis_window_title": self.get_text("analysis_window_title"),
            "help_window_title": self.get_text("help_window_title"),
            "support_window_title": self.get_text("support_window_title"),

            # 错误和信息消息
            "file_not_exist": self.get_text("file_not_exist"),
            "unsupported_format": self.get_text("unsupported_format"),
            "decode_error": self.get_text("decode_error"),
            "read_docx_error": self.get_text("read_docx_error"),
            "read_doc_error": self.get_text("read_doc_error"),
            "read_file_error": self.get_text("read_file_error"),
            "save_file_error": self.get_text("save_file_error"),
            "unsupported_export_format": self.get_text("unsupported_export_format"),
            "pdf_export_not_implemented": self.get_text("pdf_export_not_implemented"),
            "no_content_to_export": self.get_text("no_content_to_export"),
            "file_load_success": self.get_text("file_load_success"),
            "file_save_success": self.get_text("file_save_success"),
            "please_load_file_first": self.get_text("please_load_file_first"),
            "process_completed": self.get_text("process_completed"),
            "process_failed": self.get_text("process_failed"),
            "smart_process_completed": self.get_text("smart_process_completed"),
            "smart_process_failed": self.get_text("smart_process_failed"),

            # 分析窗口文本
            "word_count_stats": self.get_text("word_count_stats"),
            "wordcloud_analysis": self.get_text("wordcloud_analysis"),
            "punctuation_analysis": self.get_text("punctuation_analysis"),
            "more_analysis": self.get_text("more_analysis"),
            "basic_stats": self.get_text("basic_stats"),
            "wordcloud_params": self.get_text("wordcloud_params"),
            "max_words": self.get_text("max_words"),
            "generate_wordcloud": self.get_text("generate_wordcloud"),
            "punctuation_stats": self.get_text("punctuation_stats"),
            "punctuation_symbol": self.get_text("punctuation_symbol"),
            "occurrence_count": self.get_text("occurrence_count"),
            "percentage": self.get_text("percentage"),
            "expansion_features": self.get_text("expansion_features"),

            # 帮助窗口文本
            "function_intro": self.get_text("function_intro"),
            "usage_instructions": self.get_text("usage_instructions"),
            "about": self.get_text("about"),

            # 支持窗口文本
            "thank_you_support": self.get_text("thank_you_support"),
            "support_author_title": self.get_text("support_author_title"),
            "support_methods": self.get_text("support_methods"),
            "close": self.get_text("close"),
        }