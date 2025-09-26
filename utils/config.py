class Config:
    # 可配置参数
    SIMILARITY_THRESHOLD = 0.8
    SKIP_TIME_PATTERNS = [
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',  # 2025-09-21 21:33:30
        # 可以添加其他时间格式
    ]

    # 高亮颜色配置
    HIGHLIGHT_COLORS = {
        'addition': 'lightgreen',
        'deletion': 'lightcoral',
        'modification': 'lightyellow'
    }