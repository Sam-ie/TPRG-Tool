import os
import glob

# 路径设置
source_dir = r"E:\download\scowl-2020.12.07\final"
output_file = r"F:\My_Works\python work\TPRG-Tool\dictionary\english_dictionary.txt"

# 检查源目录是否存在
if not os.path.isdir(source_dir):
    print(f"错误：目录不存在 - {source_dir}")
    exit(1)

# 收集所有词条的集合
words_set = set()

# 获取源目录下所有文件（不递归子目录）
file_paths = [os.path.join(source_dir, f) for f in os.listdir(source_dir)
              if os.path.isfile(os.path.join(source_dir, f))]

print(f"找到 {len(file_paths)} 个文件，开始处理...")

# 尝试的编码列表（按优先级）
encodings = ['utf-8', 'latin-1', 'cp1252']

for file_path in file_paths:
    file_name = os.path.basename(file_path)
    file_processed = False
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                for line in f:
                    word = line.strip()
                    if word:  # 忽略空行
                        words_set.add(word)
            file_processed = True
            print(f"已处理：{file_name} (编码: {enc})")
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"读取文件 {file_name} 时出错：{e}")
            break
    if not file_processed:
        print(f"警告：无法读取文件 {file_name}，已跳过。")

# 将集合转换为排序列表
sorted_words = sorted(words_set)

# 写入输出文件
with open(output_file, 'w', encoding='utf-8') as f:
    for word in sorted_words:
        f.write(word + '\n')

print(f"处理完成！共收集 {len(sorted_words)} 个唯一词条，已保存至：{output_file}")