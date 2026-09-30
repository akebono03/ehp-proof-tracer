# Phase 150 Final Regression 9-Failure Repair R2

Production code changes: none.

Changed file:
- tests/test_phase150_rc4_5_visible_reasons.py

Changed function:
- test_phase150_rc4_5_visible_reason_count_matches_typed_reason_count

The test now validates multiplicity per rendered reason sentence:

- group typed reasons by their rendered sentence;
- count how many typed reason instances map to each sentence;
- require the Narrative to contain that sentence exactly the same number of times.

This preserves one-to-one instance coverage even when several typed reasons share
the same generic prose sentence.

Phase 148 repairs from R1 are left unchanged.

The runner executes:
1. the RC4-5 test file;
2. the three test files covering the original nine failures.

It does not run the full regression.
