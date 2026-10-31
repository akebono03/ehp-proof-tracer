# Phase 171 R20R13R2 — 追加空行による統合失敗の修正

## 原因

R20R12 の重複表示除去は数式行のみを消すため、空の Markdown 段落が残る場合がある。
R20R13 は式の間の空行をちょうど1行と仮定していたため、最初の `$E(\eta_2)=\eta_3$` を
後続の2式に統合できなかった。

## 修正対象

- `phase171_r20r13_eta_sentence_layout/projection.py`
- 関数 `combine_adjacent_verified_eta_sentences` 全体を置換する。
- import と `verified_eta_display_sentences` の厳格な証明木・出典検査は不変。
- 数学的規則、Proof Tree、Web Renderer の本体には手を加えない。

## 完了条件

- 限定 pytest PASS。
- 公開探索 COMPLETE、Reference 8件維持。
- [R3] の3式が**1行に**統合されていることを実証明木で検査。
- ピリオド改行と位数4の説明を維持。
- 全体 pytest は Phase 171 最終段階でのみ実行。
