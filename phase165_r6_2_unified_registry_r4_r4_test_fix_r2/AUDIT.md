# R4-4 テスト修正 R2

原因: 前回の `run.ps1` にタブ文字が混入し、`Test-Path` のパスが不正になった。

対象: `run.ps1` を全文修正。必要な場合のみ既存 `phase165_r6_2_unified_registry_r4_r4/test_r4_r4_integration.py` の `test_forward_builder_kept()` を修正する。元ファイルはバックアップする。

本番の数学的規則・共通探索は変更しない。対象 pytest のみ実行し、全体 pytest は実行しない。
