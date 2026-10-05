# Phase157 R11-R14 repair1

## 変更対象

### toda_group_proof_narrative_references.py

変更関数全体:
- `restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()`

変更:
- optional `presentation` 引数追加。
- consumer map を構築。
- used fixed Reference でも consumer が他の non-root Reference statement のみなら復元しない。

### toda_group_proof_narrative_contribution_renderer.py

変更:
- restore call に `presentation=presentation` を追加。

### tests/test_phase157_r11_reference_reason_punctuation.py

追加:
- ORDER dependency ordering regression
- H-surjectivity before short-exact regression
- ancestry-only Reference pruning regression

## 既に適用済みで今回触らないもの

- `order_toda_group_proof_narrative_order_support()`
- updated `order_toda_group_proof_narrative_surjectivity_support()`
- ordering pipeline call

## Full pytest

Phase157 closure まで実行しない。
