# Phase 155-R3-3D-r2 — divergent duplicate / unresolved pair semantic audit

## Divergent duplicate definitions

- groups: 8
- runtime uses final definition in all groups: True
- shadowed groups with unique assertions: 6
- shadowed groups without unique assertions: 2

### `tests/test_set_rules.py::test_image_membership_statement`

- definitions: 2
- runtime definition ordinal: 2
- runtime definition line: 2611
- earlier-only assertions: 1
- shadowed definition has unique assertions: True

### `tests/test_set_rules.py::test_image_membership_statement_distinguishes_image`

- definitions: 2
- runtime definition ordinal: 2
- runtime definition line: 2703
- earlier-only assertions: 0
- shadowed definition has unique assertions: False

### `tests/test_set_rules.py::test_image_membership_statement_uses_existing_image_subgroup`

- definitions: 2
- runtime definition ordinal: 2
- runtime definition line: 2646
- earlier-only assertions: 3
- shadowed definition has unique assertions: True

### `tests/test_set_rules.py::test_kernel_membership_statement`

- definitions: 2
- runtime definition ordinal: 2
- runtime definition line: 2468
- earlier-only assertions: 1
- shadowed definition has unique assertions: True

### `tests/test_set_rules.py::test_kernel_membership_statement_distinguishes_kernel`

- definitions: 2
- runtime definition ordinal: 2
- runtime definition line: 2559
- earlier-only assertions: 0
- shadowed definition has unique assertions: False

### `tests/test_set_rules.py::test_kernel_membership_statement_uses_existing_kernel_subgroup`

- definitions: 2
- runtime definition ordinal: 2
- runtime definition line: 2503
- earlier-only assertions: 3
- shadowed definition has unique assertions: True

### `tests/test_set_rules.py::test_mapped_zero_implies_kernel_membership`

- definitions: 2
- runtime definition ordinal: 2
- runtime definition line: 2755
- earlier-only assertions: 1
- shadowed definition has unique assertions: True

### `tests/test_set_rules.py::test_mapped_zero_implies_kernel_membership_uses_explicit_group_map`

- definitions: 2
- runtime definition ordinal: 2
- runtime definition line: 2820
- earlier-only assertions: 1
- shadowed definition has unique assertions: True

## Unresolved removable pairs

- pairs: 2

### `R3-00138`

- older: `tests/test_phase41_preimage_subgroup.py::test_phase41_2_preimage_subgroup_uses_map_symbol`
- newer: `tests/test_phase41_preimage_subgroup.py::test_phase41_4_preimage_subgroup_map_type_remains_map_symbol`
- classification: `graph_has_no_deletion_candidate_endpoint`

  - older graph deletion candidate: False
  - older safe function deletion row: False
  - newer graph deletion candidate: False
  - newer safe function deletion row: False

### `R3-00139`

- older: `tests/test_phase41_preimage_subgroup.py::test_phase41_2_preimage_subgroup_uses_primary_component_target`
- newer: `tests/test_phase41_preimage_subgroup.py::test_phase41_4_preimage_subgroup_target_type_remains_primary_component`
- classification: `graph_has_no_deletion_candidate_endpoint`

  - older graph deletion candidate: False
  - older safe function deletion row: False
  - newer graph deletion candidate: False
  - newer safe function deletion row: False

No production code or existing test was changed.
Repository-wide pytest was NOT run.
