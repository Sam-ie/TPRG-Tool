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
            "smart_process_failed": "智能自动处理失败",

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

            # 帮助窗口文本
            "function_intro": "功能介绍",
            "usage_instructions": "使用说明",
            "about": "关于",

            # 支持窗口文本
            "thank_you_support": "感谢支持！",
            "support_author_title": "支持作者",
            "support_methods": "支持方式",
            "close": "关闭",
        }
        return texts.get(key, key)