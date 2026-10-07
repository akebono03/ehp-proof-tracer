Phase 159-R1-5 public map-property wording

Scope
-----
Public Narrative wording only.

Rule
----
Map-property statements in the proof body use terse formula-style wording:

- 単射.
- 全射.
- 同型.
- 零写像.

The low-level generic renderer is intentionally unchanged because it is also
used by internal/reference rendering paths.

Production
----------
- toda_group_proof_narrative_renderer.py

Tests
-----
- tests/test_phase159_r1_2_pi3_2_narrative_repair.py

No theorem/inference changes.
No Reference attribution changes.
No full pytest.
