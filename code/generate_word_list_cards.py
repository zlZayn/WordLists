import os
import json
import datetime

from responsive_layout_system import SIDEBAR_MEDIA_QUERY, render_responsive_layout_style

# =============================================================================
# 项目路径配置
# =============================================================================
def get_project_root():
    """获取项目根目录路径"""
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 返回项目根目录（脚本目录的上一级）
    return os.path.dirname(script_dir)

# 项目路径常量
PROJECT_ROOT = get_project_root()
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================================================================
# 读取单词列表文件
# =============================================================================
def read_word_files():
    word_lists = {}
    
    # 从 data/ 目录读取所有 txt 文件
    txt_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    
    # 如果没有找到txt文件，创建一个示例文件
    if not txt_files:
        print("No txt files found in data/, creating sample word file...")
        sample_words = [
            "abandon|vt.遗弃，放弃；n.放纵；",
            "ability|n.能力，才能；",
            "abnormal|adj.反常的，异常的；",
            "abolish|vt.彻底废除，废止；",
            "abortion|n.流产，堕胎；",
            "absolute|adj.绝对的，完全的；",
            "absorb|vt.吸收；使全神贯注；",
            "abstract|adj.抽象的；n.摘要；"
        ]
        sample_path = os.path.join(DATA_DIR, 'sample_words.txt')
        with open(sample_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sample_words))
        txt_files = ['sample_words.txt']
    
    # 为每个txt文件创建单词列表
    for txt_file in txt_files:
        # 去除.txt后缀作为列表名称
        list_name = os.path.splitext(txt_file)[0]
        word_lists[list_name] = []
        
        file_path = os.path.join(DATA_DIR, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        try:
                            word, definition = line.split('|', 1)
                            word_lists[list_name].append({
                                'word': word.strip(),
                                'definition': definition.strip()
                            })
                        except ValueError:
                            print(f"Format error in line {line_num} ({list_name}): {line}")
        except Exception as e:
            print(f"Error reading file {txt_file}: {e}")
    
    return word_lists

# 生成HTML文件（仅修改CSS和主题切换JS）
def generate_html(word_lists):
    if not word_lists:
        print("Error: No available word lists found")
        return
    
    # 确保至少有一个列表有单词
    first_list_name = list(word_lists.keys())[0]
    if not word_lists[first_list_name]:
        print(f"Warning: List '{first_list_name}' is empty")
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>单词列表 | Word Lists</title>
    <style>
        /* ============================== 1. 基础定义 ============================== */
        /* 1.1 浅色模式变量 - 基础主题样式 */
        :root {
            /* 主题色 */
            --theme-pink: #ff99cc;
            --theme-blue: #42a5f5;
            
            /* 特殊用途变量 */
            /* 模态框相关（与暗模式保持结构一致） */
            
            /* 背景色 */
            --page-bg: #fef8ed;
            --card-bg: white;
            --sidebar-list-bg: #fef8ed;
            
            /* 文本色 */
            --text-primary: #333;
            --text-secondary: #666;
            --btn-text: #000;
            
            /* 进度条 */
            --progress-fill-bg: #f1f1f1;
            
            /* 功能按钮 */
            --btn-prev-bg: #cccccc;
            --btn-prev-hover: #999999;
            --btn-show-def-hover: #ff6699;
            --btn-next-hover: #1876F3;
            
            /* 侧边栏按钮 */
            --order-toggle-disordered: var(--btn-prev-bg);
            --order-toggle-disordered-hover: var(--btn-prev-bg);
            --order-toggle-ordered: #b7e4c7;
            --order-toggle-ordered-hover: #a7f3d0;
            --list-select-btn-active-bg: var(--card-bg);
            --list-select-btn-active-text: #333;
            
            /* 界面元素 */
            --border-color: #ccc;
            --shadow-primary: 0 6px 12px rgba(0,0,0,0.05);
            --shadow-secondary: 0 4px 8px rgba(0,0,0,0.02);
            
            /* 滚动条 */
            --scrollbar-track: #f1f1f1;
            --scrollbar-thumb: #bbb;
            --scrollbar-thumb-hover: #999;
            
            /* 过渡动画变量（鼠标点击位置、扩散半径） */
            --x: 0px;
            --y: 0px;
            --r: 0px;
        }

        /* 1.2 深色模式变量 */
        :root.dark {
            /* 主题色 */
            --theme-pink: #d64187;
            --theme-blue: #2563eb;
            
            /* 特殊用途变量 */
            /* 模态框相关 */
            --modal-dark-bg: rgba(255, 255, 255, 0.1);
            
            /* 背景色 */
            --page-bg: #2d2b3a;
            --card-bg: #3a384c;
            --sidebar-list-bg: #2d2b3a;
            
            /* 文本色 */
            --text-primary: #f0f0f0;
            --text-secondary: #ddd;
            --btn-text: white;
            
            /* 进度条 */
            --progress-fill-bg: #4a485c;
            
            /* 功能按钮 */
            --btn-prev-bg: #555;
            --btn-prev-hover: #777;
            --btn-show-def-hover: #b8326d;
            --btn-next-hover: #1d4ed8;
            
            /* 侧边栏按钮 */
            --order-toggle-disordered: var(--btn-prev-bg);
            --order-toggle-disordered-hover: var(--btn-prev-bg);
            --order-toggle-ordered: #166534;
            --order-toggle-ordered-hover: #14532d;
            --list-select-btn-active-bg: #3a384c;
            --list-select-btn-active-text: #fff;
            
            /* 界面元素 */
            --border-color: #555;
            --shadow-primary: 0 6px 12px rgba(255, 255, 255, 0.05);
            --shadow-secondary: 0 4px 8px rgba(255, 255, 255, 0.02);
            
            /* 滚动条 */
            --scrollbar-track: #4a485c;
            --scrollbar-thumb: #666;
            --scrollbar-thumb-hover: #888;
        }

        /* 1.3 模式切换过渡动画（依赖变量，紧跟变量定义） */
        /* 禁用默认过渡动画，自定义圆形扩散效果 */
        ::view-transition-old(*) {
            animation: none;
        }
        ::view-transition-new(*) {
            animation: clip 0.4s cubic-bezier(1,0,0,1);
        }
        /* 控制层级：确保新状态在上方 */
        ::view-transition-old(root) {
            z-index: 1;
        }
        ::view-transition-new(root) {
            z-index: 9999;
        }
        /* 深色模式下使用相同的动画（修复闪烁问题） */
        html.dark::view-transition-old(*) {
            animation: none;
        }
        html.dark::view-transition-new(*) {
            animation: clip 0.4s cubic-bezier(1,0,0,1);
        }
        /* 圆形扩散动画：从鼠标点击位置扩散 */
        @keyframes clip {
            from {
                clip-path: circle(0% at var(--x) var(--y));
            }
            to {
                clip-path: circle(var(--r) at var(--x) var(--y));
            }
        }

        /* ============================== 2. 全局样式 ============================== */
        /* 2.1 页面基础结构 */
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--page-bg);
            font-size: 1.2em;
            min-height: 100vh;
            position: relative;
            color: var(--text-primary);
        }

        /* 2.2 搜索框样式 */
        .search {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            border: 3px solid var(--theme-pink);
            border-radius: 15px;
            background: transparent;
            color: var(--text-primary);
            font-size: 16px;
            padding: 8px 15px;
            outline: none;
            width: 200px;
            font-weight: bold;
            text-align: center;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
            box-sizing: border-box;
            display: none; /* 默认隐藏 */
            margin: 0;
        }
        .search::placeholder {
            color: var(--text-primary);
            font-style: italic;
        }
        .search-match-char {
            color: var(--theme-pink);
            font-weight: bold;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }
        
        /* 发音和链接悬浮效果 */
        .word-definition-link {
            display: inline-block;
            opacity: 0.5;
            transition: opacity 0.2s ease, transform 0.2s ease;
        }
        
        .word-definition-link:hover {
            opacity: 1;
            transform: translateY(-2px);
        }
        
        .word-definition-link:active {
            opacity: 1;
            transform: translateY(1px);
        }
        /* 有道词典链接样式 */
        .word-youdao-link {
            color: var(--theme-pink);
            text-decoration: underline;
        }
        /* 发音按钮链接样式 */
        .word-pronunciation-btn {
            color: var(--theme-pink);
            text-decoration: none;
        }
        /* 发音按钮容器样式 */
        .word-pronunciation-container {
            margin-left: 8px;
        }
        
        /* 未匹配卡片背景样式 */
        .search-no-match {
            background-color: var(--page-bg) !important;
            transition: background-color 0.2s ease;
        }
        
        /* 2.3 页面状态显示（顶部+底部） */
        .status-top {
            position: fixed;
            top: 2px;
            left: 50%;
            transform: translateX(-50%);
            color: var(--text-secondary);
            font-weight: bold;
            font-size: 0.6rem;
            z-index: 5;
            padding: 0;
        }

        .status-bottom {
            position: fixed;
            bottom: 2px;
            left: 50%;
            transform: translateX(-50%);
            color: var(--text-secondary);
            font-weight: bold;
            font-size: 0.6rem;
            z-index: 5;
            padding: 0;
            margin: 0;
        }

        /* ============================== 3. 组件样式：按钮 ============================== */
        /* 3.1 按钮通用样式（所有按钮基础） */
        .btn {
            padding: clamp(8px, 2vw, 8px) clamp(12px, 3vw, 18px);
            font-size: 16px;
            border: none;
            border-radius: 15px;
            background-color: var(--card-bg);
            color: var(--text-primary);
            cursor: pointer;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: inherit;
            font-weight: bold;
            line-height: 1.2;
            margin: 0;
        }
        .btn:hover {
            transform: scale(1.05);
        }
        .btn.active {
            background-color: var(--theme-pink);
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        /* 3.2 浮动按钮（顶部/底部悬浮：侧边栏开关、主题切换等） */
        .btn-float {
            position: fixed;
            width: 120px;
            z-index: 20;
        }
        .btn-float:hover {
            box-shadow: var(--shadow-primary);
        }
        /* 浮动按钮位置差异化 */
        .btn-menu {
            top: 20px;
            left: 20px;
            display: none; /* 初始隐藏，响应式时显示 */
        }
        .btn-theme {
            top: 20px;
            right: 20px;
        }
        .btn-list {
            bottom: 20px;
            right: 20px;
        }
        .btn-focus {
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
        }
        .btn-focus:hover {
            transform: translateX(-50%) scale(1.05);
        }

        /* 3.3 侧边栏按钮（列表选择、顺序切换） */
        .btn-nav {
            width: 100%;
            box-sizing: border-box;
            min-height: 60px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            background-color: var(--sidebar-list-bg);
            color: var(--text-secondary);
        }
        /* 侧边栏按钮交互差异化 */
        .list-select-btn:hover, .list-select-btn.active {
            font-size: 22px;
            background-color: var(--list-select-btn-active-bg);
            color: var(--list-select-btn-active-text);
            box-shadow: var(--shadow-primary);
        }
        .btn-order:hover, .btn-order.active {
            font-size: 22px;
            color: var(--text-primary);
            box-shadow: var(--shadow-primary);
        }
        .btn-order[data-order="disordered"]:hover,
        .btn-order[data-order="disordered"].active {
            background-color: var(--order-toggle-disordered-hover);
        }
        .btn-order[data-order="ordered"]:hover {
            background-color: var(--order-toggle-ordered-hover);
        }
        .btn-order[data-order="ordered"].active {
            background-color: var(--order-toggle-ordered);
        }

        /* 3.4 中央卡片功能按钮（上一个、显示释义、下一个） */
        .card-actions {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: auto;
            padding-top: 20px;
            flex-wrap: wrap;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }
        /* 功能按钮尺寸控制 */
        .card-actions .btn {
            padding: 15px 30px;
            font-size: clamp(16px, 2vw, 20px);
            min-width: 100px;
            max-width: 200px;
            flex: 1;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }
        /* 功能按钮背景色差异化 */
        #btn-prev {
            background-color: var(--btn-prev-bg);
        }
        #btn-prev:hover {
            background-color: var(--btn-prev-hover);
        }
        #btn-toggle {
            background-color: var(--theme-pink);
        }
        #btn-toggle:hover {
            background-color: var(--btn-show-def-hover);
        }
        #btn-next {
            background-color: var(--theme-blue);
        }
        #btn-next:hover {
            background-color: var(--btn-next-hover);
        }

        /* ============================== 4. 组件样式：页面布局 ============================== */
        /* 4.1 左侧侧边栏 */
        .sidebar {
            width: 250px;
            background-color: var(--sidebar-list-bg);
            padding: 20px 0;
            box-shadow: var(--shadow-primary);
            display: flex;
            flex-direction: column;
            gap: 15px;
            position: fixed;
            left: 0;
            top: 0;
            height: 100vh;
            z-index: 100;
            transition: transform 0.2s ease;
            opacity: 0.95;
            overflow-y: auto;
        }
        /* 侧边栏内部子元素 */
        .sidebar h3,
        .list-buttons,
        .order-buttons,
        .sidebar-footer {
            padding-left: 20px;
            padding-right: 20px;
        }
        .sidebar h3 {
            color: var(--text-primary);
            margin-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
            text-align: center;
        }
        .list-buttons {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 15px;
            box-sizing: border-box;
        }
        .order-buttons {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: auto;
            box-sizing: border-box;
        }
        .sidebar-footer {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid var(--border-color);
            /* 仅显示装饰线，隐藏文字 */
            font-size: 0;
            height: 1px;
            overflow: hidden;
        }

        /* 4.2 中央单词卡片 */
        .main {
            position: fixed;
            top: 80px;
            bottom: 80px;
            left: 320px;
            right: 80px;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 5;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }
        .card {
            width: 100%;
            max-width: 800px;
            height: auto;
            min-height: 400px;
            background-color: var(--card-bg);
            border-radius: 15px;
            box-shadow: var(--shadow-primary);
            padding: 40px 30px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            text-align: center;
        }
        /* 卡片顶部（进度条+索引） */
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            gap: 20px;
        }
        .progress {
            flex-grow: 1;
            height: 10px;
            background-color: var(--progress-fill-bg);
            border-radius: 6px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background-color: var(--theme-pink);
            width: 0%;
            transition: width 0.2s ease;
        }
        .counter {
            font-size: 18px;
            color: var(--text-secondary);
            font-weight: 500;
            min-width: 120px;
            text-align: center;
        }
        /* 卡片内容（单词+释义） */
        .word {
            font-size: clamp(3rem, 6vw, 4.5rem);
            font-weight: bold;
            color: var(--text-primary);
            margin: 0;
            padding: 0;
            line-height: 1.2;
            word-break: break-word;
            display: flex;
            justify-content: center;
            align-items: center;
            flex: 1;
        }
        .definition-area {
            flex-grow: 1;
            overflow-y: auto;
            margin: 0;
            padding: 14px 0;
            min-height: 180px;
            display: flex;
            justify-content: center;
        }
        .definition {
            font-size: clamp(1.3rem, 3.5vw, 1.8rem);
            color: var(--text-secondary);
            line-height: 1.3;
            opacity: 0;
            word-break: break-word;
            text-align: center;
            width: 100%;
        }
        .definition.visible {
            opacity: 1;
            transition: opacity 0.2s ease;
        }

        /* ============================== 5. 组件样式：专注模式 ============================== */
        /* 专注模式：隐藏非核心元素 */
        body.focus-mode .sidebar, 
        body.focus-mode .btn-menu, 
        body.focus-mode .btn-theme, 
        body.focus-mode .btn-list {
            opacity: 0;
            pointer-events: none;
        }
        /* 专注模式：侧边栏收回 */
        .sidebar-container {
            transition: transform 0.2s ease, z-index 0.2s ease;
            backface-visibility: hidden;
            will-change: transform;
            z-index: 10;
        }
        body.focus-mode .sidebar-container {
            transform: translateX(-100%);
            z-index: 5;
        }
        /* 专注模式：中央卡片全屏化 */
        body.focus-mode .main {
            position: fixed;
            top: 40px;
            bottom: 40px;
            left: 5px;
            right: 5px;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 15;
        }
        body.focus-mode .card {
            width: 100%;
            max-width: 100%;
            height: 100%;
            background-color: var(--card-bg);
            border-radius: 15px;
            box-shadow: var(--shadow-primary);
            padding: 30px 10px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        /* 专注模式：进度条调整 */
        body.focus-mode .card-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 30px;
            gap: 10px;
            width: 100%;
        }
        body.focus-mode .progress {
            width: 100%;
            height: 10px;
            background-color: var(--progress-fill-bg);
            border-radius: 6px;
            overflow: hidden;
        }
        body.focus-mode .progress-fill {
            height: 100%;
            background-color: var(--theme-pink);
            transition: width 0.2s ease;
        }
        body.focus-mode .counter {
            font-size: 18px;
            color: var(--text-secondary);
            font-weight: 500;
            text-align: center;
            width: 100%;
        }
        /* 专注模式：单词和释义居中放大 */
        body.focus-mode .word {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex: 1;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
            font-size: clamp(3rem, 7vw, 5rem);
        }
        body.focus-mode .definition-area {
            display: flex;
            justify-content: center;
            align-items: center;
            flex: 1;
            margin: 0;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }
        body.focus-mode .definition {
            text-align: center;
            width: 100%;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
            font-size: clamp(1.5rem, 5vw, 2.2rem);
        }
        /* 专注模式：按钮组布局调整（向两边分布） */
        body.focus-mode .card-actions {
            justify-content: space-between;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            gap: 5px;
            padding-top: 40px;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }
        /* 专注模式：功能按钮放大 */
        body.focus-mode .card-actions .btn {
            padding: 20px 30px;
            font-size: 24px;
            min-width: 200px;
            flex: 1;
            margin: 0 10px;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
            white-space: normal;
            text-align: center;
        }
        /* 专注模式：元素过渡效果补充 */
        .definition-area {
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }
        .definition {
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        /* ============================== 6. 特殊模块：单词列表弹窗 ============================== */
        .modal {
            display: flex;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px); /* 兼容Safari */
            z-index: 1000;
            justify-content: center;
            align-items: center;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.2s ease, visibility 0.2s ease;
        }
        .modal.active {
            opacity: 1;
            visibility: visible;
        }
        /* 暗模式下弹窗背景 */
        :root.dark .modal {
            background-color: var(--modal-dark-bg);
        }
        /* 弹窗内容区 */
        .modal-content {
            background-color: var(--page-bg);
            border-radius: 15px;
            box-shadow: var(--shadow-primary);
            width: 80%;
            max-width: 1200px;
            position: fixed;
            top: 10%;
            bottom: 10%;
            padding: 2%;
            display: flex;
            flex-direction: column;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2%;
            padding-bottom: 1.5%;
            border-bottom: 1px solid var(--border-color);
        }
        .modal-title {
            text-align: left;
            font-size: 28px;
            font-weight: bold;
            color: var(--text-primary);
            margin: 0;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }
        .close-list-modal-btn {
            background: none;
            border: none;
            font-size: 30px;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 5px;
            transition: color 0.2s ease;
            margin-left: auto;
        }
        .close-list-modal-btn:hover {
            color: var(--text-primary);
        }
        /* 弹窗单词列表区 */
        .modal-body {
            flex: 1;
            overflow-y: auto;
            padding: 1%;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5%;
            align-content: start;
        }
        .modal-item {
            background-color: var(--card-bg);
            border-radius: 15px;
            padding: 1.5%;
            transition:
                transform 0.2s ease,
                opacity 0.2s ease,
                background-color 0.2s ease,
                color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
            cursor: pointer;
        }
        .modal-item:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-primary);
        }

        .item-word {
            font-size: 20px;
            font-weight: bold;
            color: var(--text-primary);
            margin-bottom: 8px;
        }
        .item-definition {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.4;
        }
        /* 弹窗底部分割线 */
        .modal-footer {
            margin-top: 1.5%;
            padding-top: 1.5%;
            border-top: 1px solid var(--border-color);
            min-height: 1px;
            font-size: 16px;
            color: var(--text-secondary);
            text-align: center;
        }

        /* ============================== 7. 通用样式：滚动条 ============================== */
        /* 7.1 侧边栏滚动条 */
        .sidebar::-webkit-scrollbar {
            width: 12px;
        }
        .sidebar::-webkit-scrollbar-track {
            background: var(--progress-fill-bg);
            border-radius: 6px;
        }
        .sidebar::-webkit-scrollbar-thumb {
            background: var(--theme-pink);
            border-radius: 6px;
        }
        .sidebar::-webkit-scrollbar-thumb:hover {
            background: var(--btn-show-def-hover);
        }

        /* 7.2 单词弹窗滚动条 */
        .modal-body::-webkit-scrollbar {
            width: 12px;
        }
        .modal-body::-webkit-scrollbar-track {
            background: var(--progress-fill-bg);
            border-radius: 6px;
        }
        .modal-body::-webkit-scrollbar-thumb {
            background: var(--theme-pink);
            border-radius: 6px;
        }
        .modal-body::-webkit-scrollbar-thumb:hover {
            background: var(--btn-show-def-hover);
        }

        /* 7.3 释义容器滚动条 */
        .definition-area::-webkit-scrollbar {
            width: 12px;
        }
        .definition-area::-webkit-scrollbar-track {
            background: var(--progress-fill-bg);
            border-radius: 6px;
        }
        .definition-area::-webkit-scrollbar-thumb {
            background: var(--theme-pink);
            border-radius: 6px;
        }
        .definition-area::-webkit-scrollbar-thumb:hover {
            background: var(--btn-show-def-hover);
        }

        /* 宽度与高度适配由 responsive_layout_system.py 统一注入。 */

        /* ============================== 9. 适配样式：触摸设备 ============================== */
        @media (hover: none) and (pointer: coarse) {
            /* 按钮最小高度适配触摸 */
            .btn {
                min-height: 44px;
            }
            /* 移除触摸设备上的hover效果 */
            .list-select-btn:hover, .btn-order:hover {
                font-size: inherit;
                background-color: var(--sidebar-list-bg);
                color: var(--text-secondary);
            }
            .list-select-btn.active:hover, .btn-order.active:hover {
                font-size: 22px;
            }
        }
    </style>
''' + render_responsive_layout_style("word-list") + '''
</head>
<body>
    <div class="top-toolbar" role="group" aria-label="Page controls">
        <!-- 移动端侧边栏按钮 -->
        <button class="btn btn-float btn-menu" id="btn-menu">Select</button>
        <!-- 主题切换按钮 -->
        <button class="btn btn-float btn-theme" id="btn-theme">Dark</button>
        <!-- 专注模式按钮 -->
        <button class="btn btn-float btn-focus" id="btn-focus">Focus</button>
    </div>
    
    <!-- 单词列表弹窗按钮 -->
    <button class="btn btn-float btn-list" id="btn-list">Word List</button>
    
    <!-- 单词列表弹窗 -->
    <div class="modal" id="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title" id="modal-title">
                    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                        <span>${activeList}</span>
                        <span>${wordLists[activeList].length} words</span>
                    </div>
                </h2>
            </div>
            <div class="modal-body" id="modal-body">
                <!-- 单词列表内容将通过JavaScript动态生成 -->
            </div>
            <div class="modal-footer" id="modal-footer">
                <!-- 统计信息将通过JavaScript动态生成 -->
            </div>
        </div>
    </div>
    
    <!-- 全局搜索框 -->
    <input type="text" class="search" id="search" placeholder="">
    
    <!-- 顶部状态显示 -->
    <div class="status-top" id="status-top"></div>
    
    <!-- 左侧列表选择器 -->
    <div class="sidebar" id="sidebar">
        <h3>Select Word List</h3>
        <div class="list-buttons">
''' + '\n'.join([f'            <button class="btn btn-nav list-select-btn {"active" if i == 0 else ""}" data-list="{list_name}">{list_name}</button>' for i, list_name in enumerate(word_lists.keys())]) + '''
        </div>
        
        <div class="order-buttons">
            <button class="btn btn-nav btn-order" data-order="disordered">Disordered</button>
            <button class="btn btn-nav btn-order active" data-order="ordered">Ordered</button>
        </div>
        <div class="sidebar-footer">
            <div id="sidebar-info">''' + f"{list(word_lists.keys())[0]} ({len(word_lists[list(word_lists.keys())[0]])} words)" + '''</div>
        </div>
    </div>
    
    <!-- 中央卡片容器 -->
    <div class="main">
        <div class="card">
            <div class="card-header">
                <div class="progress">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
                <div class="counter" id="counter"></div>
            </div>
            
            <div class="word" id="word"></div>
            <div class="definition-area">
                <div class="definition" id="definition"></div>
            </div>
            <div class="card-actions">
                <button class="btn" id="btn-prev">Previous</button>
                <button class="btn" id="btn-toggle">Display</button>
                <button class="btn" id="btn-next">Next</button>
            </div>
        </div>
    </div>
    
    <!-- 底部状态显示 -->
    <div class="status-bottom" id="status-bottom"></div>

    <script>
        // 单词列表数据 - 保持原逻辑
        const wordLists = ''' + json.dumps(word_lists, ensure_ascii=False) + ''';
        const listKeys = Object.keys(wordLists);
        let activeList = listKeys[Math.floor(Math.random() * listKeys.length)];
        let currentWords = wordLists[activeList] || [];
        let currentIndex = 0;
        let isOrdered = true;
        
        // DOM元素 - 与修改后的ID同步
        const themeSwitchBtn = document.getElementById('btn-theme');
        const mobileSidebarToggle = document.getElementById('btn-menu');
        const sidebarListSelector = document.getElementById('sidebar');
        const focusModeBtn = document.getElementById('btn-focus');
        const sidebarCollapseQuery = window.matchMedia(''' + json.dumps(SIDEBAR_MEDIA_QUERY) + ''');
        const searchInput = document.getElementById('search');
        const html = document.documentElement;
        const pageBottomStatus = document.getElementById('status-bottom');
        const pageTopStatus = document.getElementById('status-top');
        
        // 单词列表弹窗相关元素 - 与修改后的ID同步
        const wordListModalBtn = document.getElementById('btn-list');
        const wordListModal = document.getElementById('modal');
        const wordListModalContainer = document.getElementById('modal-body');
        const wordListModalTitle = document.getElementById('modal-title');
        const wordListModalStats = document.getElementById('modal-footer');
        
        console.log('Word lists loaded:', Object.keys(wordLists));
        console.log('Current words:', currentWords);

        // ========== 主题功能（核心修改：丝滑过渡） ==========
        // 初始化主题 - 逻辑不变，仅修改元素变量名
        function initTheme() {
            if (localStorage.getItem('theme') === 'dark' ||
                (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                html.classList.add('dark');
                themeSwitchBtn.textContent = 'Dark';
            } else {
                html.classList.remove('dark');
                themeSwitchBtn.textContent = 'Light ';
            }
        }

        // 新增：计算鼠标位置和扩散半径（用于过渡动画）
        function calculateTransitionParams(e) {
            const x = e.clientX;
            const y = e.clientY;
            // 计算从点击位置到屏幕对角的最大半径（确保动画覆盖全屏）
            const endRadius = Math.hypot(
                Math.max(x, innerWidth - x),
                Math.max(y, innerHeight - y)
            );
            // 设置动画变量（供CSS使用）
            html.style.setProperty('--x', x + 'px');
            html.style.setProperty('--y', y + 'px');
            html.style.setProperty('--r', endRadius + 'px');
        }

        // 主题切换事件（修改核心：加入View Transitions API）
        themeSwitchBtn.addEventListener('click', (e) => {
            // 1. 计算动画参数（鼠标点击位置、扩散半径）
            calculateTransitionParams(e);
            
            // 2. 判断浏览器是否支持View Transitions API（兼容处理）
            if (document.startViewTransition) {
                // 支持：用API包裹主题切换逻辑，实现丝滑过渡
                document.startViewTransition(() => {
                    const isDarkNow = html.classList.contains('dark');
                    if (isDarkNow) {
                        html.classList.remove('dark');
                        localStorage.setItem('theme', 'light');
                        themeSwitchBtn.textContent = 'Light ';
                    } else {
                        html.classList.add('dark');
                        localStorage.setItem('theme', 'dark');
                        themeSwitchBtn.textContent = 'Dark';
                    }
                });
            } else {
                // 不支持：降级为原逻辑（无动画）
                const isDarkNow = html.classList.contains('dark');
                if (isDarkNow) {
                    html.classList.remove('dark');
                    localStorage.setItem('theme', 'light');
                    themeSwitchBtn.textContent = 'Light ';
                } else {
                    html.classList.add('dark');
                    localStorage.setItem('theme', 'dark');
                    themeSwitchBtn.textContent = 'Dark';
                }
            }
        });
        
        // ========== 搜索功能 ==========
        // 实现单词和释义的搜索，对匹配字符进行高亮（粉色字体带过渡动画），未匹配卡片使用页面背景色
        function handleSearch() {
            // 确保searchInput存在
            if (!searchInput) return;
            
            const searchTerm = searchInput.value.toLowerCase();
            const wordItems = document.querySelectorAll('.modal-item');
            
            // 清除所有之前的高亮
            wordItems.forEach(item => {
                // 移除未匹配标记
                item.classList.remove('search-no-match');
                
                // 恢复原始文本
                const wordElement = item.querySelector('.item-word');
                const definitionElement = item.querySelector('.item-definition');
                
                // 移除之前添加的高亮标记
                wordElement.innerHTML = wordElement.textContent;
                definitionElement.innerHTML = definitionElement.textContent;
            });
            
            // 搜索框不为空时进行搜索
            if (searchTerm) {
                wordItems.forEach(item => {
                    const wordElement = item.querySelector('.item-word');
                    const definitionElement = item.querySelector('.item-definition');
                    const wordText = wordElement.textContent;
                    const definitionText = definitionElement.textContent;
                    const hasMatch = wordText.toLowerCase().indexOf(searchTerm) !== -1 || 
                                   definitionText.toLowerCase().indexOf(searchTerm) !== -1;
                    
                    // 如果没有匹配项，添加未匹配样式
                    if (!hasMatch) {
                        item.classList.add('search-no-match');
                    } else {
                        // 高亮单词中的匹配字符
                        if (wordText.toLowerCase().indexOf(searchTerm) !== -1) {
                            wordElement.innerHTML = highlightText(wordText, searchTerm);
                        }
                        
                        // 高亮释义中的匹配字符
                        if (definitionText.toLowerCase().indexOf(searchTerm) !== -1) {
                            definitionElement.innerHTML = highlightText(definitionText, searchTerm);
                        }
                    }
                });
            }
        }
        
        // 辅助函数：高亮匹配的文本字符
        function highlightText(text, searchTerm) {
            var result = '';
            var lowerText = text.toLowerCase();
            var startIndex = 0;
            var index;
            
            while ((index = lowerText.indexOf(searchTerm, startIndex)) !== -1) {
                // 添加匹配前的文本
                result += text.substring(startIndex, index);
                // 添加高亮的匹配文本
                result += '<span class="search-match-char">' + text.substring(index, index + searchTerm.length) + '</span>';
                // 更新起始位置
                startIndex = index + searchTerm.length;
            }
            
            // 添加剩余文本
            result += text.substring(startIndex);
            return result;
        }
        
        // 监听搜索框输入事件
        if (searchInput) {
            // 延迟执行搜索，提高性能
            searchInput.addEventListener('input', () => {
                clearTimeout(window.searchTimeout);
                window.searchTimeout = setTimeout(handleSearch, 200);
            });
            
            // 初始化占位符
            searchInput.placeholder = 'Search...';
            
            // 点击事件：清除占位符
            searchInput.addEventListener('click', () => {
                searchInput.placeholder = '';
            });
            
            // 失焦事件：输入框为空时恢复占位符
            searchInput.addEventListener('blur', () => {
                if (!searchInput.value.trim()) {
                    searchInput.placeholder = 'Search...';
                }
            });
        }
        
        // 移动端侧边栏功能 ==========
        // 移动端侧边栏切换 - 变量名同步
        mobileSidebarToggle.addEventListener('click', () => {
            sidebarListSelector.classList.toggle('mobile-open');
        });
        
        // 点击侧边栏外部关闭 - 变量名同步
        document.addEventListener('click', (e) => {
            if (sidebarCollapseQuery.matches &&
                !sidebarListSelector.contains(e.target) && 
                !mobileSidebarToggle.contains(e.target) &&
                sidebarListSelector.classList.contains('mobile-open')) {
                sidebarListSelector.classList.remove('mobile-open');
            }
        });
        
        // 仅在统一断点状态改变时清理临时抽屉状态
        sidebarCollapseQuery.addEventListener('change', (event) => {
            if (!event.matches) {
                sidebarListSelector.classList.remove('mobile-open');
            }
        });
        
        // ========== 专注模式功能 ==========
        // 切换Focus模式
        function toggleFocusMode() {
            const body = document.body;
            const isFocusMode = body.classList.toggle('focus-mode');
            
            if (isFocusMode) {
                focusModeBtn.textContent = 'Focusing';
                focusModeBtn.classList.add('active');
                // 保留顶部和底部状态显示
            } else {
                focusModeBtn.textContent = 'Focus';
                focusModeBtn.classList.remove('active');
                // 状态显示一直保持可见
            }
        }
        
        // 处理ESC键退出Focus模式
        function handleEscapeKey(event) {
            if (event.key === 'Escape' && document.body.classList.contains('focus-mode')) {
                toggleFocusMode();
            }
        }
        
        // Focus模式按钮点击事件
        focusModeBtn.addEventListener('click', toggleFocusMode);
        
        // 键盘事件监听
        document.addEventListener('keydown', handleEscapeKey);
        
        // ========== 进度条功能 ==========
        // 更新进度条 - 元素ID同步
        function updateProgressBar() {
            const progressBar = document.getElementById('progress-fill');
            if (currentWords.length > 0) {
                progressBar.style.width = `${((currentIndex + 1) / currentWords.length) * 100}%`;
            } else {
                progressBar.style.width = '0%';
            }
        }
        
        // ========== 列表信息功能 ==========
        // 更新列表统计信息 - 元素ID同步
        function updateListStats() {
            document.getElementById('sidebar-info').textContent = 
                `${activeList} (${currentWords.length} words)`;
        }
        
        // ========== 状态显示功能 ==========
        // 更新状态显示 - 同时更新顶部和底部
        function updateBottomStatus() {
            const statusText = `${activeList} in ${isOrdered ? 'Order' : 'Disorder'}`;
            
            if (pageBottomStatus) {
                pageBottomStatus.textContent = statusText;
            }
            
            if (pageTopStatus) {
                pageTopStatus.textContent = statusText;
            }
        }
        
        // ========== 单词列表弹窗功能 ==========
        // 打开单词列表弹窗 - 变量名同步
        function openWordTable() {
            updateWordTable();
            wordListModal.classList.add('active');
            
            // 显示搜索框
            const searchInput = document.getElementById('search');
            if (searchInput) {
                searchInput.style.display = 'block';
            }
        }
        
        // 关闭单词列表弹窗 - 变量名同步
        function closeWordTable() {
            wordListModal.classList.remove('active');
            
            // 隐藏搜索框
            const searchInput = document.getElementById('search');
            if (searchInput) {
                searchInput.style.display = 'none';
            }
        }
        
        // 更新单词列表弹窗内容 - 元素类名/ID同步
        function updateWordTable() {
            if (!wordListModalContainer) return;
            
            // 清空容器
            wordListModalContainer.innerHTML = '';
            
            // 更新标题，分别显示列表名称和单词数量（左对齐和右对齐）
            // 使用内联样式确保正确对齐，避免被其他CSS覆盖
            wordListModalTitle.innerHTML = `
                <div style="display: flex; justify-content: space-between; width: 100%; box-sizing: border-box;">
                    <span>${activeList}</span>
                    <span>${wordLists[activeList].length} words</span>
                </div>
            `;
            
            // 同步搜索框状态
            const searchInput = document.getElementById('search');
            if (searchInput && searchInput.value.trim()) {
                // 如果搜索框有内容，立即执行搜索
                setTimeout(handleSearch, 0);
            }
            // 确保标题容器本身有足够的宽度
            wordListModalTitle.style.width = '100%';
            wordListModalTitle.style.boxSizing = 'border-box';
            
            // 生成单词列表内容 - 始终使用order模式下的原始顺序
            const words = [...wordLists[activeList]]; // 直接使用原始词表顺序，不进行排序
            
            // 保留底部分隔线但不显示内容
            if (wordListModalStats) {
                // 只需清空内容，样式由CSS统一控制
                wordListModalStats.textContent = '';
                // 确保元素仍然显示
                wordListModalStats.style.display = 'block';
            }
            
            words.forEach((wordObj, index) => {
                const wordItem = document.createElement('div');
                let className = 'modal-item';
                wordItem.className = className; // 类名同步
                wordItem.innerHTML = `
                    <div class="item-word">${wordObj.word}</div> <!-- 类名同步 -->
                    <div class="item-definition">${wordObj.definition}</div> <!-- 类名同步 -->
                `;
                
                // 点击单词项可以快速跳转到该单词 - 逻辑不变
                wordItem.addEventListener('click', () => {
                    if (isOrdered) {
                        currentIndex = index;
                    } else {
                        // 在乱序模式下，找到该单词在currentWords中的实际位置
                        const actualIndex = currentWords.findIndex(w => w.word === wordObj.word);
                        if (actualIndex !== -1) {
                            currentIndex = actualIndex;
                        }
                    }
                    displayCurrentWord();
                    closeWordTable();
                });
                
                wordListModalContainer.appendChild(wordItem);
            });
            
            // 更新统计信息
            wordListModalStats.textContent = ''; // 清空内容，只保留装饰线
        }
        
        // ========== 单词列表功能 ==========
        // 切换单词列表 - 元素类名同步
        function switchList(listName) {
            console.log('Switching to list:', listName);
            activeList = listName;
            currentWords = wordLists[activeList] || [];
            currentIndex = 0;
            
            // 更新按钮激活状态 - 类名同步为.list-select-btn
            document.querySelectorAll('.list-select-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.list === listName);
            });
            
            // 更新显示 - 逻辑不变
            updateListStats();
            updateProgressBar();
            updateBottomStatus();
            
            // 加载单词 - 逻辑不变
            if (currentWords.length === 0) {
                document.getElementById('word').textContent = 'No words in this list';
                document.getElementById('definition').innerHTML = '';
                document.getElementById('counter').textContent = '';
            } else {
                currentWords = isOrdered ? [...currentWords] : [...currentWords].sort(() => Math.random() - 0.5);
                displayCurrentWord();
            }
            
            updateButtonStates();
        }
        
        // 切换顺序/随机模式 - 元素类名同步
        function setOrder(orderType) {
            isOrdered = orderType === 'ordered';
            // 类名同步为.btn-order
            document.querySelectorAll('.btn-order').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.order === orderType);
            });
            
            updateBottomStatus();
            switchList(activeList);
        }
        
        // ========== 按钮状态管理 ==========
        // 更新按钮状态 - 元素ID同步
        function updateButtonStates() {
            const prevBtn = document.getElementById('btn-prev');
            const nextBtn = document.getElementById('btn-next');
            const showBtn = document.getElementById('btn-toggle');
            const hasWords = currentWords.length > 0;
            const wordEl = document.getElementById('word');
            const isCompleted = wordEl && wordEl.textContent === 'Congratulations!';
            
            // 处理上一个按钮 - 逻辑不变
            if (prevBtn) {
                prevBtn.disabled = currentIndex === 0 || !hasWords;
                prevBtn.style.opacity = (currentIndex === 0 || !hasWords) ? '0.5' : '1';
                prevBtn.style.cursor = (currentIndex === 0 || !hasWords) ? 'not-allowed' : 'pointer';
            }
            
            // 处理下一个按钮 - 仅在完成状态时禁用
            if (nextBtn) {
                nextBtn.disabled = isCompleted;
                nextBtn.style.opacity = nextBtn.disabled ? '0.5' : '1';
                nextBtn.style.cursor = nextBtn.disabled ? 'not-allowed' : 'pointer';
            }
            
            // 处理显示定义按钮 - 在完成状态时禁用
            if (showBtn) {
                showBtn.disabled = isCompleted;
                showBtn.style.opacity = isCompleted ? '0.5' : '1';
                showBtn.style.cursor = isCompleted ? 'not-allowed' : 'pointer';
                // 非完成状态时保持文本为'Display'
                if (!isCompleted) {
                    showBtn.textContent = 'Display';
                }
            }
        }
        
        // 语音播报功能相关变量和函数
        let voices = [];
        
        // 初始化语音列表
        function initVoices() {
            voices = window.speechSynthesis.getVoices();
        }
        
        // 监听语音列表变化
        window.speechSynthesis.onvoiceschanged = initVoices;
        
        // 初始化语音
        initVoices();
        
        // 语音播报函数
        function speak(text, accent) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            // 尝试找到匹配的语音，如果找不到则使用默认语音
            utterance.voice = voices.find(v => v.lang === accent) || voices[0];
            utterance.lang = accent;
            window.speechSynthesis.speak(utterance);
        }
        
        // ========== 单词显示功能 ==========
        // 显示当前单词 - 元素ID同步
        function displayCurrentWord() {
            const wordEl = document.getElementById('word');
            const defEl = document.getElementById('definition');
            const counterEl = document.getElementById('counter');
            const defWrapper = document.querySelector('.definition-area'); // 类名同步
            const showBtn = document.getElementById('btn-toggle');
            
            if (!wordEl || !defEl || !counterEl) {
                console.error('Required DOM elements not found');
                return;
            }
            
            // 重置释义元素 - 完全清空内容
            defEl.classList.remove('visible');
            defEl.innerHTML = ''; // 清空内容，防止误触
            if (defWrapper) defWrapper.scrollTop = 0;
            
            // 重置显示定义按钮文本
            if (showBtn) {
                showBtn.textContent = 'Display';
            }
            
            if (currentWords.length > 0 && currentIndex < currentWords.length) {
                wordEl.textContent = currentWords[currentIndex].word;
                counterEl.textContent = `Word ${currentIndex + 1} / ${currentWords.length}`;
            } else {
                wordEl.textContent = 'No words available';
                counterEl.textContent = '';
            }
            
            updateProgressBar();
            updateButtonStates();
        }
        
        // 显示/隐藏定义（切换功能） - 逻辑不变
        function showDefinition() {
            const defEl = document.getElementById('definition');
            const showBtn = document.getElementById('btn-toggle');
            const wordEl = document.getElementById('word');
            
            // 检查是否处于完成状态（显示Congratulations）
            const isCompleted = wordEl && wordEl.textContent === 'Congratulations!';
            if (isCompleted) {
                // 如果是，不执行任何操作
                return;
            }
            
            if (defEl && currentWords.length > 0 && currentIndex < currentWords.length) {
                // 检查是否已显示
                if (defEl.classList.contains('visible')) {
                    // 如果已显示，则隐藏
                    defEl.classList.remove('visible');
                    defEl.innerHTML = '';
                    if (showBtn) showBtn.textContent = 'Display';
                } else {
                    // 如果未显示，则渲染并显示释义内容
                    const defParts = currentWords[currentIndex].definition.split('；').filter(part => part.trim() !== '');
                    const word = currentWords[currentIndex].word;
                    const youdaoLink = `<a href="https://dict.youdao.com/result?word=${encodeURIComponent(word)}&lang=en" target="_blank" class="word-definition-link word-youdao-link">有道词典</a>`;
                    const usPronunciation = `<span class="word-pronunciation-container"><a href="javascript:void(0)" onclick="speak('${word}', 'en-US')" class="word-definition-link word-pronunciation-btn">英式发音</a></span>`;
                    const ukPronunciation = `<span class="word-pronunciation-container"><a href="javascript:void(0)" onclick="speak('${word}', 'en-GB')" class="word-definition-link word-pronunciation-btn">美式发音</a></span>`;
                    defParts.push(youdaoLink + usPronunciation + ukPronunciation);
                    defEl.innerHTML = defParts.join('；<br>');
                    defEl.classList.add('visible');
                    if (showBtn) showBtn.textContent = 'Conceal';
                }
            }
        }
        
        // 上一个单词 - 元素ID同步
        function prevWord() {
            const wordEl = document.getElementById('word');
            if (!wordEl) return;
            
            // 检查是否正在显示完成信息
            if (wordEl.textContent === 'Congratulations!') {
                // 如果是，直接显示最后一个单词
                currentIndex = currentWords.length - 1;
                displayCurrentWord();
            } else if (currentIndex > 0) {
                currentIndex--;
                displayCurrentWord();
            }
        }
        
        // 下一个单词 - 逻辑不变
        function nextWord() {
            if (currentWords.length > 0) {
                if (currentIndex < currentWords.length - 1) {
                    currentIndex++;
                    displayCurrentWord();
                } else {
                    // 已经是最后一个单词，显示完成信息
                    const wordEl = document.getElementById('word');
                    const defEl = document.getElementById('definition');
                    const counterEl = document.getElementById('counter');
                    
                    if (wordEl && defEl && counterEl) {
                        wordEl.textContent = 'Congratulations!';
                        defEl.innerHTML = `You have completed ${activeList}!`;
                        defEl.classList.add('visible');
                        counterEl.textContent = `100%`;
                        
                        // 更新进度条为100%
                        document.getElementById('progress-fill').style.width = '100%';
                        
                        updateButtonStates();
                    }
                }
            }
        }
        
        // ========== 页面初始化 ==========
        // 页面加载完成后初始化 - 元素类名/ID同步
        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOM loaded, initializing...');
            
            // 初始化主题
            initTheme();
            
            // 初始化显示
            updateListStats();
            updateProgressBar();
            updateButtonStates();
            
            // 绑定列表切换事件 - 类名同步为.list-select-btn
            document.querySelectorAll('.list-select-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    console.log('List button clicked:', btn.dataset.list);
                    switchList(btn.dataset.list);
                });
            });
            
            // 绑定顺序切换事件 - 类名同步为.btn-order
            document.querySelectorAll('.btn-order').forEach(btn => {
                btn.addEventListener('click', () => {
                    console.log('Order button clicked:', btn.dataset.order);
                    setOrder(btn.dataset.order);
                });
            });
            
            // 绑定功能按钮事件 - 元素ID同步
            const prevBtn = document.getElementById('btn-prev');
            const showBtn = document.getElementById('btn-toggle');
            const nextBtn = document.getElementById('btn-next');
            
            if (prevBtn) prevBtn.addEventListener('click', prevWord);
            if (showBtn) showBtn.addEventListener('click', showDefinition);
            if (nextBtn) nextBtn.addEventListener('click', nextWord);
            
            // 让speak函数可以通过onclick属性访问
            window.speak = speak;
            
            // 绑定单词列表弹窗按钮事件 - 变量名同步
            if (wordListModalBtn) {
                wordListModalBtn.addEventListener('click', () => {
                    openWordTable();
                    // 打开弹窗后立即应用当前搜索条件
                    handleSearch();
                });
            }
            
            // 已移除关闭按钮，仅保留点击外部关闭功能
            
            // 点击模态框外部关闭单词列表弹窗 - 变量名同步
            wordListModal.addEventListener('click', (e) => {
                if (e.target === wordListModal) {
                    closeWordTable();
                }
            });
            
            // 绑定键盘事件 - 添加返回键关闭侧边栏和单词表
            document.addEventListener('keydown', (e) => {
                if (e.key === ' ' || e.key === 'Enter') {
                    e.preventDefault();
                    showDefinition();
                } else if (e.key === 'ArrowLeft') prevWord();
                else if (e.key === 'ArrowRight') nextWord();
                else if (e.key === 'Escape') {
                    // 关闭单词表
                    closeWordTable();
                    // 关闭移动端侧边栏（电脑模式下默认打开的侧边栏不受影响）
                    if (sidebarListSelector.classList.contains('mobile-open')) {
                        sidebarListSelector.classList.remove('mobile-open');
                    }
                }
            });
            
            // 触摸手势支持 - 逻辑不变
            let touchStartX = 0;
            document.addEventListener('touchstart', (e) => {
                touchStartX = e.changedTouches[0].screenX;
            });
            
            document.addEventListener('touchend', (e) => {
                const touchEndX = e.changedTouches[0].screenX;
                const diffX = touchEndX - touchStartX;
                
                if (Math.abs(diffX) > 50) { // 最小滑动距离
                    if (diffX > 0) {
                        prevWord();
                    } else {
                        nextWord();
                    }
                }
            });
            
            // 更新左侧按钮激活状态以匹配随机选择的词表 - 类名同步
            document.querySelectorAll('.list-select-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.list === activeList);
            });
            
            // 默认乱序设置 - 逻辑不变
            isOrdered = false; // 设为乱序模式
            document.querySelector('.btn-order[data-order="disordered"]').classList.add('active'); // 激活乱序按钮
            document.querySelector('.btn-order[data-order="ordered"]').classList.remove('active'); // 取消顺序按钮激活
            currentWords = [...wordLists[activeList]].sort(() => Math.random() - 0.5); // 加载乱序单词
            
            // 初始化显示 - 逻辑不变
            if (currentWords.length > 0) {
                displayCurrentWord();
            } else {
                const wordEl = document.getElementById('word');
                if (wordEl) {
                    wordEl.textContent = 'No words in this list';
                }
            }
            
            // 初始化底部状态显示 - 逻辑不变
            updateBottomStatus();

            console.log('Initialization complete');
        });
    </script>
</body>
</html>'''
    
    # 输出到 output/ 目录
    output_path = os.path.join(OUTPUT_DIR, 'Word List Cards.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    html_abs_path = os.path.abspath(output_path)
    print(f"HTML file generated: '{html_abs_path}'")
    
    # 备份当前Python脚本到项目根目录的 backups 文件夹
    backup_dir = os.path.join(PROJECT_ROOT, 'backups')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    backup_filename = f'generate_word_list_cards_{timestamp}.py'
    backup_path = os.path.join(backup_dir, backup_filename)
    
    script_path = os.path.abspath(__file__)
    with open(script_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
        dst.write(src.read())
    
    print(f"Python script backed up: '{backup_path}'")

# 主函数 - 逻辑完全不变
def main():
    word_lists = read_word_files()
    total = sum(len(lst) for lst in word_lists.values())
    
    print(f"Read {total} words:")
    for list_name, words in word_lists.items():
        print(f"  - {list_name}: {len(words)} words")
    
    generate_html(word_lists)
    
    # 自动打开网页
    try:
        import webbrowser
        html_path = os.path.join(OUTPUT_DIR, 'Word List Cards.html')
        webbrowser.open(f'file://{os.path.abspath(html_path)}')
        print("Webpage opened automatically in default browser")
    except Exception as e:
        print(f"Failed to open webpage automatically: {e}")
        print(f"Please open '{os.path.join(OUTPUT_DIR, 'Word List Cards.html')}' file manually")

if __name__ == "__main__":
    main()
