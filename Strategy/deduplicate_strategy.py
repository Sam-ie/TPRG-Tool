# deduplicate_strategy.py
import re
from text_strategy import TextStrategy


class DeduplicateStrategy(TextStrategy):
    def execute(self, text_lines, threshold=0.85, min_length=5, case_sensitive=False):
        # 去重策略实现
        processed = []
        seen = set()

        for line in text_lines:
            if not self._should_process(line):
                processed.append(line)
                continue

            key = line.lower() if not case_sensitive else line
            if len(key) < min_length:
                processed.append(line)
                continue

            if key not in seen:
                seen.add(key)
                processed.append(line)
            else:
                # 标记为重复
                processed.append(f"【重复】{line}")

        return processed

    def _should_process(self, line):
        # 检查是否需要处理该行
        # 跳过空行和包含时间格式的行
        if not line.strip():
            return False

        time_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        return not re.match(time_pattern, line.strip())