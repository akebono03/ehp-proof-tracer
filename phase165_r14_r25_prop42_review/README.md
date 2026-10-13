# Phase 165 R14-R25

## 変更対象
新規 `phase165_r14_r25_prop42_review.py`（`Prop42SourceReview`、`inspect_prop42_sources`、`audit_r25`、`render_report`）、関連6テスト、`audit.py`、`run.ps1`。すべて全文同梱。既存ファイルは変更しない。

## 実装
Proposition 4.2 の2候補の実際の `source_text` を元の Registry から読み出し、欠落・文献番号違い・参照不整合を拒否する。両原文を `phase165_r14_r25_output/report.md` に**全文**出力する。候補中の完全性語彙・Δ・E・指数条件を観測するが、数学的な意味を記号一致で認証したと偽らない。

## 完了条件
6件の対象テスト成功、元の Registry に副作用なし、出典原文の欠落なし、ProofStep の無断生成なし。実際の EHP 完全性の資格付与は未達。

## 次工程との境界
原文を直接確認して Proposition 4.2 の量化条件と EHP 完全列を確定し、その条件を型付きに落とし込む。`report.md` の原文を基準に改めてレビューする。全体 pytest は Phase165 終了時のみ。
