Phase 159 R1-7c R4 exact-sequence subsequence suppression audit2 fix2

Purpose
-------
Fix the audit so it follows the current multi-argument Narrative API.

Cause
-----
render_toda_group_proof_narrative_multi_argument_markdown() now requires:
- presentation
- blocks
- semantic_sidecar
- arguments

Fix
---
Build the same context used by the current Narrative pipeline:
presentation -> semantic sidecar -> blocks -> arguments.

Production code changes: none.
Test code changes: none.
No full pytest.
