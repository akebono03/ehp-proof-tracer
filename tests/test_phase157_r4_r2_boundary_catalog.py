from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_components,
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


def test_phase157_r4_r2_prop511_inventory_matches_fixed_finite_dimensional_statement():
  components = get_toda_fixed_statement_components(
    "Proposition 5.11"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "pi8_2_group_relation",
    "pi9_3_zero",
    "pi10_4_group_relation",
    "higher_nu_squared_group_relation",
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


def test_phase157_r4_r2_prop515_inventory_matches_fixed_finite_dimensional_statement():
  components = get_toda_fixed_statement_components(
    "Proposition 5.15"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "pi9_2_zero",
    "pi10_3_zero",
    "pi11_4_zero",
    "pi12_5_group_relation",
    "pi13_6_group_relation",
    "pi14_7_group_relation",
    "pi15_8_group_relation",
    "higher_sigma_group_relation",
  )
  assert tuple(
    component.order
    for component in components
  ) == tuple(
    range(
      1,
      9,
    )
  )
  assert components[6].range_text == "n = 8"
  assert components[7].range_text == "n >= 9"


def test_phase157_r4_r2_prop515_same_theorem_group_order_allows_only_earlier_results():
  selected = select_toda_fixed_statement_reference_components(
    "Proposition 5.15",
    "Proposition 5.15",
    "pi15_8_group_relation",
  )

  assert tuple(
    component.component_key
    for component in selected
  ) == (
    "pi9_2_zero",
    "pi10_3_zero",
    "pi11_4_zero",
    "pi12_5_group_relation",
    "pi13_6_group_relation",
    "pi14_7_group_relation",
  )


def test_phase157_r4_r2_lemma513_fixed_statement_is_registered():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda Lemma 5.13 sigma triple-prime definition",
      "Lemma 5.13",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert boundary.component_key == "sigma_triple_prime_statement"


def test_phase157_r4_r2_lemma514_three_fixed_branches_are_registered():
  cases = (
    (
      "Toda Lemma 5.14 sigma double-prime branch",
      "sigma_double_prime_statement",
    ),
    (
      "Toda Lemma 5.14 sigma-prime branch",
      "sigma_prime_statement",
    ),
    (
      "Toda Lemma 5.14 sigma_8 branch",
      "sigma8_statement",
    ),
  )

  for rule_name, component_key in cases:
    boundary = classify_toda_literature_statement_step(
      _step(
        rule_name,
        "Lemma 5.14",
      )
    )

    assert boundary is not None
    assert boundary.classification == (
      TodaLiteratureStatementClassification.FIXED_STATEMENT
    )
    assert boundary.component_key == component_key


def test_phase157_r4_r2_equation513_three_map_values_are_registered():
  cases = (
    (
      "Toda Equation 5.13 Delta nu_9",
      "delta_nu9_relation",
    ),
    (
      "Toda Equation 5.13 Delta eta_11 squared zero",
      "delta_eta11_squared_zero",
    ),
    (
      "Toda Equation 5.13 Delta eta_13 zero",
      "delta_eta13_zero",
    ),
  )

  for rule_name, component_key in cases:
    boundary = classify_toda_literature_statement_step(
      _step(
        rule_name,
        "Equation 5.13",
      )
    )

    assert boundary is not None
    assert boundary.classification == (
      TodaLiteratureStatementClassification.FIXED_STATEMENT
    )
    assert boundary.component_key == component_key


def test_phase157_r4_r2_prop511_derived_map_property_remains_proof_internal():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda Proposition 5.11 pi_12^6 suspension isomorphism",
      "Proposition 5.11",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.PROOF_INTERNAL
  )


def test_phase157_r4_r2_prop515_decomposition_semantics_remain_proof_internal():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda Proposition 5.15 sigma_8 transported decomposition",
      "Proposition 5.15",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.PROOF_INTERNAL
  )


def test_phase157_r4_r2_equation55_nu_family_fixed_statement_is_registered():
  boundary = classify_toda_literature_statement_step(
    _step(
      "Toda (5.5) nu-family finite-dimensional integration",
      "(5.5)",
    )
  )

  assert boundary is not None
  assert boundary.classification == (
    TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert boundary.component_key == "nu_family_relations"
