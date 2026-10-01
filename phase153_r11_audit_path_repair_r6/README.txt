Phase 153-R11 Audit Path Repair R6
===================================

Cause
-----
The R5 audit script was executed from its package subdirectory.
Python therefore placed that subdirectory, not the repository root, on
sys.path, so project modules such as toda_calculation_facade were unavailable.

Repair
------
The audit script now inserts its parent repository root into sys.path before
importing project modules.

Production changes
------------------
None.

Test changes
------------
None.

Verification
------------
- compile the audit script;
- rerun the R11 test file;
- run the corrected audit.

Full pytest remains deferred until the end of Phase 153.

Punctuation normalization remains deferred.
Final prose style should use "," and "." instead of "、" and "。".
