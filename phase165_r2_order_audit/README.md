# Phase 165 R2 — Narrative Order Audit

Read-only inspection of the existing complete-proof path for pi3_2 and pi4_3.

From the repository root, unpack the ZIP and run `phase165_r2_order_audit/run.ps1` using PowerShell.

The audit writes public Markdown, ordered ProofStep metadata, and a JSON report into `phase165_r2_order_audit_results/`. It does not modify production Python files, introduce a renderer or adapter, or run the full pytest suite. Review these outputs before attempting an ordering fix.
