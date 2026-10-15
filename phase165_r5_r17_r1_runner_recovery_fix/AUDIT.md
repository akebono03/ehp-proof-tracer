# Phase 165 R5-R17-R1 実装・安全性記録

- 修正対象：新 ZIP 内の `install.py`、`run.ps1`。新規テスト `test_recovery.py`、`test_canonical_smoke.py`。
- 旧 R5-R17 で指定した `tests/test_phase165_r52_r11_common_renderer.py` がローカルに存在せず、削除後テストに進めなかった。
- 前回の rollback により、元ファイルは復元済みだが `.phase165_r5_r17_removed_backup` は保持される。完全一致を確認した場合だけ再利用する。
- `run.ps1` のテストパスは同梱テストの実在パスのみを指定する。
- 共通 Renderer の限定スモークテスト3件は実環境での実行が必要。数学的な包括的証明テストの代替ではない。
- `tests/` 内の旧専用テスト5件の削除はユーザー合意の旧実装撤去方針に基づく。他の数学的テストは保持する。
- 全体 pytest は Phase 165 の最後のみ。
