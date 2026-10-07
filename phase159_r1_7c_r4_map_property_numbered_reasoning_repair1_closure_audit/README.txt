Phase 159 R1-7c R4 numbered map-property reasoning repair1 closure audit

Purpose
-------
Verify the current public Narrative contract after repair1.

The audit classifies same-map reasoning into:

1. injective + surjective + isomorphism trios
2. injective + surjective pairs without isomorphism

For every trio, the expected final public contract is:

  map\tag{n} は単射.
  map\tag{m} は全射.
  (n), (m) より, map は同型.

Pairs without an existing isomorphism conclusion must NOT gain one.

Scope
-----
Audit only.

Range:
  n=2..15
  k=0..7
  max_depth=2

This is a reproducible audit sample, not a permanent group-count contract.

Production code changes: none.
Test code changes: none.
No full pytest.
