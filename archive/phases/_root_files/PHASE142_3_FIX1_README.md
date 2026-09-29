# Phase 142-3 fix 1

This package replaces only `tests/test_phase142_3_generic_proof_text.py`.

The audit showed that the generic renderer already renders the PRECONDITION fact as
`$2\\eta_{3} = 0$`. The failing assertion incorrectly required the compact spelling
without spaces around `=`.

No production code is changed by this fix.
