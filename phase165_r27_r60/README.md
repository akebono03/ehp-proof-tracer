# Phase 165 R27-R60 Regression Verification

This package validates the typed public group-search route after the R59 retirement. It does not modify application source or execute the full test suite.

Run `run.ps1` from PowerShell after extracting the archive at the repository root. It runs focused checker tests and then examines public entry imports and the representative groups pi_3^2, pi_4^3, and pi_5^3.

The JSON file `phase165_r27_r60_results.json` records the observed status, count of proven steps, unresolved goals, and execution errors. An observed `complete` status is not, by itself, independent mathematical certification. The checker never infers successful proofs from a known group structure.

A failing static gate stops the representative probes; no source files are changed. Full pytest is reserved for the phase closure.
