# Phase 165 R14-R24

## 変更対象と追加位置

- 新規 `phase165_r14_r24_delta_connection.py`（プロジェクトルート）：`pi32_delta_goal`, `derive_delta_zero_from_steps`, `reviewed_r23_isomorphism`, `audit_r24`。全文同梱。
- 新規 `test_phase165_r14_r24_delta_connection.py`（ZIP 内）：6テスト。全文同梱。
- 新規 `audit.py`, `run.ps1`, `toda_51_complete.tex`。
- 既存コード・既存テスト・文書は変更しない。

## 数学的意味と境界

R23 で作成した Toda (5.1) 採用 TeX に基づく実際の E 同型 ProofStep と、R11 の既存規則を接続する。Proposition 4.2 の正しい Δ→E 完全性窓の ProofStep が別途与えられれば、一般推論規則から Δ=0 の ProofStep を生成できる。

テスト内の `ProofRule.GIVEN` による完全性は、**接続機構のテスト用仮定**であって、Toda 原文で確認済みの文献命題ではない。通常監査はそのような ProofStep を作成しない。Proposition 4.2 の原文候補2件を `phase165_r14_r24_output/prop42_source_review.md` に出力し、正しい適用範囲の識別を次工程へ残す。

## 完了条件と次工程

対象6テストの成功、R23 実 ProofStep の使用、誤った完全性窓の拒否、製品の Δ=0 未証明を正しく報告すること。次の工程は Proposition 4.2 の出典候補の原文・EHP 指数範囲を確認した上での厳密な引用資格接続。全体 pytest は Phase 165 終了時のみ。
