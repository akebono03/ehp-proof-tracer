Phase 144-6-R5-15B
====================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-15 bounded all six representative proofs, but pi_6^3 stopped at depth 6
rather than the benchmark depth 3.

The cause was global expansion of ordinary CALCULATION and GROUP_STRUCTURE
blocks.

R5-15B replaces that global rule with the generic structure already used by
the production renderer:

  required Narrative Argument
  -> Argument local body
  -> R4 production frontier
  -> visible explanatory steps

Required typed structural providers are retained as facts, but their internal
premise closures are not recursively expanded.

Existing production mechanisms reused
-------------------------------------
- extract_toda_group_proof_narrative_argument_local_body_blocks()
- _toda_group_proof_narrative_argument_frontier_hidden_step_ids()
- Narrative Argument roles
- typed structural providers from R5-13

No n/k-specific boundary rule is used.
No inference-rule-name parsing is used.

Benchmark
---------
For pi_6^3:

  full_depth = 10
  desired required_depth = 3

The audit must also preserve the required structural provider facts for:
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

This is still an audit. It does not change replay depth semantics or
production Narrative routing.
