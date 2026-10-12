# Phase 163 R4-R51 変更記録

## 変更対象

- 新規 `phase163_r4_r51_priority_semantic_review.py`: `DECISIONS` 定数、`review`、`write_results`、`main` を追加。
- 新規 `tests/test_phase163_r4_r51_priority_semantic_review.py`: import 部分と9個のテスト関数を追加。
- 新規 `run.ps1`: 限定 pytest、入力検査と監査実行。
- 新規 `README.md`、`CHANGED_CODE.md`。

既存ファイルの import・クラス・関数は変更しない。各追加コードの全文は同梱ファイルにある。

## 完了条件

1. 第3章・第5章の対象16候補のみ文脈分類を追加し、未確認は保留する。
2. 既存316レコードの索引と R4-R50 判定は維持する。
3. 原稿・カタログの SHA-256 検査に失敗すれば処理を停止する。
4. 限定 pytest 9件が通過し、JSON/CSV/報告を出力する。

## 次の R4-R52 との境界

R4-R51 では本番 Registry 登録・ID発行・原本検証・証明探索接続をしない。残る数学的候補と登録先の精査は後続の段階で実施する。全体 pytest は Phase 163 完了時まで実施しない。
