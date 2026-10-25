# Phase 168 — Active pytest 収集範囲診断

- 実行対象: `tests/ (no automatic ignores or exclusion)`
- 判定: `ACTIVE_SUITE_PASS`
- pytest exit code: `0`
- 欠落した test helper の静的参照数: `0`

収集エラーや失敗は無視していない。PASS と記録するのは pytest exit code 0 で、
既知の欠落した test helper がない場合に限る。

## 欠落するテスト依存

- 直接 import の欠落は静的検査では検出されなかった。

## pytest の主な診断行

- 取得なし

## 完了判定

静的検査は動的 import 全体を保証しない。
pytest が失敗した場合は Phase 168 の全体テスト合格と判定しない。
