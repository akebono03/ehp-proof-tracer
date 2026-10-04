Phase157-R20 repair7

Purpose
-------
Keep fixed-literature aggregate carrier steps long enough for the existing
generic aggregate-component selector to inspect their external consumers.

Root cause
----------
`filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary()`
discarded every fixed statement whose `component_key` was `None`.

That includes aggregate integration steps such as the Proposition 5.3
finite-dimensional statement.  This happened before
`_phase153_r6_reference_aggregate_component()` could select the one component
actually used by the current proof.

Generic repair
--------------
When a fixed-statement boundary has `component_key is None`, retain it as a
candidate if its literature locator has a non-empty fixed-component catalog.

Later existing stages still decide:
- whether the Reference is actually used;
- which aggregate component is relevant;
- whether it survives final Reference pruning.

No proposition number, target group, sphere dimension, or generator name is
hard-coded.

Changed files
-------------
- toda_group_proof_narrative_references.py
  - import block from toda_literature_statement_boundary
  - filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary()
- tests/test_phase157_r20_repair7_fixed_aggregate_carriers.py (new)

No documentation changes.
No repository-wide pytest.
