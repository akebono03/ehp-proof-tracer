# Phase 163 R4-R80: Fixed-Statement Registration Preflight

This package conservatively checks eight fixed-statement proposal fragments from four Toda references for source integrity, statement-component order, inherited scope, and unresolved semantic boundaries.

Unzip into the EHP Proof Tracer repository root, keeping the package folder intact, and run `run.ps1` with PowerShell. Requires the R79 output at `phase163_r4_r79_output/fixed_statement_preview.json` and original extracted TeX sources under `phase163_r4_r42_tex_extract/inputs/`.

It produces `phase163_r4_r80_output/registration_preflight.json` and `report.md`. It never modifies production source, allocates permanent IDs, or runs the full test suite.
