# Phase 165 R11 変更一覧

- 新規 `audit.py`: `function_calls()`、`main()`。R10 の規則台帳と R8 の規則発見、R57 共通 Backward Search、共有 provider の接続と規則順序を検証。専用 Adapter と六規則の不在も監査する。
- 新規 `test_audit.py`: テスト関数3件を追加。
- 新規 `run.ps1`: 読み取り専用監査と既存 R8 テストを含む対象限定 pytest のみ実行。
- 本番コード、既存テスト、既存文書は変更しない。
- 完了条件: 監査 `CONNECTED`、対象 pytest 成功。数学的証明の完成は次 Phase 165 作業に残す。全体 pytest は Phase 最後のみ。
