# Phase 165 R57-R17: Read-only Proof Search Audit

This package inspects the installed proof-search implementation without modifying project source files. It records the runtime path for pi_3^2, pi_4^3 and pi_5^4, including typed goal candidates, reviewed order records, completed predecessors, screened references, initial inference expansions, proven steps, and unresolved goals.

Run `run.ps1` from PowerShell. It executes only the four targeted diagnostic tests, then the live audit. It does not run the full test suite. The results are written to `audit_results.json` and `audit_results.txt` in this directory.

The audit does not generate a proof, certify mathematics, add a reference, or modify the repository. Instrumentation is temporary and process-local. The program may return a nonzero exit code if the installed project is missing required modules or an audit query raises an exception; inspect `audit_results.json` in that case.
