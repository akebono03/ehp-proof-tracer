# Phase 169 R3U2 — 変更一覧・実装境界

## 対象ファイル、関数、テスト

- `phase165_r14_r5_ehp_connection.py` — `expand_cited_ehp_terminal_goal()` 全体。
- `phase169_r3i_cited_ehp_inference/tests/test_phase169_r3i_cited_ehp_inference.py` — 既存4テスト関数。
- `phase169_r3i1_proof_closure_audit/tests/test_phase169_r3i_cited_ehp_inference.py` — 既存4テスト関数。
- `phase169_r3i2_import_repair/tests/test_phase169_r3i_cited_ehp_inference.py` — 既存4テスト関数。
- `phase169_r3u2_audit_module_import_fix/run.ps1` — 監査起動コマンドを修正。
- `phase169_r3u2_audit_module_import_fix/audit.py` — 新規監査関数 `main()`（全文収録）。
- `phase169_r3u2_audit_module_import_fix/tests/test_phase169_r3u_delta_diagonal_dependency.py` — 新規テストファイル、5テスト関数。

import 文の変更なし。既存クラス・メソッド変更なし。関数全文は `full_functions/` に収録。

## R3U2 の修正点

監査コマンド変更前：

```powershell
python -B "$Package\audit.py"
```

変更後：

```powershell
python -B -m phase169_r3u2_audit_module_import_fix.audit
```

`Push-Location $Repo` 済みのため Python の `sys.path[0]` はリポジトリ直下となる。
R3U1 で通過済みの限定39テストと本番数学的条件は不変更。

## 検証と境界

構文検査、PowerShell コマンド検査、モジュール検索の再現検証、ZIP 一貫性を実施。
実リポジトリの pytest と Web 表示の監査はユーザー環境で実行する。
全体 pytest は Phase 169 の最後のみ。
