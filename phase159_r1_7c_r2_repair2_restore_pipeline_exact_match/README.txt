Phase 159-R1-7c R2 repair2

Restores the exact pre-R2 public renderer pipeline from the backup created by
the original R2 apply step, then adds equality-chain normalization only as a
final wrapper.

Line matching is exact inline-math matching rather than substring matching.

No group-specific branch.
Focused tests only; no repository-wide pytest.
