# Phase157 R5-R10 repair7

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更する関数:

`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`

変更内容:
- `reference_section` の先頭に legacy intro がある場合、
  public output へ埋め込むコピーからだけ除去する。
- 低レベル Reference renderer は変更しない。

### 更新する既存テスト

- `tests/test_phase132_7_group_proof_cli_modes.py`
- `tests/test_phase150_rc4_7a_cross_group_reference_normalization.py`
- `tests/test_phase144_6_r3_production_references.py`
- `tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py`
- `tests/test_phase153_r11_generic_reference_attribution_filtering.py`

これらは public output の旧表示文を期待していたため、
Phase157-R10 の新しい section heading 契約へ更新する。

### 維持する既存テスト

`tests/test_phase153_r3_4_reference_statement_rendering_connection.py`

低レベル Reference renderer の出力契約は変更しないため、
このテストは変更せず focused pytest に含める。

## Phase 境界

proof body relevance の本体修正は R11 で扱う。
