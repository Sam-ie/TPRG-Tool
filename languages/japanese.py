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
            "sort_by_timestamp": "タイムスタンプで並べ替え",
            "reparse": "再解析",

            # 弹窗标题
            "error": "エラー",
            "info": "情報",
            "analysis_window_title": "スマート分析",
            "help_window_title": "ヘルプ",
            "support_window_title": "作者を支援",

            # 错误和信息消息
            "no_content_to_export": "エクスポートする内容がありません",
            "file_load_success": "ファイルの読み込みに成功しました",
            "file_save_success": "ファイルの保存に成功しました",
            "please_load_file_first": "まずファイルを読み込んでください",
            "process_completed": "処理が完了しました",
            "process_failed": "処理に失敗しました",
            "process_cancelled": "処理がキャンセルされました",
            "smart_process_completed": "スマート自動処理が完了しました",
            "smart_process_failed": "スマート自動処理に失敗しました",
            "smart_process_cancelled": "スマート処理がキャンセルされました",
            "no_timestamp_to_sort": "並べ替え可能なタイムスタンプがありません",
            "no_content_to_reparse": "再解析するコンテンツがありません",
            "unsupported_operation": "サポートされていない操作",

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

            # 分析窗口新增键
            "no_content_stats": "分析する内容がありません",
            "total_chars": "総文字数",
            "chinese_chars": "漢字数",
            "english_letters": "英文字母数",
            "digits": "数字数",
            "punctuation_chars": "句読点数",
            "line_count": "行数",
            "avg_line_length": "平均行長さ",
            "no_data": "データなし",
            "no_punctuation": "句読点なし",
            "wordcloud_lib_missing": "ワードクラウドライブラリがインストールされていません\nインストール：jieba, wordcloud, pillow",
            "no_content_wordcloud": "ワードクラウドを生成する内容がありません",
            "wordcloud_display_area": "ワードクラウド表示エリア\n生成ボタンをクリック",
            "wordcloud_missing_lib": "ワードクラウドライブラリが不足しています",
            "wordcloud_empty_result": "分詞結果が空またはすべてフィルタリングされました",
            "more_analysis_placeholder": "詳細分析機能は拡張予定",
            "more_analysis_content": "拡張機能:\n\n• テキスト複雑度分析\n• キーワード抽出\n• 感情分析\n• 可読性分析\n• 言語スタイル分析\n",

            # 帮助窗口文本
            "function_intro": "機能紹介",
            "usage_instructions": "使用説明",
            "about": "について",

            # 帮助窗口新增内容键
            "function_intro_content": """機能紹介
====================

主な機能説明：

1. 【タイムスタンプで並べ替え】
   • 複数のグループのログが混ざっている場合、自動的に時系列で整理
   • シールドダイスが複数グループの情報を統合し、振り返りやすくします

2. 【重複除去】
   • ダイスボットが撤回を認識できないなどによる重複内容を除去
   • 類似度しきい値を調整可能、近似重複行をインテリジェントに識別

3. 【誤字修正】
   • 一般的な誤字を自動修正（簡体字/繁体字中国語、英語に対応）
   • PLが誤字を送信し、セッション終了後に修正を忘れた問題を解決

4. 【記号修正】
   • 文末に欠落している句点を自動補完
   • 引用符の逆転や対応関係の誤りを修正
   • 中国語と英語の句読点形式を統一

5. 【スマート自動処理】
   • ワンクリックで重複除去、誤字修正、記号修正を実行
   • ドキュメント全体を迅速に最適化

6. 【統計分析】
   • 文字数統計：漢字、英文字母、数字、句読点など
   • 平均RP長：一行あたりの平均文字数を計算
   • ワードクラウド：ドキュメント言語に基づいてインテリジェントに生成（中国語/英語/日本語）
   • 句読点使用統計

7. 【マルチフォーマットインポート/エクスポート】
   • .txt、.doc、.docxファイルからインポート可能
   • QQチャット内容を直接コピーしてエディタに貼り付け可能
   • .txt または .docx 形式でエクスポート可能

8. 【多言語インターフェース】
   • 簡体字中国語、繁体字中国語、英語、日本語に対応
   • ワンクリックで言語切り替え

その他の機能は開発中です...
""",
            "usage_instructions_content": """使用説明
==========

基本操作手順：

1. テキストのインポート
   • 「ファイル選択」ボタンをクリックして .txt/.doc/.docx ファイルをインポート
   • またはチャット記録を直接コピーしてエディタに貼り付け

2. 順序の調整（オプション）
   • 「タイムスタンプで並べ替え」ボタンをクリックして、複数のグループのログを自動的に時系列で整理

3. テキストの処理
   • 個別処理：「重複除去」、「誤字修正」、「記号修正」をそれぞれクリックして実行
   • 一括処理：「スマート自動処理」をクリックしてすべての最適化を一括実行

4. 分析の表示
   • 「スマート分析」をクリックして分析ウィンドウを開き、文字数統計、ワードクラウド、句読点統計を表示
   • ワードクラウドは中国語/英語/日本語に対応、ストップワードと無意味な文字を自動フィルタリング

5. 結果のエクスポート
   • 「エクスポート」ボタンをクリック、デフォルトの保存名は「text_processing_record.txt」
   • 同名ファイルが存在する場合は自動的に番号を追加、.docx 形式も選択可能

注意事項：

• タイムスタンプでの並べ替えには、テキストに標準的な時刻形式（例：2023-01-01 12:34:56）が含まれている必要があります
日付が欠落している場合や、年をまたぐ記録で年が欠落している場合、並べ替えエラーが発生する可能性があります。その場合は日付ごとまたは年ごとに分割してインポートしてください
• 誤字修正は数百万レベルのコーパスに依存しており、処理時間が長くなります（200文字/秒）。しばらくお待ちください
• テキストボックス内の編集は元に戻す/やり直しに対応（Ctrl+Z / Ctrl+Y）

ショートカットキー：

• Ctrl+Z: 元に戻す
• Ctrl+Y: やり直し
• F1: ヘルプ表示

その他の使い方は今後のバージョンでご確認ください。
""",
            "about_content": """テキスト処理ツール v1.0

RPGログの最適化に特化したテキスト処理ソフトウェア。

主な特徴：
• インテリジェントな重複除去、誤字修正、記号補完
• 複数グループのログをタイムスタンプで自動並べ替え
• 簡体字中国語/繁体字中国語/英語/日本語のインターフェースに対応
• ワードクラウドと文字数統計の可視化分析
• 直接コピーペーストまたは txt/doc/docx のインポート

開発者：シャオ・ユー
リリース日：2026年

ご利用ありがとうございます！皆様のサポートが継続的な改善の原動力です。
""",

            # 支持窗口文本
            "thank_you_support": "ご支援ありがとうございます！",
            "support_author_title": "作者を支援",
            "support_methods": "支援方法",

            # 支持窗口新增键
            "support_text_content": """テキスト処理ツールをご利用いただきありがとうございます！

このソフトウェアがお役に立ったなら、開発活動へのご支援をご検討ください。

支援方法：
• 他のユーザーと共有する
• 貴重なご意見を提供する
• 問題点を報告する

連絡先メール：1163429473@qq.com
プロジェクトURL：https://github.com/Sam-ie/TPRG-Tool
""",
            "image_load_failed": "画像の読み込みに失敗しました",
            "need_pil": "PILが必要です",
            "please_place_image": "画像を配置してください",
            "wechat_pay": "WeChat Pay",

            # 进度窗口文本
            "reading_file": "ファイルを読み込み中...",
            "processing": "処理中",
            "completed": "完了",
            "file_read_complete": "ファイル読み込み完了",

            # 主窗口标题
            "main_window_title": "テキスト処理ツール",

            # 文件管理器相关文本
            "file_not_exist": "ファイルが存在しません",
            "unsupported_format": "サポートされていないファイル形式",
            "read_file_error": "ファイルの読み取り中にエラーが発生しました",
            "decode_error": "ファイルのエンコーディングをデコードできません",
            "reading_file_progress": "ファイルを読み込み中",
            "parsing_docx": "Word文書を解析中...",
            "converting_doc": "DOC形式を変換中...",
            "conversion_complete": "変換完了",
            "read_docx_error": "docxファイルの読み取りに失敗しました",
            "read_doc_error": "docファイルの読み取りに失敗しました",
            "save_file_error": "ファイルの保存中にエラーが発生しました",
            "unsupported_export_format": "サポートされていないエクスポート形式",

            # 文件过滤器文本
            "supported_files": "サポートされているファイル",
            "word_documents": "Word文書",
            "word_97_2003_documents": "Word 97-2003文書",
            "text_files": "テキストファイル",
            "all_files": "すべてのファイル",
        }
        return texts.get(key, key)
