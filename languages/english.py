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
            "sort_by_timestamp": "Sort by Timestamp",
            "reparse": "Reparse",

            # 弹窗标题
            "error": "Error",
            "info": "Information",
            "analysis_window_title": "Smart Analysis",
            "help_window_title": "Help",
            "support_window_title": "Support Author",

            # 错误和信息消息
            "no_content_to_export": "No content to export",
            "file_load_success": "File loaded successfully",
            "file_save_success": "File saved successfully",
            "please_load_file_first": "Please load file first",
            "process_completed": "Process completed",
            "process_failed": "Process failed",
            "process_cancelled": "Process cancelled",
            "smart_process_completed": "Smart auto process completed",
            "smart_process_failed": "Smart auto process failed",
            "smart_process_cancelled": "Smart process cancelled",
            "no_timestamp_to_sort": "No timestamps to sort",
            "no_content_to_reparse": "No content to reparse",
            "unsupported_operation": "Unsupported operation",

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

            # 分析窗口新增键
            "no_content_stats": "No content to analyze",
            "total_chars": "Total characters",
            "chinese_chars": "Chinese characters",
            "english_letters": "English letters",
            "digits": "Digits",
            "punctuation_chars": "Punctuation marks",
            "line_count": "Lines",
            "avg_line_length": "Average line length",
            "no_data": "No data",
            "no_punctuation": "No punctuation",
            "wordcloud_lib_missing": "Word cloud libraries not installed\nPlease install: jieba, wordcloud, pillow",
            "no_content_wordcloud": "No content to generate word cloud",
            "wordcloud_display_area": "Word cloud display area\nClick Generate button",
            "wordcloud_missing_lib": "Word cloud libraries missing",
            "wordcloud_empty_result": "Segmentation result empty or all filtered out",
            "more_analysis_placeholder": "More analysis features coming soon",
            "more_analysis_content": "Expansion features:\n\n• Text complexity analysis\n• Keyword extraction\n• Sentiment analysis\n• Readability analysis\n• Language style analysis\n",

            # 帮助窗口文本
            "function_intro": "Function Introduction",
            "usage_instructions": "Usage Instructions",
            "about": "About",

            # 帮助窗口新增内容键
            "function_intro_content": """Function Introduction
====================

Main Features:

1. 【Sort by Timestamp】
   • Automatically arrange mixed logs from multiple groups in chronological order
   • Helps consolidate information from multiple groups for easy review

2. 【Deduplicate】
   • Remove duplicate content caused by bot failures to detect deletions
   • Adjustable similarity threshold to intelligently identify near-duplicate lines

3. 【Spell Check】
   • Automatically correct common typos (Supports Simplified Chinese, Traditional Chinese, English)
   • Fixes player typos that were forgotten after the game ends

4. 【Correct Symbols】
   • Automatically add missing periods at the end of sentences
   • Fix reversed quotation marks and mismatched quotes
   • Unify Chinese and English punctuation formats

5. 【Smart Auto Process】
   • One-click execution of deduplication, spell check, and symbol correction
   • Quickly optimize the entire document

6. 【Statistical Analysis】
   • Word count: Chinese characters, English letters, digits, punctuation, etc.
   • Average RP length: Calculate average characters per line
   • Word cloud: Intelligently generate word clouds based on document language (Chinese/English/Japanese)
   • Punctuation usage statistics

7. 【Multi-format Import/Export】
   • Import from .txt, .doc, .docx files
   • Directly copy and paste QQ chat content into the editor
   • Export as .txt or .docx format

8. 【Multi-language Interface】
   • Supports Simplified Chinese, Traditional Chinese, English, Japanese
   • One-click language switching

More features under development...
""",
            "usage_instructions_content": """Usage Instructions
==========

Basic Workflow:

1. Import Text
   • Click "Select File" button to import .txt/.doc/.docx files
   • Or directly copy and paste chat logs into the editor

2. Adjust Order (Optional)
   • Click "Sort by Timestamp" button to automatically arrange logs from multiple groups chronologically

3. Process Text
   • Individual processing: Click "Deduplicate", "Spell Check", "Correct Symbols" respectively
   • Batch processing: Click "Smart Auto Process" to perform all optimizations in one go

4. View Analysis
   • Click "Smart Analysis" to open the analysis window and view word count, word cloud, punctuation statistics
   • Word cloud supports Chinese/English/Japanese, automatically filters stopwords and meaningless characters

5. Export Results
   • Click "Export" button, default save name is "text_processing_record.txt"
   • Automatically adds a number if name exists, can choose .docx format

Notes:

• Sorting by timestamp requires the text to contain standard time format (e.g., 2023-01-01 12:34:56)
If time is incomplete, such as missing date or year for cross-year records, sorting may be incorrect; in such cases, import by date or year separately
• Spell check relies on a million-level corpus, processing time is long (200 characters/second), please be patient
• Edits in the text box support undo/redo (Ctrl+Z / Ctrl+Y)

Shortcuts:

• Ctrl+Z: Undo
• Ctrl+Y: Redo
• F1: Show help

More tips in future versions.
""",
            "about_content": """Text Processing Tool v1.0

A text processing software specifically designed for optimizing RPG logs.

Main Features:
• Intelligent deduplication, spell check, symbol completion
• Multi-group logs automatically sorted by timestamp
• Supports Simplified Chinese/Traditional Chinese/English/Japanese interface
• Word cloud and word count visualization analysis
• Direct copy-paste or import txt/doc/docx

Developer: Xiao Yu
Release Date: 2026

Thank you for using! Your support is the motivation for continuous improvement.
""",

            # 支持窗口文本
            "thank_you_support": "Thank You for Support!",
            "support_author_title": "Support Author",
            "support_methods": "Support Methods",

            # 支持窗口新增键
            "support_text_content": """Thank you for using the Text Processing Tool!

If you find this software helpful, please consider supporting my development work.

Ways to support:
• Share with more users
• Provide valuable feedback
• Report issues

Contact Email: 1163429473@qq.com
Project URL: https://github.com/Sam-ie/TPRG-Tool
""",
            "image_load_failed": "Image loading failed",
            "need_pil": "PIL required",
            "please_place_image": "Please place image",
            "wechat_pay": "WeChat Pay",

            # 进度窗口文本
            "reading_file": "Reading file...",
            "processing": "Processing",
            "completed": "Completed",
            "file_read_complete": "File read complete",

            # 主窗口标题
            "main_window_title": "Text Processing Tool",

            # 文件管理器相关文本
            "file_not_exist": "File does not exist",
            "unsupported_format": "Unsupported file format",
            "read_file_error": "Error occurred while reading file",
            "decode_error": "Unable to decode file encoding",
            "reading_file_progress": "Reading file",
            "parsing_docx": "Parsing Word document...",
            "converting_doc": "Converting DOC format...",
            "conversion_complete": "Conversion complete",
            "read_docx_error": "Failed to read docx file",
            "read_doc_error": "Failed to read doc file",
            "save_file_error": "Error occurred while saving file",
            "unsupported_export_format": "Unsupported export format",

            # 文件过滤器文本
            "supported_files": "Supported files",
            "word_documents": "Word documents",
            "word_97_2003_documents": "Word 97-2003 documents",
            "text_files": "Text files",
            "all_files": "All files",
        }
        return texts.get(key, key)
