# Phase 165 R56 — Common Narrative Connection

This package routes completed typed proof searches through the existing whole-proof Toda presentation and narrative renderer. Incomplete searches retain the existing partial view. The n,k-only workflow from R55 is preserved, and the misleading legacy query failure is suppressed when a typed proof was completed.

Run `run.ps1` from an extracted package in the repository root. The installer checks the expected code shape, creates backups, writes full replacement functions and imports to `CHANGED_CODE.md`, and runs focused pytest only. It does not run the full suite.

This patch does not certify unverified references, create new inference rules, or add special pi3^2 rendering rules. Direct sums are explicitly rejected for complete presentation until their typed generator decomposition is supported.
