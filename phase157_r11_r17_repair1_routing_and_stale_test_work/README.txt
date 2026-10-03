Phase157 R11-R17 repair1 — routing / stale-test recovery

Initial R11-R17 focused result:
- 70 passed
- 5 failed

Failure classification
======================

1. zero-map visibility:
   production bug.
   The helper unnecessarily required the consumer itself to be classified
   MAP_PROPERTY. The correct generic condition is:
   visible consumer + direct hidden zero-map premise.

2. standalone connectors in pi_8^5 / pi_15^8:
   production routing bug.
   These routes use dedicated renderers and do not pass through the generic
   contribution finalization. Public-route finalization must normalize them.

3. pi_16^9 Reference selection:
   production stage-order bug.
   Unmarked Reference linkage was added after the body-usage filter, so the
   needed Lemma 5.14 was already gone. Link before the first usage filter.

4. pi_16^9 Lemma 5.13 ancestry-only:
   expected to disappear once linkage is moved before filtering and only
   visible direct consumers receive markers.

5. Phase156 pi6 ordering:
   stale test.
   R11-R14 established the mathematically correct dependency order:
   transported pi_5^2 result -> E injective -> ord(eta_3^3)=2.
   The Phase156 test still expected the old inverse order.

Production changes
==================

- toda_group_proof_narrative_contribution_renderer.py
  - hidden zero-map premise visibility
  - move unmarked Reference linkage before body-usage filtering
  - remove late linkage/filter

- toda_group_proof_narrative_renderer.py
  - public finalizer normalization for standalone connectors
  - public finalizer normalization for repeated numeric equality
  - covers generic and dedicated routes

Test change
===========

- tests/test_phase156_r6_canonical_connector_local_ordering.py
  - replace stale ordering test with R11-R14 dependency-compatible order

No import changes.
No docs.
Focused pytest only.
Full pytest remains deferred until Phase157 closure.
