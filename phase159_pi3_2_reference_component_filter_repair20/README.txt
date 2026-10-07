Phase 159 pi3_2 Reference component-filter repair20

Purpose
-------
Restore the existing fixed-statement component-selection path for Toda (5.1)
instead of rebuilding the whole reference entry with a post-processing string
replacement.

Changes
-------
- Use range_is_explicit_in_current_aggregate in fixed-statement filtering.
- Render Toda (5.1) general formulas per selected component.
- Remove the repair19 whole-entry canonicalization wrapper when present.
- Update the focused source-faithful reference test.

Out of scope
------------
- Proof-body derivation changes
- Restoring E(iota_1)=iota_2
- Removing specific GIVEN premises
- pi_4^3 work
- Repository-wide pytest
