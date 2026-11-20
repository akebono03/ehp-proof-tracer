# Phase 176 R3R31R1 — Outside-Function Test Correction

Fix a single faulty test fixture that previously generated invalid Python indentation. This is a test-only correction; the existing public Hopf provider, installer, inference rule, and mathematical sources remain unchanged.

The corrected fixture places the insertion anchor inside a *different* syntactically valid Python function. The production guard must reject it with `ANCHOR_OUTSIDE_SHARED_PROVIDER`.

Extract this archive at the repository root on `develop`. Run `run.ps1 -DryRun` followed by `run.ps1`. The script applies the guarded change and executes only focused pytest tests.
