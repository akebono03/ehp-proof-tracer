# Phase 165 R52-R26-R1 installer correction

This package corrects the installer guard from R26-R1. The original installer searched the entire `_build_prop51_step` function for a unique legacy lookup, but the expression occurs twice: in `pi3_2_step` and `eta2_hopf_step`. The corrected installer rewrites only the `pi3_2_step` lookup and preserves the independent `eta2_hopf_step` source.

Run `run.ps1` from the extracted package directory. It installs the targeted change (with backup), then runs the targeted regression tests. It does not run the full pytest suite.

Modified production file: `toda_prop56_zero_bootstrap.py` (`_build_prop51_step` only). No dedicated inference rules are restored.

`CHANGED_CODE.py` is the full installer source. `MODIFIED_FUNCTION.md` is created by the installer with the complete installed function.
