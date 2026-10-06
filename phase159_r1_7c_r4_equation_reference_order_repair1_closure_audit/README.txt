Phase 159 R1-7c R4 equation-reference order repair1 closure audit

Purpose
-------
Re-run the public equation-reference order audit after repair1.

Before repair1:
- rendered: 112
- failed: 0
- outputs with forward equation references: 1
- forward equation-reference occurrences: 2
- valid backward equation-reference occurrences: 21

The confirmed forward references were both in pi_5^3.

Expected closure
----------------
- rendered: 112
- failed: 0
- outputs with forward equation references: 0
- forward equation-reference occurrences: 0
- valid backward equation-reference occurrences remain present

The exact backward-reference count is reported for comparison, but the
essential contract is that every public equation-number reference points to a
tagged statement that appears earlier in the proof body.

Scope
-----
Audit only.

Range:
  n=2..15
  k=0..7
  max_depth=2

This is a reproducible audit sample, not a permanent group-count contract.

Production code changes: none.
Test code changes: none.
No full pytest.
