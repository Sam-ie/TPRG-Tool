from .base_language import BaseLanguage


class English(BaseLanguage):
    """英文"""

    @property
    def language_code(self) -> str:
        return "en"

    @property
    def language_name(self) -> str:
        return "English"

    def get_text(self, key: str) -> str:
        texts = {
            # 界面文本
            "file_selection": "File Selection",
            "text_processing": "Text Processing",
            "document_content": "Document Content",
            "select_file": "Select File",
            "no_file_selected": "No file selected",
            "deduplicate": "Deduplicate",
            "spell_check": "Spell Check",
            "correct_symbols": "Correct Symbols",
            "smart_auto_process": "Smart Auto Process",
            "smart_analysis": "Smart Analysis",
            "export": "Export",
            "help": "Help",
            "support_author": "Support Author",
            "previous_modification": "Previous Modification",
            "next_modification": "Next Modification",
            "language_label": "Language:",

            # 弹窗标题
            "error": "Error",
            "info": "Information",
            "analysis_window_title": "Smart Analysis",
            "help_window_title": "Help",
            "support_window_title": "Support Author",

            # 错误和信息消息
            "file_not_exist": "File does not exist",
            "unsupported_format": "Unsupported file format",
            "decode_error": "Unable to decode file encoding",
            "read_docx_error": "Failed to read docx file",
            "read_doc_error": "Failed to read doc file",
            "read_file_error": "Error occurred while reading file",
            "save_file_error": "Error occurred while saving file",
            "unsupported_export_format": "Unsupported export format",
            "pdf_export_not_implemented": "PDF export function not implemented yet",
            "no_content_to_export": "No content to export",
            "file_load_success": "File loaded successfully",
            "file_save_success": "File saved successfully",
            "please_load_file_first": "Please load file first",
            "process_completed": "Process completed",
            "process_failed": "Process failed",
            "smart_process_completed": "Smart auto process completed",
            "smart_process_failed": "Smart auto process failed",

            # 分析窗口文本
            "word_count_stats": "Word Count Statistics",
            "wordcloud_analysis": "Word Cloud Analysis",
            "punctuation_analysis": "Punctuation",
            "more_analysis": "More Analysis",
            "basic_stats": "Basic Statistics",
            "wordcloud_params": "Word Cloud Parameters",
            "max_words": "Maximum Words",
            "generate_wordcloud": "Generate Word Cloud",
            "punctuation_stats": "Punctuation Statistics",
            "punctuation_symbol": "Punctuation Symbol",
            "occurrence_count": "Occurrence Count",
            "percentage": "Percentage",
            "expansion_features": "Expansion Features",

            # 帮助窗口文本
            "function_intro": "Function Introduction",
            "usage_instructions": "Usage Instructions",
            "about": "About",

            # 支持窗口文本
            "thank_you_support": "Thank You for Support!",
            "support_author_title": "Support Author",
            "support_methods": "Support Methods",
            "close": "Close",
        }
        return texts.get(key, key)