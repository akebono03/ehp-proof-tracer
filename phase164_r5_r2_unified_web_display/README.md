# Phase 164 R5-R2 — Unified Web proof display

This package routes every supported group Narrative through one shared presentation and renderer. It does not change mathematical proofs, citation selection, or narrative wording.

The proof-source selector preserves the registry-backed construction for pi_5^3 and the existing stable eta construction for pi_5^4 and pi_6^5, while returning ordinary repository replays for the remaining groups. No special Web view or alternative Narrative renderer is called.

From the repository root, extract this archive to `.` and execute `powershell -ExecutionPolicy Bypass -File .\phase164_r5_r2_unified_web_display\run.ps1`.

The script makes a backup of `web_group_proof.py`, runs focused pytest only, then inspects the 112 target pairs (2 <= n <= 15, 0 <= k <= 7). Its detailed report is written to `phase164_r5_r2_output/report.json`. A target without a proof is recorded, not represented as a successful proof. Any unexpected rendering error fails the sweep. Full pytest is intentionally deferred until the end of Phase 164.

The shared Renderer can still produce existing imperfect prose; proof-text correction and removal of now-unused modules are explicitly outside R5-R2.
