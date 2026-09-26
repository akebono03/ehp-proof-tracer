Phase 143-75I R2

Test-only repair.

The production implementation is unchanged.

Reason:
_render_group_proof_narrative_fact() returns a complete Markdown
math fact wrapped in $...$. The original Phase 143-75I focused test
incorrectly asserted against the inner LaTeX only.

This repair updates the four expected values to follow the existing
renderer API contract.
