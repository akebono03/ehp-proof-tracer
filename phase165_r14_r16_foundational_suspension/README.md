# Phase 165 R14-R16 — 基本事実と文献命題の境界

## 変更対象
- 新規 `phase165_r14_r16_foundational_suspension.py`：`FoundationalClaim` クラス全文、`instantiate_foundational_identity_suspension()`、`bind_foundational_diagonal_obligations()`、`audit_r16()` の全文
- 新規 `test_phase165_r14_r16_foundational_suspension.py`：対象テスト関数全文
- 新規 `audit.py`, `run.ps1`, `README.md`
- 既存 API、Renderer、Registry は変更しない。

## 数学的内容
`E(ι_n)=ι_(n+1)` は reduced suspension（縮約懸垂）で恒等写像を懸垂したときの基本性質。Toda 文献命題と偽って登録せず、独立の `FoundationalReferenceIdentity` で区別する。`n>=1` に特殊化できる。型付き主張を作るが、独立レビューと ProofStep 接続は別工程とし、今は `proof_eligible=False` のまま。

## Proposition 4.2
ソース候補2件の TeX を `phase165_r14_r16_output/report.md` に載せる。曖昧な原文候補を1件に決め打ちしない。今工程では文献命題の意味論的認証を行わない。

## テスト・完了条件
追加テスト9ケース、元の制約を保持し、不正な次数を拒否。新規 ProofStep 0、既存 Registry に副作用なし、Proposition 4.2 は未選択。

## 次の工程
Prop 4.2 の参照境界を確定し、同型写像と必要な完全性の認証済み根拠を共通 Backward Search に接続する。全体 pytest は Phase 165 最終段階のみ。
