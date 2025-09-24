# config.py
class Config:
    def __init__(self, similarity_threshold=0.85, min_length=5, case_sensitive=False):
        self相似度阈值 = similarity_threshold
        self最小长度 = min_length
        self大小写敏感 = case_sensitive

    def update(self, **kwargs):
        # 更新参数配置
        for key, value in kwargs.items():
            if key in ['similarity_threshold', 'min_length', 'case_sensitive']:
                setattr(self, key, value)