Phase 145 Resume R3

R2 stopped before editing because its helper regex was malformed.
R3 removes regex use entirely.

It changes only:
tests/test_phase131_5_web_group_proof.py
  test_phase131_5_group_proof_post_keeps_result_and_shows_proof

The existing test explicitly requests depth=2 and asserts Trace-specific
Depth output, so R3 explicitly adds group_proof_mode=trace.

Production changes in R3: none.
Repository-wide pytest: not run.
