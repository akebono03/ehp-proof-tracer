# Phase 166 R1 出典・命題台帳接続監査

## 目的

関係式 CSV の `reference` 文字列を、現行 production の `UnifiedStatementRegistry` に存在する文献 locator と読み取り専用で照合する。**同じ locator を持つだけでは同じ数学的命題を意味しない。** 既存コード、CSV、SQLite を変更しない。

## 既存コードの確認

- `unified_statement_registry.py` : `LiteratureEntry` / `AssertionEntry` を保持。資格判定は行わない。
- `phase163_r4_registry_bridge.py` : 文献断片を `METADATA_ONLY` として保持。型付きの定理命題への自動昇格なし。
- `phase165_r4_production_connection.py` : `discover_production_registry()` は確認済み命題 ID を推測しない。
- `phase165_r2_registry_lookup.py` : `find_eligible_goal_candidates()` は出典順・確認・型一致を検査する。
- `phase165_r3_recursive_search.py` : `ProofStep` を出典だけから生成しない。
- `tests/test_phase165_r2_registry_lookup.py` : 出典が不明・後続・異文献の場合の拒否テスト。

## 判定区分

- `toda_equation` / `toda_lemma` / `toda_proposition` : 先頭から Toda の locator 候補を抽出する。文献同一性の認定ではない。
- `external_tag` : `[O]`, `[MT]` 等。Toda 本文への帰属は行わない。
- `page_reference` : `p57` 等。単独で命題を識別できない。
- `other_unparsed` / `missing` : 保留。

すべての行で `typed_relation_verified=false`, `citation_eligible=false`, `proof_step_granted=false` とする。将来の R2/R3 で独立に証明資格判定する。

## 実行

プロジェクトのルートに展開し `powershell -ExecutionPolicy Bypass -File .\phase166_r1_source_registry_audit\run.ps1` を実行。結果は `audit_result.json` と `row_matches.csv`。テストは3件の限定テストのみ。

## R2 との境界

今回の照合は候補抽出のみ。等式パーサー、型検査、数学的同値判定、引用資格付与、共通探索への追加は実装しない。
