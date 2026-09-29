# Phase 144-6 R25-9B — nu-prime Definition Depth-2 Selection Repair

## Changed production files

- `toda_group_proof_narrative_semantics.py`
  - imports
  - new `build_toda_group_proof_narrative_semantic_closure_presentation()`
- `toda_group_proof_narrative_renderer.py`
  - imports
  - `render_toda_group_proof_narrative_markdown()`

## Added test

- `tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py`

## Problem

At source replay depth 2, the nu-prime bracket specialization is selected, but
its premise-0 bracket membership is at provenance depth 3.

The existing semantic rule already says that premise 0 of the bracket
specialization is a `DEFINITION_INTRODUCTION`. However, the semantic sidecar
requires both endpoints to exist in the presentation. Therefore the definition
Argument cannot be built at depth 2.

## Repair

The source replay and the standard presentation builder remain unchanged.

Immediately before Narrative rendering, a semantic-closure presentation is
built. Starting from the already selected presentation nodes, it follows only
consumer edges registered in
`_STEP_ROLE_BY_CONSUMER_RULE_NAME_AND_INDEX` and adds their missing premise
endpoints.

For pi_6^3 at source depth 2 this adds exactly one node:

- the `TodaBracketMembershipStatement` defining nu-prime.

It does not replay all depth-3 nodes.

## Invariants

- source replay `max_depth` remains 2;
- Trace is unchanged;
- Outline is unchanged;
- upstream proof graph is unchanged;
- R25-9A suppression remains active;
- no pi_5^3 or pi_6^3 special-case is introduced into semantic closure;
- the selection rule is driven by existing semantic consumer metadata.

## Completion condition

Focused tests must show:

1. source replay/presentation still stop at depth 2;
2. the semantic closure adds exactly the required bracket-membership endpoint;
3. `ESTABLISH_DEFINITION` is present;
4. depth-2 Narrative contains `nu-prime を定める`;
5. pi_5^3 remains suppressed;
6. CLI depth-2 Narrative has the same completeness;
7. existing Web mode and R25-9A focused regressions remain green.

The full suite is intentionally deferred until the Phase 144-6 completion
boundary.
