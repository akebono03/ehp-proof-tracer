# Phase 163 R4-R50 変更対象

- 新規 `phase163_r4_r50_semantic_review.py`: 関数 `evaluate`、`write_report`、`main`、定数 `PROSE_DECISIONS`、`DISPLAY_DECISIONS`、`LINKED_DISPLAY_TO_PROSE`。
- 新規 `tests/test_phase163_r4_r50_semantic_review.py`: 限定テスト9関数。
- 新規 `run.ps1`: 既存の R4-R49・R4-R47・R4-R42 の成果物を読み込む。
- 新規 `README.md`、`CHANGED_CODE.md`。

変更対象の既存ファイル・クラス・関数・import はない。コードとテストは ZIP の各ファイル内に全文を収録し、省略はない。

## 完了条件

316候補の追跡継続、元の108環境・ID の保存、TeX と catalog の SHA-256 一致、限定テスト通過、監査資料3種の出力。新規 Statement ID などの本番登録はしない。

## 次の作業との境界

R4-R50 は20件の文章候補と9件の表示式を限定的に文脈判定した監査である。残りの数式の数学的分類と、確定した登録単位への ID 付与は次工程。全体 pytest は Phase 終了時に限定する。

## R4-R50 修正版（入力パスのみ）

- `tests/test_phase163_r4_r50_semantic_review.py` の `data()` を変更。テスト入力を `phase163_r4_r49_output/triage.json`、`phase163_r4_r47_output/catalog.json` に統一。
- `run.ps1` と監査モジュール本体は変更なし。
- 全体 pytest は実施しない。
