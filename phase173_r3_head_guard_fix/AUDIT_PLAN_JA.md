# Phase 173 R3 — HEAD 検査修正（監査専用）

- 対象: `phase173_r3_head_guard_fix/audit.py`, `run.ps1`, `README.md`, `AUDIT_PLAN_JA.md`、`__init__.py` の新規追加のみ。
- 旧 HEAD `11ea331f` から新 HEAD `10f77860` までに追加された7ファイルのみを許容する。
- 既存の証明探索・文献台帳・出典ゲート・Toda 原文の blob SHA を検査する。
- R1 で未完成だった $\pi_7^4$ と $\pi_8^5$ の Root Candidate、Subgoal、既存引用・先行結果を読み取り専用で監査する。
- 群構造の DB 目標は証明済み前提として扱わない。検証済みでない GIVEN や ProofStep は追加しない。
- 完了条件: HEAD/出典検査に PASS、監査 JSON が保存され、追跡済み Git ファイルが不変であること。
- 本監査は R3 の暫定停止点調査であり、R4 の数学規則の実装は含まない。
- 全体 pytest は Phase 173 の最後だけ実施する。
