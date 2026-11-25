# Phase 176 R3R56R2 — Namespace source fix

Restore the historical source-bound presentation by accepting the shared registry's matching numbered assertion/reference namespace. Preserve the existing direct-ID and Proposition 2.2 provenance paths and all typed GIVEN, citation membership, and ambiguity guards. No proof, source registration or old test is changed.

The only production replacement is `_source_citation` in `phase175_r3r11_cited_hopf_narrative/projection.py`. Both complete function versions are supplied as text. The patch verifies the exact inverse Git blob and is idempotent for LF and CRLF. Existing top-level imports are unchanged (`re` is already imported). The earlier R56/R56R1 audit preflight pins the old source file; only its verified pin is rebound in memory for this preflight. Historical files are not modified.

Run `run.ps1 -DryRun`, then `run.ps1` from the repository on `develop`. The R55R1 connection and R56/R56R1 packages must already be present. The focused tests include the original eight Phase 175 tests unchanged. A public complete-proof and partial-prefix comparison follows, then R56's isolated observation is repeated. R56 is not publicly connected in this package. Full pytest is not run. A failing test stops the script; the applied patch is retained for diagnosis.

Expected final gate: `PASS_R3R56R2_NAMESPACE_SOURCE_FIX_AND_R56_RECHECK`.
