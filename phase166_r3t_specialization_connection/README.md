# Phase 166 R3-T: Existing Specialization Connection

This package checks that the current generic typed scalar specialization can generate the concrete Toda (4.5) suspension-isomorphism proposition from its registered general statement, without promoting the specialized statement to a literature GIVEN.

The package is read-only: it does not patch production code. It deliberately distinguishes the concrete isomorphism from a complete finite-cyclic transport proof; the latter still needs a proven source group and a generator-suspension identification.

## Files
- `audit.py`: complete `inspect()` and `main()` functions
- `test_audit.py`: three focused tests with complete imports
- `run.ps1`: runs focused tests and writes JSON report

## Run
Expand the ZIP into the repository root, then execute:

`powershell -ExecutionPolicy Bypass -File .\phase166_r3t_specialization_connection\run.ps1`

## Pass criteria and boundary
A non-GIVEN concrete isomorphism is supported by the existing common specialization rule. The tests do **not** claim pi_5^4 is COMPLETE; subsequent work must link the proven pi_4^3 source and an independently proven generator identity. No full pytest suite is run.
