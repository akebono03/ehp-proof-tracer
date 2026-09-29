Phase 146-8 Historical Narrative Full Structural Diff Audit

Purpose
-------
Compare the completed historical pi_6^3 Narrative from Phase 136-2 with the
current local Narrative after Phase 146-7.

Historical baseline
-------------------
908e24db89669750949fa9ad149f5e306ac05546

Production changes
------------------
None.

Existing test changes
---------------------
None.

Audit units
-----------
The output is split into prose and math units. Equation tags and whitespace are
normalized for structural matching.

Classifications
---------------
PRESERVED
  Same normalized unit in approximately the same position.

LOST
  Historical unit for which no sufficiently close current unit was found.

ADDED
  Current unit with no historical counterpart.

MOVED
  Same normalized unit exists but its relative position changed materially.

DUPLICATED
  Additional repeated current unit beyond the historical occurrence count.

REWORDED
  Same mathematical signature or sufficiently similar prose/math candidate.

UNMATCHED
  Reserved for future/manual classification; the current audit avoids forcing
  uncertain candidates into semantic equivalence.

Important limitation
--------------------
REWORDED and MOVED are heuristic candidates, not mathematical proof of
equivalence. The generated Markdown report must be reviewed before deciding the
remaining implementation phases.

Generated artifact
------------------
phase146_8_historical_narrative_structural_diff.md

This report is written to the repository root so it is easy to inspect or
upload back to ChatGPT.

Full suite
----------
Not run. This Phase is an audit only and project policy reserves the full suite
for the end of an implementation Phase.


R1 repair
---------
The original runner used ProcessStartInfo.ArgumentList, which is unavailable in
the user's Windows PowerShell/.NET runtime. R1 uses the compatible
ProcessStartInfo.Arguments property instead. Audit logic is unchanged.
