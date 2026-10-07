Phase 159 R1-7c R4 exact-sequence suppression repair2 fix1

Purpose
-------
Fix only the repair2 apply-script anchor.

Cause
-----
The previous apply script depended on a large exact source block.
The user's current working tree did not match that block byte-for-byte,
so application stopped before changing production code.

Fix
---
Keep the repair2 production design unchanged.

Within:
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

the script now finds:
  generic_used_step_ids = (

and inserts the late exact-sequence suppression call immediately before it.

The helper insertion is idempotent.

No eta_2 wording changes.
No Reference changes.
No generator changes.
No full pytest.
