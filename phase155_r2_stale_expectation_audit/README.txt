Phase 155-R2 — stale expectation audit

Purpose
-------
Use the Phase 155-R1 inventory and statically inspect assertion expectations that may no longer match the current Phase 154 public Narrative contract.

Boundary
--------
- No production-code changes.
- No existing-test rewrites or deletions.
- No repository-wide pytest run.
- No automatic claim that a candidate is stale merely because its Phase number is old.

Current contracts checked
-------------------------
1. Public Japanese Narrative prose uses ASCII comma-space and ASCII period.
2. Internal Statement/type fallback names must not leak into public prose.
3. Duplicate final-result reason prose is suppressed.
4. Pre-Phase-153 positive Reference expectations are reviewed against used-reference filtering, root exclusion, and granularity rules.
5. Fixed numeric audit/snapshot expectations are marked contract-sensitive, not automatically stale.

Outputs
-------
phase155_r2_audit_output/
  phase155_r2_expectation_findings.csv
  phase155_r2_file_summary.csv
  phase155_r2_summary.md
  phase155_r2_metadata.json

Interpretation
--------------
stale_candidate_high:
  Direct conflict with a current Phase 154 presentation contract. Inspect first.

stale_candidate_medium:
  Older positive Reference expectation that may predate Phase 153 Reference rules. Manual confirmation required.

contract_sensitive_review:
  Fixed numeric audit/count/snapshot expectation. Fragile, but not automatically stale.

current_compatible:
  Negative assertion that explicitly enforces a current contract. Preserve as evidence unless later shown redundant.
