# lang_manager.py
import json
import os


class LangManager:
    SUPPORTED_LANGS = ['zh-cn', 'zh-tw', 'en', 'ja']
    LOCALEDIR = 'languages'

    @staticmethod
    def get_config(lang_code):
        """获取语言配置"""
        if lang_code not in LangManager.SUPPORTED_LANGS:
            lang_code = 'zh-cn'  # 默认简体中文

        config_path = os.path.join(LangManager.LOCALEDIR, f"{lang_code}.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 如果文件不存在，返回默认配置
            return LangManager._get_default_config(lang_code)
        except Exception as e:
            print(f"加载语言配置时出错: {e}")
            return LangManager._get_default_config('zh-cn')

    @staticmethod
    def _get_default_config(lang_code):
        """获取默认配置"""
        default_configs = {
            'zh-cn': {
                "browse": "浏览文件",
                "deduplicate": "去重",
                "correct_spelling": "去错别字",
                "correct_punctuation": "修正符号",
                "auto_process": "自动处理",
                "analyze": "分析",
                "export": "导出",
                "help": "帮助",
                "switch_language": "切换语言",
                "donate": "支持作者",
                "no_files_selected": "未选择文件",
                "invalid_lang": "不支持的语言代码",
                "wordcloud_title": "词频统计",
                "stats_title": "文本统计",
                "network_title": "文本网络",
                "analyze_title": "文本分析",
                "processing_error": "处理错误",
                "prev": "上一页",
                "next": "下一页",
                "total_words": "总词数",
                "unique_words": "唯一词数",
                "total_lines": "总行数",
                "punctuation_count": "标点符号数",
                "refresh": "刷新",
                "export_chart": "导出图表"
            },
            'en': {
                "browse": "Browse",
                "deduplicate": "Remove Duplicates",
                "correct_spelling": "Correct Spelling",
                "correct_punctuation": "Correct Punctuation",
                "auto_process": "Auto Process",
                "analyze": "Analyze",
                "export": "Export",
                "help": "Help",
                "switch_language": "Switch Language",
                "donate": "Support",
                "no_files_selected": "No files selected",
                "invalid_lang": "Invalid language code",
                "wordcloud_title": "Word Cloud",
                "stats_title": "Text Statistics",
                "network_title": "Text Network",
                "analyze_title": "Text Analysis",
                "processing_error": "Processing error",
                "prev": "Previous",
                "next": "Next",
                "total_words": "Total Words",
                "unique_words": "Unique Words",
                "total_lines": "Total Lines",
                "punctuation_count": "Punctuation Count",
                "refresh": "Refresh",
                "export_chart": "Export Charts"
            }
        }

        return default_configs.get(lang_code, default_configs['zh-cn'])

    @staticmethod
    def supported_langs():
        """获取支持的语言列表"""
        return LangManager.SUPPORTED_LANGS

    @staticmethod
    def create_language_files():
        """创建语言文件（如果不存在）"""
        if not os.path.exists(LangManager.LOCALEDIR):
            os.makedirs(LangManager.LOCALEDIR)

        # 创建英文语言文件
        en_config = LangManager._get_default_config('en')
        en_file = os.path.join(LangManager.LOCALEDIR, 'en.json')
        with open(en_file, 'w', encoding='utf-8') as f:
            json.dump(en_config, f, ensure_ascii=False, indent=2)

        # 创建中文语言文件
        zh_cn_config = LangManager._get_default_config('zh-cn')
        zh_cn_file = os.path.join(LangManager.LOCALEDIR, 'zh-cn.json')
        with open(zh_cn_file, 'w', encoding='utf-8') as f:
            json.dump(zh_cn_config, f, ensure_ascii=False, indent=2)