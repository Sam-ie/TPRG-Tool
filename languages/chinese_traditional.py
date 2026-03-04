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
            "sort_by_timestamp": "按時間戳排序",
            "reparse": "重新解析",

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
            "process_cancelled": "處理已取消",
            "smart_process_completed": "智能自動處理完成",
            "smart_process_failed": "智能自動處理失敗",
            "smart_process_cancelled": "智能處理已取消",
            "no_timestamp_to_sort": "沒有時間戳可排序",
            "no_content_to_reparse": "沒有內容可重新解析",
            "unsupported_operation": "不支持的操作",

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

            # 分析窗口新增键
            "no_content_stats": "暫無內容可統計",
            "total_chars": "總字符數",
            "chinese_chars": "中文字符數",
            "english_letters": "英文字母數",
            "digits": "數字數",
            "punctuation_chars": "標點符號數",
            "line_count": "行數",
            "avg_line_length": "平均行長度",
            "no_data": "無數據",
            "no_punctuation": "無標點符號",
            "wordcloud_lib_missing": "詞雲庫未安裝，無法生成\n請安裝：jieba, wordcloud, pillow",
            "no_content_wordcloud": "無內容可生成詞雲",
            "wordcloud_display_area": "詞雲分析顯示區域\n點擊生成按鈕",
            "wordcloud_missing_lib": "缺少詞雲庫，無法生成",
            "wordcloud_empty_result": "分詞結果為空或全部被過濾",
            "more_analysis_placeholder": "更多分析功能待拓展",
            "more_analysis_content": "拓展功能:\n\n• 文本複雜度分析\n• 關鍵詞提取\n• 情感分析\n• 可讀性分析\n• 語言風格分析\n",

            # 帮助窗口文本
            "function_intro": "功能介紹",
            "usage_instructions": "使用說明",
            "about": "關於",

            # 帮助窗口新增内容键
            "function_intro_content": """功能介紹
====================

主要功能說明：

1. 【按時間戳排序】
   • 將多個團的日誌混合在一起時，自動按時間順序整理
   • 幫助海豹骰整合多群信息，方便回顧

2. 【去重】
   • 去除因骰娘不能識別撤回等原因產生的重複內容
   • 可調節相似度閾值，智能識別近似重複行

3. 【錯別字修正】
   • 自動修正常見錯別字（支持簡中、繁中、英文）
   • 解決pl發錯別字，結團後忘記修改的問題

4. 【符號修正】
   • 自動補全句末缺失的句號
   • 修正左右引號顛倒、引號配對錯誤
   • 統一中英文標點格式

5. 【智能自動處理】
   • 一鍵執行去重、錯別字修正、符號修正
   • 快速優化整個文檔

6. 【統計分析】
   • 字數統計：中文字符、英文字母、數字、標點等
   • 平均RP長度：計算平均每行字符數
   • 詞雲分析：根據文檔語言智能生成詞雲（中文/英文/日文）
   • 標點符號使用統計

7. 【多格式導入導出】
   • 支持從 .txt、.doc、.docx 文件導入
   • 支持直接複製QQ聊天內容到編輯器
   • 可導出為 .txt 或 .docx 格式

8. 【多語言界面】
   • 支持簡體中文、繁體中文、英文、日文
   • 一鍵切換界面語言

更多功能持續開發中...
""",
            "usage_instructions_content": """使用說明
==========

基本操作流程：

1. 導入文本
   • 點擊“選擇文件”按鈕，導入 .txt/.doc/.docx 文件
   • 或直接將聊天記錄複製粘貼到編輯器中

2. 調整順序（可選）
   • 點擊“按時間戳排序”按鈕，自動將多個團的日誌按時間整理

3. 處理文本
   • 單獨處理：點擊“去重”、“錯別字修正”、“符號修正”分別執行
   • 批量處理：點擊“智能自動處理”一鍵完成所有優化

4. 查看分析
   • 點擊“智能分析”打開分析窗口，查看字數統計、詞雲、標點統計
   • 詞雲支持中/英/日文，自動過濾停用詞和無意義字符

5. 導出結果
   • 點擊“導出”按鈕，默認以“文本處理記錄.txt”為名保存
   • 若重名自動添加編號，可另選 .docx 格式

注意事項：

• 時間戳排序需文本中包含標準時間格式（如 2023-01-01 12:34:56）
如果時間缺損，如缺失日期，或跨年的記錄缺失年份，可能導致排序錯誤，遇到這種情況請分日期或年份分別導入
• 錯別字修正依賴百萬級語料庫，修正時間較長（200字/秒），請耐心等待
• 文本框中的修改支持撤銷/重做（Ctrl+Z / Ctrl+Y）

快捷鍵：

• Ctrl+Z: 撤銷
• Ctrl+Y: 重做
• F1: 顯示幫助

更多使用技巧請關注後續版本。
""",
            "about_content": """文本處理工具 v1.0

一款專為跑團日誌優化設計的文本處理軟件。

主要特點：
• 智能去重、錯別字修正、符號補全
• 多團日誌按時間戳自動排序
• 支持簡中/繁中/英文/日文界面
• 詞雲與字數統計可視化分析
• 直接複製粘貼或導入 txt/doc/docx

開發者：小雨
發布日期：2026年

感謝使用！您的支持是持續改進的動力。
""",

            # 支持窗口文本
            "thank_you_support": "感謝支持！",
            "support_author_title": "支持作者",
            "support_methods": "支持方式",

            # 支持窗口新增键
            "support_text_content": """感謝您使用文本處理工具！

如果您覺得這個軟件對您有幫助，請考慮支持我的開發工作。

支持方式：
• 分享給更多用戶
• 提供寶貴建議
• 反饋使用問題

聯繫郵箱：1163429473@qq.com
項目地址：https://github.com/Sam-ie/TPRG-Tool
""",
            "image_load_failed": "圖片加載失敗",
            "need_pil": "需安裝PIL",
            "please_place_image": "請放置圖片",
            "wechat_pay": "微信支付",

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
