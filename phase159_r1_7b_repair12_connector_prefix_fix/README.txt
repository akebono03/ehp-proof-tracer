Phase 159-R1-7b repair12

The inline `完全性より,` connector is now matched by prefix,
without requiring a literal ASCII space after the comma.

The remainder of the line is stripped and parsed as the map-property line.
If the connector has no inline remainder, the next nonblank line is used,
preserving the previous behavior.

No group-specific branch.
Focused tests only; no repository-wide pytest.
