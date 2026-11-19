# Phase 175 R4R14R7 — Zero-image proof frontier audit

This is a **read-only** diagnostic package for the missing `ImageZeroStatement` during the attempted proof of the zero group at `(n, k) = (6, 4)`.

The audit compares actual, canonical Proof Search steps with the existing R41 inference premise contract. It distinguishes a proven adopted database premise from a hypothetical reconstructed one. It does not insert missing proof steps, patch production code, run full pytest, or claim the target complete.

Run `run.ps1 -DryRun`, then `run.ps1` from the extracted directory. Results are written to `%TEMP%\EHP_Phase175_R4R14R7_image_zero_match.json`.

Existing `develop` and the R4R14R5/R4R14R6 connected implementations are prerequisites.
