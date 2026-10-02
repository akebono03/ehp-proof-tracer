# Phase 155-R3-3D-r1 — closure failure root-cause audit

- unresolved removable pairs: 2
- source-level duplicate name groups: 8
- exact duplicate name groups: 0
- divergent duplicate name groups: 8
- unresolved-pair endpoints overlapping duplicate-name groups: 0

## Unresolved removable pairs

- R3-00138
  - older: `tests/test_phase41_preimage_subgroup.py::test_phase41_2_preimage_subgroup_uses_map_symbol`
  - newer: `tests/test_phase41_preimage_subgroup.py::test_phase41_4_preimage_subgroup_map_type_remains_map_symbol`
  - older overlaps source duplicate: False
  - newer overlaps source duplicate: False
- R3-00139
  - older: `tests/test_phase41_preimage_subgroup.py::test_phase41_2_preimage_subgroup_uses_primary_component_target`
  - newer: `tests/test_phase41_preimage_subgroup.py::test_phase41_4_preimage_subgroup_target_type_remains_primary_component`
  - older overlaps source duplicate: False
  - newer overlaps source duplicate: False

## Source-level duplicate test names

- `tests/test_set_rules.py::test_image_membership_statement`
  - definitions: 2
  - exact same AST: False
- `tests/test_set_rules.py::test_image_membership_statement_distinguishes_image`
  - definitions: 2
  - exact same AST: False
- `tests/test_set_rules.py::test_image_membership_statement_uses_existing_image_subgroup`
  - definitions: 2
  - exact same AST: False
- `tests/test_set_rules.py::test_kernel_membership_statement`
  - definitions: 2
  - exact same AST: False
- `tests/test_set_rules.py::test_kernel_membership_statement_distinguishes_kernel`
  - definitions: 2
  - exact same AST: False
- `tests/test_set_rules.py::test_kernel_membership_statement_uses_existing_kernel_subgroup`
  - definitions: 2
  - exact same AST: False
- `tests/test_set_rules.py::test_mapped_zero_implies_kernel_membership`
  - definitions: 2
  - exact same AST: False
- `tests/test_set_rules.py::test_mapped_zero_implies_kernel_membership_uses_explicit_group_map`
  - definitions: 2
  - exact same AST: False

No production code or existing test was changed.
Repository-wide pytest was NOT run.
