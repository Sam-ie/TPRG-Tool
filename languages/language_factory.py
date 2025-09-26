from .base_language import BaseLanguage
from .chinese_simplified import ChineseSimplified
from .chinese_traditional import ChineseTraditional
from .english import English
from .japanese import Japanese


class LanguageFactory:
    """语言工厂类"""

    @staticmethod
    def create_language(language_code: str) -> BaseLanguage:
        """创建语言实例"""
        languages = {
            "zh_CN": ChineseSimplified,
            "zh_TW": ChineseTraditional,
            "en": English,
            "ja": Japanese
        }

        language_class = languages.get(language_code)
        if not language_class:
            # 默认返回简体中文
            language_class = ChineseSimplified

        return language_class()

    @staticmethod
    def get_available_languages() -> dict:
        """获取可用的语言列表"""
        return {
            "zh_CN": "简体中文",
            "zh_TW": "繁体中文",
            "en": "English",
            "ja": "日本語"
        }


# 导出到__init__.py的内容
__all__ = ['LanguageFactory', 'BaseLanguage']