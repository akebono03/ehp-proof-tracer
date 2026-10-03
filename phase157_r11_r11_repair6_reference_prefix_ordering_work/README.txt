Phase157 R11-R11 repair6 — Reference-prefix-aware ordering

repair5 result:
- 57 passed / 2 failed.

Failure 1:
tag(4) is rendered as:
[R2]より, $H(nu') = E^2 eta_3\tag{4}$.

The graph-ordering helper compared this whole paragraph with the raw
ProofStep statement and therefore failed to recognize tag(4).
As a result only tag(5)-tag(6) moved before H-surjectivity.

repair6:
- comparison only strips the leading `[R#]より, ` for matching.
- displayed paragraph itself is not modified.
- tag(4), tag(5), connector, tag(6) are moved as one contiguous block
  before the MAP_PROPERTY statement.

Failure 2:
old R5/R9 test still expected membership Reference line to end with comma.
Phase157 period policy now intentionally ends independent Reference statements
with period, so only the historical expectation is updated.

Production change:
- toda_group_proof_narrative_contribution_renderer.py
  - order_toda_group_proof_narrative_surjectivity_support()

Test change:
- tests/test_phase157_r5_r9_fixed_definition_body_suppression.py
  - comma -> period expectation

No new pi6_3 / nu_prime / rule-name hard-code.
Full repository pytest remains deferred until Phase157 closure.
