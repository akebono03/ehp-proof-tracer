Phase 144-6-R5-15J-R1
=========================

Minimal repair of the audit package only.

Cause
-----
The original 15J audit imported HomotopyMap from proof.py, but the current
repository has no HomotopyMap base class.

Current repository representation
---------------------------------
Map-like values are represented by concrete dataclasses such as:
- TodaSuspensionMap
- TodaHopfInvariantMap
- TodaDeltaMap
- TodaIteratedSuspensionMap
- TodaProp44DecompositionMap

Repair
------
- Remove the invalid HomotopyMap import.
- Detect a generic map-shaped dataclass structurally by source_group and
  target_group fields.

No production repository file is modified.
No test is modified.
No project document is modified.
No pytest is run.
The 15J audit question and visibility logic are unchanged.
