Phase157-R20 repair53-r2a — pi15 reference-loss audit harness fix

Purpose
-------
Fix the repair53-r2 audit harness hang.

Cause
-----
TodaGroupProofNarrativeReferenceEntry exposes:
- number
- reference
- proof_steps

The r2 audit incorrectly looked for:
- literature_reference

That returned None, causing the audit to fall back to repr(entry). The entry
contains proof steps and graph-linked objects, so the repr expansion became
very large and appeared to hang immediately after:

  GRAPH REFERENCE ENTRIES
  count: 1

Fix
---
Use entry.reference directly and print only lightweight fields:
- number
- reference.source
- reference.locator
- reference.label
- proof-step count
- each proof step's conclusion type
- each proof step's inference-rule name

No recursive repr() is used.

Production code changes
-----------------------
None.

pytest
------
Not run.

Next step
---------
Use the resulting stage-by-stage output to identify exactly where Proposition
4.4 disappears.
