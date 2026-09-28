Phase 144-6-R5-43-11C
Non-DETACHED fallback placement repair

Production file changed:
- toda_group_proof_narrative_contribution_renderer.py

Changed functions:
- new _argument_fallback_anchor_index
- full replacement of _contribution_insertion_indices
- import section updated

Repair:
When an Argument conclusion step is not directly rendered in the base
Narrative, contribution placement no longer fails immediately. The renderer
uses the latest visible provider anchor for that Argument. If no provider
anchor is visible, it uses the visible Argument purpose sentence.

This preserves the existing discourse boundary:
- 33 selected contributions in non-DETACHED populated Arguments become
  insertable;
- 157 selected contributions in DETACHED Arguments remain uninserted.

No group-specific n/k branch.
No sigma-specific branch.
No public CLI/Web route switch.
No full test suite.
