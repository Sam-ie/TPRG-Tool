import re
from typing import Optional


class LanguageDetector:
    @staticmethod
    def detect_language(text: str) -> str:
        """
        检测文本的语言
        返回: 'zh_CN', 'zh_TW', 'en', 'ja'
        """
        # 采样部分文本进行检测
        sample = text[:1000] if len(text) > 1000 else text

        # 检测日语（包含平假名、片假名、汉字）
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', sample):
            # 进一步区分简体中文、繁体中文和日语
            jp_chars = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF]', sample))
            cn_chars = len(re.findall(r'[\u4E00-\u9FFF]', sample))

            if jp_chars > cn_chars * 0.3:  # 日语字符比例较高
                return 'ja'
            else:
                # 检测繁体中文特征
                traditional_chars = re.findall(r'[為為為為為為為為為為為為為為為為]', sample)
                if len(traditional_chars) > len(sample) * 0.1:
                    return 'zh_TW'
                else:
                    return 'zh_CN'

        # 检测英文
        elif re.search(r'[a-zA-Z]', sample):
            return 'en'

        # 默认返回简体中文
        return 'zh_CN'