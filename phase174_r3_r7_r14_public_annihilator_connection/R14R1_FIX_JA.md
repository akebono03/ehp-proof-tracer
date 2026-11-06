# Phase 174 R3-R7-R14R1 — Source Guard CRLF修正

## 原因

GitHub `sources/toda/Toda_05_2.tex` の Git blob は CRLF (2394箇所、LF単独0箇所) である。一方、R14 `checked_source_blob()` は Git SHA を照合する前に改行を LF に正規化していた。その結果、正しい CRLF Git blob の SHA `579661138928499ba04a51327f686d9b971b5314` と一致しなかった。

## 変更対象

- `audit.py` の `checked_source_blob()` を関数全体で置換。
- `tests/test_audit.py` の末尾に回帰テスト2関数を追加。
- その他の R14 ファイル、本番の `phase165_r52_r9_shared_math.py`、規則、公開 Renderer は変更しない。

## 修正方式

想定 SHA を変えず、改行が統一された LF／CRLF に限って、原本・LF正規形・CRLF正規形の Git Blob SHA を照合する。bare CR、改行形式混在、想定外の内容、39文字SHAを拒否する。

## 検証と Phase 境界

R14R1 新規回帰2件を含む限定テストのみ。全体 pytest は Phase 174 完了時にのみ実施。DryRun、本実行、公開 Source-first、出典付き祖先 ProofStep は Windows 実行結果で判定。`π₁₂⁷=0` の完成証明を R14R1 で宣言しない。
