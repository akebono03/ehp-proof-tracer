Phase157-R20 repair36

Purpose
-------
Update one stale Phase157 test expectation for generic relation spacing.

Current production output
-------------------------
  [R2]より, $H\left(\nu'\right) = \eta_{5}$.

The failing test still expected:
  [R2]より, $H\left(\nu'\right)=\eta_{5}$.

The repository's generic relation renderer and existing tests use spaces
around `=`. Therefore this is a stale test expectation, not a production
rendering defect.

Changed file
------------
- tests/test_phase157_r11_reference_reason_punctuation.py

Changed test function
---------------------
- test_phase157_r11_r11_hopf_derivation_precedes_surjectivity()

Production code changes
-----------------------
None.

Repository-wide pytest
----------------------
Not run. Phase-wide full pytest remains reserved for Phase157 closure.
