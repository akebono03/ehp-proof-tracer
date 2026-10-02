Phase 155 Closure-R2C-R1 — CONTRACT_SENSITIVE static review

Purpose
-------
Review the 24 CONTRACT_SENSITIVE failures without executing them.

Inputs
------
- phase155_closure_r2_output/contract_sensitive_nodeids.txt
- phase155_closure_output/phase155_full_pytest.log
- current local test source

The three known extreme tests (508.30s, 281.49s, 276.88s) are never executed.

Recommendations
---------------
LIGHTWEIGHT_REPLACE
  The contract is small (provenance/order/identity) but the fixture is large.

AUDIT_ONLY
  Cross-group population audit; retain separately from routine regression.

KEEP_ROUTINE_CANDIDATE
  Focused contract with no static evidence yet for removal.

R2C-R1 changes no repository files and runs no repository test bodies.
