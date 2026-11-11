# EHP Proof Tracer — Phase 174 R60R1

This corrective package updates only the previously reviewed Git HEAD constant in the extracted R60 read-only Reference ownership audit. The current `develop` commit is `17b96a63c1ee400d587c14c785c4c1e697334206` (confirmed through GitHub). The original R60 script used `82d725d8649cd6307c2abd67024e3ef4f3cddfe2`; R59's audit and cache commits advanced the head without modifying R60's six pinned dependencies.

The installer requires the exact original R60 `audit.py` hash, validates the six existing R60 source blob pins and the current Git commit, patches exactly one module-level constant, and refuses any unexpected source changes. It never changes the Proof Search, Reference model, common Renderer, any GIVEN, or any inference rule.

Extract `R60R1.zip` into the repository **after** `R60.zip` has been extracted. Run `phase174_r3_r7_r60r1_reviewed_head_lineage_fix/run.ps1 -DryRun`, followed by the same script without `-DryRun`. The latter applies the checked one-line correction, runs the original R60 DryRun and full focused R60 audit, plus installer tests. All pytest invocations disable the cache provider; no full test suite is run.

If Git HEAD changes again, do not force this patch or edit the guard blindly. Re-review the new commit and the six source pins before issuing another lineage correction.
