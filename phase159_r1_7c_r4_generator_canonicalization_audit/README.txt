Phase 159 R1-7c R4 generator canonicalization audit

Purpose
-------
This package performs an audit only. It does not modify production code.

Target
------
Investigate why the public display can expose

  pi_7^5 = Z/2{eta_5 eta_6}

instead of the canonical notation

  pi_7^5 = Z/2{eta_5^2}.

Audit boundary
--------------
The audit compares four layers:

1. Proposition 5.3 semantic data
2. generic Narrative expression rendering
3. raw group-structure rendering
4. public pi_6^3 Narrative

Important distinction
---------------------
The calculation

  eta_5 eta_6 = eta_5^2

may legitimately need both sides, so this audit does NOT propose a global
string replacement of eta_5 eta_6.

Expected diagnosis
------------------
Current GitHub inspection shows:

- Proposition 5.3 stores the generator structurally as a Composition of
  eta_n and eta_(n+1).
- The generic Narrative renderer already has a general canonicalization rule
  that renders consecutive eta compositions as eta_n^k.
- Therefore the likely defect is a renderer-route mismatch: some
  group-structure/public route bypasses that canonicalization.

Execution
---------
From the repository root in PowerShell:

  Remove-Item `
    ".\phase159_r1_7c_r4_generator_canonicalization_audit" `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

  Expand-Archive `
    -Path "$HOME\Downloads\phase159_r1_7c_r4_generator_canonicalization_audit.zip" `
    -DestinationPath "." `
    -Force

  powershell `
    -ExecutionPolicy Bypass `
    -File ".\phase159_r1_7c_r4_generator_canonicalization_audit\run_phase159_r1_7c_r4_generator_canonicalization_audit.ps1"

Tests
-----
Only focused existing tests are run:

- tests/test_phase143_3_generic_eta_normalization.py
- tests/test_phase59_prop53_integration.py

The full pytest suite is intentionally NOT run in this audit.
