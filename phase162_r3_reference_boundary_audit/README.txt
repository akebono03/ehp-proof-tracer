Phase 162 R3 — Reference Boundary Audit (audit only)

Run from the repository root after applying the Phase 162 R2 fallback repair:
  powershell -ExecutionPolicy Bypass -File .\phase162_r3_reference_boundary_audit\run_phase162_r3_audit.ps1

This produces a per-ProofStep inventory, based on the existing literature
statement boundary classifier, with actual reference locator (if present),
fixed-vs-proof-internal classification, and premise indices. It also prints
the current unmodified R2 proof body for comparison.

FIXED_STATEMENT is only a candidate for the Reference section. UNTRACKED
and PROOF_INTERNAL are never silently promoted to literature general forms.
No application-specific prose or fabricated general theorem is generated.
This package does not modify production code or tests, and does not run pytest.
The audit result should be reviewed before implementing an R3 Reference renderer.
