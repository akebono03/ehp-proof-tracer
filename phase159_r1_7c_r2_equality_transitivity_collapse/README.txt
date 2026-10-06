Phase 159-R1-7c R2

Collapses a local, non-reused equality-transitivity derivation

    a = b
    b = c
    therefore a = c

into

    a = b = c

when the two equation numbers are used only by that local derivation.

The rule is proof-graph based and contains no group-, theorem-, or generator-
specific branch.

Focused tests only. No repository-wide pytest.
