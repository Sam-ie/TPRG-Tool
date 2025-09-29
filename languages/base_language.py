from abc import ABC, abstractmethod


class BaseLanguage(ABC):
    """语言基类"""

    @property
    @abstractmethod
    def language_code(self) -> str:
        """返回语言代码"""
        pass

    @property
    @abstractmethod
    def language_name(self) -> str:
        """返回语言名称"""
        pass

    @abstractmethod
    def get_text(self, key: str) -> str:
        """获取翻译文本"""
        pass
