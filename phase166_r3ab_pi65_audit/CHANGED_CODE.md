# Phase 166 R3-AB 変更内容

- 本体コードの変更なし。
- 新規 `phase166_r3ab_pi65_audit/audit.py`: `audit_pi65()`、`main()`、補助関数 `_run()`（全文同梱）。
- 新規 `phase166_r3ab_pi65_audit/test_r3ab.py`: 限定テスト2件（全文同梱）。
- 新規 `run.ps1`: 監査実行と限定 pytest。全体 pytest は実行しない。
- 掲載順を管理する `precedes_citing_assertion()` は変更しない。
- `ProofOrderCatalog` は有無を観測するだけで変更しない。

**判定**: 直接探索と Web 探索の状態、および輸送候補の subgoal を `report.json` に記録する。証明が未完成の場合も監査は失敗扱いにせず、未完成の実態を記録する。
