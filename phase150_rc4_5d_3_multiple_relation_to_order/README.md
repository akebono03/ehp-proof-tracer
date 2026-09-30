# Phase 150 / RC4-5D-3

Implements the generic Narrative reason kind `MULTIPLE_RELATION_TO_ORDER`.

Changed production files:
- `toda_group_proof_narrative_reasons.py`
- `toda_group_proof_narrative_reason_renderer.py`

New focused test:
- `tests/test_phase150_rc4_5d_3_multiple_relation_to_order.py`

The classifier uses only the audited typed shape: exact `ORDER(x)=2`,
`EQUALITY(Multiple(2,y),x)`, and exact conclusion `ORDER(y)=4`.
It does not inspect dimensions, element names, proposition numbers, rule names,
or rendered prose.

Contribution ordering is unchanged. Repository-wide tests remain deferred
until the end of Phase 150.
