# Phase 176 R3R13 監査計画

## 目的

R3R12 で原因未確定と記録された `shared_composite_zero_candidates=0` を、二つの境界に分離して調べる。

1. Toda Lemma 5.7 の明示的な零像関係 `E(η₂∘ν′)=0` が、独立引用 Provider と通常の共有 Provider で候補として現れるか。
2. R3R10 の「右合成に対する零像の伝播」が、独立一般規則と共有 Provider で候補として現れるか。

## 変更対象

新規 `phase176_r3r13_two_boundary_audit/` のみ。

- `audit.py`: `source_preflight`、`get_previous`、`static_wiring_check`、`observe`、`run_worker`、`execute`、`main` を新規追加。
- `tests/test_audit.py`: 監査条件の限定テストを新規追加。
- `run.ps1`: DryRun・本実行・限定 pytest の起動。
- `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`: 説明文書。

既存クラス・関数・import の変更なし。GIVEN・公開数学規則追加なし。

## 完了条件

DryRun と本実行が成功し、通常の共有候補数と独立候補数が両方記録されること。既存・新規限定テストが PASS すること。群構造の完成は完了条件に含めない。

## 次段階との境界

R3R13 では共有 Provider を実装・登録しない。監査結果を見て R3R14 以降で必要最小限の公開接続を検討する。全体 pytest は Phase 終了時のみ。
