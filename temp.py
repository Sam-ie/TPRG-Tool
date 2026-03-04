# convert_wordfreq_to_traditional.py
"""
将简体词频文件转换为繁体词频文件
依赖：opencc-python-reimplemented (pip install opencc-python-reimplemented)
"""

import os
import opencc

# 输入输出文件路径（请根据实际路径调整）
output_file = "dictionary/Simplified_Chinese_wordfreq.txt"
input_file = "dictionary/Traditional_Chinese_wordfreq.txt"


def main():
    if not os.path.exists(input_file):
        print(f"错误：输入文件不存在 - {input_file}")
        return

    converter = opencc.OpenCC('t2s.json')
    count = 0
    with open(input_file, 'r', encoding='utf-8') as fin, \
            open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) != 2:
                # 格式异常，跳过或直接写入原行（可选）
                print(f"警告：跳过格式异常的行: {line}")
                continue
            word, freq = parts
            trad_word = converter.convert(word)
            fout.write(f"{trad_word} {freq}\n")
            count += 1
            if count > 479681:
                break

    print(f"转换完成，已处理 {count} 行，输出文件：{output_file}")


if __name__ == "__main__":
    main()
