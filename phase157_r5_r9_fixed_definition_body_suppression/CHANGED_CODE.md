# Phase157-R5-R9 changed code

## Changed production file

`toda_group_proof_narrative_contribution_renderer.py`

### Changed import

```python
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
)
```

### New helper

`_phase157_r5_r9_selected_fixed_definition_step_ids()`

Complete post-apply function is written to:

`phase157_r5_r9_output/selected_fixed_definition_helper_after.txt`

### Changed function

`suppress_toda_group_proof_narrative_reference_internal_body()`

Complete post-apply function is written to:

`phase157_r5_r9_output/reference_internal_body_suppression_after.txt`

### Changed function

`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

Complete post-apply function is written to:

`phase157_r5_r9_output/render_multi_argument_with_contributions_after.txt`

The only call-site change is passing `semantic_sidecar`.

## Tests

Changed complete test functions:
- Phase157 R5-R6 body-boundary expectation
- Phase144 depth2 Narrative definition expectation
- Phase144 CLI depth2 Narrative definition expectation

New complete test file:
- `tests/test_phase157_r5_r9_fixed_definition_body_suppression.py`
