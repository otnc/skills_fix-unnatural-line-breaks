# Changelog

Version stays at 0.1.0 until this Skill is published on GitHub; only fixes made after that first public release bump the version.

## 0.1.0

- Captured the "no unnatural mid-sentence line breaks" detection/fix rules in `SKILL.md` and `references/`, written in English so the Skill is equally usable by English- and Japanese-speaking users. Japanese-specific detection rules and examples are fully covered, explained in English prose with real Japanese sample text (drawn from public-domain literature, not any specific product).
- Added `scripts/lint.mjs`, a dependency-free Node.js detector covering both Japanese (breaks after particles/conjunctions) and English (breaks after prepositions/conjunctions/articles, or a lowercase-initial continuation line). Chosen over a Python/`uv`-based script so the tool works wherever Claude Code itself runs, with no extra install.
- `lint.mjs` also recognizes YAML frontmatter and simple `key: value` lines (to avoid mistaking config for prose) and, for non-Markdown source files, only ever compares comment lines against each other — actual code is never treated as a candidate.
