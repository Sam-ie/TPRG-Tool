import re
from typing import List, Tuple, Optional, Any, Callable
from dataclasses import dataclass
from .language_detector import LanguageDetector
from .text_processor import TextProcessorManager


@dataclass
class LogEntry:
    """表示一条日志记录"""
    id: int                     # 条目序号（从1开始）
    player_name: str            # 玩家名（可能为空）
    timestamp: str              # 时间戳字符串（可能为空）
    content: str                # 正文内容（可能跨行，用换行符分隔）
    entry_type: str = ""        # 类型：KP, PL, OB, BOT（由_classify_entry_types设置）


def parse_log_entries(text: str, use_timestamp_parsing: bool = True) -> List[LogEntry]:
    """
    将原始文本解析为 LogEntry 列表。
    支持标准时间戳格式和尖括号玩家名格式（无时间戳）。
    时间戳格式（按优先级）：
      - YYYY-MM-DD HH:MM:SS
      - YYYY/MM/DD: HH:MM:SS 或 YYYY/MM/DD HH:MM:SS
      - MM-DD HH:MM:SS
      - HH:MM:SS
    尖括号格式：<player_name>: content 或 <player_name>：content
    """
    lines = text.splitlines()
    entries = []
    entry_id = 0

    if not use_timestamp_parsing:
        for line in lines:
            stripped = line.rstrip('\n')
            if not stripped.strip():
                continue
            entry_id += 1
            entries.append(LogEntry(
                id=entry_id,
                player_name="",
                timestamp="",
                content=stripped.strip()
            ))
        return entries

    # 时间戳匹配模式
    time_patterns = [
        r'\d{4}/\d{2}/\d{2}[:] \d{2}:\d{2}:\d{2}',     # 2026/02/26: 00:00:05 或 2026/02/26 00:00:05
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',        # 2025-09-21 21:33:30
        r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}',              # 09-21 21:33:30
        r'\d{2}:\d{2}:\d{2}',                          # 21:33:30
    ]
    compiled_time = [re.compile(p) for p in time_patterns]

    # 尖括号玩家名模式（无时间戳）
    player_pattern = re.compile(r'^<([^>]+)>[：:]\s*(.*)')

    current_entry: Optional[LogEntry] = None

    for line in lines:
        stripped = line.rstrip('\n')
        if not stripped.strip():
            continue

        # 1. 尝试匹配时间戳
        match_obj = None
        for pattern in compiled_time:
            match = pattern.search(stripped)
            if match:
                match_obj = match
                break

        if match_obj:
            # 有时间戳，开始新条目
            if current_entry:
                entries.append(current_entry)

            entry_id += 1
            start, end = match_obj.start(), match_obj.end()
            player_name = stripped[:start].strip()
            player_name = player_name.rstrip(' :：')
            timestamp = match_obj.group()
            # 标准化时间戳：将日期和时间之间的冒号（如果有）替换为空格
            timestamp = re.sub(r'(\d{4}/\d{2}/\d{2}):\s*(\d{2}:\d{2}:\d{2})', r'\1 \2', timestamp)
            rest = stripped[end:].strip()
            current_entry = LogEntry(
                id=entry_id,
                player_name=player_name,
                timestamp=timestamp,
                content=rest
            )
        else:
            # 2. 无时间戳，尝试匹配尖括号玩家名
            player_match = player_pattern.match(stripped)
            if player_match:
                # 新条目（无时间戳）
                if current_entry:
                    entries.append(current_entry)

                entry_id += 1
                player_name = player_match.group(1).strip()
                content = player_match.group(2).strip()
                current_entry = LogEntry(
                    id=entry_id,
                    player_name=player_name,
                    timestamp="",
                    content=content
                )
            else:
                # 3. 既无时间戳也无玩家名，作为当前条目的续行
                if current_entry:
                    line_content = stripped.strip()
                    if line_content:
                        if current_entry.content:
                            current_entry.content += '\n' + line_content
                        else:
                            current_entry.content = line_content

    if current_entry:
        entries.append(current_entry)

    # 如果最终没有任何条目（全空行），则将非空行作为无格式条目处理
    if not entries:
        entry_id = 0
        for line in lines:
            stripped = line.rstrip('\n')
            if not stripped.strip():
                continue
            entry_id += 1
            entries.append(LogEntry(
                id=entry_id,
                player_name="",
                timestamp="",
                content=stripped.strip()
            ))

    return entries


class DocumentModel:
    def __init__(self, similarity_threshold: float = 0.8):
        self.file_path: str = ""
        self.entries: List[LogEntry] = []
        self.detected_language: str = "zh_CN"
        self.similarity_threshold = similarity_threshold
        self.processor_manager = TextProcessorManager(similarity_threshold)
        self._observers: List[Any] = []

        self.use_timestamp_parsing: bool = True
        self.operation_stack: List[Any] = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type: str = "entries_updated"):
        for observer in self._observers:
            if hasattr(observer, 'on_model_updated'):
                observer.on_model_updated(self, event_type)

    def set_timestamp_parsing_enabled(self, enabled: bool):
        self.use_timestamp_parsing = enabled

    def load_file_with_content(self, file_path: str, content: str) -> Tuple[bool, str]:
        self.file_path = file_path
        self.entries = parse_log_entries(content, self.use_timestamp_parsing)
        self.detected_language = LanguageDetector.detect_language(content)
        self.processor_manager.set_language(self.detected_language)
        self._classify_entry_types()
        self.notify_observers("file_loaded")
        return True, "file_load_success"

    def reparse_entries(self, content: str) -> None:
        self.entries = parse_log_entries(content, self.use_timestamp_parsing)
        self.detected_language = LanguageDetector.detect_language(content)
        self.processor_manager.set_language(self.detected_language)
        self._classify_entry_types()
        self.notify_observers("entries_updated")

    def get_display_text(self) -> str:
        """生成显示文本，时间戳只显示时间部分"""
        lines = []
        for i, entry in enumerate(self.entries):
            display_time = ""
            if entry.timestamp:
                parts = entry.timestamp.split()
                if len(parts) > 1:
                    display_time = parts[-1]
                else:
                    display_time = entry.timestamp

            if entry.player_name and entry.timestamp:
                lines.append(f"{entry.player_name} {display_time}")
            elif entry.timestamp:
                lines.append(display_time)
            elif entry.player_name:
                # 无时间戳但玩家名存在（尖括号格式），只显示玩家名
                lines.append(f"{entry.player_name}")

            content_parts = entry.content.split('\n') if entry.content else [""]
            for part in content_parts:
                if part.strip():
                    lines.append(part)

            if i < len(self.entries) - 1:
                lines.append("")

        return '\n'.join(lines)

    def sort_by_timestamp(self) -> bool:
        """按时间戳排序（简单字符串排序，保持原有逻辑）"""
        if not self.entries:
            return False
        if all(not entry.timestamp for entry in self.entries):
            return False
        self.entries.sort(key=lambda e: (e.timestamp == "", e.timestamp))
        for idx, entry in enumerate(self.entries, start=1):
            entry.id = idx
        self.notify_observers("entries_updated")
        return True

    def _classify_entry_types(self):
        """根据统计给每个 entry 分配类型：KP, PL, OB, BOT"""
        if not self.entries:
            return

        player_stats = {}
        total_content_chars = 0
        for entry in self.entries:
            name = entry.player_name
            if name not in player_stats:
                player_stats[name] = {
                    'count': 0,
                    'has_eq_count': 0,
                    'char_count': 0,
                }
            player_stats[name]['count'] += 1
            if '=' in entry.content:
                player_stats[name]['has_eq_count'] += 1
            chars = len(entry.content)
            player_stats[name]['char_count'] += chars
            total_content_chars += chars

        if not player_stats:
            return

        # 找出发言次数最多的玩家（排除空名）
        valid_names = [name for name in player_stats if name]
        if not valid_names:
            # 所有玩家名都为空，则没有KP
            kp_name = None
        else:
            kp_name = max(valid_names, key=lambda n: player_stats[n]['count'])

        for entry in self.entries:
            name = entry.player_name
            stats = player_stats[name]

            if name == kp_name:
                entry.entry_type = 'KP'
            elif stats['has_eq_count'] / stats['count'] > 0.4:
                entry.entry_type = 'BOT'
            elif stats['char_count'] / total_content_chars < 0.01:
                entry.entry_type = 'OB'
            else:
                entry.entry_type = 'PL'

    def process_text(self, operation: str,
                     progress_callback: Callable[[int, int, str], None] = None,
                     stop_check: Optional[Callable[[], bool]] = None) -> Tuple[bool, str]:
        """处理文本"""
        if not self.entries:
            return False, "please_load_file_first"

        try:
            if operation == 'deduplicate':
                # 定义跳过条件
                def skip_cond(entry):
                    if entry.entry_type == 'BOT':
                        return True
                    content = entry.content
                    if content and (content[0] in ('（', '(', '.', '。') or
                                    content.startswith('<img') or content.startswith('[CQ:')):
                        return True
                    special_keywords = [".r", ".log", ".game", "="]
                    if any(keyword in content for keyword in special_keywords):
                        return True
                    return False

                self.entries = self.processor_manager.deduplicate_entries(
                    self.entries, self.similarity_threshold, skip_cond
                )
            elif operation == 'spell_check':
                # 收集所有需要处理的段落
                paragraph_tasks = []
                for entry in self.entries:
                    paragraphs = entry.content.split('\n')
                    for p_idx, para in enumerate(paragraphs):
                        if para.strip():
                            paragraph_tasks.append((entry, p_idx, para))
                total = len(paragraph_tasks)
                if total == 0:
                    return True, "process_completed"

                for i, (entry, p_idx, para) in enumerate(paragraph_tasks):
                    if stop_check and stop_check():
                        return True, "process_cancelled"
                    result, _ = self.processor_manager.process_text('spell_check', para)
                    paras = entry.content.split('\n')
                    paras[p_idx] = result
                    entry.content = '\n'.join(paras)
                    if progress_callback:
                        progress_callback(i + 1, total, f"处理段落 {i+1}/{total}")
            elif operation == 'correct_symbols':
                for entry in self.entries:
                    result, _ = self.processor_manager.process_text('correct_symbols', entry.content)
                    entry.content = result
            else:
                return False, "unsupported_operation"

            return True, "process_completed"
        except Exception as e:
            print(f"处理失败: {e}")
            return False, "process_failed"

    def smart_auto_process(self,
                           progress_callback: Callable[[int, int, str], None] = None,
                           stop_check: Optional[Callable[[], bool]] = None) -> Tuple[bool, str]:
        """智能自动处理：先去重，再符号修正，最后错别字修正"""
        if not self.entries:
            return False, "please_load_file_first"

        try:
            # 先去重
            def skip_cond(entry):
                if entry.entry_type == 'BOT':
                    return True
                content = entry.content
                if content and (content[0] in ('（', '(', '.', '。') or
                                content.startswith('<img') or content.startswith('[CQ:')):
                    return True
                special_keywords = [".r", ".log", ".game", "="]
                if any(keyword in content for keyword in special_keywords):
                    return True
                return False

            self.entries = self.processor_manager.deduplicate_entries(
                self.entries, self.similarity_threshold, skip_cond
            )

            # 收集段落
            paragraph_tasks = []
            for entry in self.entries:
                paragraphs = entry.content.split('\n')
                for p_idx, para in enumerate(paragraphs):
                    if para.strip():
                        paragraph_tasks.append((entry, p_idx, para))
            total = len(paragraph_tasks)
            if total == 0:
                return True, "smart_process_completed"

            for i, (entry, p_idx, para) in enumerate(paragraph_tasks):
                if stop_check and stop_check():
                    return True, "smart_process_cancelled"
                corrected, _ = self.processor_manager.process_text('correct_symbols', para)
                final, _ = self.processor_manager.process_text('spell_check', corrected)
                paras = entry.content.split('\n')
                paras[p_idx] = final
                entry.content = '\n'.join(paras)
                if progress_callback:
                    progress_callback(i + 1, total, f"智能处理段落 {i+1}/{total}")

            return True, "smart_process_completed"
        except Exception as e:
            return False, "smart_process_failed"
