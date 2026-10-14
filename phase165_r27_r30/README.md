# Phase 165 R27-R30 — Bulk legacy bootstrap cleanup

This installer retires two historical Phase 163 proof-builder extraction helpers and removes unreferenced or mutually isolated root-level `toda_*bootstrap.py` modules in one dependency-guarded batch. It does not remove the typed registry, general inference rules or shared backward search.

The dependency analysis uses the AST of all root-level Python modules, including imports inside functions, and preserves any bootstrap referenced by a noncandidate module and its transitive bootstrap dependencies. The historically important `toda_upstream_bootstrap.py` must be eligible for deletion; otherwise the installer aborts before modifying files. Backups are kept under `phase165_r27_r30_removed_backup`, and the audit is written to `phase165_r27_r30_audit.json`.

The legacy historical extraction functions `existing_stable_minimal_registration` and `existing_phase163_r4_r13_inventory` now raise an explicit retirement error. Their respective typed registration and inventory model APIs are otherwise left intact. Historical tests relying on those old extractors may need migration.

Unchanged modules outside the bootstrap family are not removed, including the many old Repository-dependent modules that still have live imports. This batch is not a full retirement of every old Repository API.

Run `run.ps1` from its extracted folder. Only the R27-R30 targeted tests are executed; the full suite is reserved for the end of Phase 165.
