import re
from typing import Optional


class LanguageDetector:
    # 常用繁体字列表（https://blog.csdn.net/pandaClose/article/details/112259939）
    TRADITIONAL_CHARS = set(
        '資這個會為來學時說問過請們麼還電對機後訊國發無嗎當於'
        '現點題樣經謝華話開實愛與動種應長關鳳間覺進兩將龍論別'
        '給聽體裡東風灣見區錯網樂讓選較場書從歡數認幾頭難買許'
        '記統處號師並計誰張黨結連轉報設變氣陳試戰義單臺卻隊聲'
        '寫業檔討妳則員興強價總辦議傳萬決貓組獨級馬門線語觀視'
        '聯參黃錢兒腦換錄專遠幫確裝備畫訴講類帶邊識雖飛運賽夢'
    )

    @staticmethod
    def detect_language(text: str) -> str:
        """
        检测文本的语言
        返回: 'zh_CN', 'zh_TW', 'en', 'ja'
        """
        if not text or len(text.strip()) < 5:
            # 文本过短或为空，默认简体中文
            return 'zh_CN'

        # 采样前2000字符进行检测
        sample = text[:2000]

        # 1. 检测是否包含韩文（如果项目支持韩文可扩展，暂返回默认）
        if re.search(r'[\uAC00-\uD7AF]', sample):
            # 暂按简体中文处理
            return 'zh_CN'

        # 2. 检测日语（假名比例）
        hiragana = re.findall(r'[\u3040-\u309F]', sample)  # 平假名
        katakana = re.findall(r'[\u30A0-\u30FF]', sample)  # 片假名
        total_kana = len(hiragana) + len(katakana)
        total_chars = len(sample)
        kana_ratio = total_kana / total_chars if total_chars > 0 else 0

        if kana_ratio > 0.05:  # 假名占比超过5%判定为日语
            return 'ja'

        # 3. 检测中文（汉字）
        chinese_chars = re.findall(r'[\u4E00-\u9FFF]', sample)
        if chinese_chars:
            # 统计繁体字数量
            traditional_count = sum(1 for c in chinese_chars if c in LanguageDetector.TRADITIONAL_CHARS)
            traditional_ratio = traditional_count / len(chinese_chars) if chinese_chars else 0

            if traditional_ratio > 0.1:  # 繁体字占比超过10%判为繁体中文
                return 'zh_TW'
            else:
                return 'zh_CN'

        # 4. 检测英文（英文字母占比）
        english_letters = re.findall(r'[a-zA-Z]', sample)
        english_ratio = len(english_letters) / total_chars if total_chars > 0 else 0
        if english_ratio > 0.5:
            return 'en'

        # 默认返回简体中文
        return 'zh_CN'
