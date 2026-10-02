# Phase 155-R3-3D-r3 — hidden coverage preservation / pair decision repair

## Hidden coverage

- duplicate-name groups: 8
- shadowed cleanup ready: 2
- hidden coverage preservation required: 6

### `tests/test_set_rules.py::test_image_membership_statement`

- hidden assertions: 1
- all hidden assertions covered by other runtime tests: False
- recommendation: `preserve_hidden_coverage_before_cleanup`

### `tests/test_set_rules.py::test_image_membership_statement_distinguishes_image`

- hidden assertions: 0
- all hidden assertions covered by other runtime tests: True
- recommendation: `shadowed_definition_cleanup_ready`

### `tests/test_set_rules.py::test_image_membership_statement_uses_existing_image_subgroup`

- hidden assertions: 3
- all hidden assertions covered by other runtime tests: False
- recommendation: `preserve_hidden_coverage_before_cleanup`

### `tests/test_set_rules.py::test_kernel_membership_statement`

- hidden assertions: 1
- all hidden assertions covered by other runtime tests: False
- recommendation: `preserve_hidden_coverage_before_cleanup`

### `tests/test_set_rules.py::test_kernel_membership_statement_distinguishes_kernel`

- hidden assertions: 0
- all hidden assertions covered by other runtime tests: True
- recommendation: `shadowed_definition_cleanup_ready`

### `tests/test_set_rules.py::test_kernel_membership_statement_uses_existing_kernel_subgroup`

- hidden assertions: 3
- all hidden assertions covered by other runtime tests: False
- recommendation: `preserve_hidden_coverage_before_cleanup`

### `tests/test_set_rules.py::test_mapped_zero_implies_kernel_membership`

- hidden assertions: 1
- all hidden assertions covered by other runtime tests: False
- recommendation: `preserve_hidden_coverage_before_cleanup`

### `tests/test_set_rules.py::test_mapped_zero_implies_kernel_membership_uses_explicit_group_map`

- hidden assertions: 1
- all hidden assertions covered by other runtime tests: False
- recommendation: `preserve_hidden_coverage_before_cleanup`

## Unresolved pair decision repair

- pairs: 2
- delete-older / keep-newer candidates: 2
- manual semantic review required: 0

### `R3-00138`

- older: `tests/test_phase41_preimage_subgroup.py::test_phase41_2_preimage_subgroup_uses_map_symbol`
- newer: `tests/test_phase41_preimage_subgroup.py::test_phase41_4_preimage_subgroup_map_type_remains_map_symbol`
- verified decision: `removable_duplicate`
- older assertions subset newer: True
- older calls subset newer: True
- external references to older test function: 0
- repaired decision: `delete_older_keep_newer_candidate`

### `R3-00139`

- older: `tests/test_phase41_preimage_subgroup.py::test_phase41_2_preimage_subgroup_uses_primary_component_target`
- newer: `tests/test_phase41_preimage_subgroup.py::test_phase41_4_preimage_subgroup_target_type_remains_primary_component`
- verified decision: `removable_duplicate`
- older assertions subset newer: True
- older calls subset newer: True
- external references to older test function: 0
- repaired decision: `delete_older_keep_newer_candidate`

No production code or existing tests were changed.
Repository-wide pytest was NOT run.
