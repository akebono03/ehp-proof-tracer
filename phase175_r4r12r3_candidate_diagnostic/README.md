# Phase 175 R4R12R3 — Read-only Root Candidate Diagnostic

This package reads the existing R4R12 provider, R4R3 typed quotient rule and database-prior group statements. It does not modify production code, admit a new GIVEN, infer a mathematical conclusion, or run the whole test suite.

Unzip into the repository root on the reviewed `develop` HEAD. Execute `run.ps1 -DryRun` and then `run.ps1`. Both are intentionally read-only. The audit writes a JSON report under the user's local application-data folder. Share the console output and the `candidate` section of the JSON report to determine whether a typed-generator mismatch, an exactness index, or an R4R12 provider construction problem prevented candidate creation.
