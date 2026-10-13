# Phase 165 R50 — Adopted source reference boundary

This package updates only the fixed-reference boundary filter to recognize a premise-free `ProofRule.GIVEN` step with a matching explicit literature reference as an adopted source assertion. It does not elevate derived inference steps, alter the source registry, or modify the proof-body reason ordering introduced in R49. The original references module is backed up before editing.

Run `run.ps1` from the extracted package in the repository root. It runs only two targeted tests; it does not run the full test suite. A failed test is not an indication of success. This patch is a first validation of the entry filter and the final Web output; further downstream filtering may require separate investigation if the Web test fails.
