# Phase 150 / RC4-5B-3-R2

Test-only repair for the incorrect beta LaTeX expectation introduced in
RC4-5B-3-R1.

Changed file:

- `tests/test_phase150_rc4_5b_3_r1_beta_latex.py`

The expected value is corrected from two literal backslashes to the actual
single-backslash LaTeX command `\beta`.

Production code is unchanged. Repository-wide tests are intentionally not run.
