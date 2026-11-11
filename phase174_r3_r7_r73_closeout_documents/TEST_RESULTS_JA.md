# Phase 174 R73 — 作成環境の限定テスト

実行したコマンド：

```powershell
python -B -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib phase174_r3_r7_r73_closeout_documents/tests/test_audit.py
```

作成環境の結果：**20 passed**。本実行の Windows リポジトリにおける Git Source Guard、R72 保存 JSON、全文文書の元ファイルと限定 pytest についてはまだ未実行である。全体 pytest は実施していない。Gate はユーザー環境の `run.ps1` 実行後に確定する。
