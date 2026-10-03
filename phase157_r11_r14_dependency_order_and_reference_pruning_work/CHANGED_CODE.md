# Phase157 R11-R14 change summary

## Production

### toda_group_proof_narrative_contribution_renderer.py

新規関数:
- `order_toda_group_proof_narrative_order_support()`
  - 追加位置: `order_toda_group_proof_narrative_surjectivity_support()` の直前。

変更関数:
- `order_toda_group_proof_narrative_surjectivity_support()`
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

目的:
- ORDER statement を visible direct premises の後ろへ。
- MAP_PROPERTY の equality support + map statement を、
  その全射性を使う short-exact derivation より前へ。

### toda_group_proof_narrative_references.py

変更関数:
- `restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()`

変更:
- optional `presentation` を追加。
- used fixed Reference でも、その consumer が別の non-root Reference statement だけなら復元しない。
- root または Reference 外の proof step に使われる fixed Reference は従来どおり復元。

## Tests

### tests/test_phase157_r11_reference_reason_punctuation.py

追加:
- `test_phase157_r11_r14_eta3_cube_order_follows_injectivity()`
- `test_phase157_r11_r14_surjectivity_precedes_short_exact_derivation()`
- `test_phase157_r11_r14_ancestry_only_reference_is_not_public()`

## 完了条件

- E injective < ord(eta_3^3)=2
- H support / H surjective < short exact derivation
- ancestry-only [R3] absent from public Reference
- focused pytest pass
- full pytest はまだ実行しない
