# Phase 175 R4R6R2 — テスト記録

## 先行ユーザー環境ログ（2026-11-17）

- R4R6（初版）：限定 pytest 81 passed。先行 report を発見できないと表示し、DryRun FAIL。
- R4R6R1：限定 pytest 84 passed。先行 report を明示指定後、`R4R6_PRIOR_EVIDENCE_INVALID` で DryRun FAIL。
- 原因：過去の `source_guard.reviewed_head` を、後から変更された R4R6 HEAD 集合に直接比較していた。

## R4R6R2 作成環境

- `python -B -m pytest -q -p no:cacheprovider --import-mode=importlib phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py`
- **47 passed**（合成レポート、改ざん検出、合成 Git 履歴の正常・異常検証）。
- 合成 Git 履歴でコミット後の HEAD と当時の監査 HEAD が異なる正常系を検査。
- 不正な変更ファイルやルール SHA の不一致を拒否することを確認。
- ZIP の整合性検査を実施。

## 未実行

- ユーザー実環境 DryRun：未実施。
- ユーザー実環境本実行：未実施。
- ユーザー実環境全体 pytest：未実施（Phase 175 最終段階のみ）。

## 監査の範囲

新規 GIVEN 0、数学規則0、本番変更0、既存完成証明の再探索0。
期待 Gate：`PASS_R4R6_PROP25_EQ58_SOURCE_FRONTIER_RECORDED_NOT_PUBLIC`。
