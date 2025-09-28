from .base_language import BaseLanguage


class ChineseTraditional(BaseLanguage):
    """繁体中文"""

    @property
    def language_code(self) -> str:
        return "zh_TW"

    @property
    def language_name(self) -> str:
        return "繁體中文"

    def get_text(self, key: str) -> str:
        texts = {
            # 界面文本
            "file_selection": "文件選擇",
            "text_processing": "文本處理",
            "document_content": "文檔內容",
            "select_file": "選擇文件",
            "no_file_selected": "未選擇文件",
            "deduplicate": "去重",
            "spell_check": "去錯別字",
            "correct_symbols": "修正符號",
            "smart_auto_process": "智能自動處理",
            "smart_analysis": "智能分析",
            "export": "導出",
            "help": "幫助",
            "support_author": "支持作者",
            "previous_modification": "前一處修改",
            "next_modification": "後一處修改",
            "language_label": "語言:",

            # 弹窗标题
            "error": "錯誤",
            "info": "信息",
            "analysis_window_title": "智能分析",
            "help_window_title": "幫助",
            "support_window_title": "支持作者",

            # 错误和信息消息
            "no_content_to_export": "沒有內容可導出",
            "file_load_success": "文件加載成功",
            "file_save_success": "文件保存成功",
            "please_load_file_first": "請先加載文件",
            "process_completed": "處理完成",
            "process_failed": "處理失敗",
            "smart_process_completed": "智能自動處理完成",
            "smart_process_failed": "智能自動處理失敗",

            # 分析窗口文本
            "word_count_stats": "字數統計",
            "wordcloud_analysis": "詞雲分析",
            "punctuation_analysis": "標點符號",
            "more_analysis": "更多分析",
            "basic_stats": "基本統計",
            "wordcloud_params": "詞雲參數",
            "max_words": "最大詞語數",
            "generate_wordcloud": "生成詞雲",
            "punctuation_stats": "標點符號統計",
            "punctuation_symbol": "標點符號",
            "occurrence_count": "出現次數",
            "percentage": "佔比",
            "expansion_features": "拓展功能",

            # 帮助窗口文本
            "function_intro": "功能介紹",
            "usage_instructions": "使用說明",
            "about": "關於",

            # 支持窗口文本
            "thank_you_support": "感謝支持！",
            "support_author_title": "支持作者",
            "support_methods": "支持方式",
            "close": "關閉",

            # 进度窗口文本
            "reading_file": "正在讀取文件...",
            "processing": "正在處理",
            "completed": "完成",
            "file_read_complete": "文件讀取完成",

            # 主窗口标题
            "main_window_title": "文本處理工具",

            # 文件管理器相关文本
            "file_not_exist": "文件不存在",
            "unsupported_format": "不支持的文件格式",
            "read_file_error": "讀取文件時發生錯誤",
            "decode_error": "無法解碼文件編碼",
            "reading_file_progress": "讀取文件中",
            "parsing_docx": "解析Word文檔...",
            "converting_doc": "正在轉換DOC格式...",
            "conversion_complete": "完成轉換",
            "read_docx_error": "讀取docx文件失敗",
            "read_doc_error": "讀取doc文件失敗",
            "save_file_error": "保存文件時發生錯誤",
            "unsupported_export_format": "不支持的導出格式",

            # 文件过滤器文本
            "supported_files": "支持的文件",
            "word_documents": "Word文檔",
            "word_97_2003_documents": "Word 97-2003文檔",
            "text_files": "文本文件",
            "all_files": "所有文件",
        }
        return texts.get(key, key)