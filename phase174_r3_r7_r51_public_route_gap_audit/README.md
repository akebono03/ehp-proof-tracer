# Phase 174 R3-R7-R51 — Public Route Gap Audit

Read-only comparison of the actual `search_group_from_registered_goal` and `build_standard_web_group_proof_view` with the fully certified R50 scoped backward search. The audit identifies whether the public R35 cyclic-kernel rule still receives a direct source relation instead of a source-bound inferred relation. It never registers a derived group claim, injects steps, changes the model renderer, or modifies production files.

Run from repository root: `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r51_public_route_gap_audit\run.ps1 -DryRun`, then the same command without `-DryRun`.

Outputs are saved under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r51\`. Only focused pytest runs. A passing audit is **not** a successful Web proof or HTTP test: the next phase must connect a generic, source-checked inference route and verify the common model trust boundary.
