# Phase 165 R14-R19 — Toda (5.1) reviewed diagonal facts

## 変更対象
- `phase165_r14_r19_registry_gate.py`：新規 `DiagonalSourceReview`、`_diagonal_goals()`、`reviewed_diagonal_bridge()`、`audit_r19()`（全文）
- `test_phase165_r14_r19_registry_gate.py`：新規の対象6テスト（全文）
- `audit.py`、`run.ps1`：追加。既存ファイルは変更しない。

## 意味
Todo (5.1) の採用 TeX に現れる二つの対角群構造を、明示的にレビューした場合に限り、独立の RegistryBridgeResult に固定文献命題として登録し、`GIVEN` ProofStepLink を作る。元の Registry を一切変更せず、source-archive の主張を勝手に昇格させない。

ユーザーからの今回の命令「R19」は原文確認・数学的認証の承認そのものではないため、標準監査は fail-closed で認証0とする。テストでは合成レビュー承認を用い、既存 R18 の一般推論規則で E の同型まで到達できることを検証するが、製品の Toda 証明として報告しない。

`find_eligible_goal_candidates` で利用するには Phase 164 の引用制約（独立認証・位置関係・レビュー記録）も満たす必要がある。

## 完了条件
対象6テスト通過。非認証で ProofStep を出さない、認証済み Fixture は E 同型を導ける、旧証明を使わない。全体 pytest は Phase 165 の末尾のみ。

## 次工程
採用 TeX の命題範囲の独立レビュー、引用資格検査との接続、Proposition 4.2 の EHP 完全性の原文同定。
