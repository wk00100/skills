#!/usr/bin/env python3
"""PostToolUse hook：檢查 Write／Edit／MultiEdit 寫入的中文是否違反 ~/.claude/CLAUDE.md 用字規則。

只檢查 regex 抓得到的違規，同概念換詞、業務名稱回譯等需要理解語意的規則仍靠人工自檢。
命中時以 additionalContext 回報給模型，不阻擋寫入。部分規則會誤判，由模型確認是否為合理用法。
"""
import json
import re
import sys
from pathlib import Path

CJK = re.compile(r"[一-鿿]")

# 規則範例行（「A → B」）與引號內的示範文字會刻意出現禁用詞，不檢查
SKIP_LINE = re.compile(r"→|←")
STRIP_SPANS = [re.compile(r"`[^`\n]*`"), re.compile(r"「[^」\n]*」")]

RULES = [
    ("指示詞", re.compile(r"這個|那個|這些|那些|這條|那條|這類|這次|一句話")),
    ("「的是」強調句", re.compile(r"的是")),
    ("破折號", re.compile(r"——|—")),
    ("全形分號", re.compile(r"；")),
    # 後面接英數時多半是 YAML 或程式碼範例（`topic: [升版, nuxt]`），不算
    ("中文旁的半形標點", re.compile(r"[一-鿿][,;:?!](?!\s*[A-Za-z0-9])|[一-鿿][()]|[()][一-鿿]")),
    (
        "大陸用詞／自造縮寫",
        re.compile(
            r"大概率|視頻|信息|質量|優化|屏幕|文件夾|默認|調用|接口|軟件|打印|內存|鼠標"
            r"|網絡|服務器|代碼|項目|文檔|野路子|接地氣|靠譜|天然|判準|縮略|靜默|兜底"
            r"|契約(?!式設計)"
        ),
    ),
    ("醫療用語", re.compile(r"症狀|病灶|診斷|治療")),
    ("物理比喻／口語動詞", re.compile(r"炸|丟例外|丟出")),
    ("姿態詞", re.compile(r"順手|順便|隨手|乾脆")),
    ("行銷用語", re.compile(r"強大|完美|輕鬆搞定|大幅提升|優雅地|無縫|好問題")),
    ("語境對齊", re.compile(r"讓我確認一下|首先，?讓我")),
    ("emoji", re.compile(r"[\U0001F300-\U0001FAFF☀-➿⭐⭕]")),
]

# 只檢查 Markdown 標題行，內文的數量與問句屬於正常用法
HEADING = re.compile(r"^\s*#{1,6}\s")
HEADING_RULES = [
    ("標題寫數量", re.compile(r"[二三四五六七八九十兩\d]+\s*(?:個|點|種|步驟?|條|類|項|件)")),
    ("標題用問句", re.compile(r"[？?]\s*$|是什麼|怎麼|什麼時候")),
]

CODE_SUFFIXES = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".py", ".sh", ".java",
    ".kt", ".go", ".rb", ".php", ".cs", ".css", ".scss",
}
# 整行註解，取出註解內文
COMMENT_LINE = re.compile(r"^\s*(?://+|#+|/\*+|\*+|<!--)\s?(.*?)\s*(?:\*/|-->)?\s*$")
COMMENT_RULES = [
    # UTF-8、SHA-256 這類標準名稱不算單號
    ("註解寫需求單號", re.compile(r"\b(?!(?:UTF|ISO|SHA|RFC|HTTP|TLS|AES|CRC|MD)-)[A-Z][A-Z0-9]+-\d+\b")),
    ("註解行尾標點", re.compile(r"[，。]$")),
]

MAX_HITS = 20

# 規則檔與本腳本的規則定義會列出禁用詞
# 比對檔名而非完整路徑，repo 內的 CLAUDE.global.md 與 hooks/zh-tw-lint.py 也要跳過
SKIP_FILES = (
    str(Path.home() / ".claude" / "CLAUDE.md"),
)
SKIP_NAMES = ("CLAUDE.global.md", "zh-tw-lint.py")


def collect_texts(tool_input):
    texts = []
    if isinstance(tool_input.get("content"), str):
        texts.append(tool_input["content"])
    if isinstance(tool_input.get("new_string"), str):
        texts.append(tool_input["new_string"])
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict) and isinstance(edit.get("new_string"), str):
            texts.append(edit["new_string"])
    return texts


def find(rules, text):
    return [(name, m.group(0)) for name, pattern in rules for m in pattern.finditer(text)]


def lint_comment(line):
    m = COMMENT_LINE.match(line)
    return find(COMMENT_RULES, m.group(1)) if m else []


def lint_line(line, is_code):
    hits = lint_comment(line) if is_code else []
    if not CJK.search(line) or SKIP_LINE.search(line):
        return hits
    stripped = line
    for span in STRIP_SPANS:
        stripped = span.sub("", stripped)
    hits += find(RULES, stripped)
    if not is_code and HEADING.match(stripped):
        hits += find(HEADING_RULES, stripped)
    return hits


def lint(texts, is_code):
    hits = []
    for text in texts:
        for line in text.splitlines():
            for name, matched in lint_line(line, is_code):
                hits.append(f"- {name}「{matched}」：{line.strip()[:80]}")
    return hits


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path", "")
    if file_path in SKIP_FILES or Path(file_path).name in SKIP_NAMES:
        return
    is_code = Path(file_path).suffix in CODE_SUFFIXES
    hits = lint(collect_texts(tool_input), is_code)
    if not hits:
        return
    shown = hits[:MAX_HITS]
    more = f"\n（另有 {len(hits) - MAX_HITS} 筆未列出）" if len(hits) > MAX_HITS else ""
    context = (
        f"zh-tw-lint：{file_path} 寫入的內容命中 CLAUDE.md 用字規則，逐筆確認後修正。"
        "部分規則會誤判（例如「項目」指條目、「完美匹配」、「炸」出現在專有名詞），確認不是合理用法再修改。\n"
        + "\n".join(shown)
        + more
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": context}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
