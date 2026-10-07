Phase 159 R1-7c R4 map-property numbered-reasoning audit2

Purpose
-------
Audit1 incorrectly reported zero numbered injective/surjective statements.

Cause:
current public Narrative stores the equation number inside the math span:

  $H: ... \tag{1}$ は単射.

Audit1 only detected a number placed after the prose, so it classified these
as unnumbered.

Audit2 is tag-aware.

It groups public proof-body lines by normalized map text and reports only maps
for which both:
- injective;
- surjective

appear for the same map.

For each pair it classifies:
- FULLY_NUMBERED_PAIR
- UNNUMBERED_PAIR
- MIXED_PAIR

and checks whether an isomorphism conclusion for the same normalized map is
also visible.

This distinguishes standalone map-property facts from genuine
injective+surjective -> isomorphism reasoning candidates.

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
