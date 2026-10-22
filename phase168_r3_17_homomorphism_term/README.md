# Phase 168 R3-17 — Homomorphism Theorem Terminology Guard

This patch aligns the duplicate-paragraph guard in the existing public renderer with the established Japanese phrase `準同型定理`. No other rendering logic is changed.

Run `run.ps1` from the repository root. The script saves a backup, applies one exact replacement, emits the full affected function and unchanged import prefix into `output/`, then runs targeted tests. The full suite is intentionally not run.
