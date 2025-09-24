# model.py
from subject import Subject
from FileProcessor.text_processor_file import TextFileProcessor
from FileProcessor.file_handler import FileHandler
from Language.lang_manager import LangManager

class ApplicationModel(Subject):
    def __init__(self):
        super().__init__()
        self.file_paths = []
        self.text_content = []
        self.processed_text = []
        self.lang_config = LangManager.get_config('zh-cn')
        self.processor_params = {
            'similarity_threshold': 0.85,
            'min_length': 5,
            'case_sensitive': False
        }
        self.text_processor = TextFileProcessor()
        self.file_handler = FileHandler()
        self.modifiable_params = ['similarity_threshold', 'min_length', 'case_sensitive']

    def set_files(self, paths):
        self.file_paths = paths
        self.text_content = self.file_handler.read_files(paths)
        self._notify_observers()

    def get_files(self):
        return self.file_paths

    def process_text(self, operation_type):
        if operation_type == '去重':
            self.processed_text = self.text_processor.remove_duplicates(
                self.text_content,
                threshold=self.processor_params['similarity_threshold'],
                min_length=self.processor_params['min_length'],
                case_sensitive=self.processor_params['case_sensitive']
            )
        elif operation_type == '去错别字':
            self.processed_text = self.text_processor.remove_spelling_errors(self.text_content)
        # 其他操作处理...

    def export_files(self, output_path, format_type):
        return self.file_handler.export_files(self.processed_text, output_path, format_type)