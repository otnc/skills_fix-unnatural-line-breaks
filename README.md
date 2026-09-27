# fix-unnatural-line-breaks

**English** | [日本語](README.ja.md)

An [Agent Skill](https://agentskills.io/specification) that detects and fixes "unnatural line breaks": newlines inserted mid-sentence just to keep lines under some fixed column width. It works with any agent that supports Agent Skills (Claude Code, Codex, GitHub Copilot, Cursor, OpenCode and more) and installs with the [skills CLI](https://github.com/vercel-labs/skills).

## What this fixes

It catches things like this:

```
Call me Ishmael. Some years ago—never mind how long
precisely—having little or no money in my purse, and
nothing particular to interest me on shore, I thought
I would sail about a little and see the watery part
of the world.
```

The rule is simple: only break lines at meaningful boundaries, such as paragraph breaks, list item boundaries, or around headings.

```
Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.
```

It targets both prose documentation (Markdown, README files) and code comments (docstrings, JSDoc, line/block comments). It handles both English and Japanese.

## Why this matters

Most Markdown renderers treat a single newline inside a paragraph as a space, so the rendered output often looks fine either way. Still, the raw source suffers in a few concrete ways.

- The source itself is harder to read and review; a sentence cut off mid-way looks broken in a diff.
- A one-word edit turns into a full-paragraph reflow, making diffs needlessly large.
- In places where line breaks are shown as-is (code comments, terminals, commit messages), the awkward wrapping is visible directly.

## Layout

```
skills/
└── fix-unnatural-line-breaks/   # the skill itself: what the skills CLI installs
    ├── SKILL.md                 # Core rules + workflow + quick self-check
    ├── references/
    │   ├── detection.md         # How to spot unnatural breaks (Japanese/English)
    │   ├── rules.md             # How to fix them
    │   └── examples.md          # Before/after pairs
    └── scripts/
        └── lint.mjs             # Heuristic detector (plain Node.js, no dependencies)
tests/
└── lint.test.mjs                # node:test suite for lint.mjs (`npm test`)
base/
└── README.base.md               # Source of README.md and README.ja.md (built by kiritan)
.agents/skills/kiritan/          # kiritan's own skill, for agents editing the README
```

Only `skills/fix-unnatural-line-breaks/` is installed into your agent; the tests, README sources and CI files stay in this repository.

`SKILL.md`, `references/`, and `scripts/` are all written in English so the Skill itself is equally usable and reviewable by Japanese and English speakers alike (the `description` field that triggers it also includes both English and Japanese phrasing). Detection rules and examples specific to Japanese text are covered within that English prose, using actual Japanese sample sentences where relevant.

## Install

Install with the [skills CLI](https://github.com/vercel-labs/skills). Without `-a`, it asks which agents to install for:

```bash
npx skills add otnc/skills_fix-unnatural-line-breaks
```

Or name the agent directly:

```bash
npx skills add otnc/skills_fix-unnatural-line-breaks -a claude-code
npx skills add otnc/skills_fix-unnatural-line-breaks -a codex
npx skills add otnc/skills_fix-unnatural-line-breaks -a github-copilot
npx skills add otnc/skills_fix-unnatural-line-breaks -a cursor
npx skills add otnc/skills_fix-unnatural-line-breaks -a opencode
```

- Add `-g` to install for your user (all projects) instead of the current project.
- Update later with `npx skills update fix-unnatural-line-breaks`, and uninstall with `npx skills remove fix-unnatural-line-breaks`.
- Without the CLI, copy `skills/fix-unnatural-line-breaks/` into your agent's skills directory (for example `~/.claude/skills/` or `.agents/skills/`).

> [!NOTE]
>   
> Up to v0.4.0, `SKILL.md` sat at the repository root and the README suggested `git clone`-ing the whole repository into `~/.claude/skills/`. If you installed it that way, delete that clone and install again with the command above.

## Usage

Ask the agent in your own words, for example "fix the unnatural line breaks in README.md" or "文の途中で改行が入っているので直して". The skill also applies while the agent writes or reviews documentation and comments.

Detection runs mechanically with plain Node.js — no install, no third-party dependency. Run it from your project root, pointing at the installed skill's directory:

```bash
node .claude/skills/fix-unnatural-line-breaks/scripts/lint.mjs path/to/README.md
node .agents/skills/fix-unnatural-line-breaks/scripts/lint.mjs --json path/to/file.ts
```

Without Node.js, the agent reviews the file manually using the criteria in `references/detection.md`.

Detections are only suggestions, and the list is not exhaustive: the script is a small set of regex heuristics, so it flags some lines that are actually fine (code blocks, tables, intentional line breaks) and misses real unnatural breaks that don't match any of its rules. Whether to fix a flagged line is a judgment call based on context, and the agent also reads the whole file by eye — not just the flagged lines — to catch what the script missed.

## Files

**SKILL.md**
Core principles, what to do / what not to do, workflow, and a quick self-check.

**references/detection.md**
How to spot unnatural line breaks: Japanese-specific cues (right after/before a particle, etc.), English-specific cues (mid-prepositional-phrase, etc.), and places where false positives are common.

**references/rules.md**
How to fix what's detected: merging at the paragraph level, deciding upfront which breaks to keep, and how to handle code comments.

**references/examples.md**
Before/after pairs for README prose, bullet lists, and code comments (TypeScript/Python).

**scripts/lint.mjs**
A dependency-free Node.js detector. It flags likely mechanical wraps based on sentence-ending punctuation, trailing particles/conjunctions, and how the next line starts, plus a bare `//`/`#`/`*` line used as a paragraph separator inside a comment block. For non-Markdown files, it only ever compares comment lines (`//`, `#`, `*`, `///`, `;;`) against each other, so it works across `#`-comment languages (Python, Shell, Ruby, YAML, ...) and C-style `//`/`/** */` comments alike. Its own output is always in English, regardless of the language of the file being checked. Its findings are not exhaustive — see `references/detection.md`.

**tests/lint.test.mjs** (repository only, not installed)
A `node:test` suite covering `lint.mjs`'s core detection and false-positive-avoidance behavior. Run it with `npm test`.

## Development

The skill and its tests need only Node.js 18+. Building the README needs Node.js 22.7+ for [kiritan](https://github.com/otnc/kiritan), installed as a dev dependency with `npm install`.

```bash
npm test                 # lint.mjs test suite
npm run lint:self        # run lint.mjs over this repository's own docs and comments
npm run docs:build       # regenerate README.md and README.ja.md from base/README.base.md
npm run docs:verify      # confirm they match the base file (CI)
```

`README.md` and `README.ja.md` are generated: edit `base/README.base.md`, which holds both languages in `:::kiritan{locale=...}` blocks, then run `npm run docs:build`.

The repository also carries [kiritan's own skill](https://github.com/otnc/kiritan/tree/main/skills/kiritan) in `.agents/skills/kiritan/`, which agents that read `.agents/skills/` (Codex, Cursor, GitHub Copilot, OpenCode and others) pick up directly. Claude Code reads `.claude/skills/`, which is not committed; run `npx skills add otnc/kiritan --skill kiritan -a claude-code` once to link it there.

## Credits

The rule this Skill encodes started as a personal `CLAUDE.md` convention used by [otoneko.](https://github.com/otnc): never insert unnatural mid-sentence line breaks in documentation or code comments. This Skill packages that rule for general use.

## License

MIT. See `LICENSE`.
