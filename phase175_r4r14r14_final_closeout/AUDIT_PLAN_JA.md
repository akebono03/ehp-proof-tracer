# Phase 175 R4R14R14 — 最終 Gate（実行計画）

## 目的と変更範囲

対象は k=4 登録6群の正式終了審査。変更対象はこの新規ディレクトリの `gate.py`、`run.ps1`、`tests/test_gate.py` のみ。既存の数学規則、GIVEN、Provider、Web Renderer、旧 Source Guard、その他のテストは変更しない。

## 実行順序

1. `-DryRun`：R13 の現行コード・5文書・HEAD・追跡済み Git 差分検査を再利用。全体 pytest はしない。
2. 限定 pytest：本 Gate と R13 の監査契約のみ。
3. 実行直前の R13 preflight と全6群の実探索、14段階の零群証明木・4出典の再監査。
4. 上記が成功した後に限り、`python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests` を Phase 末尾に **1回だけ**実行する。
5. 開始前に `attempt.json` を排他的に作成し、stdout/stderr、HEAD、検査対象、SHA-256 を保存する。失敗しても自動再実行しない。
6. 全体 pytest が成功した場合のみ、主要5文書の全文を original_full/final_full に出力し、5文書の全文 ZIP を作成。過去の本文を保全し正式終了節を追記する。
7. 最終 `report.json` で Phase 175 の正式終了可否と認定範囲を判定する。

## テスト・出典・数学的境界

過去の Phase 174 固定 HEAD／関数全文スナップショット Source Guard テスト4件は、アクティブ `tests/` の範囲外にある **既知の未解決失敗** である。これらを PASS と見なさず、テスト削除・guard 緩和も行わない。最終 Gate は現行 `tests/` の PASS と登録 k=4 の6群の完成証明に限定した正式終了である。全テストディレクトリの無条件 PASS を意味しない。

## 次 Phase との境界

Phase 176 の数学規則、未登録群、他 stem の未完成群、文献全件の数学的独立検証は対象外。失敗の証拠は記録して次工程で監査する。
