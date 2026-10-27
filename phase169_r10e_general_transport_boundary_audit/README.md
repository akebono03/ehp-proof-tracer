# Phase 169 R10E0 — General transport boundary audit

This read-only audit differentiates stable-range applicability, typed group structure, prior result citation eligibility, and generic R7 expansion eligibility.

It does not modify production modules, tests, registries, or mathematical proof records. The tool writes `output/audit.json` and `output/audit.md` to its own extracted directory. Results such as `source_not_uniquely_positioned` are diagnostic, not proof certificates.

Extract the ZIP in the repository root, then run `powershell -ExecutionPolicy Bypass -File ".\phase169_r10e_general_transport_boundary_audit\run.ps1"`.

Required baseline: Phase 169 R10D2 completed with the R10B and R7 modules present. Focused tests only; no full pytest suite is run.
