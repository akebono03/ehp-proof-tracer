Phase 159-R1-7c R2 repair6

Uses the already-established generic public rendering of equality proof steps
as the semantic equality contract for chain composition.

The raw proof expression graph is not changed.

If generic rendering supplies:
  a = b
  b = c
  a = c
then the public narrative may render:
  a = b = c

Identity chains are ignored.
No group-specific branch.
Focused tests only.
