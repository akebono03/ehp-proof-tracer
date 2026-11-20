# Phase 176 R3R4 — Read-Only Zero Image and Hopf Lift Frontier Audit

This package audits the unresolved n=3, k=5 proof frontier without altering tracked production files or certifying any new mathematical fact.

It checks the reviewed GitHub `develop` lineage, inspected source contracts, actual registered proof-search status, the typed suspension-zero-image goal required for Hopf injectivity, the existing isolated finite-cyclic generator zero-image rule, and the shared provider's actual proposed subgoals. It records whether a cited Lemma 5.7 zero-generator step directly matches or still needs composition transport.

The historical four Phase 174 source-guard failures remain unresolved; this package neither masks nor modifies them. No full suite is run.

Extract the archive into the repository root. Run `run.ps1 -DryRun`, then `run.ps1`. Both write a JSON report outside the repository, under `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r4_zero_image_and_hopf_lift_frontier\report.json`. The full run executes only the six focused tests.

The archive contains `CODE_FULL_JA.md` with complete source and test function bodies, `AUDIT_PLAN_JA.md` with the audited mathematical boundary, and the complete runner.
