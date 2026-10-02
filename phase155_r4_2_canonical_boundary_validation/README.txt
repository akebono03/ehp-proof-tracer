Phase 155-R4-2 — canonical boundary validation

Purpose
-------
R4-1 found 1,620 initial canonical candidates but left 8,199 test functions
as `review_required`.

GitHub inspection showed that many older Phase tests still directly verify
current public CLI/Web modules. Phase number alone is therefore not a valid
reason to exclude them from the canonical lane.

R4-2 validates the canonical boundary against the current public modules:

- `main`
- `web_app`
- `web_group_query`
- `web_group_proof`
- `web_operation_query`
- `web_operation_query_proof`
- `web_generator_proof`
- `web_generator_exploration`
- `web_generator_proof_scope`
- `web_generator_applicability`
- `web_generator_execution`

Function-level evidence
-----------------------
A test is promoted from `review_required` only when its own function body, or
a same-file helper reachable from that function, actually uses an imported
current public module symbol.

This avoids promoting every test merely because its file contains an unused
public import.

Precedence
----------
The R4-1 lanes remain authoritative in this order:

- `historical_compatibility`
- `audit_only_candidate`
- `performance_heavy_integration_candidate`
- existing `canonical_candidate`

Only `review_required` can become
`canonical_public_surface_candidate` in R4-2.

Validation
----------
R4-2 requires:

1. every current public module has at least one canonical direct/reachable
   test;
2. proposed canonical files collect successfully;
3. historical/audit/heavy lane counts are unchanged;
4. review population does not increase.

No production code, existing test, marker, or file layout is changed.
No test is executed beyond `pytest --collect-only`.
Repository-wide pytest is NOT run.

Next boundary
-------------
R4-3 will address the still-unclassified internal/current-contract test
population using Phase lineage and semantic ownership. R4-2 does not claim
remaining `review_required` tests are removable.
