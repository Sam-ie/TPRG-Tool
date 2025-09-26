from .base_language import BaseLanguage


class Japanese(BaseLanguage):
    """日文"""

    @property
    def language_code(self) -> str:
        return "ja"

    @property
    def language_name(self) -> str:
        return "日本語"

    def get_text(self, key: str) -> str:
        texts = {
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
            "language_label": "言語:",

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
            "smart_process_failed": "スマート自動処理に失敗しました",

            # 分析窗口文本
            "word_count_stats": "文字数統計",
            "wordcloud_analysis": "ワードクラウド分析",
            "punctuation_analysis": "句読点",
            "more_analysis": "詳細分析",
            "basic_stats": "基本統計",
            "wordcloud_params": "ワードクラウドパラメータ",
            "max_words": "最大単語数",
            "generate_wordcloud": "ワードクラウド生成",
            "punctuation_stats": "句読点統計",
            "punctuation_symbol": "句読点記号",
            "occurrence_count": "出現回数",
            "percentage": "割合",
            "expansion_features": "拡張機能",

            # 帮助窗口文本
            "function_intro": "機能紹介",
            "usage_instructions": "使用説明",
            "about": "について",

            # 支持窗口文本
            "thank_you_support": "ご支援ありがとうございます！",
            "support_author_title": "作者を支援",
            "support_methods": "支援方法",
            "close": "閉じる",
        }
        return texts.get(key, key)