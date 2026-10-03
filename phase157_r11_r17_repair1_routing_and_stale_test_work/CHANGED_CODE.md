# Phase157 R11-R17 repair1

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

import 変更なし。

変更関数全体:
- `insert_toda_group_proof_narrative_hidden_zero_map_premises()`

pipeline 変更:
- `link_toda_group_proof_narrative_unmarked_reference_consumers()` を
  body-usage filter 前へ移動。
- 後段の重複 linkage/filter を削除。

### `toda_group_proof_narrative_renderer.py`

import 変更なし。

新規関数:
- `_phase157_r11_r17_normalize_public_connectors()`
- `_phase157_r11_r17_normalize_public_numeric_equalities()`

追加位置:
- `_finalize_toda_group_proof_narrative_markdown()` の直前。

変更関数全体:
- `_finalize_toda_group_proof_narrative_markdown()`

目的:
- dedicated route を含む public Narrative 全体で standalone connector を除去。
- `=N=N` を public output 全体で正規化。

### `tests/test_phase156_r6_canonical_connector_local_ordering.py`

変更テスト関数全体:
- old `test_phase156_r6_pi6_places_equation3_before_order_and_group_transport()`
- new `test_phase156_r6_pi6_places_equation3_before_transport_and_order()`

新しい期待順:
- equation (3)
- [R1] pi_5^2 group
- E injective
- ord(eta_3^3)=2

これは R11-R14 の dependency graph に一致する。

## 実行 pytest

focused pytest のみ。
full repository pytest は Phase157 closure まで実行しない。

## 完了条件

- R11-R17 7 tests pass。
- R11/R5/R9/R10 regressions pass。
- Phase156 stale test update 後の connector/order tests pass。
- Phase148/Phase93 regressions pass。

## 次 Phase 境界

repair1 完了後に 112-group R11-R18 re-audit。
docs / full pytest はまだ行わない。
