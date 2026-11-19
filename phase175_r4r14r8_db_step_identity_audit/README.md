# Phase 175 R4R14R8 — Adopted DB ProofStep identity audit

This read-only audit diagnoses why the existing R41 inference does not match the real ProofStep for a prior database group. It reports exact field differences against the canonical admitted database step, and runs focused tests. It does not change source code, admit new GIVEN statements, relax citation verification, or assert that the target proof is complete.

Requirements: the prior R4R14R5 and R4R14R6 production connections; the Phase 175 R4R14R7 audit package.

Usage: `run.ps1 -DryRun` followed by `run.ps1`. The JSON report is written into `%TEMP%`.
