# Phase 174 R3-R7-R46R1 実装前監査・変更計画

## 変更対象

既存の変更対象：`phase174_r3_r7_r46_prop42_dfs_audit/source_guard.py` の import 全体、定数、`normalized_sha256()`、`verify_checkout()`。
数学本番コード、探索エンジン、R46 の `audit.py`・`run.ps1`・既存テスト：**変更しない**。
新規追加：`phase174_r3_r7_r46r1_source_guard_merge_fix/` にパッチ実装、run.ps1、限定テストと監査文書。
新規関数：`patch.normalized_sha256()`、`patch.reviewed_files()`、`patch.verify_revised_merge()`、`patch.pending_replacement()`、`patch.main()`、`tests/test_patch.py` の4テスト。
新規クラスなし。

## GitHub 現行コード・関連テストの確認

2026-11-09 GitHub `akebono03/ehp-proof-tracer` `develop` HEAD `4d37adab06b40330832c8ec1f08a1b7924ff95af`。
直前 HEAD `4b06ef96628b39e591cfa0b423fa0e0dec366a3b` との差分は R45/R45R1 監査ディレクトリ内の23追加ファイルのみ。数学本番コードと探索エンジンに差分なし。
GitHub の R45 `source_guard.py`・`audit.py`・`run.ps1`・`tests/test_static.py`、R45R1 の `run.ps1`・`tests/test_patch.py` を確認。
元 R46 の `source_guard.py`・`audit.py`・`run.ps1`・`tests/test_guard.py`・`tests/test_audit.py`・`tests/test_static.py` を照合。

## エラー原因と修正方針

元 R46 の `verify_checkout()` は古い R45 の `verify_checkout()` を無条件に呼び出す。GitHub HEAD が変わったため、数学的監査に進む前に失敗する。
新 R46 は、現行 HEAD と直前 HEAD のみを許容したうえで、全12件の R45 本番ファイル Git Blob、共有探索エンジン Git Blob、R45R1 の4件の監査ファイル SHA256、branch・staged・tracked 状態をすべて検証する。

## 実行と完了条件

1. DryRun：ファイル書き込みなしで全ガードと置換対象ハッシュを確認。
2. 本実行：R46 の `source_guard.py` のみを指定済みの全文に置換。すでに置換済みなら再適用しない。
3. 元 R46 `run.ps1` を実行し、数学的監査と5グループの限定 pytest を実施。
4. R46R1 の追加テストを実施し、旧/new HEAD 受理、予期しない変更の拒否を確認。

全体 pytest は Phase 174 終了時のみ。R46R1 の対象外：根の完成、数学推論規則や Narrative の修正、各種ドキュメント5本の変更。
