# Phase 144-6 R25-8R1 — Rollback and Semantic-Route Audit

## Changed production files

None after rollback.

The runner restores `toda_upstream_bootstrap.py` exactly from Git HEAD and
removes the temporary R25-8 regression test file.

## Purpose

R25-8 proved that exposing the existing `nu'` bracket membership at depth 2
recovers the definition Argument, but changing the returned membership
`ProofStep` premises also changes proof-graph ownership. That caused existing
support suppression and derivation-transition regressions.

R25-8R1 therefore does not add another production repair.

It audits the semantic route already implemented in
`toda_group_proof_narrative_semantics.py`.

The existing semantic vocabulary recognizes:

- premise 0 of the Toda 5.3 nu-prime bracket specialization as
  `DEFINITION_INTRODUCTION`;
- the relevant Lemma 5.2 specialization precondition as `PRECONDITION`;
- the semantic dependency between them as
  `PRECONDITION_FOR_DEFINITION`.

The audit compares replay depths 1, 2 and 3 and reports whether the bracket
membership endpoint, semantic definition role, semantic dependency and
definition Argument exist at each depth.

## Completion condition

R25-8R1 is complete when:

1. `toda_upstream_bootstrap.py` matches Git HEAD;
2. focused semantic-route controls pass;
3. the depth audit identifies the exact selection boundary at which the
   existing semantic definition route becomes available;
4. no production repair is applied;
5. the full suite is not run.

The next repair must preserve the proof graph and existing suppression /
transition behavior.
