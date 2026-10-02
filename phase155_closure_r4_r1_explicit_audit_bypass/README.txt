Phase 155 Closure-R4-R1

Cause
-----
The first R4 attempt did not execute any audit body. Each exact audit nodeid was
reported as `1 deselected`.

Repair
------
For explicit Phase-final audit execution only:
- clear `PYTEST_ADDOPTS`;
- use `--noconftest` so routine-regression deselection hooks cannot suppress
  the exact audit nodeid;
- add both repository root and `tests/` to `PYTHONPATH` so the existing test
  imports continue to work;
- keep the exact five reviewed audit nodeids;
- keep 600-second timeout and checkpoint behavior.

No test body is modified.
No production code is modified.
No documentation is updated unless all five audit bodies actually PASS.

After 5/5 PASS, this wrapper reuses the already-reviewed documentation updater
and verifier from the original Closure-R4 package.
