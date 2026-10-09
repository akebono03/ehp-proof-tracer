# Phase 162 R4-B3 — Common Renderer Audit

This package compares output from the existing root and the independently derived stable-transport root using the **same common baseline renderer**. The public stable renderer is not invoked, and production files are not modified.

Run the included PowerShell script from the EHP Proof Tracer repository root. It installs a read-only audit script and focused tests, runs only targeted pytest tests, then produces `phase162_r4_b3_common_renderer_audit/audit_output/comparison.md` and `audit.json`.

The baseline renderer may still include the previous Phase 162 R4-B appendage. The audit explicitly flags that appendage; it does not claim the resulting prose is fully ProofStep-driven. A rendering exception is recorded as an audit failure observation rather than suppressed without evidence.

No public route, source repository entry, proof-search rule, or production renderer is changed.
