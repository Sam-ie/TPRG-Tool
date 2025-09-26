from abc import ABC, abstractmethod
from typing import List, Tuple
import re


class BaseTextProcessor(ABC):
    """文本处理器的基类"""

    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold

    @abstractmethod
    def deduplicate(self, text: str) -> Tuple[str, List[dict]]:
        """去重处理"""
        pass

    @abstractmethod
    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        """错别字修正"""
        pass

    @abstractmethod
    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        """符号修正"""
        pass

    def should_skip_line(self, line: str) -> bool:
        """判断是否应该跳过该行处理"""
        if not line.strip():  # 空行
            return True

        # 检测时间字符串模式（跑团log格式）
        time_patterns = [
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',  # 2025-09-21 21:33:30
            r'\d{2}:\d{2}:\d{2}',  # 21:33:30
        ]

        for pattern in time_patterns:
            if re.search(pattern, line):
                return True

        return False


class ChineseSimplifiedProcessor(BaseTextProcessor):
    """简体中文文本处理器"""

    def deduplicate(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现简体中文去重逻辑
        print("使用简体中文去重处理器")
        return text, []

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现简体中文错别字修正
        print("使用简体中文错别字修正处理器")
        return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现简体中文符号修正
        print("使用简体中文符号修正处理器")
        return text, []


class ChineseTraditionalProcessor(BaseTextProcessor):
    """繁体中文文本处理器"""

    def deduplicate(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现繁体中文去重逻辑
        print("使用繁体中文去重处理器")
        return text, []

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现繁体中文错别字修正
        print("使用繁体中文错别字修正处理器")
        return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现繁体中文符号修正
        print("使用繁体中文符号修正处理器")
        return text, []


class EnglishProcessor(BaseTextProcessor):
    """英文文本处理器"""

    def deduplicate(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现英文去重逻辑
        print("使用英文去重处理器")
        return text, []

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现英文拼写检查
        print("使用英文拼写检查处理器")
        return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现英文符号修正
        print("使用英文符号修正处理器")
        return text, []


class JapaneseProcessor(BaseTextProcessor):
    """日文文本处理器"""

    def deduplicate(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现日文去重逻辑
        print("使用日文去重处理器")
        return text, []

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现日文错别字修正
        print("使用日文错别字修正处理器")
        return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        # TODO: 实现日文符号修正
        print("使用日文符号修正处理器")
        return text, []


class TextProcessorFactory:
    """文本处理器工厂"""

    @staticmethod
    def create_processor(language: str, similarity_threshold: float = 0.8) -> BaseTextProcessor:
        processors = {
            'zh_CN': ChineseSimplifiedProcessor,
            'zh_TW': ChineseTraditionalProcessor,
            'en': EnglishProcessor,
            'ja': JapaneseProcessor
        }

        processor_class = processors.get(language, ChineseSimplifiedProcessor)
        return processor_class(similarity_threshold)


class TextProcessorManager:
    """文本处理器管理器"""

    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold
        self.current_processor = None

    def set_language(self, language: str):
        """根据语言设置对应的处理器"""
        self.current_processor = TextProcessorFactory.create_processor(
            language, self.similarity_threshold
        )

    def process_text(self, operation: str, text: str) -> Tuple[str, List[dict]]:
        """处理文本"""
        if not self.current_processor:
            raise ValueError("未设置文本处理器")

        operations = {
            'deduplicate': self.current_processor.deduplicate,
            'spell_check': self.current_processor.spell_check,
            'correct_symbols': self.current_processor.correct_symbols
        }

        processor_func = operations.get(operation)
        if not processor_func:
            raise ValueError(f"不支持的操作: {operation}")

        return processor_func(text)

    def smart_auto_process(self, text: str) -> Tuple[str, List[dict]]:
        """智能自动处理（组合多个处理功能）"""
        if not self.current_processor:
            raise ValueError("未设置文本处理器")

        # TODO: 实现智能自动处理逻辑
        print("执行智能自动处理")
        return text, []