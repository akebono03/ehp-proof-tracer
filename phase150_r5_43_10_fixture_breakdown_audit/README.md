# Phase 150 R5-43-10 Fixture Breakdown Audit

## Purpose

Break down the expensive `data_by_target` fixture from R5-43-10 without
changing production code or existing tests.

For each of the six representative `(n, k)` targets, the audit measures:

1. `context` — `_context(n, k)`
2. `base` — `render_toda_group_proof_narrative_multi_argument_markdown`
3. `ordered` — `build_toda_group_proof_narrative_ordered_contributions`
4. `connected` —
   `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`

Every START and END line is flushed immediately to:

`phase150_r5_43_10_fixture_breakdown_audit.txt`

If one stage runs for several minutes, the process can be interrupted and the
completed measurements remain available.

## Interpretation

A dominant `connected` stage would support the hypothesis that the connected
renderer is rebuilding work already performed by `base` and `ordered`.

A dominant `ordered` stage would instead point to contribution ordering itself.

A dominant `context` stage would move the bottleneck back into proof-context
construction.

This audit performs no optimization and no full regression.
