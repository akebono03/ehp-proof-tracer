# Phase 150 / RC4-5F-2

Implements generic final group-structure reason prose.

## Changed production files

- `toda_group_proof_narrative_reasons.py`
  - adds `FINAL_GROUP_STRUCTURE`
  - adds `_final_group_structure_reason()`
  - classifies only from typed direct premises and compatible group/map shapes
- `toda_group_proof_narrative_reason_renderer.py`
  - renders the structural order argument and generator argument before the
    existing final group conclusion

## Added test

- `tests/test_phase150_rc4_5f_2_final_group_structure_reason.py`

## Mathematical boundary

The implementation does not create a new proof step for the intermediate
statement that the middle group has order four. It decomposes the existing
final inference rule's typed direct premises for presentation only.

No target dimensions, generator names, proposition numbers, or inference-rule
names are used by the classifier.

Repository-wide tests remain deferred until the end of Phase 150.
