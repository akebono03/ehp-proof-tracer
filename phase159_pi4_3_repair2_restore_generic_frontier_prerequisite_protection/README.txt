Phase 159 — pi_4^3 repair 2
Restore generic frontier prerequisite protection
================================================

Problem
-------
The pi_4^3 depth=2 local Narrative body already contains:
- pi_3^2 = Z{eta_2},
- ker(E),
- E surjectivity,
- pi_4^5 = 0,
- E-H exactness.

The frontier-hidden policy nevertheless hides five non-exact steps.

Historical contract
-------------------
Phase 144-6 Final Regression Repair R15 established the generic rule:

  Direct-premise prerequisites are protected for every NarrativeArgument
  role, not only ESTABLISH_DEFINITION.

The current production helper again limits this protection to
ESTABLISH_DEFINITION.

Repair
------
Change only:

  toda_group_proof_narrative_argument_multi_renderer.py
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids()

The role guard around direct-premise prerequisite protection is removed.

No pi_4^3-specific type or group hard-code is added.

Internal supporting facts not lying on that protected frontier remain hidden.

Tests
-----
Added:
  tests/test_phase159_pi4_3_repair2_frontier_prerequisite_protection.py

Focused existing tests:
  tests/test_phase144_6_r4_supporting_fact_filtering.py
  tests/test_phase143_36_argument_body_blocks.py
  Phase 159 direct provenance tests

Completion condition
--------------------
- ker(E) support is no longer frontier-hidden.
- E-surjectivity support is no longer frontier-hidden.
- pi_3^2 support is visible in rendered pi_4^3 body.
- internal TodaEtaFamilyDefinitionStatement remains hidden.
- Phase 144 supporting-fact filtering contract remains green.
- public depth=2 Narrative is printed for the next diagnosis.

Boundary
--------
This repair does not expand semantic closure.

Therefore these remain for the next repair:
- Proposition 5.1 direct Delta statement,
- Im(Delta),
- Delta-E exactness.

Repository-wide pytest is not run.
