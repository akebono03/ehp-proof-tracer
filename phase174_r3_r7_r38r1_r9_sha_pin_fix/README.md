# Phase 174 R3-R7 R38R1 — R9 Git Blob SHA Pin Correction

The previous R38 installer's Git blob SHA for `phase174_r3_r7_r9_composition_associativity/rule.py` has only 39 hexadecimal characters. The reviewed GitHub blob is 40 characters and ends with `e`.

R38R1 corrects **only that single-character pin**, preserving the exact original source verification logic, mathematical rules, production providers, database contents, and narrative renderer. The ZIP includes a guarded idempotent installer, a read-only in-memory DryRun, full replacement source, complete changed top-level assignment, and focused tests. Regular execution automatically delegates to the previously supplied R38 `run.ps1` with its existing focused suites.

No Git reset, checkout, pull, or mathematical GIVEN insertion is performed. The full pytest suite remains deferred until the end of the phase.
