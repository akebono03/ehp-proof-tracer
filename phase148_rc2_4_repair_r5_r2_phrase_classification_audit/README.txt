Phase 148 RC2-4 Repair R5-R2
Exactness phrase classification audit

R5-R1 finding
-------------
For both pi_10^4 and pi_12^5:
- the TodaProp42ExactnessStatement exists in proof data,
- RC2 classifies it,
- its normalized raw rendering is NOT visible in the final Narrative.

Nevertheless the six-group audit counted one occurrence of the generic text
"is exact" in each final Narrative.

Purpose
-------
Determine whether that remaining phrase is:
A. an actual raw exactness ProofStep leak, or
B. a distinct higher-level EHP method sequence that RC2 intentionally keeps.

The current six-group audit counts text phrases only and therefore cannot
distinguish A from B.

GitHub develop inspection
-------------------------
Current source contains "is exact" rendering in more than one presentation
path, including higher-level method-sequence presentation. RC2 R2 explicitly
preserved higher-level method sequences while suppressing raw windows.

Production changes
------------------
None.

Existing tests changed
----------------------
None.

Repository-wide pytest
----------------------
Not run.

Phase boundary
--------------
If R5-R2 confirms case B, repair the audit invariant rather than production.
The corrected invariant must compare against actual normalized
TodaProp42ExactnessStatement renderings, not merely count the Japanese phrase.
Do not alter RC3 ordering.
