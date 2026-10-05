Phase157-R20 repair53-r1 — stale pi8 label test

Purpose
-------
Repair one stale Phase134 public Narrative expectation encountered while
validating repair53.

Observed failure
----------------
The existing test required:

  Toda (5.6) の ν₄ 分解

to remain visible in the public pi_8^5 Narrative.

Why this is stale
-----------------
Later public Reference work no longer guarantees historical Phase133
human-readable internal labels as public output.

Repository history confirms:
- analogous Phase133 label expectations were replaced during Phase150
  finalization;
- the Phase155 test inventory classified
  test_phase134_9_pi8_5_keeps_phase133_labels as review_required rather than
  a decisive canonical contract.

Changed file
------------
tests/test_phase134_9_pi8_5_narrative.py

Changed function
----------------
test_phase134_9_pi8_5_keeps_phase133_labels()

The function name is retained to avoid unnecessary test-ID churn.
Its assertions now verify the current public contract:
- Toda Proposition 5.6 proof target is visible;
- structured Reference and Proof headings exist;
- the pi_8^5 group result is visible.

Imports
-------
No changes.

Production changes
------------------
None.

Then the repair53 validation sequence is resumed.

Repository-wide pytest remains deferred to Phase157 closure.
