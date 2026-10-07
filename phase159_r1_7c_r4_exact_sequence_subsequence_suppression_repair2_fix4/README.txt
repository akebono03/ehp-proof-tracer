Phase 159 R1-7c R4 exact-sequence suppression repair2 fix4

Cause
-----
The current pi_6^3 public Narrative uses display math with line breaks inside
the EHP sequence block.

repair2 fix3 still compared the entire sequence as one literal line, so the
test failed even though the sequence was present.

Fix
---
Production code changes: none.

Only the two Phase157 regression tests are updated.

They normalize whitespace using:

  normalized_body = " ".join(body.split())

and then verify the exact sequence core and its ordering.

This keeps the tests independent of harmless line wrapping while preserving
the mathematical sequence and duplicate-suppression contract.

No eta_2 wording changes.
No Reference changes.
No generator changes.
No full pytest.
