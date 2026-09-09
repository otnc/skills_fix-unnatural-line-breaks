# Changelog

## 0.2.0

- Rewrote `SKILL.md` and all of `references/` in English so the Skill is equally usable and reviewable for English- and Japanese-speaking users. Japanese-specific detection rules and examples are still fully covered, explained in English prose with real Japanese sample text.
- Made the `description` frontmatter trigger on both English and Japanese phrasing (e.g. "fix the line breaks" / "改行がおかしい").
- Translated `scripts/lint.py`'s docstring, comments, and output messages to English. Detection logic and heuristics are unchanged.
- Swapped which README is primary: `README.md` is now English, `README.ja.md` is Japanese (previously `README.md` was Japanese and `README.en.md` was English).

## 0.1.0

- Initial version. Captured the "no unnatural mid-sentence line breaks" detection/fix rules in `SKILL.md` and `references/`.
- Added `scripts/lint.py`, a standard-library-only detector covering both Japanese (breaks after particles/conjunctions) and English (breaks after prepositions/conjunctions/articles, or a lowercase-initial continuation line).
