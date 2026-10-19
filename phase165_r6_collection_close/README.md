# Phase 165 R6 — 最終 collection 監査

## 対象ファイル
新規 `phase165_r6_collection_close/check.py`、`run.ps1`、`README.md`。既存の production code・テスト・import は変更しない。

## 実施内容
既存 R6 の対象選定と同じ `tests/` およびルート直下の `test_*.py` を `--collect-only` で収集する。テスト本体は実行せず、全体 pytest も行わない。180秒を上限とし、10秒ごとに進行状況を表示する。成功しなければ BLOCKED と記録し、ゼロ件とみなさない。結果は `phase165_r6_audit_results/collection_close/report.json` と `collection.log` に出力。

## 使用方法
`powershell -ExecutionPolicy Bypass -File .\phase165_r6_collection_close\run.ps1`

## 完了条件
収集が終了し終了コード0、エラーファイル0。未完了・タイムアウトでは R6 を閉じない。ブラウザー確認と Phase 165 最終 pytest は別途必要。

## ブラウザーでの確認
アプリの Group query で `(n,k)=(2,1)` と `(3,1)` を順に実行し、両群の数式表示・本文・出典を目視確認する。`generic-complete-proof` でも本文の数学的正しさが保証されるわけではない。実際の画面表示が必要。
