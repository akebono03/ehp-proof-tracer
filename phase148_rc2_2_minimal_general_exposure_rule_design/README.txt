Phase 148 RC2-2 — Minimal General Exposure Rule Design

This package is design-only.

Files
-----
- rc2_2_design.md
  Full Japanese design for the general recursive exactness exposure rule.
- audit_phase148_rc2_2.py
  Checks that the required design boundaries are present.
- run_phase148_rc2_2.ps1
  Runs syntax preflight, design audit, and existing focused boundary tests.

Production changes
------------------
None.

Existing repository test changes
--------------------------------
None.

Main design decision
--------------------
Narrative exposure is decided from existing semantic ownership/relevance,
not from `primary_component is None` alone.

Owned primary exactness keeps the current higher-level contribution behavior.
Unowned recursive exactness remains in provenance but is not automatically
expanded in the Argument body.
Ambiguous directly relevant cases use a conservative fallback.

Run
---
From repository root:

powershell -ExecutionPolicy Bypass `
  -File ".\phase148_rc2_2_minimal_general_exposure_rule_design\run_phase148_rc2_2.ps1"

No repository-wide pytest is run in RC2-2.
RC3 Narrative ordering remains out of scope.
