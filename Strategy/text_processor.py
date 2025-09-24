# text_processor.py
from deduplicate_strategy import DeduplicateStrategy
from spelling_strategy import SpellingStrategy
from symbol_strategy import SymbolStrategy

class TextProcessor:
    def __init__(self):
        self._strategies = {
            '去重': DeduplicateStrategy(),
            '去错别字': SpellingStrategy(),
            '修正符号': SymbolStrategy()
        }

    def remove_duplicates(self, text_lines, **kwargs):
        return self._strategies['去重'].execute(text_lines, **kwargs)

    def remove_spelling_errors(self, text_lines):
        result, _ = self._strategies['去错别字'].execute(text_lines)
        return result

    def correct_symbols(self, text_lines):
        return self._strategies['修正符号'].execute(text_lines)