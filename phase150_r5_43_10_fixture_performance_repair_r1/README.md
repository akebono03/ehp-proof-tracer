# Phase 150 R5-43-10 Fixture Performance Repair R1

Changed only `tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py`.

The performance fixture split from the previous repair is retained.

Two historical exact-adjacency assertions are aligned with the current generic
Narrative contract:

- transport connector: verify `c2 < Proposition 5.3 connector < c3`
- direct connector: verify `c4 < これより、 < c5`

The connector text, endpoints, ordering, sixteen-chain count, semantic metadata,
and no-special-branch assertions remain tested.

Production code, public APIs, mathematical semantics, and documentation are
unchanged. Full regression is intentionally not run here.
