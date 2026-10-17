# Phase 165 R6-2 R4-R10 Candidate-to-ProofStep Trace

A read-only diagnostic for the canonical proof search of `pi_4^3`.

Run `run.ps1` from the repository root after extracting this package. The script runs only focused package tests and emits `audit_output/candidate_trace.json` and `audit_output/candidate_trace.md`. It never runs the full test suite or edits production files.

The diagnostic evaluates complete and individual root branches against both full and screened reference contexts. Branch isolation is for diagnosis only, not a production proof-selection policy.
