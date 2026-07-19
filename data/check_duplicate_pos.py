import re
import glob

POS_PATTERN = re.compile(r'\b(adj\.|adv\.|n\.|v\.|vt\.|vi\.|prep\.|conj\.|pron\.|art\.|num\.|interj\.)')

def find_duplicates(pos_tags):
    seen = set()
    return [p for p in pos_tags if p in seen or seen.add(p)]

def check_file(filename):
    issues = []
    with open(filename, 'r', encoding='utf-8') as f:
        for num, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or '|' not in line:
                continue
            word, defs = line.split('|', 1)
            blocks = [b.strip() for b in defs.split('；') if b.strip()]
            tags = [m.group(1) for b in blocks if (m := POS_PATTERN.match(b))]
            if dups := find_duplicates(tags):
                issues.append((num, word, list(set(dups)), line))
    return issues

def print_result(txt_file, issues):
    print(f"\n{'='*60}\n[FILE] {txt_file}\n{'-'*60}")
    if issues:
        for num, word, dups, line in issues:
            print(f"[LINE {num}] {word}\n  POS: {', '.join(dups)}\n  TEXT: {line}")
    else:
        print("[OK] No duplicate POS tags found")
    print('='*60)

if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for txt_file in sorted(glob.glob('*.txt')):
        print_result(txt_file, check_file(txt_file))
    print("\n[HINT] Use skill wordlist-formatter to format")
    print("  Correct: word|n.意思1，意思2；adj.意思3；")
    print("  Error:   word|n.意思1；n.意思2；adj.意思3； (duplicate POS 'n.' with semicolon)")
