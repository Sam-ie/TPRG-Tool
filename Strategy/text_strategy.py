# text_strategy.py
from abc import ABC, abstractmethod

class TextStrategy(ABC):
    @abstractmethod
    def execute(self, text_lines, **kwargs):
        pass