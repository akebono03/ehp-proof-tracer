# Phase 166 R2 — Three Group Correspondence Audit

This package checks candidate mappings from the existing sphere and generator CSV data to individual Toda literature statement component identifiers for pi_3^2, pi_4^3, and pi_5^3. It uses the live production registry and leaves all production files untouched.

## Usage

Unzip the package at the project root, then run `powershell -ExecutionPolicy Bypass -File .\phase166_r2_three_groups\run.ps1`.

The supplied CSV files are fallback audit inputs. Existing files at the project root or in `data/` take precedence. Output is saved under `phase166_r2_three_groups/results/summary.json`.

## Boundary

Candidate component identity is not mathematical identity. No group structure or generator theorem is proved. No ProofStep, proof link, or citation permission is created. Only four focused tests run; no full pytest is executed.
