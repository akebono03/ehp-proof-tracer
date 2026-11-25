# Phase 176 R3R50 — Strict typed nu-prime notation connection

This package connects the original R3R41 proof plan to the actual DB-spelled Hopf equality. The original exact plan always has priority. The fallback requires a strictly typed alias of Toda's nu-prime, a unique screened Hopf witness, and a separately inferred canonical equality. It adds one checked notation-transport inference, no mathematical theorem, and no GIVEN. The database, registry, global expression equality, and finite cyclic lift remain unchanged.

The installer replaces three reviewed files only, using exact Git blob hashes of the LF forms and preserving LF/CRLF. Complete replacement source files are in `replacements/` (text suffix to avoid accidental module loading). R3R49 was reviewed from its original distributed ZIP, because its files were not in the verified GitHub HEAD. Its audit pin and historical regression test are updated to reflect the new planner. Other prior phases are unchanged.

From the repository root, run `run.ps1 -DryRun`, then `run.ps1`. The script runs six focused pytest files in separate canonical import processes and audits the actual Web proof search. It never runs the full suite. It requires the exact installed R3R48 and R3R49 packages. On an unreviewed local file, it fails closed without replacing any of the three files.

The gate is `PASS_R3R50_ACTUAL_WEB_HOPF_NOTATION_CONNECTED`. A partial group result is expected: the finite cyclic lift's DB prior guard is outside the scope. No completion is claimed in advance. The report is written outside the repository under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r50_strict_nu_prime_connection/report.json`.
