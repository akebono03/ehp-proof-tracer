Phase 148 RC2-1 — Recursive Exactness Evidence Exposure Audit

Purpose
-------
Audit the current exactness-evidence exposure behavior before defining any
new production policy.

This package does NOT change production code or existing tests.

Audit target
------------
The audit starts from pi_6^3 and also records the same evidence/component
shape for:

- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

Diagnostic classification
-------------------------
Each exactness component is reported as one of:

- PRIMARY_METHOD
- DIRECT_SUPPORT_CANDIDATE
- RECURSIVE_PROVENANCE_CANDIDATE

These labels are audit labels only. They are NOT the RC2 production rule.

Important boundary
------------------
RC2-1 does not decide which recursive evidence should be hidden.
RC2-2 will design that general rule.

RC3 is responsible for proof-ordering problems such as a short exact
sequence appearing after the conclusion. RC2-1 does not change ordering.

Run
---
From the repository root:

powershell -ExecutionPolicy Bypass `
  -File ".\phase148_rc2_1_recursive_exactness_exposure_audit\run_phase148_rc2_1.ps1"

Expected result
---------------
1. Syntax preflight passes.
2. Focused existing/boundary tests pass.
3. rc2_1_output.txt is generated.
4. Production code remains unchanged.
5. Repository-wide pytest is NOT run in RC2-1.
