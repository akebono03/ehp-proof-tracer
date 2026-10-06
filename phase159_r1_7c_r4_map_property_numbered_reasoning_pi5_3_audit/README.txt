Phase 159 R1-7c R4 pi_5^3 numbered-reasoning focused audit

Reason
------
Audit2 previously detected pi_5^3 as a fully numbered injective/surjective
pair with an isomorphism conclusion.

After numbered-reasoning repair1, the closure audit no longer listed pi_5^3
among injective+surjective+isomorphism trios.

This focused audit prints:
- every current public line involving E: pi_4^2 -> pi_5^3;
- the full pi_5^3 proof body;
- whether injective / surjective / isomorphism prose is present.

The goal is to distinguish:
- an actual public-output regression;
- a closure-audit parser miss.

Production code changes: none.
Test code changes: none.
No full pytest.
