Phase 143-75AF implementation

Production file changed:
- toda_proof_narrative_renderer.py

Changed import:
- add TodaProp44FirstSummandRestrictionStatement to the existing toda_rules import block

Changed function:
- render_toda_proof_statement_latex()
  - add semantic rendering for TodaProp44FirstSummandRestrictionStatement

Rendering semantics:
- use decomposition_map.formula
- restrict it to the first summand of decomposition_map.source_group
- identify that restriction with the recorded suspension_map
- do not assert injectivity
- do not assert isomorphism

Focused tests:
- tests/test_phase48_toda_prop44_first_summand_restriction.py
- tests/test_phase48_toda_prop44_e_injective_applicability.py
- phase143_75af_impl/test_phase143_75af_first_summand_rendering.py

Expected completion-audit effect after focused tests pass:
- fallback occurrences: 171 -> 152
- TodaProp44FirstSummandRestrictionStatement: 19 -> 0

No inference changes.
No API changes.
No docs changes.
No full pytest.
