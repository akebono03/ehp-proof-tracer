# Phase 165 R14-R2: General Typed Clauses from Toda (5.1)

## Scope

This package constructs two general typed mathematical claim schemas for (5.1) without creating verified premises. The user-provided narrative specifies the ranges `i > 1` and `n >= 1`. Original printed-text verification and proof eligibility remain pending.

## Changed files

- New production module `phase165_r14_r2_toda51.py` (repository root).
- New focused test file `phase165_r14_r2_toda51/test_phase165_r14_r2.py`.
- New read-only audit script `phase165_r14_r2_toda51/audit.py`.
- Existing production files and existing tests unchanged.

## Run

Extract ZIP at repository root and execute `powershell -ExecutionPolicy Bypass -File .\phase165_r14_r2_toda51\run.ps1`.

## Completion and boundaries

Complete when the focused pytest passes and `phase165_r14_r2_output/report.json` records two generic clauses and source matches, without `ProofStep` production or proof eligibility. This phase does **not** prove pi_3^2. Further work must certify the TeX clauses, connect verified premises and common EHP inference rules, and then generate a root ProofStep. Whole-suite pytest is deferred to the end of Phase 165.
