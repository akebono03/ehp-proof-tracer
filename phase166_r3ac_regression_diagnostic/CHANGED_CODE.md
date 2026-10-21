# Phase 166 R3-AC 回帰調査

本体ファイル・既存テストは変更しない。新規 `diagnose.py` の `main()` で、旧 R3-V 候補の生成、root gate 判定、共通探索の最終候補を比較する。出力先は `report.json`。`run.ps1` は診断のみ実行する。全体 pytest は実施しない。
