# Phase 173 R4-R1 — Toda (5.6) 直和分解の依存関係監査

## 変更対象

新規追加のみ：`phase173_r4_r1_audit_only/__init__.py`、`audit.py`、`run.ps1`、`tests/test_audit.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。
既存クラス・既存関数・import・公式5文書の変更は行わない。

`audit.py` 新規関数：`git`、`verify_audit_only_changes`、`verify_source_text`、`inspect_named_function`、`preflight`、`inspect_public_root`、`main`。新規テスト関数は `tests/test_audit.py` 内に全定義する。

## 数学的依存

Toda (5.6) を $i=7$ に特殊化すると、$\pi_6^3\oplus\pi_7^7\cong\pi_7^4$ で、$(\alpha,\beta)\mapsto E\alpha+\nu_4\circ\beta$。
必要な前提は、(1) Proposition 4.4 の Hopf 不変量1の条件、(2) Lemma 5.4 による $H(\nu_4)=\iota_7$、(3) 出典と証明を備えた $\pi_6^3\cong\mathbb Z/4$、(4) 出典と証明を備えた $\pi_7^7\cong\mathbb Z$、(5) 同型写像と生成元像の型付き対応。

過去のレガシーな `pi7_7_step` を、現行の引用チェックを経ない GIVEN として採用してはならない。構造が DB に登録済みであることと、ProofStep が存在することは別である。

## 監査境界

- 対象は $\pi_7^4$ のみ。$\pi_8^5$ の位数8を推論しない。
- 現行 Provider の Root Proposal と直下 Subgoal は観測するが、Proof Tree は構成しない。
- `status=OBSERVATION_ONLY_NOT_A_PROOF` を必ず報告する。
- 全体 pytest を行わず、新規監査テストだけ実行する。
- 既存の追跡済みファイルを変更せず、監査 JSON のみ `%LOCALAPPDATA%` に書き出す。

## 次工程

R4-R1 のレポートで出典位置、位数・生成元・同型写像の不足前提を特定し、すべて検証できた場合にだけ別途、最小限の公開 Proof Search 接続を検討する。R4-R2（$\pi_8^5$）と Web 表示は対象外。
