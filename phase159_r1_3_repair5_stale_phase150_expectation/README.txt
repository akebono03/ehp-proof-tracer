Phase 159-R1-3 repair5

Classification:
test-only stale expectation repair

Production code changes:
none

Test change:
tests/test_phase150_rc4_5c_2_exactness_to_map_property.py

The raw reason renderer still returns the connector `したがって, `.
The contribution/public pipeline later normalizes standalone connectors.
Therefore the final rendered-output assertion now checks the semantic reason body
and its ordering before the injective conclusion, instead of requiring the raw
reason string to survive byte-for-byte.

Full pytest is not run.
