from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)


CASES = (
  (
    'Proposition 5.3',
    'Toda Proposition 5.3 finite-dimensional integration',
    'fixed_statement',
    None,
  ),
  (
    'Proposition 5.1',
    'Toda Proposition 5.1 finite-dimensional integration',
    'fixed_statement',
    None,
  ),
  (
    'Proposition 5.6',
    'Toda Proposition 5.6 finite-dimensional integration',
    'fixed_statement',
    None,
  ),
  (
    'Proposition 5.11',
    'Toda Proposition 5.11 finite-dimensional integration',
    'fixed_statement',
    None,
  ),
  (
    '(4.5)',
    'Toda 4.5 stable-range iterated suspension isomorphism',
    'fixed_statement',
    'stable_range_suspension_isomorphism',
  ),
  (
    '(4.5)',
    'Toda 4.5 pi_4^3 finite-cyclic transport',
    'proof_internal',
    None,
  ),
  (
    'Proposition 5.8',
    'Toda Proposition 5.8 higher four-stem zero transport',
    'fixed_statement',
    'higher_four_stem_zero',
  ),
  (
    'Proposition 5.9',
    'Toda Proposition 5.9 higher five-stem zero transport',
    'fixed_statement',
    'higher_five_stem_zero',
  ),
  (
    '(5.2)',
    'Toda 5.2 eta_2 composition isomorphism',
    'fixed_statement',
    'eta2_composition_isomorphism',
  ),
  (
    '(5.2)',
    'Toda 5.2 pi_4^2 finite-cyclic transport',
    'proof_internal',
    None,
  ),
  (
    'Lemma 5.14',
    'Toda Lemma 5.14 sigma-family definition',
    'proof_internal',
    None,
  ),
  (
    'Proposition 4.4',
    'Toda Proposition 4.4 eta_2 n=2 specialization',
    'fixed_statement',
    'nu4_decomposition_isomorphism',
  ),
  (
    'Proposition 4.4',
    'Toda Proposition 4.4 eta_2 second-summand restriction',
    'proof_internal',
    None,
  ),
  (
    'Equation 5.7',
    'Toda Equation 5.7 nu-prime eta_6 Hopf value',
    'fixed_statement',
    'nu_prime_eta6_hopf_relation',
  ),
  (
    'Lemma 5.4',
    'Toda Lemma 5.4 integration',
    'fixed_statement',
    'nu4_statement',
  ),
  (
    'Proposition 5.8',
    'Toda Proposition 5.8 pi_7^3 finite cyclic',
    'fixed_statement',
    'pi7_3_group_relation',
  ),
  (
    'Proposition 5.9',
    'Toda Proposition 5.9 finite-dimensional integration',
    'fixed_statement',
    'finite_dimensional_aggregate',
  ),
  (
    '(5.5)',
    'Toda 5.5 nu-family finite-dimensional integration',
    'fixed_statement',
    'nu_family_relations',
  ),
  (
    'Lemma 5.4',
    'Toda Lemma 5.4 pi_6^5 finite-cyclic specialization',
    'proof_internal',
    None,
  ),
  (
    'Lemma 5.7',
    'Toda Lemma 5.7 pi_6^2 eta_2 nu-prime',
    'proof_internal',
    None,
  ),
  (
    'Proposition 5.8',
    'Toda Proposition 5.8 finite-dimensional integration',
    'fixed_statement',
    'finite_dimensional_aggregate',
  ),
  (
    'Proposition 5.8',
    'Toda Proposition 5.8 pi_8^4 decomposition',
    'fixed_statement',
    'pi8_4_group_relation',
  ),
  (
    'Proposition 5.9',
    'Toda Proposition 5.9 pi_8^3 finite cyclic',
    'fixed_statement',
    'pi8_3_group_relation',
  ),
  (
    'Equation 5.8',
    'Toda Equation 5.8 integration',
    'fixed_statement',
    'delta_iota9_relation',
  ),
  (
    'Lemma 5.7',
    'Toda Lemma 5.7 Delta nu_5 generator',
    'fixed_statement',
    'delta_nu5_relation',
  ),
  (
    'Proposition 2.5',
    'Toda Proposition 2.5 Delta eta_9 composition',
    'fixed_statement',
    'delta_composition_formula',
  ),
  (
    'Proposition 3.1',
    'Toda Proposition 3.1 nu_6 eta_9 zero consequence',
    'proof_internal',
    None,
  ),
  (
    'Proposition 4.4',
    'Toda Proposition 4.4 nu_4 n=4 decomposition specialization',
    'fixed_statement',
    'nu4_decomposition_isomorphism',
  ),
  (
    'Proposition 5.8',
    'Toda Proposition 5.8 Delta eta_9 value',
    'proof_internal',
    None,
  ),
  (
    'Proposition 5.8',
    'Toda Proposition 5.8 eta_6 nu_7 zero specialization',
    'proof_internal',
    None,
  ),
  (
    'Proposition 5.8',
    'Toda Proposition 5.8 pi_7^3 Hopf injective',
    'fixed_statement',
    'pi7_3_group_relation',
  ),
  (
    'Proposition 5.8',
    'Toda Proposition 5.8 pi_9^5 finite cyclic',
    'fixed_statement',
    'pi9_5_group_relation',
  ),
  (
    'Proposition 5.9',
    'Toda Proposition 5.9 pi_11^6 Hopf injective',
    'fixed_statement',
    'pi11_6_group_relation',
  ),
  (
    'Proposition 5.9',
    'Toda Proposition 5.9 pi_13^13 Delta surjective',
    'fixed_statement',
    'pi11_6_group_relation',
  ),
  (
    'Proposition 5.9',
    'Toda Proposition 5.9 pi_8^3 Hopf injective',
    'fixed_statement',
    'pi8_3_group_relation',
  ),
  (
    'Proposition 5.9',
    'Toda Proposition 5.9 pi_9^4 decomposition',
    'fixed_statement',
    'pi9_4_group_relation',
  ),
)


def _step(
  locator: str,
  rule_name: str,
) -> ProofStep:
  return ProofStep(
    conclusion="phase157-r5-r3",
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


def test_phase157_r5_r3_all_r5_r2_catalog_candidates_are_classified():
  for (
    locator,
    rule_name,
    expected_classification,
    expected_component,
  ) in CASES:
    boundary = classify_toda_literature_statement_step(
      _step(
        locator,
        rule_name,
      )
    )

    assert boundary is not None
    assert (
      boundary.classification.value
      == expected_classification
    )
    assert (
      boundary.reference_locator
      == locator
    )
    assert (
      boundary.component_key
      == expected_component
    )


def test_phase157_r5_r3_aggregate_fixed_statements_do_not_expand_component_inventory():
  aggregate_locators = (
    "Proposition 5.1",
    "Proposition 5.3",
    "Proposition 5.6",
    "Proposition 5.11",
  )

  for locator in aggregate_locators:
    aggregate_cases = tuple(
      case
      for case in CASES
      if (
        case[0] == locator
        and case[3] is None
        and case[2] == "fixed_statement"
      )
    )

    assert aggregate_cases
