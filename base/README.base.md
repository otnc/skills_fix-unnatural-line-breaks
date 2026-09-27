# fix-unnatural-line-breaks

:::kiritan{locale=en}
An [Agent Skill](https://agentskills.io/specification) that detects and fixes "unnatural line breaks": newlines inserted mid-sentence just to keep lines under some fixed column width. It works with any agent that supports Agent Skills (Claude Code, Codex, GitHub Copilot, Cursor, OpenCode and more) and installs with the [skills CLI](https://github.com/vercel-labs/skills).
:::

:::kiritan{locale=ja}
文章の途中で、一定の文字数(カラム幅)に合わせて改行を挿入する「不自然な改行」を検出し、直すための [Agent Skill](https://agentskills.io/specification) です。Agent Skills に対応したエージェント(Claude Code、Codex、GitHub Copilot、Cursor、OpenCode など)で使え、[skills CLI](https://github.com/vercel-labs/skills) でインストールできます。
:::

:::kiritan{locale=en}
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
:::

:::kiritan{locale=ja}
## これは何を直すのか

こういう改行を捕まえます。

```
吾輩は猫である。名前はまだ無い。どこで生れたかとんと
見当がつかぬ。何でも薄暗いじめじめした所でニャーニャー
泣いていた事だけは記憶している。
```

改行は段落の区切り・箇条書きの項目・見出しの前後といった、意味のある境界にだけ入れる、というのが基本方針です。

```
吾輩は猫である。名前はまだ無い。どこで生れたかとんと見当がつかぬ。何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。
```

対象はMarkdownなどのドキュメント本文と、コード中のコメント・docstring・JSDocの両方です。日本語・英語のどちらにも対応します。
:::

:::kiritan{locale=en}
## Why this matters

Most Markdown renderers treat a single newline inside a paragraph as a space, so the rendered output often looks fine either way. Still, the raw source suffers in a few concrete ways.

- The source itself is harder to read and review; a sentence cut off mid-way looks broken in a diff.
- A one-word edit turns into a full-paragraph reflow, making diffs needlessly large.
- In places where line breaks are shown as-is (code comments, terminals, commit messages), the awkward wrapping is visible directly.
:::

:::kiritan{locale=ja}
## なぜ直すのか

多くのMarkdownレンダラーは段落内の単一改行を空白1つとして扱うため、見た目には影響しないことが多いですが、次のような場面で実害があります。

- ソース自体が読みにくい(diffやレビューで、文の途中で行が切れているのは不自然)
- 1文字の修正のつもりで段落全体を書き直すと、diffが無意味に大きくなる
- コードコメントやターミナル、コミットメッセージなど、改行がそのまま表示される環境では、見た目にもそのまま崩れる
:::

:::kiritan{locale=en}
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
:::

:::kiritan{locale=ja}
## 構成

```
skills/
└── fix-unnatural-line-breaks/   # スキル本体(skills CLI がインストールするのはここだけ)
    ├── SKILL.md                 # コアルール + 進め方 + クイックチェック
    ├── references/
    │   ├── detection.md         # 不自然な改行の見分け方(日本語/英語)
    │   ├── rules.md             # 直し方のルール
    │   └── examples.md          # before/after の対比例
    └── scripts/
        └── lint.mjs             # 疑わしい改行を機械的に検出するスクリプト(Node.js、依存パッケージなし)
tests/
└── lint.test.mjs                # lint.mjs の node:test テストスイート(`npm test`)
base/
└── README.base.md               # README.md と README.ja.md の原本(kiritan でビルド)
.agents/skills/kiritan/          # README を編集するエージェント向けの kiritan スキル
```

エージェントに入るのは `skills/fix-unnatural-line-breaks/` だけです。テストや README の原本、CI の設定はこのリポジトリに残ります。

SKILL.md・references・scripts の中身はすべて英語で書かれています。Skill自体が日本語話者にも英語話者にも同じように使えるようにするための判断です(トリガーとなる`description`も英語・日本語両方のフレーズを含めています)。日本語のドキュメント・コメントに対する検出ルールや実例は、英語の説明文の中で日本語のサンプル文を示す形で扱っています。
:::

:::kiritan{locale=en}
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
:::

:::kiritan{locale=ja}
## インストール

[skills CLI](https://github.com/vercel-labs/skills) でインストールします。`-a` を付けなければ、どのエージェントに入れるかを対話形式で選べます。

```bash
npx skills add otnc/skills_fix-unnatural-line-breaks
```

エージェントを直接指定する場合は次のとおりです。

```bash
npx skills add otnc/skills_fix-unnatural-line-breaks -a claude-code
npx skills add otnc/skills_fix-unnatural-line-breaks -a codex
npx skills add otnc/skills_fix-unnatural-line-breaks -a github-copilot
npx skills add otnc/skills_fix-unnatural-line-breaks -a cursor
npx skills add otnc/skills_fix-unnatural-line-breaks -a opencode
```

- 現在のプロジェクトではなくユーザー全体(全プロジェクト)に入れるときは `-g` を付けます。
- 更新は `npx skills update fix-unnatural-line-breaks`、削除は `npx skills remove fix-unnatural-line-breaks` です。
- CLI を使わない場合は、`skills/fix-unnatural-line-breaks/` をエージェントのスキル用ディレクトリ(`~/.claude/skills/` や `.agents/skills/` など)にコピーします。

> [!NOTE]
>
> v0.4.0 までは `SKILL.md` がリポジトリ直下にあり、README ではリポジトリ全体を `~/.claude/skills/` に `git clone` する方法を案内していました。その方法で入れている場合は、クローンを削除してから上記のコマンドで入れ直してください。
:::

:::kiritan{locale=en}
## Usage

Ask the agent in your own words, for example "fix the unnatural line breaks in README.md" or "文の途中で改行が入っているので直して". The skill also applies while the agent writes or reviews documentation and comments.

Detection runs mechanically with plain Node.js — no install, no third-party dependency. Run it from your project root, pointing at the installed skill's directory:

```bash
node .claude/skills/fix-unnatural-line-breaks/scripts/lint.mjs path/to/README.md
node .agents/skills/fix-unnatural-line-breaks/scripts/lint.mjs --json path/to/file.ts
```

Without Node.js, the agent reviews the file manually using the criteria in `references/detection.md`.

Detections are only suggestions, and the list is not exhaustive: the script is a small set of regex heuristics, so it flags some lines that are actually fine (code blocks, tables, intentional line breaks) and misses real unnatural breaks that don't match any of its rules. Whether to fix a flagged line is a judgment call based on context, and the agent also reads the whole file by eye — not just the flagged lines — to catch what the script missed.
:::

:::kiritan{locale=ja}
## 使い方

普段の言葉で頼めば動きます。たとえば "README.md の不自然な改行を直して" や "Fix the unnatural line breaks in this file" のように依頼します。エージェントがドキュメントやコメントを書いたりレビューしたりするときにも適用されます。

検出はNode.jsだけで機械的に行えます。インストールも依存パッケージも不要です。プロジェクトのルートから、インストールされたスキルのディレクトリを指定して実行します。

```bash
node .claude/skills/fix-unnatural-line-breaks/scripts/lint.mjs path/to/README.md
node .agents/skills/fix-unnatural-line-breaks/scripts/lint.mjs --json path/to/file.ts
```

Node.jsが無い環境では、エージェントが `references/detection.md` の観点で目視チェックします。

検出結果はあくまで疑いの提示であり、網羅的なリストではありません。スクリプトは少数の正規表現ヒューリスティックにすぎないため、実際は問題ない行(コードブロック・テーブル・意図的な改行など)を誤検出することもあれば、どのルールにも一致しない本物の不自然な改行を見逃すこともあります。実際に直すかどうかは文脈で判断したうえで、エージェントはフラグの立った行だけでなくファイル全体を目視でも読み、スクリプトが見逃した箇所まで拾います。
:::

:::kiritan{locale=en}
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
:::

:::kiritan{locale=ja}
## ファイル

**SKILL.md**
大原則、やること/やらないこと、進め方、クイックセルフチェック。

**references/detection.md**
不自然な改行の見分け方。日本語特有の観点(助詞の直後・直前など)と英語特有の観点(前置詞句の途中など)、誤検出しやすい箇所を整理しています。

**references/rules.md**
検出したあとの直し方。段落単位でまとめる、残すべき改行を先に確定させる、コードコメントでの扱いなど。

**references/examples.md**
README・箇条書き・コードコメント(TypeScript/Python)のbefore/after対比。

**scripts/lint.mjs**
依存パッケージなしで動くNode.js製の検出スクリプト。行末の文末記号・助詞・接続語・次の行の書き出しに加え、コメントブロック内で段落区切りとして使われている裸の`//`・`#`・`*`行からも、機械的な折り返しの疑いを洗い出します。Markdown以外のファイルでは、コメント行(`//`・`#`・`*`・`///`・`;;`)同士だけを比較するので、`#`でコメントを書く言語(Python・Shell・Ruby・YAMLなど)でも、C系の`//`・`/** */`コメントでも動作します。出力メッセージは(チェック対象のファイルの言語に関わらず)英語です。検出結果は網羅的ではありません(`references/detection.md`参照)。

**tests/lint.test.mjs**(リポジトリのみ。インストールはされません)
`lint.mjs`の中核的な検出動作・誤検出回避動作を検証する`node:test`テストスイート。`npm test`で実行できます。
:::

:::kiritan{locale=en}
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
:::

:::kiritan{locale=ja}
## 開発

スキルとテストの実行に必要なのは Node.js 18 以上だけです。README のビルドには [kiritan](https://github.com/otnc/kiritan) を使うため Node.js 22.7 以上が必要で、kiritan は `npm install` で devDependencies として入ります。

```bash
npm test                 # lint.mjs のテスト
npm run lint:self        # このリポジトリ自身のドキュメントとコメントに lint.mjs をかける
npm run docs:build       # base/README.base.md から README.md と README.ja.md を再生成
npm run docs:verify      # 原本と一致しているか確認(CI)
```

`README.md` と `README.ja.md` は生成物です。両言語を `:::kiritan{locale=...}` ブロックで持つ `base/README.base.md` を編集し、`npm run docs:build` を実行してください。

このリポジトリには、README を編集するエージェント向けに [kiritan のスキル](https://github.com/otnc/kiritan/tree/main/skills/kiritan) を `.agents/skills/kiritan/` に同梱しています。`.agents/skills/` を読むエージェント(Codex、Cursor、GitHub Copilot、OpenCode など)はそのまま使えます。Claude Code は `.claude/skills/` を読みますが、こちらはコミットしていないので、一度 `npx skills add otnc/kiritan --skill kiritan -a claude-code` を実行してリンクしてください。
:::

:::kiritan{locale=en}
## Credits

The rule this Skill encodes started as a personal `CLAUDE.md` convention used by [otoneko.](https://github.com/otnc): never insert unnatural mid-sentence line breaks in documentation or code comments. This Skill packages that rule for general use.
:::

:::kiritan{locale=ja}
## クレジット

このSkillが対象とする規則は、[otoneko.](https://github.com/otnc) が個人のCLAUDE.mdで運用していた「ドキュメントやコードコメントで不自然な改行を入れない」というルールを、汎用のSkillとして切り出したものです。
:::

:::kiritan{locale=en}
## License

MIT. See `LICENSE`.
:::

:::kiritan{locale=ja}
## ライセンス

MIT。詳細は `LICENSE` を参照。
:::
