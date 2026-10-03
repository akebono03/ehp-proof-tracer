from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  TodaLiteratureStatementRole,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_component,
  get_toda_fixed_statement_components,
  is_toda_fixed_statement_component_reference_eligible,
  select_toda_fixed_statement_reference_components,
)


def _step(
  rule_name: str,
  locator: str,
) -> ProofStep:
  return ProofStep(
    conclusion=rule_name,
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=rule_name,
      literature_reference=LiteratureReference(
        label="Toda " + locator,
        locator=locator,
      ),
    ),
  )


def test_phase157_r2_prop51_inventory_preserves_current_four_components():
  components = get_toda_fixed_statement_components(
    "Proposition 5.1"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "pi3_2_group_relation",
    "eta2_hopf_relation",
    "delta_iota5_relation",
    "higher_eta_group_relation",
  )
  assert tuple(
    component.order
    for component in components
  ) == (
    1,
    2,
    3,
    4,
  )
  assert components[-1].range_text is None
  assert (
    components[-1].range_is_explicit_in_current_aggregate
    is False
  )


def test_phase157_r2_prop53_inventory_preserves_order_and_range():
  components = get_toda_fixed_statement_components(
    "Proposition 5.3"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "pi4_2_group_relation",
    "pi5_3_group_relation",
    "pi6_4_group_relation",
    "higher_eta_squared_group_relation",
  )
  assert tuple(
    component.order
    for component in components
  ) == (
    1,
    2,
    3,
    4,
  )
  assert components[-1].range_text == "n >= 5"
  assert all(
    component.statement_role
    == TodaLiteratureStatementRole.GROUP_STRUCTURE
    for component in components
  )


def test_phase157_r2_prop56_inventory_preserves_split_n5_and_n6_range():
  components = get_toda_fixed_statement_components(
    "Proposition 5.6"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "pi5_2_group_relation",
    "pi6_3_group_relation",
    "pi7_4_group_relation",
    "pi8_5_group_relation",
    "higher_nu_group_relation",
  )
  assert tuple(
    component.order
    for component in components
  ) == (
    1,
    2,
    3,
    4,
    5,
  )
  assert components[3].range_text == "n = 5"
  assert components[4].range_text == "n >= 6"


def test_phase157_r2_equation53_inventory_has_no_group_order_policy():
  components = get_toda_fixed_statement_components(
    "(5.3)"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "nu_prime_membership",
    "nu_prime_hopf_relation",
    "nu_prime_double_relation",
  )
  assert all(
    component.order is None
    for component in components
  )
  assert tuple(
    component.statement_role
    for component in components
  ) == (
    TodaLiteratureStatementRole.MEMBERSHIP,
    TodaLiteratureStatementRole.MAP_VALUE,
    TodaLiteratureStatementRole.RELATION,
  )


def test_phase157_r2_same_prop56_group_result_allows_only_earlier_component():
  pi5_2 = get_toda_fixed_statement_component(
    "Proposition 5.6",
    "pi5_2_group_relation",
  )
  pi6_3 = get_toda_fixed_statement_component(
    "Proposition 5.6",
    "pi6_3_group_relation",
  )
  pi7_4 = get_toda_fixed_statement_component(
    "Proposition 5.6",
    "pi7_4_group_relation",
  )

  assert is_toda_fixed_statement_component_reference_eligible(
    pi5_2,
    "Proposition 5.6",
    "pi6_3_group_relation",
  )
  assert not is_toda_fixed_statement_component_reference_eligible(
    pi6_3,
    "Proposition 5.6",
    "pi6_3_group_relation",
  )
  assert not is_toda_fixed_statement_component_reference_eligible(
    pi7_4,
    "Proposition 5.6",
    "pi6_3_group_relation",
  )


def test_phase157_r2_different_theorem_fixed_group_result_remains_eligible():
  pi5_3 = get_toda_fixed_statement_component(
    "Proposition 5.3",
    "pi5_3_group_relation",
  )

  assert is_toda_fixed_statement_component_reference_eligible(
    pi5_3,
    "Proposition 5.6",
    "pi6_3_group_relation",
  )


def test_phase157_r2_component_selector_for_pi6_3_keeps_only_prop56_predecessor():
  selected = select_toda_fixed_statement_reference_components(
    "Proposition 5.6",
    "Proposition 5.6",
    "pi6_3_group_relation",
  )

  assert tuple(
    component.component_key
    for component in selected
  ) == (
    "pi5_2_group_relation",
  )


def test_phase157_r2_fixed_prop56_group_step_is_classified_as_fixed_statement():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda Proposition 5.6 pi_5^2 eta_2 cube",
      "Proposition 5.6",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert boundary.component_key == "pi5_2_group_relation"


def test_phase157_r2_prop56_order_fact_is_classified_as_proof_internal():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda Proposition 5.6 nu-prime order four",
      "Proposition 5.6",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.PROOF_INTERNAL
  )
  assert boundary.component_key is None


def test_phase157_r2_prop53_map_property_is_classified_as_proof_internal():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity",
      "Proposition 5.3",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.PROOF_INTERNAL
  )


def test_phase157_r2_prop51_order_consequence_is_classified_as_proof_internal():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda 5.3 eta_3 twice zero",
      "Proposition 5.1",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.PROOF_INTERNAL
  )


def test_phase157_r2_equation53_public_relations_are_fixed_statements():
  cases = (
    (
      "Toda 5.3 nu-prime Lemma 5.2 membership specialization",
      "nu_prime_membership",
    ),
    (
      "Toda 5.3 nu-prime Lemma 5.2 Hopf specialization",
      "nu_prime_hopf_relation",
    ),
    (
      "Toda 5.3 nu-prime Lemma 5.2 double specialization",
      "nu_prime_double_relation",
    ),
  )

  for rule_name, component_key in cases:
    boundary = classify_toda_literature_statement_step(
      _step(
        rule_name,
        "(5.3)",
      )
    )

    assert boundary is not None
    assert boundary.classification == (
      TodaLiteratureStatementClassification.FIXED_STATEMENT
    )
    assert boundary.component_key == component_key


def test_phase157_r2_equation53_bracket_specialization_is_proof_internal():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda 5.3 nu-prime Lemma 5.2 bracket specialization",
      "(5.3)",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.PROOF_INTERNAL
  )


def test_phase157_r2_untracked_rule_in_tracked_reference_is_proof_internal():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda Proposition 5.15 test",
      "Proposition 5.15",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.PROOF_INTERNAL
  )
  assert boundary.reference_locator == "Proposition 5.15"
  assert boundary.component_key is None
