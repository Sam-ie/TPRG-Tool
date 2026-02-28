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
            if entry.player_name and entry.timestamp:
                lines.append(f"{entry.player_name}: {entry.timestamp}")
            elif entry.timestamp:
                lines.append(entry.timestamp)

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

    def process_text(self, operation: str,
                     progress_callback: Callable[[int, int, str], None] = None,
                     stop_check: Optional[Callable[[], bool]] = None) -> Tuple[bool, str]:
        """
        处理文本（去重、错别字修正、符号修正）
        :param operation: 'deduplicate', 'spell_check', 'correct_symbols'
        :param progress_callback: 进度回调函数，参数 (current, total, status)
        :param stop_check: 可选函数，返回True表示应停止处理
        """
        if not self.entries:
            return False, "please_load_file_first"

        try:
            if operation == 'deduplicate':
                self.entries = self.processor_manager.deduplicate_entries(
                    self.entries, self.similarity_threshold
                )
            elif operation == 'spell_check':
                # 收集所有需要处理的段落
                paragraph_tasks = []  # (entry, paragraph_index, text)
                for entry in self.entries:
                    paragraphs = entry.content.split('\n')
                    for p_idx, para in enumerate(paragraphs):
                        if para.strip():
                            paragraph_tasks.append((entry, p_idx, para))
                total = len(paragraph_tasks)
                if total == 0:
                    return True, "process_completed"

                for i, (entry, p_idx, para) in enumerate(paragraph_tasks):
                    # 检查是否应取消
                    if stop_check and stop_check():
                        # 停止处理，返回成功（已处理部分有效）
                        return True, "process_cancelled"

                    result, _ = self.processor_manager.process_text('spell_check', para)
                    # 更新该段落
                    paras = entry.content.split('\n')
                    paras[p_idx] = result
                    entry.content = '\n'.join(paras)
                    if progress_callback:
                        progress_callback(i + 1, total, f"处理段落 {i + 1}/{total}")
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
        """智能自动处理：先去重，再对每个段落做符号修正和错别字修正"""
        if not self.entries:
            return False, "please_load_file_first"

        try:
            # 先去重（通常较快，不设进度）
            self.entries = self.processor_manager.deduplicate_entries(
                self.entries, self.similarity_threshold
            )

            # 收集所有需要处理的段落
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

                # 符号修正
                corrected, _ = self.processor_manager.process_text('correct_symbols', para)
                # 错别字修正
                final, _ = self.processor_manager.process_text('spell_check', corrected)
                # 更新段落
                paras = entry.content.split('\n')
                paras[p_idx] = final
                entry.content = '\n'.join(paras)
                if progress_callback:
                    progress_callback(i + 1, total, f"智能处理段落 {i + 1}/{total}")

            return True, "smart_process_completed"
        except Exception as e:
            return False, "smart_process_failed"
