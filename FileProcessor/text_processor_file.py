# text_processor_file.py
import chardet


class TextFileProcessor:
    def read_file(self, path):
        # 读取文本文件，自动检测编码
        with open(path, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding']

            # 如果检测失败，尝试常见编码
            if not encoding:
                encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
                for enc in encodings:
                    try:
                        text = raw_data.decode(enc)
                        return text.split('\n')
                    except UnicodeDecodeError:
                        continue
                raise Exception(f"无法解码文件: {path}")

            try:
                text = raw_data.decode(encoding)
                return text.split('\n')
            except UnicodeDecodeError:
                raise Exception(f"编码检测失败: {path}")

    def export_file(self, text, output_path):
        # 导出为文本文件
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in text:
                f.write(line + '\n')
        return True