# Phase 171 Closeout R1R1 — Semantic R3Z Test Guard

This package repairs one brittle assertion in the Phase 169 R3Z regression test. The canonical proof now has 27 model steps rather than the historical count of 28; the previous count assertion fails even though the current proof reports `complete` and the cited reference/specialization assertions remain the meaningful contract.

The replacement checks that the Proof Narrative Model uses the *exact* `proven_steps` returned by search, that the completed root is an `INFERENCE` for the searched conclusion, and that no goals remain open. All existing source-citation and presentation assertions are retained.

The only production-tree change performed by this package is **none**. It modifies only `phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py` (one complete test function). No mathematical source, renderer, proof tree, reference database, or top-level documentation is modified.

## Use

Extract the archive at the repository root. Run the PowerShell entry point with `-DryRun`, then run it without the flag. The installer requires the reviewed `develop` test blob and rejects unreviewed working-tree changes. It stores the before-image and report under `%LOCALAPPDATA%\EHPProofTracerRecovery`.

On execution it runs five installer tests and the same 17-file focused regression manifest as Closeout R1. When a test fails, it restores the original test bytes. The full active `tests/` suite is **not** run; that suite remains reserved for Phase 171 final closeout.

The entire replacement test source is available at `output/test_r3z_reference_only_generic_eta_FULL.py` inside this package.
