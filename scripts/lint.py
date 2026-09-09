#!/usr/bin/env python3
"""
Detects line breaks that look like they were mechanically wrapped mid-sentence,
in Markdown documentation or code comments. Standard library only.

Usage:
    uv run scripts/lint.py <file> [<file> ...]
    uv run scripts/lint.py --json <file>

This is a lint, not a gate: it always exits 0 regardless of how many
findings it reports. It only exits 1 when an input file can't be read.
A finding is a suggestion, not a verdict — deciding whether to fix it
is left to the human or the AI reading the output.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict

# Force UTF-8 output so Japanese text doesn't get mangled on a Windows
# console using a legacy code page (e.g. cp932).
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

# A line ending in one of these characters is considered "sentence-complete"
# and is never flagged.
SENTENCE_END_CHARS = tuple("。」』.!?！？:;：；」)]}>*`")

# A line ending in one of these single Japanese particles/conjunctions is a
# strong signal that the sentence was cut off mid-way.
JP_TRAILING_PARTICLES = (
    "は", "が", "を", "に", "で", "と", "も", "の", "へ", "や", "な", "な、",
    "から", "まで", "より", "ので", "けど", "けれど", "しかし", "ただし",
)

# A line ending in one of these English words (preposition/conjunction/
# article/etc.) is treated the same way.
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

# A YAML mapping key ("name: ...", "- type: markdown", "attributes:").
# Used to skip structural lines in .yml/.yaml files so they aren't mistaken
# for wrapped prose; this deliberately does not try to parse block scalars
# (`key: |`) since that requires tracking indentation, so genuinely wrapped
# prose inside a block scalar can still slip through undetected.
YAML_KEY_RE = re.compile(r"^\s*(-\s+)?[A-Za-z0-9_.\-]+:(\s|$)")

YAML_EXTENSIONS = (".yml", ".yaml")


@dataclass
class Finding:
    file: str
    line: int
    reason: str
    snippet: str
    next_snippet: str


def is_intentional_break(line: str) -> bool:
    """Whether this is an explicit Markdown line break (two trailing spaces
    or a trailing backslash)."""
    return line.rstrip("\n").endswith("  ") or line.rstrip("\n").endswith("\\")


def strip_comment_prefix(line: str) -> str:
    return COMMENT_PREFIX_RE.sub("", line, count=1)


def last_word(text: str) -> str:
    words = re.findall(r"[A-Za-z']+", text)
    return words[-1].lower() if words else ""


def looks_like_mid_sentence_break(current: str, nxt: str) -> str | None:
    """Returns a reason string if this looks like a suspicious break,
    otherwise None."""
    stripped = current.rstrip()
    if not stripped:
        return None
    if is_intentional_break(current):
        return None
    if stripped.endswith(SENTENCE_END_CHARS):
        return None

    next_stripped = nxt.strip()
    if not next_stripped:
        return None  # next line is blank -> paragraph boundary
    if LIST_ITEM_RE.match(nxt) or HEADING_RE.match(nxt) or BLOCKQUOTE_RE.match(nxt):
        return None  # next line starts a new structural element

    body = strip_comment_prefix(stripped)
    for particle in JP_TRAILING_PARTICLES:
        if body.endswith(particle):
            return f'line ends with the particle/conjunction "{particle}"'

    word = last_word(body)
    if word in EN_TRAILING_WORDS:
        return f'line ends with the conjunction/preposition/article "{word}"'

    # English line with no terminal punctuation, continuing into a
    # lowercase-initial next line: likely a mechanical wrap.
    if re.search(r"[A-Za-z]", body) and re.match(r"^[a-z]", next_stripped):
        return "no terminal punctuation, and the next line continues in lowercase (English)"

    # Japanese line with no terminal punctuation and no trailing particle,
    # continuing into a line starting with hiragana/kanji: likely a
    # mechanical wrap.
    if re.search(r"[぀-んァ-ヶ一-龠]", body) and re.match(
        r"^[぀-んァ-ヶ一-龠]", next_stripped
    ):
        return "no terminal punctuation, and the next line continues (Japanese)"

    return None


def frontmatter_end_index(lines: list[str]) -> int:
    """If the file opens with a `---` YAML frontmatter block, return the
    index of its closing `---` line; otherwise return -1. Frontmatter is
    key: value data, not prose, so it's excluded from scanning."""
    if not lines or lines[0].rstrip() != "---":
        return -1
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return i
    return -1


MARKDOWN_EXTENSIONS = (".md", ".markdown", ".mdx")


def is_comment_line(line: str) -> bool:
    return bool(COMMENT_PREFIX_RE.match(line))


def scan_file(path: str) -> list[Finding]:
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    findings: list[Finding] = []
    in_code_fence = False
    frontmatter_end = frontmatter_end_index(lines)
    is_yaml_file = path.lower().endswith(YAML_EXTENSIONS)
    is_markdown = path.lower().endswith(MARKDOWN_EXTENSIONS)

    for i, line in enumerate(lines):
        if i <= frontmatter_end:
            continue
        if is_yaml_file and YAML_KEY_RE.match(line):
            continue
        if CODE_FENCE_RE.match(line):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        if TABLE_ROW_RE.match(line):
            continue
        # In a non-Markdown source file, only comment lines are prose;
        # actual code is never a candidate (it isn't sentences at all,
        # and comparing code line N to code line N+1 produces constant
        # false positives).
        if not is_markdown and not is_comment_line(line):
            continue
        if i + 1 >= len(lines):
            continue

        nxt = lines[i + 1]
        # Likewise, don't compare a comment line to a following line of
        # actual code — that's the end of the comment block, not a
        # mid-sentence continuation.
        if not is_markdown and not is_comment_line(nxt):
            continue

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
            print("No suspicious line breaks found.")
        for f in all_findings:
            print(f"{f.file}:{f.line}: {f.reason}")
            print(f"    > {f.snippet}")
            print(f"    > {f.next_snippet}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
