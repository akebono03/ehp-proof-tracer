# Phase 174 R3-R7-R5R1: HEAD 引き継ぎ修正

- 問題: 限定 pytest 85件 PASS の後、R5 の `verify_git_and_sources` が R4R1 追加コミットを拒否した。
- GitHub `develop` で確認した従来の HEAD: `1f3a61d7d6cfc7854e56c4f5c372bf5c71e203df`。
- 確認済みの後続 HEAD: `db9ef1cd1560744352bced43d3b4e1b95003edfb`。
- GitHub 比較で後続コミットによる追加は `phase174_r3_r7_r4_delta_surjectivity_audit/` 以下の9ファイルのみ。R5 の `SOURCE_BLOBS` 9件は変更されていない。
- 修正: 監査済み2コミットのいずれかに local/remote がともに一致した場合のみ許可し、9ソースの blob SHA・staged/unstaged 差分検査は一切変更しない。
- 変更対象: `audit.py` の定数1件追加、関数 `reviewed_develop_head_pair` を `verify_git_and_sources` の直前に追加、`verify_git_and_sources` の HEAD 条件のみ修正。`tests/test_audit.py` の import を全文更新し、新規テスト関数4件（パラメータ6例を含む）を追加。
- 既存 `run.ps1`・`rule.py`・ほかのファイルは不変。Source-first・First Successful Proof Search・公開経路に変更なし。
- 完了条件: DryRun・本実行・限定 pytest・SOURCE_GUARD=PASS、R5 の未解決 `ImageZero(E)` の現状を記録。全体 pytest は Phase 174 終了時のみ。
