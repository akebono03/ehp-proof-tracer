# Original Completed Narrative Restoration

Restore the completed-proof narrative route that was replaced in Phase 165 R57-R21. The patch uses the repository's saved pre-switch completed presentation adapter. Completed proofs again pass through the established Toda proof replay, presentation, and narrative renderer. Incomplete proofs continue using the partial-proof renderer. Search, inference, and provenance data are not changed.

Extract the ZIP at the project root and run `phase165_r57_r21_original_narrative_restore/run.ps1`. This backs up the two modified files and runs five targeted pytest cases. Full pytest is not run.

The installer rejects unexpected source versions instead of overwriting them. The original adapter's support boundaries remain unchanged.
