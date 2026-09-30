# Phase 150 / RC4-5E-1

Read-only audit for the proposed `SHORT_EXACT_DERIVATION` generic reason.

## Target

Audit the existing derivation of a short exact sequence from:

- a typed `TodaProp42ExactnessStatement`;
- a matching injective statement for the first map;
- a matching surjective statement for the second map.

The current production helper
`_generic_short_exact_sequence_latex(...)` already requires those three
structural facts. This audit verifies that the visible `pi_6^3` short exact
sequence is generated under that generic typed contract rather than by
target-specific names.

## Expected conclusion

If the audit passes, Phase 150 can add a generic
`SHORT_EXACT_DERIVATION` reason without hard-coding `pi_6^3`, `nu_prime`,
Proposition 5.6, or fixed group coordinates.

The reason should explain that exactness, injectivity of the left map, and
surjectivity of the right map yield the displayed short exact sequence.

## Boundary

No production files or existing tests are changed. This audit does not yet
change the fixed prose in the exactness contribution renderer.

Repository-wide tests remain deferred until the end of Phase 150.
