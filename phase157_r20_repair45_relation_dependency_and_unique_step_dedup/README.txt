Phase157-R20 repair45

Purpose
-------
Resolve the two remaining ownership-confirmed pi_6^3 Narrative defects after
repair44.

repair44 findings
-----------------
1. The Proposition 2.2 specialization
   H(nu' eta_6) = H(nu') eta_6
   is a direct premise of the Equation 5.7 relation
   H(nu' eta_6) = eta_5^2, but appears after its consumer.

2. The Delta-zero statement exists as exactly one
   TodaDeltaZeroStatement step in the presentation, but is rendered twice in
   the public body.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

New functions
-------------
1. order_toda_group_proof_narrative_visible_relation_dependencies()
   - for visible Relation consumers;
   - if a visible direct Relation premise occurs after its consumer;
   - move that premise immediately before the consumer;
   - no theorem/group/generator-specific condition.

2. suppress_toda_group_proof_narrative_repeated_unique_step_statements()
   - build normalized rendered keys for presentation steps;
   - only keys owned by exactly one proof step are eligible;
   - pure repeated body statements for the same unique semantic step are
     suppressed after the first occurrence;
   - generic leading connectors such as `以上より, ` are ignored for the
     comparison;
   - larger derivation sentences are not matched or removed.

Pipeline insertion
------------------
After the repair43 dangling-connector cleanup:
1. relation dependency ordering;
2. unique-step repeated-statement suppression.

Import changes
--------------
None.

New test
--------
- tests/test_phase157_r20_repair45_relation_dependency_and_unique_step_dedup.py

Completion conditions
---------------------
- Proposition 2.2 fixed statement
  < Proposition 2.2 specialized relation
  < Equation 5.7 Hopf value;
- Delta-zero is rendered exactly once;
- Delta-zero remains before suspension injectivity;
- short-exact ordering remains intact;
- focused Phase157 and Phase156 Reference regressions remain passing.

No documentation changes.
No repository-wide pytest.
