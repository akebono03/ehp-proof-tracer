# Phase 166 R1 — 台帳 import 失敗の修正

## 診断

初回監査では `phase165_r4_production_connection` が見つからず、`registry_available=false` のまま `audit.py` が終了コード0を返していた。CSV の分類と限定テスト3件は成功したが、命題台帳との実照合は行われていない。

## 変更対象

- `phase166_r1_source_registry_audit/audit.py`: `main()` 全体のうち、失敗時の終了判定を更新。台帳が利用できない場合は出力に失敗理由を残し、終了コード2を返す。既存の CSV 分類と候補判定はそのまま。
- `phase166_r1_registry_import_fix/run.ps1`: 新規実行スクリプト。台帳モジュールの所在・import を事前確認。対象監査スクリプトをバックアップして置換後、限定テストを実行。
- `phase166_r1_registry_import_fix/test_fix.py`: 新規テスト2件。台帳不在で失敗扱いになること、証明資格を付与しないことを検査。

## 実行と完了条件

プロジェクトのルートに `phase165_r4_production_connection.py` が必要。存在しない場合、過去のコピーを勝手に本番へ戻さず、その所在を表示して停止する。存在する場合は import 成功、687行の照合、限定テスト5件の成功を確認する。全体 pytest は Phase 166 の R10 まで実行しない。

## 次 Phase との境界

このパッケージは出典候補の監査のみ。R2 の数学的事実 ID 対応付け、R3 の資格判定、R4 の関係式探索への組込は行わない。
