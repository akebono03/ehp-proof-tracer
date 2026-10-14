# Phase 165 R52-R27-R4 — Toda Reference Registry Audit

This read-only package examines the live production Registry, adopted typed Toda source, and their merged shared bridge for Proposition 4.4 and equation (5.2).

It distinguishes bibliographic entry registration, typed assertions, qualifying fixed `GIVEN` ProofStep links, and unverified theorem specialization. It does not change application code, authorize unsupported `GIVEN` steps, or run the full test suite.

Run the included `run.ps1` in PowerShell after extracting to the repository root. Inspect `audit_output/registry_audit.json` and `audit_output/review.md`.
