Phase 155-R4-3 — review-required lineage / current-contract consolidation

Purpose
-------
R4-2 established a canonical boundary for all current public CLI/Web modules,
but 7,992 test functions remained `review_required`.

R4-3 classifies internal current-contract coverage by actual ownership of the
current repository-root production modules.

Current production ownership
----------------------------
The audit discovers current root-level `.py` production modules, excluding
obvious audit/apply/show/test/probe scripts.

For each test function, it follows same-file helper calls and records which
current production imports are actually used.

A `review_required` test becomes:

- `canonical_internal_contract_candidate`
  when it directly or transitively uses a current production module;
- `lineage_support_candidate`
  when it uses a `tests.*` helper but has no direct current production
  ownership;
- remains `review_required`
  when neither evidence exists.

Existing R4-2 lanes are preserved:
- canonical candidate,
- public-surface canonical,
- historical compatibility,
- audit-only,
- heavy integration.

Why lineage-support is separate
-------------------------------
A test depending only on another test helper may still carry useful historical
or semantic coverage. R4-3 does not delete or demote it automatically. It is
kept as an explicit input to the next boundary decision.

Validation
----------
R4-3 requires:
- canonical candidate files collect successfully;
- review population decreases;
- historical/audit/heavy counts remain unchanged.

The output also records current root production modules with and without
detected direct/reachable test ownership.

No production code or existing test is changed.
No marker/file move/deletion is performed.
No test is executed beyond `pytest --collect-only`.
Repository-wide pytest is NOT run.

Next boundary
-------------
R4-4 will use the consolidated categories to define the concrete canonical
regression command and decide what remains outside routine regression.
