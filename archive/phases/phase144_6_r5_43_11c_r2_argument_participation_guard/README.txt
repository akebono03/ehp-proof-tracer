Phase 144-6-R5-43-11C-R2
Argument participation guard

Production file changed:
- toda_group_proof_narrative_contribution_renderer.py

Changed function:
- _argument_fallback_anchor_index

Repair:
A visible provider block can be shared by a DETACHED Argument and another
Narrative-participating Argument. Therefore provider visibility alone cannot
activate fallback contribution placement.

R2 requires the current Argument's purpose sentence to be visible in the base
Narrative before any fallback anchor is accepted. After that participation
guard, the latest visible provider anchor is preferred; otherwise the purpose
sentence itself is used.

Expected boundary:
- non-DETACHED selected=33, insertable=33
- DETACHED selected=157, insertable=0

No target-specific branch.
No public CLI/Web route switch.
No full test suite.
