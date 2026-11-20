# Phase 176 R3R30 — Generic Hopf Right-Substitution (Isolated)

This incremental package introduces a **general, typed and source-dependent** Hopf-value substitution inference, isolated from public proof-search registration.

The rule requires two independently proved subgoals: a cited specialization of Toda Proposition 2.2 and a verified Hopf image of the left composition factor. It never registers a desired image or target group as a GIVEN.

The package changes no existing modules, public provider, API, or root proof.

## Run

Extract in the repository root on the `develop` branch. Run `run.ps1 -DryRun` and then `run.ps1` using Windows PowerShell.

The report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r30_generic_hopf_substitution_isolated\report.json`. Only focused pytest tests run.
