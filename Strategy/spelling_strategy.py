# spelling_strategy.py
from text_strategy import TextStrategy
from collections import defaultdict
import re


class SpellingStrategy(TextStrategy):
    def execute(self, text_lines, lang='zh-cn'):
        # 基础拼写策略
        processed = []

        for line in text_lines:
            if not self._should_process(line):
                processed.append(line)
                continue

            # 简单的拼写修正逻辑
            corrected_line = self._basic_correction(line)
            processed.append(corrected_line)

        return processed, {}  # 返回空修正映射

    def _should_process(self, line):
        return bool(line.strip())

    def _basic_correction(self, line):
        # 基础修正逻辑
        corrections = {
            '。.': '。',
            '，，': '，',
            '。。': '。'
        }

        corrected_line = line
        for wrong, right in corrections.items():
            corrected_line = corrected_line.replace(wrong, right)

        return corrected_line