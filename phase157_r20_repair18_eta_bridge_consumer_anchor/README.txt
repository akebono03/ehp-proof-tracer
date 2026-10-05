Phase157-R20 repair18

Purpose
-------
Fix the eta-family suspension bridge anchor without adding target-specific
rendering.

Audit result
------------
Equation (5.7) has four premises, including:
- TodaEtaFamilyDefinitionStatement(index=5)
- TodaEtaFamilyDefinitionStatement(index=6)

However, at bridge-insertion time neither eta-definition paragraph is visible
in the public body. Therefore repair16's strategy of anchoring the bridge to
the visible eta_6 definition paragraph cannot work.

Generic repair
--------------
For every proof step:
1. collect TodaEtaFamilyDefinitionStatement premises;
2. sort them by index;
3. find adjacent indices n and n+1;
4. render:
     eta_(n+1) = E eta_n
5. insert that bridge immediately before the visible consumer step.

The consumer may be Equation (5.7) here, but the implementation does not
inspect rule names, proposition numbers, dimensions, generator names, or the
pi_6^3 target.

Changed files
-------------
- toda_group_proof_narrative_contribution_renderer.py
  - insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges()
- tests/test_phase157_r20_repair18_eta_bridge_consumer_anchor.py

No documentation changes.
No repository-wide pytest.
