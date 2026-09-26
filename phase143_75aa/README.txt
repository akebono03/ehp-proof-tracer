Phase 143-75AA

Purpose:
Add generic semantic rendering for Toda56Nu4Prop44SpecializationStatement.

The renderer intentionally uses only:
- n
- alpha
- membership
- hopf_relation

It intentionally does not expand lemma54_statement, avoiding duplication with the preceding Lemma 5.4 narrative.

Expected semantic rendering:
n = 4, alpha = nu_4, nu_4 in pi_7^4, H(nu_4) = iota_7

Only focused tests are run. Full pytest is deferred until the end of Phase 143.
