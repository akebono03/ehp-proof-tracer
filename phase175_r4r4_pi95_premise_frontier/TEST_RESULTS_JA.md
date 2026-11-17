# Phase 175 R4R4 — テスト記録

## 作成環境で確認した内容（2026-11-17）

- 新規 `tests/test_audit.py` の限定 pytest：**42 passed**。
- Git HEAD 系譜の正当・不当な分岐、前回実行レポートの改変、Toda Source Proposition 2.5/5.8 の節欠落、6前提の昇格禁止、Source PIN と R4R3 規則内容ハッシュの改変拒否を模擬データで検査。
- `audit.py`、`tests/test_audit.py` は Python 構文検査済み。
- 既存の EHP Proof Tracer 本番 checkout による実際の参照元テキスト・型付きウィンドウ検査は **未実施**。作成環境では GitHub の現行コード・出典テキストを別途閲覧して計画した。
- ユーザー環境から報告された先行 R4R3R2：DryRun／本実行とも **85 passed**、Gate PASS。R4R4 のテスト結果と混同しない。

## ユーザー環境で行う限定検査

`run.ps1 -DryRun` と `run.ps1` の順に実行。スクリプトが `-p no:cacheprovider --import-mode=importlib` と4つの限定テストファイルのみを指定する。全体 pytest は実行しない。

## 完了条件

- 限定 pytest PASS。
- 先行 R4R3 本実行レポートとの整合性 PASS。
- R4 18件＋追加7件の Source PIN、R4R3 `rule.py` の内容ハッシュ PASS。
- Toda 原文の Proposition 2.5 条件、(5.8)、Proposition 5.8 の前提記述 PASS。
- 適切な EHP $\Delta\to E$ window の型検査 PASS。ただし検証済み `ProofStep` とは主張しない。
- 前提6件と今後の証明義務のレポート作成 PASS。

DryRun は `PASS_R4R4_PREMISE_FRONTIER_DRYRUN`、本実行は `PASS_R4R4_PREMISE_FRONTIER_RECORDED_NOT_PUBLIC` を期待する。Windows での実結果はログ確認前に PASS と断定しない。
