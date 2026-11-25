# Phase 176 R3R56R1 — Historical source display audit

This read-only diagnostic reproduces the two historical Phase 175 assertions on the same verified model using the pinned pre-R55 renderer and the connected renderer. It then temporarily tests a matching namespace pair in memory. The historical tests and production modules on disk are unchanged. The old renderer comparison removes only the R55 insertion, not other historical changes or the current proof search. The namespace experiment is not a public fix. If the two failures do not reproduce on both renderers, execution stops; otherwise the separate R56 isolated audit may proceed. A successful diagnostic does not mark the historical pytest suite or Phase 176 complete.

Run `run.ps1 -DryRun` and then `run.ps1` from the repository. Outputs are under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r56r1_historical_source_audit`. The report records all three assertion outcomes and actual citation IDs. No full pytest is run.
