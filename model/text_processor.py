# model/text_processor.py
import re
import os
from typing import List, Tuple, Any, Set, Optional
import difflib

# 尝试导入各语言处理库
try:
    import pycorrector
except ImportError:
    pycorrector = None
    print("警告: pycorrector 未安装，中文错别字修正功能将不可用")

try:
    import symspellpy
    from symspellpy import SymSpell
except ImportError:
    symspellpy = None
    SymSpell = None
    print("警告: symspellpy 未安装，英文错别字修正功能将不可用")

try:
    import jieba
except ImportError:
    jieba = None
    print("警告: jieba 未安装，中文/日文分词将不可用")

# 词典文件路径
DICTIONARY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dictionary")
EN_DICT = os.path.join(DICTIONARY_DIR, "English_dictionary.txt")
EN_STOP = os.path.join(DICTIONARY_DIR, "English_stopwords.txt")
ZH_CN_FREQ = os.path.join(DICTIONARY_DIR, "Simplified_Chinese_wordfreq.txt")
ZH_CN_STOP = os.path.join(DICTIONARY_DIR, "Simplified_Chinese_stopwords.txt")
ZH_TW_FREQ = os.path.join(DICTIONARY_DIR, "Traditional_Chinese_wordfreq.txt")
ZH_TW_STOP = os.path.join(DICTIONARY_DIR, "Traditional_Chinese_stopwords.txt")
JA_DICT = os.path.join(DICTIONARY_DIR, "Japanese_dictionary.txt")
JA_STOP = os.path.join(DICTIONARY_DIR, "Japanese_stopwords.txt")


def load_word_set(filepath: str) -> Set[str]:
    """从文件加载每行一个词的集合（跳过空行和注释）"""
    words = set()
    if not os.path.exists(filepath):
        print(f"警告: 词典文件不存在 {filepath}")
        return words
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    words.add(line)
    except Exception as e:
        print(f"读取词典文件失败 {filepath}: {e}")
    return words


# ========== 引号修正核心函数 ==========
def fix_quotes(text: str, lang: str) -> str:
    """修正引号：平衡左右引号，动态调整顺序错误，补齐缺失"""
    # 定义每种语言的引号对
    quote_configs = {
        'zh_CN': [('“', '”'), ('‘', '’')],
        'zh_TW': [('「', '」'), ('『', '』')],
        'en': [('"', '"'), ("'", "'")],
        'ja': [('「', '」'), ('『', '』')],
    }
    configs = quote_configs.get(lang, [('"', '"')])  # 默认英文

    for left, right in configs:
        if left == right:
            # 相同字符引号（如英文双引号），使用计数器法
            count = 0
            result_chars = []
            for ch in text:
                if ch == left:
                    if count == 0:
                        count = 1
                    else:
                        count -= 1
                    result_chars.append(ch)
                else:
                    result_chars.append(ch)
            if count > 0:
                result_chars.append(right * count)
            text = ''.join(result_chars)
        else:
            # 不同字符引号，使用栈匹配
            stack = []
            result_chars = []
            for ch in text:
                if ch == left:
                    stack.append(left)
                    result_chars.append(ch)
                elif ch == right:
                    if stack:
                        stack.pop()
                        result_chars.append(ch)
                    else:
                        # 栈空时出现右引号，将其改为左引号
                        result_chars.append(left)
                        stack.append(left)
                else:
                    result_chars.append(ch)
            # 补全未闭合的左引号
            for _ in stack:
                result_chars.append(right)
            text = ''.join(result_chars)
    return text


def add_period_if_needed(text: str, lang: str) -> str:
    """如果文本长度≥10且末尾没有句末标点，添加句号"""
    if not text:
        return text
    if len(text) < 10:
        return text
    sentence_end = {'。', '！', '？', '!', '?', '.', '…'}
    last_char = text[-1]
    if last_char not in sentence_end:
        if lang.startswith('zh') or lang == 'ja':
            text += '。'
        elif lang == 'en':
            text += '.'
        else:
            text += '.'
    return text


def fix_brackets(text: str) -> str:
    """补全括号（适用于中英文括号）"""
    stack = []
    result = []
    bracket_pairs = {
        '(': ')', '[': ']', '{': '}',
        '（': '）', '【': '】', '《': '》'
    }
    left_brackets = set(bracket_pairs.keys())
    right_brackets = set(bracket_pairs.values())

    for ch in text:
        if ch in left_brackets:
            stack.append(ch)
        elif ch in right_brackets:
            if stack:
                last = stack[-1]
                if bracket_pairs.get(last) == ch:
                    stack.pop()
            # 栈空时多余的右括号忽略
        result.append(ch)

    for left in reversed(stack):
        result.append(bracket_pairs[left])
    return ''.join(result)


def correct_chinese_symbols(text: str, lang='zh_CN') -> str:
    """简体/繁体中文符号修正"""
    text = re.sub(r',', '，', text)
    text = re.sub(r'!', '！', text)
    text = re.sub(r'\?', '？', text)
    text = re.sub(r':', '：', text)
    text = re.sub(r';', '；', text)
    text = re.sub(r'\(', '（', text)
    text = re.sub(r'\)', '）', text)
    text = re.sub(r'\[', '【', text)
    text = re.sub(r'\]', '】', text)

    text = fix_quotes(text, lang)
    text = add_period_if_needed(text, lang)
    text = fix_brackets(text)
    return text


def correct_english_symbols(text: str) -> str:
    """英文符号修正"""
    text = re.sub(r'，', ',', text)
    text = re.sub(r'。', '.', text)
    text = re.sub(r'！', '!', text)
    text = re.sub(r'？', '?', text)
    text = re.sub(r'：', ':', text)
    text = re.sub(r'；', ';', text)
    text = re.sub(r'（', '(', text)
    text = re.sub(r'）', ')', text)
    text = re.sub(r'【', '[', text)
    text = re.sub(r'】', ']', text)

    text = fix_quotes(text, 'en')
    text = add_period_if_needed(text, 'en')
    text = fix_brackets(text)
    return text


def correct_japanese_symbols(text: str) -> str:
    """日文符号修正"""
    text = re.sub(r',', '、', text)
    text = fix_quotes(text, 'ja')
    text = add_period_if_needed(text, 'ja')
    text = fix_brackets(text)
    return text


# ========== 基类 ==========
class BaseTextProcessor:
    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold
        self.dictionary: Set[str] = set()       # 纠错词典
        self.stopwords: Set[str] = set()        # 停用词

    def load_dictionary(self, filepath: str):
        self.dictionary = load_word_set(filepath)

    def load_stopwords(self, filepath: str):
        self.stopwords = load_word_set(filepath)

    def deduplicate(self, text: str) -> Tuple[str, List[dict]]:
        return text, []

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        raise NotImplementedError

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        raise NotImplementedError

    def deduplicate_entries(self, entries: List[Any], threshold: float) -> List[Any]:
        """对整个条目列表进行去重"""
        filtered = []
        for entry in entries:
            content = entry.content
            if content and (content[0] in ('（', '(') or content[0:4] == '<img'):
                continue
            filtered.append(entry)

        result = []
        seen = []
        special_keywords = [".r", ".log", ".game", "="]

        for entry in reversed(filtered):
            if any(keyword in entry.content for keyword in special_keywords):
                result.append(entry)
                seen.append(entry)
                continue

            if len(entry.content) < 10:
                result.append(entry)
                seen.append(entry)
            else:
                duplicate = False
                for kept in seen:
                    s = difflib.SequenceMatcher(None, entry.content, kept.content)
                    if s.ratio() >= threshold:
                        duplicate = True
                        break
                if not duplicate:
                    result.append(entry)
                    seen.append(entry)

        result.reverse()
        for idx, entry in enumerate(result, start=1):
            entry.id = idx
        return result


# ========== 简体中文处理器 ==========
class ChineseSimplifiedProcessor(BaseTextProcessor):
    def __init__(self, similarity_threshold: float = 0.8):
        super().__init__(similarity_threshold)
        self.load_dictionary(ZH_CN_FREQ)  # 注意：这里实际上加载的是词频文件，但为了统一接口，我们仍称为dictionary
        self.load_stopwords(ZH_CN_STOP)
        self.corrector = None
        if pycorrector:
            try:
                if os.path.exists(ZH_CN_FREQ):
                    self.corrector = pycorrector.Corrector(custom_word_freq_path=ZH_CN_FREQ)
                else:
                    self.corrector = pycorrector.Corrector()
            except Exception as e:
                print(f"pycorrector 初始化失败: {e}")

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        if self.corrector:
            try:
                result = self.corrector.correct(text)
                corrected = text
                if isinstance(result, str):
                    corrected = result
                elif isinstance(result, (tuple, list)) and result:
                    if isinstance(result[0], str):
                        corrected = result[0]
                    elif isinstance(result[0], dict) and 'target' in result[0]:
                        corrected = result[0]['target']
                elif isinstance(result, dict):
                    corrected = result.get('target', text)
                return corrected, []
            except Exception as e:
                print(f"pycorrector 处理出错: {e}")
                return text, []
        else:
            print("警告: pycorrector 不可用，简体中文错别字修正跳过")
            return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        return correct_chinese_symbols(text, 'zh_CN'), []


# ========== 繁体中文处理器 ==========
class ChineseTraditionalProcessor(BaseTextProcessor):
    def __init__(self, similarity_threshold: float = 0.8):
        super().__init__(similarity_threshold)
        self.load_dictionary(ZH_TW_FREQ)
        self.load_stopwords(ZH_TW_STOP)
        self.corrector = None
        if pycorrector:
            try:
                if os.path.exists(ZH_TW_FREQ):
                    self.corrector = pycorrector.Corrector(custom_word_freq_path=ZH_TW_FREQ)
                else:
                    self.corrector = pycorrector.Corrector()
            except Exception as e:
                print(f"pycorrector 初始化失败: {e}")

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        if self.corrector:
            try:
                result = self.corrector.correct(text)
                corrected = text
                if isinstance(result, str):
                    corrected = result
                elif isinstance(result, (tuple, list)) and result:
                    if isinstance(result[0], str):
                        corrected = result[0]
                    elif isinstance(result[0], dict) and 'target' in result[0]:
                        corrected = result[0]['target']
                elif isinstance(result, dict):
                    corrected = result.get('target', text)
                return corrected, []
            except Exception as e:
                print(f"pycorrector 繁体处理出错: {e}")
                return text, []
        else:
            print("警告: pycorrector 不可用，繁体中文错别字修正跳过")
            return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        return correct_chinese_symbols(text, 'zh_TW'), []


# ========== 英文处理器 ==========
class EnglishProcessor(BaseTextProcessor):
    def __init__(self, similarity_threshold: float = 0.8):
        super().__init__(similarity_threshold)
        self.load_dictionary(EN_DICT)
        self.load_stopwords(EN_STOP)
        self.sym_spell = None
        if SymSpell and self.dictionary:
            try:
                self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
                # 将词典转换为列表供 SymSpell 加载（需要每行一词，频率可选）
                # 这里简单地将集合写入临时文件或直接加载，但 SymSpell 要求文件路径
                # 我们可以创建一个临时文件，或者使用 load_dictionary 方法，需要文件路径。
                # 为简化，将词典保存到临时文件（或使用已有的文件路径）
                if os.path.exists(EN_DICT):
                    self.sym_spell.load_dictionary(EN_DICT, term_index=0, count_index=None)
                else:
                    print(f"警告: 英文词典文件 {EN_DICT} 不存在")
            except Exception as e:
                print(f"SymSpell 加载词典失败: {e}")

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        if self.sym_spell:
            words = text.split()
            corrected_words = []
            for word in words:
                suggestions = self.sym_spell.lookup(word, symspellpy.Verbosity.CLOSEST, max_edit_distance=2)
                if suggestions:
                    corrected_words.append(suggestions[0].term)
                else:
                    corrected_words.append(word)
            return ' '.join(corrected_words), []
        else:
            print("警告: SymSpell 不可用，英文错别字修正跳过")
            return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        return correct_english_symbols(text), []


# ========== 日文处理器 ==========
class JapaneseProcessor(BaseTextProcessor):
    def __init__(self, similarity_threshold: float = 0.8):
        super().__init__(similarity_threshold)
        self.load_dictionary(JA_DICT)
        self.load_stopwords(JA_STOP)
        if not jieba:
            print("警告: jieba 未安装，日文分词将不可用，纠错功能受限")

    def _word_segment(self, text: str) -> List[str]:
        """日文分词（使用 jieba 作为简易分词器）"""
        if jieba:
            return list(jieba.cut(text))
        else:
            # 降级：按字符分割
            return list(text)

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        if not self.dictionary:
            print("警告: 日文词典未加载，纠错跳过")
            return text, []

        words = self._word_segment(text)
        corrected_words = []
        for word in words:
            if word in self.dictionary:
                corrected_words.append(word)
            else:
                # 尝试在词典中找最相似的词（编辑距离）
                close_matches = difflib.get_close_matches(word, self.dictionary, n=1, cutoff=0.8)
                if close_matches:
                    corrected_words.append(close_matches[0])
                else:
                    corrected_words.append(word)
        return ''.join(corrected_words), []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        return correct_japanese_symbols(text), []


# ========== 工厂和管理器 ==========
class TextProcessorFactory:
    @staticmethod
    def create_processor(language: str, similarity_threshold: float = 0.8) -> BaseTextProcessor:
        processors = {
            'zh_CN': ChineseSimplifiedProcessor,
            'zh_TW': ChineseTraditionalProcessor,
            'en': EnglishProcessor,
            'ja': JapaneseProcessor
        }
        processor_class = processors.get(language, ChineseSimplifiedProcessor)
        return processor_class(similarity_threshold)


class TextProcessorManager:
    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold
        self.current_processor = None

    def set_language(self, language: str):
        self.current_processor = TextProcessorFactory.create_processor(
            language, self.similarity_threshold
        )

    def process_text(self, operation: str, text: str) -> Tuple[str, List[dict]]:
        if not self.current_processor:
            raise ValueError("未设置文本处理器")

        operations = {
            'spell_check': self.current_processor.spell_check,
            'correct_symbols': self.current_processor.correct_symbols,
        }
        processor_func = operations.get(operation)
        if not processor_func:
            raise ValueError(f"不支持的操作: {operation}")
        return processor_func(text)

    def deduplicate_entries(self, entries: List[Any], threshold: float) -> List[Any]:
        if not self.current_processor:
            raise ValueError("未设置文本处理器")
        return self.current_processor.deduplicate_entries(entries, threshold)

    def text_processor(self, text: str) -> Tuple[str, List[dict]]:
        if not self.current_processor:
            raise ValueError("未设置文本处理器")
        # 智能自动处理：先符号修正，再错别字修正
        text, _ = self.current_processor.correct_symbols(text)
        text, _ = self.current_processor.spell_check(text)
        return text, []
