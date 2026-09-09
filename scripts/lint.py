#!/usr/bin/env python3
"""
文章(Markdownドキュメント・コードコメント)の中から、文の途中で機械的に
折り返されたと思われる改行を検出する。標準ライブラリのみで動作する。

使い方:
    uv run scripts/lint.py <file> [<file> ...]
    uv run scripts/lint.py --json <file>

このスクリプトはlintであり、検出件数によって終了コードを変えることはしない
(exit code 0)。入力ファイルが読めない場合のみ exit code 1 を返す。
検出はあくまで疑いの提示であり、直すかどうかの判断は人間・AIが行う。
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict

# Windowsのコンソールがcp932等の場合に日本語出力が文字化けするのを防ぐ。
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

# 行末がこれらで終わっていれば「文が終わっている」とみなし、疑わない。
SENTENCE_END_CHARS = tuple("。」』.!?！？:;：；」)]}>*`")

# 行末がこれらの助詞・接続助詞1語で終わっていれば、文の途中で切れている疑いが強い。
JP_TRAILING_PARTICLES = (
    "は", "が", "を", "に", "で", "と", "も", "の", "へ", "や", "な", "な、",
    "から", "まで", "より", "ので", "けど", "けれど", "しかし", "ただし",
)

# 行末がこれらの英単語(前置詞・接続詞・冠詞など)で終わっていれば疑う。
EN_TRAILING_WORDS = {
    "a", "an", "the", "and", "or", "but", "of", "to", "with", "in", "on",
    "at", "for", "that", "which", "who", "as", "is", "are", "was", "were",
    "be", "been", "this", "these", "those", "it", "its", "not",
}

CODE_FENCE_RE = re.compile(r"^\s*```")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
LIST_ITEM_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
HEADING_RE = re.compile(r"^\s*#{1,6}\s+")
COMMENT_PREFIX_RE = re.compile(r"^\s*(//|#|\*|///|;;)\s?")
BLOCKQUOTE_RE = re.compile(r"^\s*>")


@dataclass
class Finding:
    file: str
    line: int
    reason: str
    snippet: str
    next_snippet: str


def is_intentional_break(line: str) -> bool:
    """Markdownの明示的な改行(行末半角スペース2つ、バックスラッシュ)かどうか"""
    return line.rstrip("\n").endswith("  ") or line.rstrip("\n").endswith("\\")


def strip_comment_prefix(line: str) -> str:
    return COMMENT_PREFIX_RE.sub("", line, count=1)


def last_word(text: str) -> str:
    words = re.findall(r"[A-Za-z']+", text)
    return words[-1].lower() if words else ""


def looks_like_mid_sentence_break(current: str, nxt: str) -> str | None:
    """怪しい改行なら理由の文字列を、問題なければNoneを返す"""
    stripped = current.rstrip()
    if not stripped:
        return None
    if is_intentional_break(current):
        return None
    if stripped.endswith(SENTENCE_END_CHARS):
        return None

    next_stripped = nxt.strip()
    if not next_stripped:
        return None  # 次が空行 = 段落境界
    if LIST_ITEM_RE.match(nxt) or HEADING_RE.match(nxt) or BLOCKQUOTE_RE.match(nxt):
        return None  # 新しい構造の始まり

    body = strip_comment_prefix(stripped)
    for particle in JP_TRAILING_PARTICLES:
        if body.endswith(particle):
            return f'行末が助詞・接続語「{particle}」で終わっている'

    word = last_word(body)
    if word in EN_TRAILING_WORDS:
        return f'行末が接続語/前置詞/冠詞 "{word}" で終わっている'

    # 英語の行で、文末記号がなく、次の行が小文字始まりで続いている場合は
    # 機械的な折り返しの可能性が高い。
    if re.search(r"[A-Za-z]", body) and re.match(r"^[a-z]", next_stripped):
        return "文末記号がないまま次の行が小文字で続いている(英語)"

    # 日本語の行で、文末記号もなく助詞でもないが、次の行がひらがな/漢字から
    # 始まっていて大文字開始でもない場合は、機械的な折り返しの可能性を示す。
    if re.search(r"[぀-んァ-ヶ一-龠]", body) and re.match(
        r"^[぀-んァ-ヶ一-龠]", next_stripped
    ):
        return "文末記号がないまま次の行に続いている(日本語)"

    return None


def scan_file(path: str) -> list[Finding]:
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    findings: list[Finding] = []
    in_code_fence = False

    for i, line in enumerate(lines):
        if CODE_FENCE_RE.match(line):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        if TABLE_ROW_RE.match(line):
            continue
        if i + 1 >= len(lines):
            continue

        nxt = lines[i + 1]
        reason = looks_like_mid_sentence_break(line, nxt)
        if reason:
            findings.append(
                Finding(
                    file=path,
                    line=i + 1,
                    reason=reason,
                    snippet=line.strip(),
                    next_snippet=nxt.strip(),
                )
            )

    return findings


def main() -> int:
    args = sys.argv[1:]
    as_json = "--json" in args
    files = [a for a in args if a != "--json"]

    if not files:
        print("usage: lint.py [--json] <file> [<file> ...]", file=sys.stderr)
        return 1

    all_findings: list[Finding] = []
    for path in files:
        try:
            all_findings.extend(scan_file(path))
        except OSError as e:
            print(f"error: {path}: {e}", file=sys.stderr)
            return 1

    if as_json:
        print(json.dumps([asdict(f) for f in all_findings], ensure_ascii=False, indent=2))
    else:
        if not all_findings:
            print("不自然な改行の疑いは見つかりませんでした。")
        for f in all_findings:
            print(f"{f.file}:{f.line}: {f.reason}")
            print(f"    > {f.snippet}")
            print(f"    > {f.next_snippet}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
