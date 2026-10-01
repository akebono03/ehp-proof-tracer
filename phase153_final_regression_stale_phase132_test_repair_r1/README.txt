Phase 153 Final Regression — Stale Phase 132 Test Repair R1
================================================================

Production changes
------------------
None.

Updated file
------------
tests/test_phase132_6_group_proof_narrative_renderer.py

Updated tests
-------------
test_phase132_6_depth_two_uses_nested_edges_before_parent_fact
test_phase138_4_sigma9_narrative_states_proof_purpose

Reason
------
The current pi_16^9 depth-2 Narrative uses the generic Reference route.
Phase 153 R11/R12 allow this route to omit the public
"## 使用する結果" heading and exclude root Proposition 5.15 from external
References.

The old Phase 132 expectations still required both presentation details.

The repaired tests now verify the current structural contract instead:
- nested proof content appears before the final result;
- Lemma 5.14 is the external R1 Reference;
- Proposition 5.15 is not reintroduced as external R1;
- the final pi_16^9 result remains present.

No Phase 154 prose cleanup is included.

After this focused repair passes, run:
python -m pytest .\tests -x

to locate the next final-regression failure, if any.
