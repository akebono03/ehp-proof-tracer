# Phase 171 R20R13R4 — Test Assertion Correction

This package corrects a single mistaken test assertion in `phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py`.

The existing merged output is already one complete line. The failed assertion incorrectly used `list.count()` with a citation-prefix string, whereas each list item is a whole Markdown line. The corrected assertion counts matching line prefixes.

**No production source, proof search, mathematics, or references are changed.**

Run `run.ps1 -DryRun` and then `run.ps1` after extraction. The latter runs focused tests and replays the R20R13R3 verification. Full pytest remains reserved for Phase closeout.
