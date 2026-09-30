# Phase 150 Finalization Repair R2

## 目的

Phase 150 の generic Narrative route への移行後に残った 19 件の historical test contract を、現在の renderer ownership と generic route の構造に合わせる。

## 変更対象

production code は変更しない。

変更する test files:

- `tests/test_phase132_6_group_proof_narrative_renderer.py`
- `tests/test_phase132_7_group_proof_cli_modes.py`
- `tests/test_phase132_8_group_proof_narrative_dedup.py`
- `tests/test_phase132_9_web_group_proof_modes.py`
- `tests/test_phase133_10_sigma_label_wording.py`
- `tests/test_phase133_6_group_proof_narrative_labels.py`
- `tests/test_phase133_9_group_proof_narrative_labels.py`
- `tests/test_phase144_6_r3_production_references.py`
- `tests/test_phase144_6_r3_structured_references.py`
- `tests/test_phase144_6_r4_supporting_fact_filtering.py`

変更後の各 test file 全文は `reference_updated_tests/` に収録している。

## 契約変更

Phase 132–133 の旧 recursive/dedicated renderer 固有の文言（「すでに得た」「〜を用いる。」「このことから〜を得る。」等）を直接要求する assertion を、現在の generic route が保持すべき構造へ変更する。

主に次を確認する。

- Narrative heading が存在する。
- depth 2 では structured reference section が存在する。
- 文献参照が deduplicate される。
- target group の数式が保持される。
- CLI/Web adapter が Narrative と数式を保持する。

Phase 144-6 については現在の責務に合わせる。

- reference section の owner は `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`。
- explicit `LiteratureReference` が無い場合でも、Toda の rule name から安全に locator を推定できる現在仕様をテストする。

## 実行範囲

R2 では変更対象10ファイルの focused pytest のみを実行する。repository-wide full regression は実行しない。

R2 focused tests がすべて PASS した場合のみ、Phase 150 closure の最後に full regression を1回実行する。

## Phase 151 との境界

R2 は Narrative の品質改善を行わない。generic Narrative に残る proof-purpose、label、final-result derivation、raw fallback 等の品質問題は Phase 151 の all-group generic baseline 以降で全群横断に評価する。
