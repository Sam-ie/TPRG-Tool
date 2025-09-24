# doc_processor.py
import os
import tempfile
import subprocess


class DocProcessor:
    def __init__(self):
        self._libreoffice_path = self._find_libreoffice()

    def _find_libreoffice(self):
        # 查找libreoffice命令路径
        try:
            # 在Windows上可能是不同的路径
            if os.name == 'nt':
                # Windows路径示例
                possible_paths = [
                    r"C:\Program Files\LibreOffice\program\soffice.exe",
                    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        return path
                return None
            else:
                # Linux/Mac
                return subprocess.check_output(['which', 'soffice']).decode().strip()
        except Exception:
            return None

    def read_file(self, path):
        # 读取doc文件，需要libreoffice
        if not self._libreoffice_path:
            raise FileNotFoundError("未找到libreoffice命令，请安装libreoffice以处理.doc文件")

        temp_dir = tempfile.mkdtemp()
        docx_path = os.path.join(temp_dir, 'temp.docx')

        try:
            # 转换doc到docx
            if os.name == 'nt':
                # Windows命令
                subprocess.run([
                    self._libreoffice_path,
                    "--headless",
                    "--convert-to", "docx",
                    "--outdir", temp_dir,
                    path
                ], check=True, shell=True)
            else:
                # Linux/Mac命令
                subprocess.run([
                    self._libreoffice_path,
                    "--headless",
                    "--convert-to", "docx",
                    "--outdir", temp_dir,
                    path
                ], check=True)

            # 使用docx处理器读取转换后的文件
            from docx_processor import DocxProcessor
            return DocxProcessor().read_file(docx_path)
        finally:
            # 清理临时文件
            if os.path.exists(docx_path):
                os.remove(docx_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)