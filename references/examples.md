# Before/after examples

## README / documentation (Japanese)

```
# Before
このツールはconnpassのイベント参加者情報を取得し、
ランダムに並び替えることができます。LT大会などで
発表順を決める際にお使いください。

## インストール方法
以下のコマンドを実行してインストールしてください。
```

```
# After
このツールはconnpassのイベント参加者情報を取得し、ランダムに並び替えることができます。LT大会などで発表順を決める際にお使いください。

## インストール方法

以下のコマンドを実行してインストールしてください。
```

Line breaks inside a paragraph get merged, but the blank line between a heading and the body text stays (and should be added if it was missing).

## README / documentation (English)

```
# Before
This tool fetches participant information from a
connpass event and lets you shuffle the order at
random. Useful for deciding presentation order at
lightning talk events.
```

```
# After
This tool fetches participant information from a connpass event and lets you shuffle the order at random. Useful for deciding presentation order at lightning talk events.
```

## Bullet lists

```
# Before (an item's description is wrapped)
- `shuffle(array)`: 配列をFisher-Yatesアルゴリズムで
  シャッフルする。非破壊的な実装になっている。
- `saveResult(...)`: 結果をファイルに保存する。
```

```
# After
- `shuffle(array)`: 配列をFisher-Yatesアルゴリズムでシャッフルする。非破壊的な実装になっている。
- `saveResult(...)`: 結果をファイルに保存する。
```

## What NOT to fix (intentional line breaks)

```markdown
Two trailing spaces at the end of a line  
force a line break in Markdown.
```

The above uses two trailing spaces to force an explicit line break (equivalent to `<br>`) — leave it as-is.

```markdown
| Item | Description |
| --- | --- |
| `foo` | This description is quite long, but it lives inside one table cell, so leave it alone |
```

Text inside a table cell should be left alone regardless of length, as long as it isn't split across multiple lines inside the cell itself.

## Code comments (TypeScript)

```ts
// Before
/**
 * connpassのイベント参加者ページをスクレイピングし、
 * 募集枠ごとの参加者一覧を取得する。connpassの公式APIには
 * 参加者一覧を返すエンドポイントが存在しないため、この機能は
 * 常にHTMLスクレイピングで実現している。
 */
```

```ts
// After
/**
 * connpassのイベント参加者ページをスクレイピングし、募集枠ごとの参加者一覧を取得する。connpassの公式APIには参加者一覧を返すエンドポイントが存在しないため、この機能は常にHTMLスクレイピングで実現している。
 */
```

## Code comments (Python docstring)

```python
# Before
def shuffle(items):
    """Shuffle the given list using the Fisher-Yates
    algorithm. The input list is not mutated; a new
    list is returned instead.
    """
```

```python
# After
def shuffle(items):
    """Shuffle the given list using the Fisher-Yates algorithm. The input list is not mutated; a new list is returned instead."""
```

If a docstring is too long to fit in a single readable line, it's fine to break it sentence-by-sentence, as long as no single sentence spans more than one line.

```python
def shuffle(items):
    """Shuffle the given list using the Fisher-Yates algorithm.

    The input list is not mutated; a new list is returned instead.
    """
```
