# Phase 144-6 R25-9A-R1-R3

## Production changes

None.

## Why the R2 test failed

R2 attempted to identify the internal pi_5^3 `ProofStep` by applying `str()` to
its structured conclusion and searching for rendered LaTeX.

That assumption is invalid: the structured statement's Python string
representation is not the generic Narrative renderer output.

The failure therefore did not show a production regression. In the same run,
all other 17 focused tests passed, including the existing Phase 144-6 R4 test
that directly asserts pi_5^3 is absent from the final Narrative.

## Corrected test scope

The R25-9A tests already verify the role-based hidden frontier structurally.
R3 therefore tests the separate R1 contract at the observable rendering
boundary:

- pi_5^3 is absent;
- the nu-prime definition is retained at the depth-3 method-evidence fixture;
- the two derivation connectors remain;
- the Hopf and double relations remain;
- the final pi_6^3 group conclusion remains.

This avoids duplicating statement-renderer internals in the regression test.

## Next boundary

If the focused suite passes, R25-9A is complete. R25-9B may then address only
the missing nu-prime definition at depth 2.

The full suite is intentionally deferred until the end of Phase 144-6.
