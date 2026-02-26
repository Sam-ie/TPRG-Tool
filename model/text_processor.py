import re
from typing import List, Tuple, Any
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
    import opencc
except ImportError:
    opencc = None
    print("警告: opencc-python-reimplemented 未安装，繁体中文转换功能将不可用")


# ========== 引号修正核心函数 ==========

def fix_quotes(text: str, lang: str) -> str:
    """
    修正引号：
    - 左右数量平衡
    - 顺序错误时动态调整（如第一个字符为右引号时转为左引号）
    - 缺失时在首尾补齐
    支持多种引号类型，根据语言选择：
        zh_CN: 双引号“”，单引号‘’
        zh_TW: 双引号「」，单引号『』
        en: 双引号"，单引号'
        ja: 双引号「」，单引号『』
    """
    # 定义每种语言的引号对
    quote_configs = {
        'zh_CN': [('“', '”'), ('‘', '’')],
        'zh_TW': [('「', '」'), ('『', '』')],
        'en': [('"', '"'), ("'", "'")],
        'ja': [('「', '」'), ('『', '』')],
    }
    configs = quote_configs.get(lang, [('"', '"')])  # 默认英文

    # 对每种引号类型分别处理
    for left, right in configs:
        if left == right:
            # 相同字符引号（如英文双引号），使用计数器法
            count = 0
            result_chars = []
            for ch in text:
                if ch == left:
                    if count == 0:
                        # 第一个引号视为左引号
                        count = 1
                    else:
                        # 后续引号交替左右
                        # 由于字符相同，无法区分左右，我们根据当前奇偶决定：如果count>0，则视为右引号，count减1；否则视为左引号，count加1。
                        # 实际上在相同字符情况下，我们只能根据计数规则：遇到引号时，如果当前是期待左引号（count==0），则视为左引号；否则视为右引号。
                        # 但更简单的做法是统一按嵌套处理：左引号增加计数，右引号减少计数。然而我们不知道当前字符是左还是右，所以只能根据当前计数决定其角色。
                        # 这里采用标准做法：当遇到引号时，如果当前计数为0，则视为左引号，计数+1；否则视为右引号，计数-1。
                        # 这样能保证引号成对出现。
                        count -= 1
                    result_chars.append(ch)
                else:
                    result_chars.append(ch)
            # 如果最后计数 > 0，需要在末尾添加相应数量的右引号
            if count > 0:
                result_chars.append(right * count)
            text = ''.join(result_chars)
        else:
            # 不同字符引号（如中文双引号），使用栈匹配
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
                        # 栈空时出现右引号，将其改为左引号（翻转）
                        result_chars.append(left)
                        stack.append(left)
                else:
                    result_chars.append(ch)
            # 栈中剩余左引号，在末尾补全对应的右引号
            for _ in stack:
                result_chars.append(right)
            text = ''.join(result_chars)

    return text


def add_period_if_needed(text: str, lang: str) -> str:
    """如果文本长度≥10且末尾没有句末标点，添加句号"""
    if not text:
        return text
    if len(text) < 10:  # 长度小于10的文本不补句号
        return text
    sentence_end = {'。', '！', '？', '!', '?', '.', '…'}
    last_char = text[-1]
    if last_char not in sentence_end:
        if lang.startswith('zh') or lang == 'ja':
            text += '。'
        elif lang == 'en':
            text += '.'
        else:
            text += '.'  # 默认英文句号
    return text


def fix_brackets(text: str) -> str:
    """补全括号（适用于中英文括号）"""
    stack = []
    result = []
    # 定义括号对应关系
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
                # 检查是否匹配
                last = stack[-1]
                if bracket_pairs.get(last) == ch:
                    stack.pop()
                else:
                    # 不匹配，将当前右括号当作左括号处理？这里简化：忽略不匹配
                    pass
            # 栈空时多余的右括号，忽略（不添加）
        result.append(ch)

    # 补全未闭合的左括号
    for left in reversed(stack):
        result.append(bracket_pairs[left])
    return ''.join(result)


# ========== 符号修正主函数 ==========

def correct_chinese_symbols(text: str, lang='zh_CN') -> str:
    """简体/繁体中文符号修正"""
    # 标点转换（不转英文句点）
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
    # 日文句点通常用'。'，但英文句点也常见，此处不强制转换

    text = fix_quotes(text, 'ja')
    text = add_period_if_needed(text, 'ja')
    text = fix_brackets(text)
    return text


# ========== 基类 ==========

class BaseTextProcessor:
    """文本处理器的基类"""

    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold

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
        # 特殊关键词列表（条目包含这些关键词时直接保留，不参与去重）
        special_keywords = [".r", ".log", ".game", "="]

        for entry in reversed(filtered):
            # 先检查是否包含特殊关键词
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
        self.corrector = None
        if pycorrector:
            try:
                self.corrector = pycorrector.corrector.Corrector()
            except Exception as e:
                print(f"pycorrector 初始化失败: {e}")

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        if self.corrector:
            try:
                result = self.corrector.correct(text)
                # 处理各种可能的返回类型，确保最终得到字符串
                corrected = text  # 默认返回原文本
                if isinstance(result, str):
                    corrected = result
                elif isinstance(result, (tuple, list)):
                    if result and isinstance(result[0], str):
                        corrected = result[0]
                    elif result and isinstance(result[0], dict) and 'target' in result[0]:
                        corrected = result[0]['target']
                elif isinstance(result, dict):
                    corrected = result.get('target', text)
                return corrected, []
            except Exception as e:
                print(f"pycorrector 处理出错: {e}")
                return text, []
        else:
            print("警告: pycorrector 不可用，中文错别字修正跳过")
            return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        return correct_chinese_symbols(text, 'zh_CN'), []


# ========== 繁体中文处理器 ==========

class ChineseTraditionalProcessor(BaseTextProcessor):
    def __init__(self, similarity_threshold: float = 0.8):
        super().__init__(similarity_threshold)
        self.converter = None
        self.corrector = None
        if opencc:
            try:
                self.converter = opencc.OpenCC('t2s.json')
            except Exception as e:
                print(f"opencc 初始化失败: {e}")
        if pycorrector and self.converter:
            try:
                self.corrector = pycorrector.corrector.Corrector()
            except Exception as e:
                print(f"pycorrector 初始化失败: {e}")

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        if self.corrector and self.converter:
            simplified = self.converter.convert(text)
            try:
                result = self.corrector.correct(simplified)
                corrected_simple = simplified
                if isinstance(result, str):
                    corrected_simple = result
                elif isinstance(result, (tuple, list)):
                    if result and isinstance(result[0], str):
                        corrected_simple = result[0]
                    elif result and isinstance(result[0], dict) and 'target' in result[0]:
                        corrected_simple = result[0]['target']
                elif isinstance(result, dict):
                    corrected_simple = result.get('target', simplified)

                converter_back = opencc.OpenCC('s2t.json')
                result_text = converter_back.convert(corrected_simple)
                return result_text, []
            except Exception as e:
                print(f"pycorrector 繁体处理出错: {e}")
                return text, []
        else:
            print("警告: 繁体中文错别字修正不可用")
            return text, []

    def correct_symbols(self, text: str) -> Tuple[str, List[dict]]:
        return correct_chinese_symbols(text, 'zh_TW'), []


# ========== 英文处理器 ==========

class EnglishProcessor(BaseTextProcessor):
    def __init__(self, similarity_threshold: float = 0.8):
        super().__init__(similarity_threshold)
        self.sym_spell = None
        if SymSpell:
            try:
                self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
                dictionary_path = symspellpy.__path__[0] + "/frequency_dictionary_en_82_765.txt"
                self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
            except Exception as e:
                print(f"SymSpell 初始化失败: {e}")

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


# ========== 日文处理器（禁用错别字修正） ==========

class JapaneseProcessor(BaseTextProcessor):
    def __init__(self, similarity_threshold: float = 0.8):
        super().__init__(similarity_threshold)
        # 禁用错别字修正，不加载任何模型

    def spell_check(self, text: str) -> Tuple[str, List[dict]]:
        # 直接返回原文本，不做任何修正
        return text, []

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
