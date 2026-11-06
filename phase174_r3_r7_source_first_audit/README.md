# Phase 174 R3-R7: Source-First Frontier Audit

This package performs a **read-only implementation preflight** against the reviewed `develop` branch of `akebono03/ehp-proof-tracer`.

It verifies the current remote HEAD, reviews the local worktree without cleaning it, validates source transcriptions and their Git blob hashes, records the historical Phase 173 `n=4` frontier, and (on normal execution) inspects seven selected production searches and source-screened backward expansion proposals.

A proposal is not a verified proof. The audit does not add new group GIVENs, inference rules, proof steps, renderers, or documentation updates. It does not run the full test suite.

Run `run.ps1 -DryRun` before `run.ps1`. The full report is written outside the repository, at `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7\audit.json`. The report contains detailed source-screened root and open-goal proposals, along with any errors. If `develop` advances, the program intentionally refuses to certify an unreviewed revision.

The live inspection samples the existing `π₈⁵` baseline, the previously unresolved `π₁₂⁴` and `π₁₃⁴` goals, and the Toda (5.6) dependency groups. This is **not** an exhaustive current-status audit of every registered group, and the sample does not preselect any implementation target.
