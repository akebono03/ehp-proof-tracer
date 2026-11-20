# EHP Proof Tracer — Phase 176 R3R3

This is a read-only audit of a pre-existing **general** finite-cyclic Hopf lift rule versus the specific need to derive a finite cyclic group from a proper order-two Hopf image inside an order-eight codomain.

Extract the ZIP at the repository root on the `develop` branch. Run `run.ps1 -DryRun`, then `run.ps1`. The script performs focused pytest only and writes its JSON report outside the repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r3_finite_hopf_image_subgroup_design\report.json`.

No existing production code, test or documentation is patched. No source assertion, rule, proof or database group is created or trusted by this package. A hypothetical Hopf image is only a typed observation, not mathematical evidence. Full-suite pytest is not run; known historical source-guard failures are not altered.

`AUDIT_PLAN_JA.md` explains the mathematical boundary and `CODE_FULL_JA.md` contains the complete newly added code.
