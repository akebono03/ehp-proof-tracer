# Phase 170 R1 — Read-only capability audit

This standalone package inspects the **production** typed Backward Search, Proof Tree, screened Narrative Model, references and Trust Boundary. It records exact database-row availability separately from the evidence **actually cited** by a proof. It does not change application code, existing tests, source data, Git index, or worktree tracked files.

Reviewed GitHub `develop` HEAD: `790db364a8531693572fc510f969da831f1f9ffb`. The earlier handoff HEAD `83b1400d55890cea7b8ab44579c11e11f8dd8e69` is also accepted because the two additional commits add only audit-package files. Each critical production file is checked against a reviewed Git blob hash. Any unknown branch, HEAD, or modified critical source is refused.

Run `run.ps1` from the extracted package at repository root. Default scope audits 2-stem groups plus a **non-exhaustive** selection of other stems. Use `-Scope core` for just the three 2-stem groups. Focused regressions run by default, and the repository-wide pytest suite is intentionally not executed.

Reports are written into a new unique subdirectory of `%LOCALAPPDATA%\EHPProofTracerRecovery`, never into tracked project paths. The main outputs are `audit.json`, `audit.md`, and per-group `*_trace.json` and `*_narrative.md`. `PARTIAL`, missing contexts, missing registered goals, and verifier errors are reported, never treated as successes.

This is an evidence-gathering audit, not a proof of correctness for all groups or all source assertions. A missing DB citation does not alone prove that the database information is mathematically inapplicable. Detailed DB usability analysis belongs to Phase 170 R2.
