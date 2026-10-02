Phase 155-R4-1 — canonical regression set evidence audit

Purpose
-------
R3 removed or resolved duplicate/superseded test coverage.
R4 now defines a smaller, explicit routine regression boundary.

R4-1 does NOT finalize that boundary. It performs evidence classification only.

Evidence used
-------------
1. Tests explicitly named by the Phase 153 and Phase 154 closure focused
   regression scripts.
2. Core `tests/test_*.py` files whose names do not depend on a numbered Phase.
3. R3 `historical_keep` decisions.
4. Static filename signals for audit/inventory/snapshot/closure tests.
5. Static filename signals for all-group/full-depth/cross-group/heavy-style
   tests.
6. Recent Phase >=149 tests as lower-confidence current-contract candidates.

Categories
----------
- `canonical_candidate`
- `historical_compatibility`
- `audit_only_candidate`
- `performance_heavy_integration_candidate`
- `review_required`

Important precedence
--------------------
`historical_keep` takes precedence over canonical/focused evidence because
historical compatibility is intentionally a separate lane.

R4-1 is conservative:
- no production change;
- no existing-test change;
- no deletion;
- no marker insertion;
- no file move;
- no repository-wide pytest.

It performs pytest `--collect-only` for canonical candidate files to prove the
candidate collection boundary is syntactically/import-wise viable.

Next boundary
-------------
R4-2 will inspect `review_required` and category overlaps, validate whether the
candidate set actually covers the current public surfaces, and only then decide
whether a concrete canonical command/marker boundary should be introduced.
