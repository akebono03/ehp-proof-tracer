Phase 155-R2C — confirmed stale expectation repair

Scope
-----
This package repairs only the 45 tests that failed in the Phase 155-R2B
focused verification and were therefore backed by confirmed-stale findings.

It does not modify production code.
It does not delete tests.
It does not run repository-wide pytest.

Repair classes
--------------
1. Punctuation-only expectation maintenance
   - Japanese comma -> ASCII comma + space
   - Japanese period -> ASCII period
   This is applied only inside R2B-confirmed failing test functions.

2. Current-contract replacement for four superseded assumption families
   - Phase 132 old source prose
   - Phase 143 short-exact explanatory wording
   - Phase 144 exact public-renderer == generic-renderer equality
   - Phase 153 old fixed Reference selection / compact marker wording

Verification
------------
After repair the package re-runs the Phase 155-R2B verifier against the same
61 unique high-candidate tests and writes its result to:

phase155_r2c_verification_output/

Completion requires:
- pytest_exit_code == 0
- confirmed_stale == 0
- verification_inconclusive == 0

The full repository suite remains deferred until Phase 155 closure.
