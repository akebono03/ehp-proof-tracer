# Phase 165 R6-2 統一規則台帳 R3-2

目的：R3 の13接続と22個の `expand_` 候補について、Provider ID と直接参照された推論規則 factory を照合する。

変更対象：新規 `r3_r2_audit.py` の `imports_for`、`resolve`、`top_functions`、`inspect_function`、`inspect_shared`、`perform`、`markdown`、`main`。新規 `test_r3_r2_audit.py` の7テスト、新規 `run.ps1`。既存のクラス・関数・import は変更しない。

静的監査のため、間接呼び出し、型付き前提の充足、数学的同値性、証明成功は認定しない。R3-3 に統一台帳への実接続と動的検証を残す。全体 pytest は Phase の末尾まで行わない。
