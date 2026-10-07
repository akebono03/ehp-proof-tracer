# Phase 159-R1-3 repair4

## 変更対象
- `toda_group_proof_narrative_renderer.py`
  - import に `_generic_group_map_name` を追加
  - `_phase159_unique_preimage_definition_line()` 全体を置換

## import 変更後
```python
from toda_group_proof_generic_narrative_renderer import (
  _GENERIC_INJECTIVE_STATEMENT_TYPES,
  _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  _generic_group_map_name,
  _render_generic_narrative_group_map_latex,
  _render_generic_narrative_step,
)
```

## 修正内容
`group_map.name` は使わず、既存の `_generic_group_map_name(group_map)` を使用する。

## 完了条件
- Phase 159 focused tests 全 PASS
- related regression 全 PASS
- `git diff --check` PASS
- pi_3^2 Narrative に unique-preimage prose が表示

## 次 Phase との境界
Reference attribution、exactness、numbering、inference rules、stable range は変更しない。
