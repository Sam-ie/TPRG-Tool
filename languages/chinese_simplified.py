from .base_language import BaseLanguage

class ChineseSimplified(BaseLanguage):
    """简体中文"""

    @property
    def language_code(self) -> str:
        return "zh_CN"

    @property
    def language_name(self) -> str:
        return "简体中文"

    def get_text(self, key: str) -> str:
        texts = {
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
            "language_label": "语言:",
            "sort_by_timestamp": "按时间戳排序",
            "reparse": "重新解析",

            # 弹窗标题
            "error": "错误",
            "info": "信息",
            "analysis_window_title": "智能分析",
            "help_window_title": "帮助",
            "support_window_title": "支持作者",

            # 错误和信息消息
            "no_content_to_export": "没有内容可导出",
            "file_load_success": "文件加载成功",
            "file_save_success": "文件保存成功",
            "please_load_file_first": "请先加载文件",
            "process_completed": "处理完成",
            "process_failed": "处理失败",
            "process_cancelled": "处理已取消",
            "smart_process_completed": "智能自动处理完成",
            "smart_process_failed": "智能自动处理失败",
            "smart_process_cancelled": "智能处理已取消",
            "no_timestamp_to_sort": "没有时间戳可排序",
            "no_content_to_reparse": "没有内容可重新解析",
            "unsupported_operation": "不支持的操作",

            # 分析窗口文本
            "word_count_stats": "字数统计",
            "wordcloud_analysis": "词云分析",
            "punctuation_analysis": "标点符号",
            "more_analysis": "更多分析",
            "basic_stats": "基本统计",
            "wordcloud_params": "词云参数",
            "max_words": "最大词语数",
            "generate_wordcloud": "生成词云",
            "punctuation_stats": "标点符号统计",
            "punctuation_symbol": "标点符号",
            "occurrence_count": "出现次数",
            "percentage": "占比",
            "expansion_features": "拓展功能",

            # 分析窗口新增键
            "no_content_stats": "暂无内容可统计",
            "total_chars": "总字符数",
            "chinese_chars": "中文字符数",
            "english_letters": "英文字母数",
            "digits": "数字数",
            "punctuation_chars": "标点符号数",
            "line_count": "行数",
            "avg_line_length": "平均行长度",
            "no_data": "无数据",
            "no_punctuation": "无标点符号",
            "wordcloud_lib_missing": "词云库未安装，无法生成\n请安装：jieba, wordcloud, pillow",
            "no_content_wordcloud": "无内容可生成词云",
            "wordcloud_display_area": "词云分析显示区域\n点击生成按钮",
            "wordcloud_missing_lib": "缺少词云库，无法生成",
            "wordcloud_empty_result": "分词结果为空或全部被过滤",
            "more_analysis_placeholder": "更多分析功能待拓展",
            "more_analysis_content": "拓展功能:\n\n• 文本复杂度分析\n• 关键词提取\n• 情感分析\n• 可读性分析\n• 语言风格分析\n",

            # 帮助窗口文本
            "function_intro": "功能介绍",
            "usage_instructions": "使用说明",
            "about": "关于",

            # 帮助窗口新增内容键
            "function_intro_content": """功能介绍
====================

主要功能说明：

1. 【按时间戳排序】
   • 将多个团的日志混合在一起时，自动按时间顺序整理
   • 帮助海豹骰整合多群信息，方便回顾

2. 【去重】
   • 去除因骰娘不能识别撤回等原因产生的重复内容
   • 可调节相似度阈值，智能识别近似重复行

3. 【错别字修正】
   • 自动修正常见错别字（支持简中、繁中、英文）
   • 解决pl发错别字，结团后忘记修改的问题

4. 【符号修正】
   • 自动补全句末缺失的句号
   • 修正左右引号颠倒、引号配对错误
   • 统一中英文标点格式

5. 【智能自动处理】
   • 一键执行去重、错别字修正、符号修正
   • 快速优化整个文档

6. 【统计分析】
   • 字数统计：中文字符、英文字母、数字、标点等
   • 平均RP长度：计算平均每行字符数
   • 词云分析：根据文档语言智能生成词云（中文/英文/日文）
   • 标点符号使用统计

7. 【多格式导入导出】
   • 支持从 .txt、.doc、.docx 文件导入
   • 支持直接复制QQ聊天内容到编辑器
   • 可导出为 .txt 或 .docx 格式

8. 【多语言界面】
   • 支持简体中文、繁体中文、英文、日文
   • 一键切换界面语言

更多功能持续开发中...
""",
            "usage_instructions_content": """使用说明
==========

基本操作流程：

1. 导入文本
   • 点击“选择文件”按钮，导入 .txt/.doc/.docx 文件
   • 或直接将聊天记录复制粘贴到编辑器中

2. 调整顺序（可选）
   • 点击“按时间戳排序”按钮，自动将多个团的日志按时间整理

3. 处理文本
   • 单独处理：点击“去重”、“错别字修正”、“符号修正”分别执行
   • 批量处理：点击“智能自动处理”一键完成所有优化

4. 查看分析
   • 点击“智能分析”打开分析窗口，查看字数统计、词云、标点统计
   • 词云支持中/英/日文，自动过滤停用词和无意义字符

5. 导出结果
   • 点击“导出”按钮，默认以“文本处理记录.txt”为名保存
   • 若重名自动添加编号，可另选 .docx 格式

注意事项：

• 时间戳排序需文本中包含标准时间格式（如 2023-01-01 12:34:56）
如果时间缺损，如缺失日期，或跨年的记录缺失年份，可能导致排序错误，遇到这种情况请分日期或年份分别导入
• 错别字修正依赖百万级语料库，修正时间较长（200字/秒），请耐心等待
• 文本框中的修改支持撤销/重做（Ctrl+Z / Ctrl+Y）

快捷键：

• Ctrl+Z: 撤销
• Ctrl+Y: 重做
• F1: 显示帮助

更多使用技巧请关注后续版本。
""",
            "about_content": """文本处理工具 v1.0

一款专为跑团日志优化设计的文本处理软件。

主要特点：
• 智能去重、错别字修正、符号补全
• 多团日志按时间戳自动排序
• 支持简中/繁中/英文/日文界面
• 词云与字数统计可视化分析
• 直接复制粘贴或导入 txt/doc/docx

开发者：小雨
发布日期：2026年

感谢使用！您的支持是持续改进的动力。
""",

            # 支持窗口文本
            "thank_you_support": "感谢支持！",
            "support_author_title": "支持作者",
            "support_methods": "支持方式",

            # 支持窗口新增键
            "support_text_content": """感谢您使用文本处理工具！

如果您觉得这个软件对您有帮助，请考虑支持我的开发工作。

支持方式：
• 分享给更多用户
• 提供宝贵建议
• 反馈使用问题

联系邮箱：1163429473@qq.com
项目地址：https://github.com/Sam-ie/TPRG-Tool
""",
            "image_load_failed": "图片加载失败",
            "need_pil": "需安装PIL",
            "please_place_image": "请放置图片",
            "wechat_pay": "微信支付",

            # 进度窗口文本
            "reading_file": "正在读取文件...",
            "processing": "正在处理",
            "completed": "完成",
            "file_read_complete": "文件读取完成",

            # 主窗口标题
            "main_window_title": "文本处理工具",

            # 文件管理器相关文本
            "file_not_exist": "文件不存在",
            "unsupported_format": "不支持的文件格式",
            "read_file_error": "读取文件时发生错误",
            "decode_error": "无法解码文件编码",
            "reading_file_progress": "读取文件中",
            "parsing_docx": "解析Word文档...",
            "converting_doc": "正在转换DOC格式...",
            "conversion_complete": "完成转换",
            "read_docx_error": "读取docx文件失败",
            "read_doc_error": "读取doc文件失败",
            "save_file_error": "保存文件时发生错误",
            "unsupported_export_format": "不支持的导出格式",

            # 文件过滤器文本
            "supported_files": "支持的文件",
            "word_documents": "Word文档",
            "word_97_2003_documents": "Word 97-2003文档",
            "text_files": "文本文件",
            "all_files": "所有文件",
        }
        return texts.get(key, key)
