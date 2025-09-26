import os
from typing import Optional, Tuple
from docx import Document
import pythoncom
import win32com.client


class FileManager:
    SUPPORTED_IMPORT_EXTENSIONS = ['.docx', '.doc', '.txt']
    SUPPORTED_EXPORT_EXTENSIONS = ['.docx', '.txt', '.pdf']

    @staticmethod
    def read_file(file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """读取文件内容，返回(内容, 错误信息)"""
        try:
            if not os.path.exists(file_path):
                return None, "文件不存在"

            ext = os.path.splitext(file_path)[1].lower()

            if ext == '.txt':
                # 尝试多种编码读取txt文件
                encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        return content, None
                    except UnicodeDecodeError:
                        continue
                return None, "无法解码文件编码"

            elif ext == '.docx':
                try:
                    doc = Document(file_path)
                    content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                    return content, None
                except Exception as e:
                    return None, f"读取docx文件失败: {str(e)}"

            elif ext == '.doc':
                try:
                    # 使用Word应用程序读取.doc文件
                    pythoncom.CoInitialize()
                    word = win32com.client.Dispatch("Word.Application")
                    word.Visible = False
                    doc = word.Documents.Open(file_path)
                    content = doc.Content.Text
                    doc.Close()
                    word.Quit()
                    pythoncom.CoUninitialize()
                    return content, None
                except Exception as e:
                    return None, f"读取doc文件失败: {str(e)}"

            else:
                return None, "不支持的文件格式"

        except Exception as e:
            return None, f"读取文件时发生错误: {str(e)}"

    @staticmethod
    def write_file(file_path: str, content: str, file_type: str) -> Optional[str]:
        """写入文件，返回错误信息（成功返回None）"""
        try:
            ext = os.path.splitext(file_path)[1].lower()

            if file_type == 'txt' or ext == '.txt':
                # 保存为txt文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return None

            elif file_type == 'docx' or ext == '.docx':
                # 保存为docx文件
                doc = Document()
                # 按行分割内容并添加到文档
                lines = content.split('\n')
                for line in lines:
                    doc.add_paragraph(line)
                doc.save(file_path)
                return None

            elif file_type == 'pdf' or ext == '.pdf':
                # TODO: 实现PDF导出功能
                return "PDF导出功能暂未实现"

            else:
                return "不支持的导出格式"

        except Exception as e:
            return f"保存文件时发生错误: {str(e)}"

    @staticmethod
    def is_supported_import_file(file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in FileManager.SUPPORTED_IMPORT_EXTENSIONS

    @staticmethod
    def is_supported_export_file(file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in FileManager.SUPPORTED_EXPORT_EXTENSIONS

    @staticmethod
    def get_file_filters(import_filter: bool = True) -> list:
        """获取文件过滤器"""
        if import_filter:
            return [
                ("支持的文件", "*.docx *.doc *.txt"),
                ("Word文档", "*.docx"),
                ("Word 97-2003文档", "*.doc"),
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        else:
            return [
                ("Word文档", "*.docx"),
                ("文本文件", "*.txt"),
                ("PDF文档", "*.pdf"),
                ("所有文件", "*.*")
            ]