# Phase 166 R3-AU-12 — Public Web Proof Route Audit

Runs the real `build_group_proof_progress_view` route for (n,k)=(3,2) and records the conclusion LaTeX, narrative line count, proof status, and proven-step count. Also inspects the second `build_standard_web_group_proof_view` route statically. No changes to production files and no full test suite run.

Execute `powershell -ExecutionPolicy Bypass -File ".\phase166_r3au12_public_web_route\run.ps1"` from the repository root. Results are saved to `results/summary.json`.
