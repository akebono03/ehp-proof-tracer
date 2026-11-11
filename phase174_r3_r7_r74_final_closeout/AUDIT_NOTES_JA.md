# Phase 174 R74 — 最終終了監査仕様

## 対象

`akebono03/ehp-proof-tracer` の `develop` に対し、R73 書き込み時 HEAD `12e56cd06a3f896924313c978a628445d90228ed` の主要5文書だけが未ステージ変更として残る状態、または R73 マージ後 HEAD `38788cec179c16fba7bba606ed35aa1e890ee79f` における追跡ファイル変更なしの状態のいずれかを確認する。`HEAD` と `origin/develop` は一致しなければならない。外部 Git fetch、reset、clean、stage、commit をしない。

R73 の実行時ログに含まれる全5文書の SHA-256、監査ソースの Git blob SHA、R72/R73 のローカル JSON レポートと未完成境界を検査する。R71 の監査結果は R72 の保存記録として確認し、再実行したことにはしない。

## 対象変更

本パッケージは `phase174_r3_r7_r74_final_closeout/` を新規追加する。既存の Python クラス・関数・import、数学推論規則、GIVEN、ProofStep、Renderer は変更しない。全体テストが成功した場合に限り、次の主要5文書を**全文の単位**で置換する。

- `README.md`：英語で現行の正式終了結果を追加し、過去 R73 の終了前記録を保持する。
- `docs/design.md`：日本語で証明探索・表示の有効な不変条件を追記する。
- `docs/development_log.md`：日本語でテスト結果と終了経緯を追記する。
- `docs/roadmap.md`：日本語で Phase 174 の終了と次 Phase の境界を記載する。
- `docs/proof_records.md`：日本語で型付き完成証明2群と認定範囲を追記する。

## 全体テスト

最終 Gate 内で `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests` を一度だけ実行する。先に R74/R73 の限定 pytest を行う。全体テストの stdout/stderr、実行前 `attempt.json`、実行後 `report.json` を `%LOCALAPPDATA%` に保存し、再実行を自動許可しない。

## 完了条件

1. Source Guard、Git 前提、R72/R73 ローカル監査記録、主要5文書の SHA-256 が一致する。
2. 限定 pytest と全体 pytest の exit code が 0 で、全体テスト結果に `passed in` が実際に含まれる。
3. 全体テスト後も監査済みの Git／文書状態に変更がない。
4. README と4文書の**全文**を出力し、ZIP と SHA-256 検査で内容を保持する。
5. R74 の成功レポートが保存され、`PASS_R74_PHASE174_FINAL_CLOSEOUT` を出力する。

失敗または中断時に Phase 174 の正式終了を宣言しない。全体テストが失敗した場合は過去の失敗証拠を保持して修復後に別の審査済み Gate を用意する。
