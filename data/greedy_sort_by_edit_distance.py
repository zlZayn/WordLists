import os
from functools import lru_cache


@lru_cache(maxsize=100000)
def levenshtein_distance(s1: str, s2: str) -> int:
    """计算两个字符串的编辑距离（带缓存）"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def parse_word_line(line: str) -> tuple:
    """解析单词行，返回 (单词, 完整行)"""
    line = line.strip()
    if '|' in line:
        word = line.split('|')[0].strip()
        return word, line
    return line, line


def calculate_total_distance(words: list) -> int:
    """计算序列的总编辑距离"""
    total = 0
    for i in range(len(words) - 1):
        total += levenshtein_distance(words[i][0], words[i + 1][0])
    return total


def greedy_sort_from_start(words_data: list, start_idx: int) -> list:
    """从指定起点开始的贪心排序"""
    if not words_data:
        return []

    remaining = words_data.copy()
    result = [remaining.pop(start_idx)]

    while remaining:
        current_word = result[-1][0]
        min_dist = float('inf')
        min_idx = 0

        for i, (word, _) in enumerate(remaining):
            dist = levenshtein_distance(current_word, word)
            if dist < min_dist:
                min_dist = dist
                min_idx = i

        result.append(remaining.pop(min_idx))

    return result


def two_opt_improve(words_data: list, max_passes: int = 3) -> list:
    """
    2-Opt 局部搜索优化（简化版，适合100个数据规模）
    max_passes: 最大遍历轮数
    """
    result = words_data.copy()
    n = len(result)
    if n < 4:
        return result

    words_list = [w[0] for w in result]

    def get_dist(i, j):
        w1, w2 = words_list[i], words_list[j]
        # 利用编辑距离对称性，统一缓存键顺序
        key = (w1, w2) if w1 <= w2 else (w2, w1)
        if key not in dist_cache:
            dist_cache[key] = levenshtein_distance(w1, w2)
        return dist_cache[key]

    dist_cache = {}

    for _ in range(max_passes):
        improved = False

        for i in range(1, n - 2):
            for j in range(i + 2, n):
                old_dist = get_dist(i - 1, i) + get_dist(j - 1, j)
                new_dist = get_dist(i - 1, j - 1) + get_dist(i, j)

                if new_dist < old_dist:
                    result[i:j] = result[i:j][::-1]
                    words_list[i:j] = words_list[i:j][::-1]
                    improved = True

        if not improved:
            break

    return result


def optimized_sort(words_data: list) -> list:
    """
    多起点贪心 + 2-Opt 优化（简化版）
    """
    n = len(words_data)
    if n <= 1:
        return [line for _, line in words_data]

    # 选择起点：第一个、最后一个、中间几个
    start_indices = [0, n - 1, n // 2]
    if n >= 4:
        start_indices.extend([n // 4, 3 * n // 4])

    best_result = None
    best_dist = float('inf')

    for start_idx in start_indices:
        greedy_result = greedy_sort_from_start(words_data, start_idx)
        optimized = two_opt_improve(greedy_result)
        dist = calculate_total_distance(optimized)

        if dist < best_dist:
            best_dist = dist
            best_result = optimized

    return [line for _, line in best_result]


def process_file(input_path: str, output_path: str = None):
    """处理单个文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    words_data = []
    for line in lines:
        line = line.strip()
        if line:
            words_data.append(parse_word_line(line))

    print(f"处理文件: {os.path.basename(input_path)}")
    print(f"  共 {len(words_data)} 个单词")

    # 清空缓存
    levenshtein_distance.cache_clear()

    # 优化排序
    sorted_lines = optimized_sort(words_data)

    # 确定输出路径
    if output_path is None:
        output_path = input_path

    # 写入文件（最后一行不加空行）
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, line in enumerate(sorted_lines):
            if i == len(sorted_lines) - 1:
                f.write(line)
            else:
                f.write(line + '\n')

    print(f"  输出到: {os.path.basename(output_path)}")

    # 显示部分结果
    print("  前15个单词:")
    for i, line in enumerate(sorted_lines[:15]):
        word = line.split('|')[0] if '|' in line else line
        print(f"    {i+1}. {word}")

    return output_path


def process_all_files(data_dir: str):
    """处理目录下所有单词列表文件"""
    word_files = [
        'Word List 1.txt',
        'Word List 2.txt',
        'Word List 3.txt',
        "Zayn's List 1.txt",
        "Zayn's List 2.txt"
    ]

    for filename in word_files:
        input_path = os.path.join(data_dir, filename)
        if os.path.exists(input_path):
            process_file(input_path)
            print()


if __name__ == '__main__':
    data_dir = os.path.dirname(os.path.abspath(__file__))
    process_all_files(data_dir)
