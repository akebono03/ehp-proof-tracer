Phase 148 RC2-4 Repair R5-R1
Exposure-path audit runner repair

Observed R5 result
------------------
R5 stopped with:
46 passed, 2 failed.

The two failures were not new regressions. They were the already-known
six-group completion assertions requiring zero visible raw exactness in:
- pi_10^4
- pi_12^5

R5 exists specifically to diagnose those two known failures. Including the
completion test before the reverse-trace diagnostic prevented the diagnostic
from running.

R5-R1 correction
----------------
Production changes: none.
Existing tests changed: none.
Audit code changes: none.

The runner now executes:
1. R5 reproduction/diagnostic tests.
2. Existing focused RC2/R4.2 regression tests that are expected to pass.
3. The R5 exactness reverse-trace diagnostic.

The still-unmet six-group zero-leak completion test is intentionally excluded
from this diagnostic run. It will be restored after the leakage path is fixed.

GitHub check
------------
The audit-only six-group test is not present on develop, which is expected
because it was installed locally by the preceding audit package.

Phase boundary
--------------
Do not weaken or delete the six-group completion invariant.
Do not change production code in R5-R1.
Do not change Narrative ordering.
Do not run repository-wide pytest.
