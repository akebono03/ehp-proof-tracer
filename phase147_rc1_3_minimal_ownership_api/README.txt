Phase 147 RC1-3

Establishes one generic API mapping a NarrativeArgument to its owned primary
exactness method while preserving the existing selection semantics.

Production:
- toda_group_proof_narrative_exactness_selection.py
- toda_group_proof_narrative_argument_multi_renderer.py

Test:
- tests/test_phase147_rc1_argument_method_ownership.py

RC2-RC6 are intentionally untouched.
The runner executes focused tests only.
