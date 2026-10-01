Phase 153-R9 R8 Test Expectation Repair R1
==========================================

Observed failure
----------------
R9 correctly removes the explicit gamma -> eta_2 gamma re-derivation from
the pi_6^2 final proof body by reusing selected Reference [R3].

The R8 integration test still required that old derivation line to remain.
That expectation conflicts with the R9 specification.

Repair
------
Production changes: none.

Changed:
tests/test_phase153_r8_reference_use_prose_normalization.py

The R8 direct unit test that checks ordinary non-Reference derivation prose is
not rewritten remains unchanged.

The integration test now checks only that the final pi_6^2 conclusion remains.

Full pytest remains deferred until the end of Phase 153.
