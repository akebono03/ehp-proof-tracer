from proof import (
  InferenceRule,
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_references import (
  _infer_toda_group_proof_literature_reference_from_rule_name,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)


RULE_NAME = (
  "Toda Equation 5.7 nu-prime eta_6 Hopf value"
)


def _step() -> ProofStep:
  return ProofStep(
    conclusion="phase159-fix9",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=RULE_NAME,
    ),
  )


def test_phase159_r1_7c_r4_repair9_fix9_equation57_fixed_statement_uses_parenthesized_locator():
  boundary = classify_toda_literature_statement_step(
    _step()
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert boundary.reference_locator == "(5.7)"
  assert boundary.component_key == "nu_prime_eta6_hopf_relation"


def test_phase159_r1_7c_r4_repair9_fix9_named_equation_inference_matches_boundary_locator():
  boundary = classify_toda_literature_statement_step(
    _step()
  )
  reference = (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      RULE_NAME
    )
  )

  assert boundary is not None
  assert reference is not None
  assert reference.locator == "(5.7)"
  assert (
    boundary.reference_locator
    == reference.locator
  )
