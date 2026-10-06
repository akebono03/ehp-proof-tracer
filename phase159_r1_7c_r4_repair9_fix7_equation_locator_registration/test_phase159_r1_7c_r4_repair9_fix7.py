from proof import (
  InferenceRule,
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_references import (
  _infer_toda_group_proof_literature_reference_from_rule_name,
  extract_toda_group_proof_step_literature_reference,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_components,
)


def _step(
  rule_name: str,
) -> ProofStep:
  return ProofStep(
    conclusion=rule_name,
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=rule_name,
    ),
  )


def test_phase159_r1_7c_r4_repair9_fix7_named_equation_reference_uses_parenthesized_locator():
  reference = (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      "Toda Equation 5.7 nu-prime eta_6 Hopf value"
    )
  )

  assert reference is not None
  assert reference.label == "Toda (5.7)"
  assert reference.locator == "(5.7)"


def test_phase159_r1_7c_r4_repair9_fix7_equation57_keeps_existing_boundary_classification():
  step = _step(
    "Toda Equation 5.7 nu-prime eta_6 Hopf value"
  )
  boundary = classify_toda_literature_statement_step(
    step
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.PROOF_INTERNAL
  )
  assert boundary.reference_locator == "(5.7)"

  reference = extract_toda_group_proof_step_literature_reference(
    step
  )
  assert reference is not None
  assert reference.locator == "(5.7)"


def test_phase159_r1_7c_r4_repair9_fix7_equation58_fixed_boundary_uses_parenthesized_locator():
  step = _step(
    "Toda Equation 5.8 integration"
  )
  boundary = classify_toda_literature_statement_step(
    step
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert boundary.reference_locator == "(5.8)"
  assert boundary.component_key == "delta_iota9_relation"


def test_phase159_r1_7c_r4_repair9_fix7_equation513_fixed_components_use_parenthesized_locator():
  components = get_toda_fixed_statement_components(
    "(5.13)"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "delta_nu9_relation",
    "delta_eta11_squared_zero",
    "delta_eta13_zero",
  )

  assert all(
    component.reference_locator == "(5.13)"
    for component in components
  )
