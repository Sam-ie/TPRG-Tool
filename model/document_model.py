import re
from typing import List, Tuple, Optional, Any
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


def parse_log_entries(text: str, use_timestamp_parsing: bool = True) -> List[LogEntry]:
    """将原始文本解析为 LogEntry 列表。"""
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

    time_patterns = [
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
        r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
        r'\d{2}:\d{2}:\d{2}',
    ]
    compiled = [re.compile(p) for p in time_patterns]

    current_entry: Optional[LogEntry] = None

    for line in lines:
        stripped = line.rstrip('\n')
        if not stripped.strip():
            continue

        match_obj = None
        for pattern in compiled:
            match = pattern.search(stripped)
            if match:
                match_obj = match
                break

        if match_obj:
            if current_entry:
                entries.append(current_entry)

            entry_id += 1
            start, end = match_obj.start(), match_obj.end()
            player_name = stripped[:start].strip()
            player_name = player_name.rstrip(' :：')
            timestamp = match_obj.group()
            rest = stripped[end:].strip()
            current_entry = LogEntry(
                id=entry_id,
                player_name=player_name,
                timestamp=timestamp,
                content=rest
            )
        else:
            if current_entry:
                line_content = stripped.strip()
                if line_content:
                    if current_entry.content:
                        current_entry.content += '\n' + line_content
                    else:
                        current_entry.content = line_content

    if current_entry:
        entries.append(current_entry)

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
        self.notify_observers("file_loaded")
        return True, "file_load_success"

    def reparse_entries(self, content: str) -> None:
        self.entries = parse_log_entries(content, self.use_timestamp_parsing)
        self.detected_language = LanguageDetector.detect_language(content)
        self.processor_manager.set_language(self.detected_language)
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
                lines.append(f"{entry.player_name}： {display_time}")
            elif entry.timestamp:
                lines.append(display_time)

            content_parts = entry.content.split('\n') if entry.content else [""]
            for part in content_parts:
                if part.strip():
                    lines.append(part)

            if i < len(self.entries) - 1:
                lines.append("")

        return '\n'.join(lines)

    def sort_by_timestamp(self) -> bool:
        if not self.entries:
            return False
        if all(not entry.timestamp for entry in self.entries):
            return False
        self.entries.sort(key=lambda e: (e.timestamp == "", e.timestamp))
        for idx, entry in enumerate(self.entries, start=1):
            entry.id = idx
        self.notify_observers("entries_updated")
        return True

    def process_text(self, operation: str) -> Tuple[bool, str]:
        if not self.entries:
            return False, "please_load_file_first"

        try:
            if operation == 'deduplicate':
                self.entries = self.processor_manager.deduplicate_entries(
                    self.entries, self.similarity_threshold
                )
            else:
                for entry in self.entries:
                    result, modifications = self.processor_manager.process_text(operation, entry.content)
                    entry.content = result

            self.notify_observers("content_modified")
            return True, "process_completed"
        except Exception as e:
            print(f"处理失败: {e}")
            return False, "process_failed"

    def smart_auto_process(self) -> Tuple[bool, str]:
        if not self.entries:
            return False, "please_load_file_first"

        try:
            self.entries = self.processor_manager.deduplicate_entries(
                self.entries, self.similarity_threshold
            )

            for entry in self.entries:
                result, _ = self.processor_manager.text_processor(entry.content)
                entry.content = result
            self.notify_observers("content_modified")
            return True, "smart_process_completed"
        except Exception as e:
            return False, "smart_process_failed"

    def save_file(self, file_path: str, file_type: str) -> Tuple[bool, str]:
        if not self.entries:
            return False, "no_content_to_export"
        full_text = self.get_display_text()
        from utils.file_manager import FileManager
        error = FileManager.write_file(file_path, full_text, file_type)
        if error:
            return False, error
        return True, "file_save_success"
