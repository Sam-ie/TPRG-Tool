class UILanguageManager:
    """UI语言管理器"""

    def __init__(self):
        self.current_language = "zh_CN"
        self.translations = {
            "zh_CN": self._load_simplified_chinese(),
            "zh_TW": self._load_traditional_chinese(),
            "en": self._load_english(),
            "ja": self._load_japanese()
        }

    def _load_simplified_chinese(self) -> dict:
        return {
            # 界面文本
            "file_selection": "文件选择",
            "text_processing": "文本处理",
            "document_content": "文档内容",
            "select_file": "选择文件",
            "no_file_selected": "未选择文件",
            "deduplicate": "去重",
            "spell_check": "去错别字",
            "correct_symbols": "修正符号",
            "smart_auto_process": "智能自动处理",
            "smart_analysis": "智能分析",
            "export": "导出",
            "help": "帮助",
            "support_author": "支持作者",
            "previous_modification": "前一处修改",
            "next_modification": "后一处修改",
            "language_label": "语言:",  # 新增语言标签

            # 弹窗标题
            "error": "错误",
            "info": "信息",
            "analysis_window_title": "智能分析",
            "help_window_title": "帮助",
            "support_window_title": "支持作者",

            # 错误和信息消息
            "file_not_exist": "文件不存在",
            "unsupported_format": "不支持的文件格式",
            "decode_error": "无法解码文件编码",
            "read_docx_error": "读取docx文件失败",
            "read_doc_error": "读取doc文件失败",
            "read_file_error": "读取文件时发生错误",
            "save_file_error": "保存文件时发生错误",
            "unsupported_export_format": "不支持的导出格式",
            "pdf_export_not_implemented": "PDF导出功能暂未实现",
            "no_content_to_export": "没有内容可导出",
            "file_load_success": "文件加载成功",
            "file_save_success": "文件保存成功",
            "please_load_file_first": "请先加载文件",
            "process_completed": "处理完成",
            "process_failed": "处理失败",
            "smart_process_completed": "智能自动处理完成",
            "smart_process_failed": "智能自动处理失败"
        }

    def _load_traditional_chinese(self) -> dict:
        return {
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
            "language_label": "語言:",  # 新增语言标签

            # 弹窗标题
            "error": "錯誤",
            "info": "信息",
            "analysis_window_title": "智能分析",
            "help_window_title": "幫助",
            "support_window_title": "支持作者",

            # 错误和信息消息
            "file_not_exist": "文件不存在",
            "unsupported_format": "不支持的文件格式",
            "decode_error": "無法解碼文件編碼",
            "read_docx_error": "讀取docx文件失敗",
            "read_doc_error": "讀取doc文件失敗",
            "read_file_error": "讀取文件時發生錯誤",
            "save_file_error": "保存文件時發生錯誤",
            "unsupported_export_format": "不支持的導出格式",
            "pdf_export_not_implemented": "PDF導出功能暫未實現",
            "no_content_to_export": "沒有內容可導出",
            "file_load_success": "文件加載成功",
            "file_save_success": "文件保存成功",
            "please_load_file_first": "請先加載文件",
            "process_completed": "處理完成",
            "process_failed": "處理失敗",
            "smart_process_completed": "智能自動處理完成",
            "smart_process_failed": "智能自動處理失敗"
        }

    def _load_english(self) -> dict:
        return {
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
            "language_label": "Language:",  # 新增语言标签

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
            "smart_process_failed": "Smart auto process failed"
        }

    def _load_japanese(self) -> dict:
        return {
            # 界面文本
            "file_selection": "ファイル選択",
            "text_processing": "テキスト処理",
            "document_content": "文書内容",
            "select_file": "ファイル選択",
            "no_file_selected": "ファイル未選択",
            "deduplicate": "重複除去",
            "spell_check": "誤字修正",
            "correct_symbols": "記号修正",
            "smart_auto_process": "スマート自動処理",
            "smart_analysis": "スマート分析",
            "export": "エクスポート",
            "help": "ヘルプ",
            "support_author": "作者を支援",
            "previous_modification": "前の修正",
            "next_modification": "次の修正",
            "language_label": "言語:",  # 新增语言标签

            # 弹窗标题
            "error": "エラー",
            "info": "情報",
            "analysis_window_title": "スマート分析",
            "help_window_title": "ヘルプ",
            "support_window_title": "作者を支援",

            # 错误和信息消息
            "file_not_exist": "ファイルが存在しません",
            "unsupported_format": "サポートされていないファイル形式",
            "decode_error": "ファイルのエンコーディングをデコードできません",
            "read_docx_error": "docxファイルの読み取りに失敗しました",
            "read_doc_error": "docファイルの読み取りに失敗しました",
            "read_file_error": "ファイルの読み取り中にエラーが発生しました",
            "save_file_error": "ファイルの保存中にエラーが発生しました",
            "unsupported_export_format": "サポートされていないエクスポート形式",
            "pdf_export_not_implemented": "PDFエクスポート機能はまだ実装されていません",
            "no_content_to_export": "エクスポートする内容がありません",
            "file_load_success": "ファイルの読み込みに成功しました",
            "file_save_success": "ファイルの保存に成功しました",
            "please_load_file_first": "まずファイルを読み込んでください",
            "process_completed": "処理が完了しました",
            "process_failed": "処理に失敗しました",
            "smart_process_completed": "スマート自動処理が完了しました",
            "smart_process_failed": "スマート自動処理に失敗しました"
        }

    def set_language(self, language: str):
        """设置UI语言"""
        if language in self.translations:
            self.current_language = language

    def get_text(self, key: str) -> str:
        """获取翻译文本"""
        return self.translations[self.current_language].get(key, key)