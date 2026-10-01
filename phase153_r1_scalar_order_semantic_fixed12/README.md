# Phase153-R1 Fixed12

This package replaces the Phase153-R1 regression test with a direct classifier
unit test.

The existing supported Phase134-9 presentation does not contain a
ScalarGreaterEqualStatement node. Therefore the regression test must not search
the presentation tree for one.

Instead, Fixed12:

1. Builds the existing supported pi_6^3 presentation using the same route as
   the Phase134-9 baseline tests.
2. Constructs a standalone ProofStep whose conclusion is
   ScalarGreaterEqualStatement.
3. Passes that ProofStep to classify_toda_group_proof_narrative_step.
4. Asserts that its block role is ORDER.

The classifier does not require the supplied ProofStep to be a node of the
presentation. Production code is not changed.
