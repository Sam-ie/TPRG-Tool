# visualization_factory.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import jieba
import re


class VisualizationFactory:
    def __init__(self, lang_config):
        self.lang_config = lang_config

    def create_wordcloud_data(self, text):
        """创建词云数据（由于Plotly没有原生词云，我们创建词频柱状图代替）"""
        # 合并所有文本
        all_text = ' '.join(text)
        # 使用jieba进行中文分词
        words = jieba.cut(all_text)
        # 过滤短词和标点
        words = [word for word in words if len(word) > 1 and re.match(r'[\u4e00-\u9fa5]', word)]
        # 统计词频
        word_counts = Counter(words)
        # 取前20个最常出现的词
        top_words = word_counts.most_common(20)

        return pd.DataFrame(top_words, columns=['word', 'count'])

    def create_wordcloud_chart(self, text):
        """创建词频图表（替代词云）"""
        df = self.create_wordcloud_data(text)
        fig = px.bar(df, x='word', y='count',
                     title=self.lang_config.get('wordcloud_title', '词频统计'),
                     labels={'word': '词语', 'count': '出现次数'})
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    def create_stats_chart(self, text):
        """创建统计图表"""
        stats = self._generate_stats(text)
        df = pd.DataFrame(list(stats.items()), columns=['category', 'count'])
        fig = px.bar(df, x='category', y='count',
                     title=self.lang_config.get('stats_title', '文本统计'),
                     labels={'category': '统计项目', 'count': '数量'})
        return fig

    def create_network_chart(self, text):
        """创建简单的共现网络图"""
        # 简化的共现分析
        cooccurrence_data = self._analyze_cooccurrence(text)
        if not cooccurrence_data:
            # 如果没有共现数据，创建空图表
            fig = go.Figure()
            fig.update_layout(title=self.lang_config.get('network_title', '文本网络图'),
                              xaxis_title="", yaxis_title="")
            return fig

        # 这里简化实现，实际应用中需要更复杂的网络分析
        fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[1, 2, 1],
                                        mode='markers+text',
                                        text=['示例', '网络', '图']))
        fig.update_layout(title=self.lang_config.get('network_title', '文本网络图'))
        return fig

    def _generate_stats(self, text):
        """生成统计数据"""
        all_text = ' '.join(text)
        words = jieba.cut(all_text)
        words = [word for word in words if len(word) > 1]

        stats = {
            self.lang_config.get('total_words', '总词数'): len(words),
            self.lang_config.get('unique_words', '唯一词数'): len(set(words)),
            self.lang_config.get('total_lines', '总行数'): len(text),
            self.lang_config.get('punctuation_count', '标点符号数'): len(re.findall(r'[^\w\s]', all_text))
        }
        return stats

    def _analyze_cooccurrence(self, text):
        """分析词语共现（简化版）"""
        # 这里实现简单的共现分析逻辑
        try:
            # 提取名词和动词进行共现分析
            words_per_line = [list(jieba.cut(line)) for line in text if len(line) > 10]
            cooccurrence = {}

            for line_words in words_per_line:
                # 过滤出有意义的词
                meaningful_words = [word for word in line_words
                                    if len(word) > 1 and re.match(r'[\u4e00-\u9fa5]', word)]

                # 简单的共现计数
                for i, word1 in enumerate(meaningful_words):
                    for word2 in meaningful_words[i + 1:]:
                        pair = tuple(sorted([word1, word2]))
                        cooccurrence[pair] = cooccurrence.get(pair, 0) + 1

            return cooccurrence
        except Exception:
            return None