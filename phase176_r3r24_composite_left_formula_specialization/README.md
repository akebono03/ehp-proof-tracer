# Phase 176 R3R24 — Composite-left Hopf formula specialization

This package makes one scoped production change: replace the entire `_formula_parts` function in `phase171_r2h_prop22_cited_hopf/source.py`. The cited universal Toda Proposition 2.2 remains the only allowed source leaf. The new recognizer accepts a correctly typed composite left factor and preserves the existing simple-factor behavior.

Run `run.ps1 -DryRun` first, then `run.ps1` from the unpacked repository root. The latter installs the full-function replacement and runs only the focused pytest modules. It does not run the complete suite. The installer refuses a dirty target or an unfamiliar baseline.

This change does not derive the Hopf image, add a group theorem or a GIVEN, or close the group proof. Revert the single target file with `git restore -- phase171_r2h_prop22_cited_hopf/source.py` if focused pytest fails, after examining the diff.
