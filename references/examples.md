# before/after 例集

## README・ドキュメント(日本語)

```
# 修正前
このツールはconnpassのイベント参加者情報を取得し、
ランダムに並び替えることができます。LT大会などで
発表順を決める際にお使いください。

## インストール方法
以下のコマンドを実行してインストールしてください。
```

```
# 修正後
このツールはconnpassのイベント参加者情報を取得し、ランダムに並び替えることができます。LT大会などで発表順を決める際にお使いください。

## インストール方法

以下のコマンドを実行してインストールしてください。
```

段落内の改行は詰めるが、見出しとその後の本文の間の空行はそのまま残す(むしろ無かった場合は追加してよい)。

## README・ドキュメント(英語)

```
# 修正前
This tool fetches participant information from a
connpass event and lets you shuffle the order at
random. Useful for deciding presentation order at
lightning talk events.
```

```
# 修正後
This tool fetches participant information from a connpass event and lets you shuffle the order at random. Useful for deciding presentation order at lightning talk events.
```

## 箇条書き

```
# 修正前(項目の説明が折り返されている)
- `shuffle(array)`: 配列をFisher-Yatesアルゴリズムで
  シャッフルする。非破壊的な実装になっている。
- `saveResult(...)`: 結果をファイルに保存する。
```

```
# 修正後
- `shuffle(array)`: 配列をFisher-Yatesアルゴリズムでシャッフルする。非破壊的な実装になっている。
- `saveResult(...)`: 結果をファイルに保存する。
```

## 直さない例(意図的な改行)

```markdown
Markdownでは、行末に半角スペースを2つ置くと  
改行が強制されます。
```

上記は行末の半角スペース2つによる意図的な改行(`<br>`相当)なので、詰めずにそのまま残す。

```markdown
| 項目 | 説明 |
| --- | --- |
| `foo` | これはとても長い説明文だが、テーブルのセル内の改行なので触らない |
```

テーブルのセル内の文章は、たとえ長くても行として分割されていない限り触らない(セル自体を複数行に分けている場合は別)。

## コードコメント(TypeScript)

```ts
// 修正前
/**
 * connpassのイベント参加者ページをスクレイピングし、
 * 募集枠ごとの参加者一覧を取得する。connpassの公式APIには
 * 参加者一覧を返すエンドポイントが存在しないため、この機能は
 * 常にHTMLスクレイピングで実現している。
 */
```

```ts
// 修正後
/**
 * connpassのイベント参加者ページをスクレイピングし、募集枠ごとの参加者一覧を取得する。connpassの公式APIには参加者一覧を返すエンドポイントが存在しないため、この機能は常にHTMLスクレイピングで実現している。
 */
```

## コードコメント(Python, docstring)

```python
# 修正前
def shuffle(items):
    """Shuffle the given list using the Fisher-Yates
    algorithm. The input list is not mutated; a new
    list is returned instead.
    """
```

```python
# 修正後
def shuffle(items):
    """Shuffle the given list using the Fisher-Yates algorithm. The input list is not mutated; a new list is returned instead."""
```

1行に収まらないほど長いdocstringになる場合は、文単位で改行してもよいが、1つの文を複数行に割らない。

```python
def shuffle(items):
    """Shuffle the given list using the Fisher-Yates algorithm.

    The input list is not mutated; a new list is returned instead.
    """
```
