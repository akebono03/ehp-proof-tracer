# Phase 169 R10EE — 1-stem 固定基準との差異監査

## 背景

R10ED は 8-stem と 9-stem の代表5群について、完成証明、信頼境界、表示圧縮の安全条件を監査し、全件 PASS を記録した。ただし Phase 168 最終資料では $\pi_5^4$ が10ステップの完成証明なのに、R10EC の限定テストでは `partial` と候補2件の診断になった。

## 今回の検査

- $\pi_3^2$（2,1）、$\pi_4^3$（3,1）、$\pi_5^4$（4,1）を Phase 168 固定基準と比較。
- $\pi_6^5$（5,1）および $\pi_{10}^8$（8,2）を対照群として観測。
- Goal 候補数、DB Goal 候補、検索診断、open goals、ProofStep 数、GIVEN/INFERENCE、引用対象 ID、選別済み Bridge、完全証明だけの Trust Boundary 再検証を記録。
- 完成証明でない結果は trust の適用対象から外し、`complete` に読み替えない。

## 変更対象

新規 `phase169_r10ee_one_stem_regression_audit/` のみ。既存本番ファイル、既存テスト、README.md、docs 下の文書は無変更。

- `audit.py`: `status_assessment()`、`_text()`、`inspect_case()`、`make_report()`、`main()` の全文。
- `tests/test_r10ee_reporting.py`: 各テスト関数と import 全文。
- `run.ps1`: 現行ブランチ・Git BLOB 確認、限定 pytest、読み取り専用監査、差分確認。

## 終了条件と次 Phase の境界

R10EE は差異の観測であり、原因が未特定なら Phase 169 を終了しない。差異が見つかった場合は次の限定修正で根本原因を調べる。全体 pytest は Phase 169 終了時にのみ実行する。R10ED の直和群監査の合格と、1-stem の固定基準の合格を混同しない。
