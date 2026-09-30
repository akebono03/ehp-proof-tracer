# Phase 150 RC4-7B-1 Revert

This package reverts only the experimental recursive Argument-frontier change
introduced by Phase 150 RC4-7B-1.

It does not modify the RC4-7A Reference normalization work.
It does not modify renderer routing.
It does not run the repository-wide test suite.

After the revert, the Phase 143 pi15^8 test is run separately. If that test
still fails because the Reference section is prepended, the failure is
independent of the RC4-7B-1 frontier experiment and should be repaired at the
Reference-rendering boundary before continuing RC4-7B.
