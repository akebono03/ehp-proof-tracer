# Phase 167 R5: Beta LaTeX Test Expectation Correction

This package updates one assertion in `tests/test_phase150_rc4_5b_3_r1_beta_latex.py`: the expected output is changed from a double backslash to the canonical single-backslash LaTeX command `\beta`. Production code is unchanged.

`test_phase150_rc4_5b_3_r1_beta_latex_full.py` contains the complete revised test with its imports. `patch.py` backs up the original test, checks the original assertion, and replaces it. `run.ps1` executes only the focused test; the full suite is reserved for the Phase 167 closing gate.
