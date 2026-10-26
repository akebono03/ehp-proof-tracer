# Phase 169 R3M — 変更内容と境界

## 目的

先行する群構造の「結果」を、その証明が完了しているかどうかに依存せず取得する。文献順を確認できない DB 行から、証明の前提を勝手に作成しない。

## 変更対象

- 新規 `phase169_r3m_prior_result_catalog/prior_results.py`：`PriorGroupResult` 全体、`_database_result_candidates` 全体、`resolve_prior_group_result` 全体。
- 新規 `phase169_r3m_prior_result_catalog/audit.py`：`build_report`、`main` 全体。
- 新規 `phase169_r3m_prior_result_catalog/tests/test_prior_results.py`：6テストおよびヘルパー関数全文。
- 新規 `phase169_r3m_prior_result_catalog/__init__.py`、`run.ps1`、`README.md`、`IMPLEMENTATION_NOTES.md`。

既存 API、検索、Renderer、命題台帳、既存テスト、ルートの README.md/design.md/development_log.md/roadmap.md/proof_records.md は変更しない。

## 機能

- `sphere.csv` および `HyoujiGen.csv` から先行群の型付き群構造を取得する。取得順序は既存の Goal 選択と同じ。
- `resolve_specialized_goal_citing_id` を使い、既に登録された固定文献命題への結合を確認する。
- `precedes_citing_assertion` を使い、利用対象より前の命題かを確認する。
- 証明状態を引数にも取らず、一切読み出さない。
- 文献の結合が未確認なら `eligible=False` を返すが、DB の結果そのものは取得したままとする。

## 限定テスト

`python -B -m pytest -q phase169_r3m_prior_result_catalog/tests/test_prior_results.py`

## 完了条件

限定6テスト PASS、実 DB による3組の結果取得・文献順の監査ログ、証明検索なし、既存ファイル無変更。

## 次工程との境界

本 R3M は「結果の取得と資格判定」のみ。次 R3N で、適格な結果を共通 Backward Search の前提へ接続し、最終証明本文が先行証明の本文を再展開しないことを監査する。`R3M_COMPLETE` は Web の結果再利用機能の完成を意味しない。
