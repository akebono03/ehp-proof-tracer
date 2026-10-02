Phase 155-R3-3D-r4 — hidden coverage migration / final duplicate cleanup

Purpose
-------
This is the first R3-3D step that changes existing tests.

Inputs already established by the preceding audits:
- 8 divergent same-name duplicate groups;
- 6 groups contain hidden assertions in an earlier shadowed definition;
- 2 groups have no hidden coverage requiring preservation;
- 2 unresolved removable pairs are safe `delete older / keep newer`
  candidates;
- manual semantic review required: 0.

Changed files / functions
-------------------------
The exact test files and function names are taken from the current local
R3-3D-r2/r3 audit outputs and are printed before the apply step.

No production file is changed.
No import block is changed.
No class is changed.

Repair rule
-----------
For the 6 hidden-coverage groups, the earlier shadowed definition is renamed
to a deterministic new `test_*` name. This activates the exact historical
test body that Python previously shadowed, without rewriting its assertions,
fixtures, setup, local variables, or decorators.

For the 2 cleanup-ready duplicate groups, the earlier shadowed definition is
deleted and the runtime/final definition remains unchanged.

For the 2 repaired removable pairs, the older test function is deleted and
the newer test remains unchanged.

Verification
------------
The verifier checks:
- every original safe deletion ID plus the 2 repaired older IDs is absent;
- both newer pair tests remain;
- every renamed hidden-coverage test exists;
- source-level duplicate top-level `test_*` names are zero;
- graph survivors remain, except the two explicitly repaired older IDs;
- historical_keep IDs remain;
- unresolved removable pairs are zero;
- focused pytest passes for the changed duplicate/pair surfaces.

Repository-wide pytest is NOT run. It remains deferred to Phase 155 closure.

Completion
----------
If all repaired closure conditions pass, Phase 155 R3
duplicate/superseded cleanup is complete and Phase 155-R4 can begin.
