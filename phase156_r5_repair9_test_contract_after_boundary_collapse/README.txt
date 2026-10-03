Phase 156-R5 repair9 — test contract after Reference boundary collapse

結論
====
repair8 production behavior is correct.

The public pi_6^3 Narrative no longer contains:
- nu' definition argument
- Lemma 5.2 application prose
- internal bracket-membership proof

Therefore the first visible proof argument is now:
  次に, nu' の位数を決定するために ...

The previous tests incorrectly assumed every public Narrative body starts with:
  まず

Production changes
==================
None.

Test contract changes
=====================
1. Phase150 visible-reason tests
   Reference-owned reason semantics remain in the semantic sidecar,
   but they are intentionally absent from the public Narrative.

2. Phase156-R5 tests
   Stop using split("まず") as a section boundary.
   For pi_6^3, verify the remaining public proof begins at the order argument.

3. New repair9 focused test and 112-group depth2/depth3 audit.

Import changes
==============
tests/test_phase150_rc4_5_visible_reasons.py import block is replaced in full.
Production imports are unchanged.

Boundary
========
No further Reference-collapse production behavior is introduced in repair9.
Repository-wide pytest remains reserved for Phase 156 closure.
