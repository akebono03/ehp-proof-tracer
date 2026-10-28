# Phase 169 R10EJ-R1 — pytest キャッシュ分離

## 観測結果

R10EJ 本体の限定 pytest 40件と5群の完成証明・Trust Boundary 監査は PASS。しかし Git 管理下の `.pytest_cache/v/cache/nodeids` が pytest により更新され、R10EJ の「対象外追跡ファイルに変更なし」検査で失敗したため、実装済み `projection.py` がバイト単位でロールバックされた。

## 修正範囲

新規フォルダ `phase169_r10ejr1_pytest_cache_isolation` のみを追加する。元の `phase169_r10ej_cyclic_verified_projection/run.ps1`、本番の `projection.py`、既存テスト、データベース、数学的証明規則は編集しない。README は英語、本ファイルは日本語。

`verify.py` の `verify_reviewed_runner()` で旧ランナーの SHA-256 と2回の pytest 実行、および復元処理の存在を検証する。`run.ps1` は元の環境変数 `PYTEST_ADDOPTS` を退避し、`-p no:cacheprovider` を加えて元のランナーを別プロセスで実行し、終了時に環境変数を元に戻す。

`.pytest_cache/v/cache/nodeids` の実行前後のバイト内容を SHA-256 で比較する。すでに汚れている追跡ファイルを無断で `git restore` しない。

## 限定テスト

新規 `tests/test_r10ejr1_verify.py` の5テストで runner の整合性、既存の pytest オプション保持、未承認スクリプト拒否、実際の pytest キャッシュ無効化を検証する。続いて元の R10EJ のパッチテスト・既存限定回帰テスト・証明監査を再実行する。全体 pytest は Phase 169 終了時にのみ行う。

## 完了条件と次工程

本ランナーの PASS、元の R10EJ の40限定 pytest・5群証明監査 PASS、対象外追跡ファイルの不変性、R10A `projection.py` の変更が保持されること。次工程は R10A・R10EC・R10EJ の Projection 共通化の設計・監査であり、この工程では先取りしない。
