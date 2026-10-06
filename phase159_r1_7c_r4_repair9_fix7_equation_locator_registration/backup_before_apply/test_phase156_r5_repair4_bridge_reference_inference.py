from toda_group_proof_narrative_references import (
  _infer_toda_group_proof_literature_reference_from_rule_name,
)
from toda_rules import (
  toda_53_eta5_iterated_suspension_bridge_inference_rule,
)


def test_phase156_r5_repair4_unreferenced_bridge_does_not_infer_reference():
  reference = (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      "Toda 5.3 eta_5 iterated suspension bridge"
    )
  )

  assert reference is None


def test_phase156_r5_repair4_standard_equation_rule_still_infers_reference():
  reference = (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      "Toda 5.3 nu-prime specialization"
    )
  )

  assert reference is not None
  assert reference.label == "Toda (5.3)"
  assert reference.locator == "(5.3)"


def test_phase156_r5_repair4_named_rule_still_infers_reference():
  reference = (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      "Toda Proposition 5.3 finite-dimensional result"
    )
  )

  assert reference is not None
  assert reference.label == "Toda Proposition 5.3"
  assert reference.locator == "Proposition 5.3"


def test_phase156_r5_repair4_eta5_bridge_rule_has_no_fallback_reference():
  rule = (
    toda_53_eta5_iterated_suspension_bridge_inference_rule()
  )

  assert rule.literature_reference is None
  assert (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      rule.name
    )
    is None
  )
