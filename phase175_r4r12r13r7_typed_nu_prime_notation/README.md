# Phase 175 R4R12R13R7 — Typed nu-prime notation bridge

This patch identifies strictly equivalent encodings of the same *typed* nu-prime generator: the documented LaTeX/Unicode prime spelling and a one-fold suspension encoded as either `Suspension` or `IteratedSuspension(..., 1)`. It does not introduce a new mathematical theorem, GIVEN, or target conclusion.

The only production edit is to the coordinate matcher of the existing isolated R13R2 Delta injectivity inference. Every original source formula and group relation remains a separate, independently verified backward goal.

Run `run.ps1 -DryRun`, followed by `run.ps1`. The report requires one public Delta candidate after installation, but explicitly does not claim that the overall proof is complete. `output/rule_FULL.py` provides the complete patched source file. No full pytest suite is run.
