# Phase 175 R4R6R2 — 過去 HEAD の検証方法を修正する監査

## 1. 原因と訂正

2026-11-17、R4R6R1 のユーザー実環境限定 pytest は 84 passed だったが、
R4R5R3 の成功レポートを明示指定した DryRun が
`R4R6_PRIOR_EVIDENCE_INVALID` で停止した。

R4R6R1 の `validate_prior()` は、R4R5R3 が監査時点で記録した
`source_guard.reviewed_head` を、**後からコミットされた**
R4R6 のチェックアウト HEAD (`8d8c1eaa…` / `c48fdc30…`) と照合していた。
しかし R4R5R3 の公開接続とコミットは当該レポート作成後に行われた。
この直接比較は誤りである。GitHub `develop` のコードと関連テストで、
R4R5R3 の基準 HEAD `2789fb62…`、対象パス範囲、当時の生データの SHA を確認した。

本修正では R4R5R3 の監査時 HEAD の**履歴と出典内容**を独立に確認し、
後日の R4R6 HEAD との単純一致条件を廃止する。検証条件を緩和しない。

## 2. 変更対象（先に列挙）

- `phase175_r4r6_prop25_eq58_source_frontier/audit.py`
  - import 全体（`hashlib` を追加）
  - 定数 `PRIOR_REVIEWED_BASE_HEAD`, `PRIOR_CHANGED_PREFIX`, `PRIOR_PRODUCTION_BLOB`, `PRIOR_RULE_SHA256` を追加
  - `validate_prior()` を全文置換
  - `validate_prior_history()` を `validate_prior()` 直後に追加
  - `run()` を全文置換
- `phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py`
  - import 全体（`subprocess` を追加）
  - `prior_fixture()` を全文置換
  - 合成 Git 履歴の正常系・異常系などテスト4関数を末尾追加
- `README.md`（英語）と、本 `AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md` を全文更新

その他の Python ソース、`run.ps1`、本番コード、ルートの5文書は変更しない。

## 3. 監査の失敗停止条件

1. R4R5R3 実レポート Gate / DryRun / Scope / Provider 3件 / 既存証明の再検索禁止 / 統合テスト終了コードを検証。
2. R4R5R3 の Source Guard が記録する基準 HEAD、Production blob、孤立規則 SHA と変更対象パスの形式を検証。
3. Git の実履歴で基準 HEAD → 監査当時 HEAD → 現在の HEAD の祖先関係を確認。
4. 基準→監査当時 HEAD の `git diff --name-only` が記録と一致し、R4R5R2 の対象パスだけであることを確認。
5. 監査当時 HEAD の既存共有 Provider blob と、実環境の R4R5R2 孤立規則ファイルの SHA256 を検証。
6. 出典 Toda Proposition 2.5 / (5.8) の原文・型・符号と境界監査は既存どおり実行。

不一致は `R4R6_PRIOR_EVIDENCE_INVALID` または `R4R6_PRIOR_HISTORY_INVALID` として失敗停止する。
監査履歴を自動修復・偽造しない。

## 4. 実行と完了条件

PowerShell の `Expand-Archive -Force` で展開後、`run.ps1 -DryRun` と `run.ps1` を順に実行。
成功時の Gate は `PASS_R4R6_PROP25_EQ58_SOURCE_FRONTIER_RECORDED_NOT_PUBLIC`。
両方成功するまで R4R7 に進まない。限定 pytest のみ実施し、全体 pytest は Phase 175 終了時に実施する。

## 5. R4R7 の境界

R4R6R2 は監査の履歴認証修正だけであり、新規 GIVEN 0、新規数学規則0、公開 ProofStep 登録0。
`π₉⁵` は未完成のまま。Proposition 2.5 の条件付き一般推論の実装は R4R7 のみで扱う。
