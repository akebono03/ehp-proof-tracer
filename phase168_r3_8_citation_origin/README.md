# Phase 168 R3-8 — Citation Origin Audit

Read-only provenance diagnosis for the two expected literature sources of both pi_3^2 and pi_4^3: (5.1) and Proposition 5.1.

The model currently distinguishes complete `LiteratureReference` values. This audit diagnoses repeated locators without merging them or dropping any other citation. It prints the exact proof-step indices and inference-rule names behind unexpected entries. It does not change any existing Search, Renderer, or Web production module.

Run in the repository root using `powershell -ExecutionPolicy Bypass -File .\phase168_r3_8_citation_origin\run.ps1`.

Four targeted tests run, followed by the two actual searches. Full pytest is deferred to the end of Phase 168.
