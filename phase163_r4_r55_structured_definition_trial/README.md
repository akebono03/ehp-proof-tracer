# Phase 163 R4-R55: Source-Grounded Definition Trial

A read-only, isolated experiment that creates three temporary references and typed definition assertions using Toda TeX equations (2.9), (2.10), and (4.3). The records contain source-grounded TeX and surrounding prose as context. They are not formal parsed mathematical statements and do not establish equivalence, bibliographic original verification, or proof availability.

From the project root, extract the ZIP, then execute `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r55_structured_definition_trial\run.ps1`.

Inputs: `phase163_r4_r47_output/catalog.json`, `phase163_r4_r53_output/overlap_audit.json`, and existing `unified_statement_registry.py`. Outputs: `phase163_r4_r55_output/trial.json`, `trial.csv`, and `report.md`.

No production source files, existing identifiers, TeX documents, or proof-search behavior are modified. Only the nine targeted tests are run; the full suite is reserved for the end of Phase 163.
