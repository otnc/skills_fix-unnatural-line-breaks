# How to fix it

## Basic operation: join the lines

Once you find an unnatural break, remove the newline and merge the two lines into one. For Japanese, just delete the newline — no space is needed between the joined text. For English, replace the newline with a single space so the words don't run together.

```
# Before (Japanese, mechanically wrapped)
これはとても長い説明文で、途中で改行が
入ってしまっているために読みにくく
なっている例です。

# After
これはとても長い説明文で、途中で改行が入ってしまっているために読みにくくなっている例です。
```

```
# Before (English)
This is a long explanation that has
been wrapped at an arbitrary column
width, which makes it awkward to read.

# After
This is a long explanation that has been wrapped at an arbitrary column width, which makes it awkward to read.
```

## Work paragraph by paragraph

When a paragraph has several unnatural breaks, join the whole paragraph into one line first, then re-check for any boundary that should actually be kept. Fixing line-by-line in isolation can leave inconsistencies with the next line you haven't looked at yet, so treat each paragraph as one unit of work.

## Decide which breaks to keep before you start joining

Before merging anything, decide that the following breaks are off-limits.

- Blank lines (paragraph boundaries).
- The line breaks immediately before and after a heading.
- The line break between one list item and the next.
- Any line break inside a fenced code block (\`\`\`).
- Any line break inside a table row.
- An explicit Markdown line break (two trailing spaces, a trailing backslash, or `<br>`).

Only join line breaks that don't fall into one of these categories.

## When a single list item is long

If one bullet's description is long and has been wrapped across multiple lines, merge the whole item back into one line. It's fine to split the item into multiple sentences if that helps clarity, but don't then wrap those sentences again.

```
# Before
- この関数は与えられた配列をシャッフルする。
  内部的にはFisher-Yatesアルゴリズムを使って
  おり、引数の配列自体は書き換えない。

# After
- この関数は与えられた配列をシャッフルする。内部的にはFisher-Yatesアルゴリズムを使っており、引数の配列自体は書き換えない。
```

## Code comments and docstrings

Keep the comment syntax (`//`, `#`, `*`, etc.) intact and only merge the text content. When one sentence spans several `//` lines, collapse it into a single `//` line. If the comment intentionally separates paragraphs (for example, with a blank comment line between them), keep that separation and merge within each paragraph.

```ts
// Before
// この関数はイベントIDを受け取り、connpassの
// 参加者ページをスクレイピングして、募集枠ごとの
// 参加者一覧を返す。

// After
// この関数はイベントIDを受け取り、connpassの参加者ページをスクレイピングして、募集枠ごとの参加者一覧を返す。
```

For JSDoc/docstrings with tags like `@param` or `@returns`, keep each tag on its own line as a structural boundary, and only merge the description text within a single tag.

```ts
/**
 * Before
 * @param eventId 対象イベントのID。connpassのURLに含まれる
 *   数値部分を渡す。
 */

/**
 * After
 * @param eventId 対象イベントのID。connpassのURLに含まれる数値部分を渡す。
 */
```

## After you fix it

- Re-read the merged text to confirm the meaning and nuance haven't shifted.
- A resulting line that's now very long is not a sign of failure — let the display's soft-wrap handle it.
- If a diff would otherwise balloon in size (a one-character fix turning into a full paragraph reflow), either explain why in the commit/PR description, or avoid bundling it with an unrelated change.
