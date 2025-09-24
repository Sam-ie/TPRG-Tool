# symbol_strategy.py
from text_strategy import TextStrategy
import re

class SymbolStrategy(TextStrategy):
    def execute(self, text_lines):
        # 符号修正策略
        processed = []

        # 定义全角符号映射表
        full_width_symbol_map = {
            '!': '！',
            '?': '？',
            '(': '（',
            ')': '）',
            '[': '【',
            ']': '】',
            '{': '《',
            '}': '》'
        }

        for line in text_lines:
            if not self._should_process(line):
                processed.append(line)
                continue

            # 修正英文标点为中文全角
            corrected_line = line
            for half, full in full_width_symbol_map.items():
                corrected_line = corrected_line.replace(half, full)

            # 补全句号等符号
            if not corrected_line.endswith(('.', '。', '!', '！', '?', '？')):
                corrected_line += '。'

            processed.append(corrected_line)

        return processed

    def _should_process(self, line):
        return bool(line.strip())