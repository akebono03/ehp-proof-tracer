# Phase 169 Closeout R1 — Phase 終了時テストの実行境界

## 対象

現行 `develop` に登録された R10ET-R5D/R6C/R6D の実装と、R2A の文書5ファイルを事前確認し、Phase 169 最終段階として限定回帰および現行アクティブテスト `tests/` の全体 pytest を実行する。先行する R3A の文書5件・実装8件・R6 19例 PASS の結果を出発点とする。

## 変更対象のファイル・関数

既存の本体・テスト・文書に変更はない。追加するパッケージは `run.py` の `inspect_environment`、`inspect_r6`、`execute_pytest`、`execute`、`main` と補助関数、`run.ps1`、`tests/test_gate.py`、説明文書である。新規関数は新規モジュールにすべて全文収録する。文書5件を変更していないので全文上書きは行わない。

## 検証境界

R6D の監査記録は数学的な新しい形式認証を意味しない。特定の19件に関する既存の監査根拠としてだけ検証する。Phase 169 の歴史的パッケージ全フォルダを無差別に `pytest` で収集せず、現在のアクティブ範囲 `tests/` と明示的な重点回帰ファイル10件に限定する。`tests/conftest.py` にある歴史的 Phase155 監査限定除外は引き続き有効。

## 成功・失敗

監査前に HEAD、13ファイルの Git blob、R6 JSON と19例を検査する。限定 pytest が失敗した場合は全体テストを開始しない。全体 pytest が失敗した場合は `TEST_GATE_PASS=False` として Phase 169 未完了とする。成功しても Phase 169 の最終文書と closeout 記録を更新するまでは `phase169_certified=False` に固定する。

## 安全対策

Git の `reset`、`restore`、`checkout`、`pull`、`add`、`commit` および追跡ファイルの変更は一切行わない。Git index は変更前後で照合する。外部出力 `%LOCALAPPDATA%\EHPProofTracerRecovery` にログを保存する。ユーザーの作業中ファイルはそのまま残す。

## 次 Phase との境界

全体テストの結果を受けて、Phase 169 正式終了の記録と次 Phase の未達成事項の確定を行う。未監査の Definition、全 stem の一般的数学的証明、旧台帳削除などは先取りしない。
