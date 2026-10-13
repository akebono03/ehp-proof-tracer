# Phase 165 R14-R10 — π₃² の EHP 前提監査

## 変更対象
- 新規 `phase165_r14_r10_premise_audit.py`
  - `ObligationAudit` dataclass、`audit_pi32_premises()`、`audit_summary()` の完全な実装
- 新規 `test_phase165_r14_r10_premise_audit.py`：テスト関数5件
- 新規 `audit.py`, `run.ps1`, `README.md`

既存 Registry / Renderer / ProofStep は変更しない。ファイルは ZIP 内に全文収録。

## 監査
- `(5.1)` の `π_i¹=0 (i>1)` を π₂¹=0 に特殊化できる。ただし出典文字列との照合と ProofStep の認証は別である。
- `E→H` / `H→Δ` 完全性は、関連する完全性命題に一致する Registry の承認済み主張を要する。
- `Δ:π₃³→π₁¹` が零であることは、終域 π₁¹ が自由巡回群であるという情報からは導けない。別途の数学的根拠が必要。

## 完了条件
4つの未解決前提を正確に特定し、証明を誤って完成させないこと。新規証明資格0、ProofStep 0。対象 pytest 5件だけ実施。全体 pytest は行わない。

## 次段階
R14-R11 は上記4前提の原典と意味の精査、具体的な `Δ=0` の数学的根拠の確認。認証できる前提だけを Registry に接続する。
