English | [日本語](README.ja.md)

# fix-unnatural-line-breaks

A Claude Skill that detects and fixes "unnatural line breaks": newlines inserted mid-sentence just to keep lines under some fixed column width.

## What this fixes

It catches things like this:

```
This tool fetches participant information from a
connpass event and lets you shuffle the order at
random. Useful for deciding presentation order at
lightning talk events.
```

The rule is simple: only break lines at meaningful boundaries, such as paragraph breaks, list item boundaries, or around headings.

```
This tool fetches participant information from a connpass event and lets you shuffle the order at random. Useful for deciding presentation order at lightning talk events.
```

It targets both prose documentation (Markdown, README files) and code comments (docstrings, JSDoc, line/block comments). It handles both English and Japanese.

## Why this matters

Most Markdown renderers treat a single newline inside a paragraph as a space, so the rendered output often looks fine either way. Still, the raw source suffers in a few concrete ways.

- The source itself is harder to read and review; a sentence cut off mid-way looks broken in a diff.
- A one-word edit turns into a full-paragraph reflow, making diffs needlessly large.
- In places where line breaks are shown as-is (code comments, terminals, commit messages), the awkward wrapping is visible directly.

## Layout

```
fix-unnatural-line-breaks/
├── SKILL.md              # Core rules + workflow + quick self-check
├── references/
│   ├── detection.md      # How to spot unnatural breaks (Japanese/English)
│   ├── rules.md          # How to fix them
│   └── examples.md       # Before/after pairs
├── scripts/
│   └── lint.py           # Heuristic detector (standard library only)
├── README.md
├── README.ja.md
└── LICENSE
```

`SKILL.md`, `references/`, and `scripts/` are all written in English so the Skill itself is equally usable and reviewable by Japanese and English speakers alike (the `description` field that triggers it also includes both English and Japanese phrasing). Detection rules and examples specific to Japanese text are covered within that English prose, using actual Japanese sample sentences where relevant.

## Install

**Claude Code (personal)**

```bash
git clone https://github.com/otnc/fix-unnatural-line-breaks ~/.claude/skills/fix-unnatural-line-breaks
```

**Claude Code (per-project)**

```bash
git clone https://github.com/otnc/fix-unnatural-line-breaks <project>/.claude/skills/fix-unnatural-line-breaks
```

## Usage

If `uv` is available, detection can run mechanically.

```bash
uv run scripts/lint.py path/to/README.md
uv run scripts/lint.py --json path/to/file.ts
```

Without `uv`, Claude reviews the file manually using the criteria in `references/detection.md`.

Detections are only suggestions. Code blocks, tables, and intentional line breaks (two trailing spaces, etc.) are excluded, and whether to actually fix a flagged line is a judgment call based on context.

## Files

**SKILL.md**
Core principles, what to do / what not to do, workflow, and a quick self-check.

**references/detection.md**
How to spot unnatural line breaks: Japanese-specific cues (right after/before a particle, etc.), English-specific cues (mid-prepositional-phrase, etc.), and places where false positives are common.

**references/rules.md**
How to fix what's detected: merging at the paragraph level, deciding upfront which breaks to keep, and how to handle code comments.

**references/examples.md**
Before/after pairs for README prose, bullet lists, and code comments (TypeScript/Python).

**scripts/lint.py**
A standard-library-only detector. It flags likely mechanical wraps based on sentence-ending punctuation, trailing particles/conjunctions, and how the next line starts. Its own output is always in English, regardless of the language of the file being checked.

## Credits

The rule this Skill encodes started as a personal `CLAUDE.md` convention used by [otoneko1102](https://github.com/otoneko1102): never insert unnatural mid-sentence line breaks in documentation or code comments. This Skill packages that rule for general use.

## License

MIT. See `LICENSE`.
