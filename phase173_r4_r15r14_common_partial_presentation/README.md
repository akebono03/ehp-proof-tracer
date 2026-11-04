# R15R14 — Common Partial Proof Presentation

This is a source-guarded, minimal Web presentation correction for the existing single Narrative Model route. It provides typed cyclic-goal mathematical rendering and hides Python object representations from public search diagnostics. It does **not** change any proof inference, status, citation, reference, or open-goal data.

Use `run.ps1 -DryRun` before `run.ps1`. The runner fetches `origin/develop`, checks that both local and remote branches point to reviewed commit `9729d3ee51e93f26cf6b31a3880cb1a92a552f2c`, and checks reviewed Git blobs and a clean tracked tree. It fails closed on unreviewed differences.

A successful install modifies only `web_group_proof_common.py` and `phase173_r4_r15r13_unified_presentation/layout.py`. Backups reside under `backups/`. The focused pytest suite does not run the full test suite. Failure attempts an automatic rollback.

Expected checks: cyclic goals for real `k=8,15`, public diagnostics redaction, exact proof statuses, unchanged abstract evidence, regression for a completed group and existing R15R13/R15R12/R15R11 tests.

See `design.md` for the boundary and `FULL_CHANGED_UNITS.md` for complete modified function bodies and imports. `SOURCE_CODE.md` contains complete implementation and test sources.
