Phase 145-2 Stage 2 - Relative Path Risk Refinement

Purpose
-------
Refine the 408 artifacts marked MOVE_REQUIRES_RELATIVE_PATH_REVIEW in Stage 1.
This stage performs no move, deletion, production change, test change, or docs change.

Classification
--------------
MOVE_REQUIRES_PATH_UPDATE
  Concrete archive-sensitive path assumption was detected.

MOVE_SAFE_AFTER_REFINEMENT
  Only broad Stage 1 markers remain; no archive-sensitive path calculation was detected.

MOVE_SAFE_STAGE1_FALSE_POSITIVE
  The refined executable patterns do not reproduce the Stage 1 risk.

Boundary
--------
Historical runners are not rewritten in Stage 2. Stage 3 will decide how to handle
MOVE_REQUIRES_PATH_UPDATE. Full pytest remains reserved for the end of Phase 145-2.
