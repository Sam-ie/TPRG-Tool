from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from .language_detector import LanguageDetector
from .text_processor import TextProcessorManager
from utils.file_manager import FileManager


@dataclass
class TextModification:
    original_text: str
    modified_text: str
    modification_type: str
    position: int
    line_number: int


class DocumentModel:
    def __init__(self, similarity_threshold: float = 0.8):
        self.file_path = ""
        self.original_content = ""
        self.modified_content = ""
        self.modifications: List[TextModification] = []
        self.current_modification_index = -1
        self.detected_language = "zh_CN"
        self._observers = []

        # 文本处理器管理器
        self.processor_manager = TextProcessorManager(similarity_threshold)

    def add_observer(self, observer):
        """添加观察者"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """移除观察者"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type: str = "content_updated"):
        """通知所有观察者"""
        for observer in self._observers:
            if hasattr(observer, 'on_model_updated'):
                observer.on_model_updated(self, event_type)

    def load_file_with_content(self, file_path: str, content: str) -> Tuple[bool, str]:
        """使用已有内容加载文件"""
        self.file_path = file_path
        self.original_content = content
        self.modified_content = content

        # 检测语言并设置对应的处理器
        self.detected_language = LanguageDetector.detect_language(content)
        self.processor_manager.set_language(self.detected_language)

        # 通知观察者内容已更新
        self.notify_observers("file_loaded")
        return True, "file_load_success"

    def save_file(self, file_path: str, file_type: str) -> Tuple[bool, str]:
        """保存文件，返回(成功与否, 错误信息)"""
        if not self.modified_content:
            return False, "no_content_to_export"

        error = FileManager.write_file(file_path, self.modified_content, file_type)
        if error:
            return False, error

        return True, "file_save_success"

    def process_text(self, operation: str) -> Tuple[bool, str]:
        """处理文本，返回(成功与否, 错误信息)"""
        if not self.original_content:
            return False, "please_load_file_first"

        try:
            result, modifications = self.processor_manager.process_text(
                operation, self.original_content
            )
            self.modified_content = result
            # TODO: 将modifications转换为TextModification对象

            # 通知观察者内容已修改
            self.notify_observers("content_modified")
            return True, "process_completed"
        except Exception as e:
            return False, "process_failed"

    def smart_auto_process(self) -> Tuple[bool, str]:
        """智能自动处理，返回(成功与否, 错误信息)"""
        if not self.original_content:
            return False, "please_load_file_first"

        try:
            result, modifications = self.processor_manager.smart_auto_process(
                self.original_content
            )
            self.modified_content = result
            # TODO: 将modifications转换为TextModification对象

            # 通知观察者内容已修改
            self.notify_observers("content_modified")
            return True, "smart_process_completed"
        except Exception as e:
            return False, "smart_process_failed"