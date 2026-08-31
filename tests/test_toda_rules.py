from algebra import (
  GroupElement,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IndexedTodaBracketData,
  IteratedSuspension,
  Multiple,
  Suspension,
  TodaBracket,
  Zero,
  eta,
  nu,
  sigma,
)
from indeterminacy_rules import (
  CosetMembershipStatement,
  SignIndeterminacyStatement,
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from proof import (
  InferenceTerminationReason,
  LiteratureReference,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  derive_inference_round_result,
  find_inference_match,
  relation_proof_step,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  composition_equality_to_zero_inference_rule,
  equality_symmetry_inference_rule,
)
from set_rules import (
  Coset,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  TodaBracketMembershipStatement,
  TodaBracketMembershipTheoremStatement,
  indexed_toda_bracket_membership_from_theorem_inference_rule,
  toda_bracket_defined_by_zero_compositions_inference_rule,
  toda_bracket_membership_from_theorem_inference_rule,
  toda_bracket_membership_proof_step,
  toda_bracket_membership_theorem_proof_step,
)


def make_cyclic_group(
  order,
  generator,
):
  return AbelianGroup(
    n=0,
    k=0,
    components=[
      GroupComponent(
        id=0,
        order=order,
        generator=generator,
        element=[],
        gen_coe=[],
      )
    ],
  )


def make_subgroup(
  group,
  generators,
):
  generators = tuple(
    GroupElement(
      group,
      coefficients,
    )
    for coefficients in generators
  )

  elements = generated_subgroup_elements(
    group,
    generators,
  )

  return Subgroup(
    ambient_group=group,
    elements=elements,
    generators=generators,
  )


def test_toda_bracket_membership_statement():
  x = eta(3)

  bracket = TodaBracket(
    first=nu(4),
    second=sigma(8),
    third=eta(9),
  )

  statement = TodaBracketMembershipStatement(
    element=x,
    bracket=bracket,
  )

  assert statement.element == x
  assert statement.bracket == bracket


def test_toda_bracket_membership_statement_has_structural_equality():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  first = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  second = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  assert first == second


def test_toda_bracket_membership_statement_distinguishes_element():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  first = TodaBracketMembershipStatement(
    element=eta(9),
    bracket=bracket,
  )

  second = TodaBracketMembershipStatement(
    element=nu(9),
    bracket=bracket,
  )

  assert first != second


def test_toda_bracket_membership_statement_distinguishes_bracket():
  element = eta(9)

  first = TodaBracketMembershipStatement(
    element=element,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  second = TodaBracketMembershipStatement(
    element=element,
    bracket=TodaBracket(
      first=eta(3),
      second=sigma(8),
      third=nu(4),
    ),
  )

  assert first != second


def test_toda_bracket_membership_coexists_with_sign_indeterminacy():
  x = eta(9)
  alpha = nu(9)

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  sign_indeterminacy = SignIndeterminacyStatement(
    value=x,
    representative=alpha,
  )

  knowledge = (
    bracket_membership,
    sign_indeterminacy,
  )

  assert bracket_membership in knowledge
  assert sign_indeterminacy in knowledge
  assert bracket_membership.element == sign_indeterminacy.value


def test_toda_bracket_membership_coexists_with_coset_indeterminacy():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  x = eta(9)
  beta = nu(9)

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  coset_membership = CosetMembershipStatement(
    element=x,
    coset=Coset(
      representative=beta,
      subgroup=subgroup,
    ),
  )

  knowledge = (
    bracket_membership,
    coset_membership,
  )

  assert bracket_membership in knowledge
  assert coset_membership in knowledge
  assert bracket_membership.element == coset_membership.element


def test_toda_bracket_membership_does_not_collapse_sign_indeterminacy():
  x = eta(9)
  alpha = nu(9)

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  sign_indeterminacy = SignIndeterminacyStatement(
    value=x,
    representative=alpha,
  )

  assert bracket_membership != sign_indeterminacy
  assert bracket_membership.element == sign_indeterminacy.value


def test_toda_bracket_membership_does_not_collapse_coset_indeterminacy():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  x = eta(9)

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=TodaBracket(
      first=eta(3),
      second=nu(4),
      third=sigma(8),
    ),
  )

  coset_membership = CosetMembershipStatement(
    element=x,
    coset=Coset(
      representative=nu(9),
      subgroup=subgroup,
    ),
  )

  assert bracket_membership != coset_membership
  assert bracket_membership.element == coset_membership.element


def test_phase19_known_epsilon3_toda_membership_fact():
  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  statement = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
  )

  assert statement.element == epsilon_3

  assert statement.bracket == TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  assert statement.bracket.second == (
    Suspension(
      nu_prime,
    )
  )


def test_phase19_known_epsilon3_toda_membership_preserves_provenance():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  statement = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=TodaBracket(
      first=eta(3),
      second=Suspension(
        nu_prime,
      ),
      third=nu(7),
    ),
    source=reference,
    note=(
      "Known Toda membership fact; "
      "Phase 19 stores the current "
      "unindexed projection of "
      "{η_3,Eν′,ν_7}_1."
    ),
  )

  assert statement.source == reference

  assert statement.note == (
    "Known Toda membership fact; "
    "Phase 19 stores the current "
    "unindexed projection of "
    "{η_3,Eν′,ν_7}_1."
  )


def test_phase19_known_toda_membership_proof_step():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  statement = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=TodaBracket(
      first=eta(3),
      second=Suspension(
        nu_prime,
      ),
      third=nu(7),
    ),
    source=reference,
    note=(
      "Known Toda membership fact; "
      "Phase 19 stores the current "
      "unindexed projection."
    ),
  )

  step = toda_bracket_membership_proof_step(
    statement
  )

  assert step.conclusion == statement
  assert step.premises == ()
  assert step.rule == ProofRule.GIVEN
  assert step.inference_rule is None

  assert step.conclusion.source == reference

  assert step.conclusion.note == (
    "Known Toda membership fact; "
    "Phase 19 stores the current "
    "unindexed projection."
  )


def test_toda_bracket_defined_statement():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  statement = TodaBracketDefinedStatement(
    bracket=bracket,
  )

  assert statement.bracket == bracket


def test_toda_bracket_defined_by_zero_compositions():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  second_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  assert match is not None

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  expected = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=a,
      second=b,
      third=c,
    ),
  )

  assert expected in tuple(
    step.conclusion
    for step in result.steps
  )

  derived_step = next(
    step
    for step in result.steps
    if step.conclusion == expected
  )

  assert derived_step.rule == ProofRule.INFERENCE
  assert derived_step.inference_rule == rule
  assert derived_step.premises == (
    first_zero_step,
    second_zero_step,
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_toda_bracket_defined_rule_rejects_mismatched_middle_entry():
  a = eta(3)
  b = nu(4)
  different_b = nu(5)
  c = sigma(8)

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  second_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=different_b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  assert match is None


def test_toda_bracket_defined_rule_requires_both_zero_compositions():
  a = eta(3)
  b = nu(4)

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_zero_step,
    ),
  )

  assert match is None


def test_toda_bracket_defined_from_known_zero_composition_equalities():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="known zero composition",
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="known zero composition",
    )
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
    ),
  )

  first_zero = Relation(
    lhs=Composition(
      left=a,
      right=b,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  second_zero = Relation(
    lhs=Composition(
      left=b,
      right=c,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  defined = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=a,
      second=b,
      third=c,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert first_zero in conclusions
  assert second_zero in conclusions
  assert defined in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_toda_bracket_definedness_provenance_chain():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="first defining zero composition",
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="second defining zero composition",
    )
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
    ),
  )

  first_zero_relation = Relation(
    lhs=Composition(
      left=a,
      right=b,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  second_zero_relation = Relation(
    lhs=Composition(
      left=b,
      right=c,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=a,
      second=b,
      third=c,
    ),
  )

  first_zero_step = next(
    step
    for step in result.steps
    if step.conclusion == first_zero_relation
  )

  second_zero_step = next(
    step
    for step in result.steps
    if step.conclusion == second_zero_relation
  )

  defined_step = next(
    step
    for step in result.steps
    if step.conclusion == defined_statement
  )

  assert first_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert first_zero_step.inference_rule == (
    zero_rule
  )

  assert first_zero_step.premises == (
    first_equality_step,
  )

  assert second_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert second_zero_step.inference_rule == (
    zero_rule
  )

  assert second_zero_step.premises == (
    second_equality_step,
  )

  assert defined_step.rule == (
    ProofRule.INFERENCE
  )

  assert defined_step.inference_rule == (
    defined_rule
  )

  assert defined_step.premises == (
    first_zero_step,
    second_zero_step,
  )

  assert (
    defined_step.premises[0].premises[0]
    == first_equality_step
  )

  assert (
    defined_step.premises[1].premises[0]
    == second_equality_step
  )

  assert (
    first_equality_step.conclusion.source
    == "Toda"
  )

  assert (
    first_equality_step.conclusion.note
    == "first defining zero composition"
  )

  assert (
    second_equality_step.conclusion.source
    == "Toda"
  )

  assert (
    second_equality_step.conclusion.note
    == "second defining zero composition"
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_toda_bracket_definedness_provenance_excludes_unrelated_fact():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="first defining zero composition",
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="second defining zero composition",
    )
  )

  unrelated_step = relation_proof_step(
    Relation(
      lhs=eta(10),
      rhs=nu(11),
      relation_type=RelationType.EQUALITY,
      source="unrelated",
      note="unrelated equality",
    )
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
      unrelated_step,
    ),
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=a,
      second=b,
      third=c,
    ),
  )

  defined_step = next(
    step
    for step in result.steps
    if step.conclusion == defined_statement
  )

  assert unrelated_step not in (
    defined_step.premises
  )

  assert all(
    unrelated_step not in premise.premises
    for premise in defined_step.premises
  )


def test_phase18_representative_toda_bracket_indeterminacy_scenario():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  x = eta(9)
  alpha = nu(9)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="first defining zero composition",
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="second defining zero composition",
    )
  )

  bracket_membership_step = ProofStep(
    conclusion=TodaBracketMembershipStatement(
      element=x,
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_indeterminacy_step = ProofStep(
    conclusion=SignIndeterminacyStatement(
      value=x,
      representative=alpha,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
      bracket_membership_step,
      sign_indeterminacy_step,
    ),
  )

  first_zero = Relation(
    lhs=Composition(
      left=a,
      right=b,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  second_zero = Relation(
    lhs=Composition(
      left=b,
      right=c,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=bracket,
  )

  bracket_membership = TodaBracketMembershipStatement(
    element=x,
    bracket=bracket,
  )

  sign_indeterminacy = SignIndeterminacyStatement(
    value=x,
    representative=alpha,
  )

  selected_value = Relation(
    lhs=x,
    rhs=alpha,
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert first_zero in conclusions
  assert second_zero in conclusions
  assert defined_statement in conclusions

  assert bracket_membership in conclusions
  assert sign_indeterminacy in conclusions

  assert selected_value not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase18_toda_rules_reach_genuine_fixed_point():
  a = eta(3)
  b = nu(4)
  c = sigma(8)

  x = eta(9)
  alpha = nu(9)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="first defining zero composition",
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note="second defining zero composition",
    )
  )

  bracket_membership_step = ProofStep(
    conclusion=TodaBracketMembershipStatement(
      element=x,
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_indeterminacy_step = ProofStep(
    conclusion=SignIndeterminacyStatement(
      value=x,
      representative=alpha,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  rules = (
    zero_rule,
    defined_rule,
  )

  result = run_inference_until_stable_with_history(
    rules,
    (
      first_equality_step,
      second_equality_step,
      bracket_membership_step,
      sign_indeterminacy_step,
    ),
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  terminal_round = derive_inference_round_result(
    rules,
    result.steps,
  )

  assert terminal_round.new_steps == ()


def test_toda_bracket_definedness_does_not_imply_membership():
  a = eta(3)
  b = nu(4)
  c = sigma(8)
  x = eta(9)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  second_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=bracket,
  )

  membership_statement = (
    TodaBracketMembershipStatement(
      element=x,
      bracket=bracket,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert defined_statement in conclusions
  assert membership_statement not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_toda_bracket_membership_does_not_imply_exact_value():
  x = eta(9)
  alpha = nu(9)

  bracket_membership_step = ProofStep(
    conclusion=TodaBracketMembershipStatement(
      element=x,
      bracket=TodaBracket(
        first=eta(3),
        second=nu(4),
        third=sigma(8),
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_indeterminacy_step = ProofStep(
    conclusion=SignIndeterminacyStatement(
      value=x,
      representative=alpha,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable_with_history(
    (),
    (
      bracket_membership_step,
      sign_indeterminacy_step,
    ),
  )

  positive_value = Relation(
    lhs=x,
    rhs=alpha,
    relation_type=RelationType.EQUALITY,
  )

  negative_value = Relation(
    lhs=x,
    rhs=Multiple(
      coefficient=-1,
      expression=alpha,
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert positive_value not in conclusions
  assert negative_value not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_toda_statements_are_outside_generic_equality_scope():
  bracket = TodaBracket(
    first=eta(3),
    second=nu(4),
    third=sigma(8),
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  membership_step = ProofStep(
    conclusion=TodaBracketMembershipStatement(
      element=eta(9),
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = equality_symmetry_inference_rule()

  defined_match = find_inference_match(
    rule,
    (
      defined_step,
    ),
  )

  membership_match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert defined_match is None
  assert membership_match is None


def test_phase19_toda_membership_theorem_statement():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  statement = TodaBracketMembershipTheoremStatement(
    element=epsilon_3,
    bracket=bracket,
    source=reference,
    note=(
      "Literature-backed theorem for "
      "the current unindexed projection "
      "of {η_3,Eν′,ν_7}_1."
    ),
  )

  assert statement.element == epsilon_3
  assert statement.bracket == bracket
  assert statement.source == reference

  assert statement.note == (
    "Literature-backed theorem for "
    "the current unindexed projection "
    "of {η_3,Eν′,ν_7}_1."
  )

  assert not isinstance(
    statement,
    TodaBracketMembershipStatement,
  )


def test_phase19_toda_membership_theorem_bridge():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  theorem_statement = (
    TodaBracketMembershipTheoremStatement(
      element=epsilon_3,
      bracket=bracket,
      source=reference,
      note=(
        "Literature-backed theorem for "
        "the current unindexed projection."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      theorem_statement
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert match is not None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  expected = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
    source=reference,
    note=(
      "Literature-backed theorem for "
      "the current unindexed projection."
    ),
  )

  derived_step = next(
    step
    for step in result.steps
    if step.conclusion == expected
  )

  assert derived_step.rule == ProofRule.INFERENCE
  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    theorem_step,
    defined_step,
  )

  assert derived_step.conclusion.source == reference

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase19_toda_membership_theorem_bridge_rejects_different_bracket():
  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  theorem_bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  different_bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=sigma(8),
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=theorem_bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=different_bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert match is None


def test_phase19_toda_membership_theorem_does_not_imply_membership_without_definedness():
  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
      )
    )
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
    ),
  )

  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase19_toda_membership_multi_round_from_defining_compositions():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  a = eta(3)

  b = Suspension(
    nu_prime,
  )

  c = nu(7)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "First defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "Second defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
        source=reference,
        note=(
          "Literature-backed theorem for "
          "the current unindexed projection "
          "of {η_3,Eν′,ν_7}_1."
        ),
      )
    )
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
      membership_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
      theorem_step,
    ),
  )

  first_zero = Relation(
    lhs=Composition(
      left=a,
      right=b,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  second_zero = Relation(
    lhs=Composition(
      left=b,
      right=c,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=bracket,
  )

  membership_statement = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
    source=reference,
    note=(
      "Literature-backed theorem for "
      "the current unindexed projection "
      "of {η_3,Eν′,ν_7}_1."
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert first_zero in conclusions
  assert second_zero in conclusions
  assert defined_statement in conclusions
  assert membership_statement in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3


def test_phase19_theorem_derived_toda_membership_coexists_with_sign_indeterminacy():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  a = eta(3)

  b = Suspension(
    nu_prime,
  )

  c = nu(7)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "First defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "Second defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
        source=reference,
        note=(
          "Literature-backed theorem for "
          "the current unindexed projection "
          "of {η_3,Eν′,ν_7}_1."
        ),
      )
    )
  )

  sign_step = ProofStep(
    conclusion=SignIndeterminacyStatement(
      value=epsilon_3,
      representative=alpha,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
      membership_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
      theorem_step,
      sign_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
    source=reference,
    note=(
      "Literature-backed theorem for "
      "the current unindexed projection "
      "of {η_3,Eν′,ν_7}_1."
    ),
  )

  sign_indeterminacy = SignIndeterminacyStatement(
    value=epsilon_3,
    representative=alpha,
  )

  positive_value = Relation(
    lhs=epsilon_3,
    rhs=alpha,
    relation_type=RelationType.EQUALITY,
  )

  negative_value = Relation(
    lhs=epsilon_3,
    rhs=Multiple(
      coefficient=-1,
      expression=alpha,
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership in conclusions
  assert sign_indeterminacy in conclusions

  assert positive_value not in conclusions
  assert negative_value not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3


def test_phase19_theorem_derived_toda_membership_coexists_with_coset_indeterminacy():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  a = eta(3)

  b = Suspension(
    nu_prime,
  )

  c = nu(7)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "First defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "Second defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
        source=reference,
        note=(
          "Literature-backed theorem for "
          "the current unindexed projection "
          "of {η_3,Eν′,ν_7}_1."
        ),
      )
    )
  )

  coset_step = ProofStep(
    conclusion=CosetMembershipStatement(
      element=epsilon_3,
      coset=Coset(
        representative=beta,
        subgroup=subgroup,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
      membership_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
      theorem_step,
      coset_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
    source=reference,
    note=(
      "Literature-backed theorem for "
      "the current unindexed projection "
      "of {η_3,Eν′,ν_7}_1."
    ),
  )

  coset_membership = CosetMembershipStatement(
    element=epsilon_3,
    coset=Coset(
      representative=beta,
      subgroup=subgroup,
    ),
  )

  selected_representative = Relation(
    lhs=epsilon_3,
    rhs=beta,
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership in conclusions
  assert coset_membership in conclusions

  assert selected_representative not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3


def test_phase19_theorem_derived_toda_membership_does_not_create_indeterminacy():
  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    membership_rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
  )

  sign_indeterminacy = SignIndeterminacyStatement(
    value=epsilon_3,
    representative=alpha,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership in conclusions
  assert sign_indeterminacy not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase19_toda_membership_full_provenance_chain():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  a = eta(3)

  b = Suspension(
    nu_prime,
  )

  c = nu(7)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "First defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "Second defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  theorem_statement = (
    TodaBracketMembershipTheoremStatement(
      element=epsilon_3,
      bracket=bracket,
      source=reference,
      note=(
        "Literature-backed theorem for "
        "the current unindexed projection "
        "of {η_3,Eν′,ν_7}_1."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      theorem_statement
    )
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
      membership_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
      theorem_step,
    ),
  )

  first_zero_relation = Relation(
    lhs=Composition(
      left=a,
      right=b,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  second_zero_relation = Relation(
    lhs=Composition(
      left=b,
      right=c,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=bracket,
  )

  membership_statement = (
    TodaBracketMembershipStatement(
      element=epsilon_3,
      bracket=bracket,
      source=reference,
      note=(
        "Literature-backed theorem for "
        "the current unindexed projection "
        "of {η_3,Eν′,ν_7}_1."
      ),
    )
  )

  first_zero_step = next(
    step
    for step in result.steps
    if step.conclusion == first_zero_relation
  )

  second_zero_step = next(
    step
    for step in result.steps
    if step.conclusion == second_zero_relation
  )

  defined_step = next(
    step
    for step in result.steps
    if step.conclusion == defined_statement
  )

  membership_step = next(
    step
    for step in result.steps
    if step.conclusion == membership_statement
  )

  assert first_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert first_zero_step.inference_rule == (
    zero_rule
  )

  assert first_zero_step.premises == (
    first_equality_step,
  )

  assert second_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert second_zero_step.inference_rule == (
    zero_rule
  )

  assert second_zero_step.premises == (
    second_equality_step,
  )

  assert defined_step.rule == (
    ProofRule.INFERENCE
  )

  assert defined_step.inference_rule == (
    defined_rule
  )

  assert defined_step.premises == (
    first_zero_step,
    second_zero_step,
  )

  assert membership_step.rule == (
    ProofRule.INFERENCE
  )

  assert membership_step.inference_rule == (
    membership_rule
  )

  assert membership_step.premises == (
    theorem_step,
    defined_step,
  )

  assert theorem_step.rule == (
    ProofRule.GIVEN
  )

  assert theorem_step.premises == ()

  assert theorem_step.conclusion.source == (
    reference
  )

  assert theorem_step.conclusion.note == (
    "Literature-backed theorem for "
    "the current unindexed projection "
    "of {η_3,Eν′,ν_7}_1."
  )

  assert (
    membership_step.premises[1]
    .premises[0]
    .premises[0]
    == first_equality_step
  )

  assert (
    membership_step.premises[1]
    .premises[1]
    .premises[0]
    == second_equality_step
  )

  assert (
    first_equality_step.conclusion.source
    == "Toda"
  )

  assert (
    second_equality_step.conclusion.source
    == "Toda"
  )

  assert membership_step.conclusion.source == (
    reference
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3


def test_phase19_toda_membership_provenance_excludes_unrelated_fact():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  a = eta(3)

  b = Suspension(
    nu_prime,
  )

  c = nu(7)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "First defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "Second defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
        source=reference,
        note=(
          "Literature-backed theorem for "
          "the current unindexed projection."
        ),
      )
    )
  )

  unrelated_step = relation_proof_step(
    Relation(
      lhs=eta(10),
      rhs=nu(11),
      relation_type=RelationType.EQUALITY,
      source="unrelated",
      note="unrelated equality",
    )
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
      membership_rule,
    ),
    (
      first_equality_step,
      second_equality_step,
      theorem_step,
      unrelated_step,
    ),
  )

  membership_statement = (
    TodaBracketMembershipStatement(
      element=epsilon_3,
      bracket=bracket,
      source=reference,
      note=(
        "Literature-backed theorem for "
        "the current unindexed projection."
      ),
    )
  )

  membership_step = next(
    step
    for step in result.steps
    if step.conclusion == membership_statement
  )

  theorem_premise = (
    membership_step.premises[0]
  )

  defined_premise = (
    membership_step.premises[1]
  )

  first_zero_premise = (
    defined_premise.premises[0]
  )

  second_zero_premise = (
    defined_premise.premises[1]
  )

  assert unrelated_step not in (
    membership_step.premises
  )

  assert unrelated_step not in (
    theorem_premise.premises
  )

  assert unrelated_step not in (
    defined_premise.premises
  )

  assert unrelated_step not in (
    first_zero_premise.premises
  )

  assert unrelated_step not in (
    second_zero_premise.premises
  )

  assert (
    first_zero_premise.premises
    == (
      first_equality_step,
    )
  )

  assert (
    second_zero_premise.premises
    == (
      second_equality_step,
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase19_representative_toda_membership_scenario():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  a = eta(3)

  b = Suspension(
    nu_prime,
  )

  c = nu(7)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "First defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "Second defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
        source=reference,
        note=(
          "Literature-backed theorem for "
          "the current unindexed projection "
          "of {η_3,Eν′,ν_7}_1."
        ),
      )
    )
  )

  sign_step = ProofStep(
    conclusion=SignIndeterminacyStatement(
      value=epsilon_3,
      representative=alpha,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  coset_step = ProofStep(
    conclusion=CosetMembershipStatement(
      element=epsilon_3,
      coset=Coset(
        representative=beta,
        subgroup=subgroup,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  rules = (
    zero_rule,
    defined_rule,
    membership_rule,
  )

  result = run_inference_until_stable_with_history(
    rules,
    (
      first_equality_step,
      second_equality_step,
      theorem_step,
      sign_step,
      coset_step,
    ),
  )

  first_zero = Relation(
    lhs=Composition(
      left=a,
      right=b,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  second_zero = Relation(
    lhs=Composition(
      left=b,
      right=c,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=bracket,
  )

  membership_statement = (
    TodaBracketMembershipStatement(
      element=epsilon_3,
      bracket=bracket,
      source=reference,
      note=(
        "Literature-backed theorem for "
        "the current unindexed projection "
        "of {η_3,Eν′,ν_7}_1."
      ),
    )
  )

  sign_indeterminacy = SignIndeterminacyStatement(
    value=epsilon_3,
    representative=alpha,
  )

  coset_indeterminacy = CosetMembershipStatement(
    element=epsilon_3,
    coset=Coset(
      representative=beta,
      subgroup=subgroup,
    ),
  )

  positive_value = Relation(
    lhs=epsilon_3,
    rhs=alpha,
    relation_type=RelationType.EQUALITY,
  )

  negative_value = Relation(
    lhs=epsilon_3,
    rhs=Multiple(
      coefficient=-1,
      expression=alpha,
    ),
    relation_type=RelationType.EQUALITY,
  )

  coset_representative_value = Relation(
    lhs=epsilon_3,
    rhs=beta,
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert first_zero in conclusions
  assert second_zero in conclusions

  assert defined_statement in conclusions
  assert membership_statement in conclusions

  assert sign_indeterminacy in conclusions
  assert coset_indeterminacy in conclusions

  assert positive_value not in conclusions
  assert negative_value not in conclusions
  assert coset_representative_value not in conclusions

  membership_step = next(
    step
    for step in result.steps
    if step.conclusion == membership_statement
  )

  defined_step = next(
    step
    for step in result.steps
    if step.conclusion == defined_statement
  )

  assert membership_step.rule == (
    ProofRule.INFERENCE
  )

  assert membership_step.inference_rule == (
    membership_rule
  )

  assert membership_step.premises == (
    theorem_step,
    defined_step,
  )

  assert sign_step not in (
    membership_step.premises
  )

  assert coset_step not in (
    membership_step.premises
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3


def test_phase19_toda_rules_reach_genuine_fixed_point():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  a = eta(3)

  b = Suspension(
    nu_prime,
  )

  c = nu(7)

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=a,
        right=b,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "First defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=b,
        right=c,
      ),
      rhs=Zero(),
      relation_type=RelationType.EQUALITY,
      source="Toda",
      note=(
        "Second defining zero composition "
        "for the epsilon_3 Toda bracket."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
        source=reference,
        note=(
          "Literature-backed theorem for "
          "the current unindexed projection "
          "of {η_3,Eν′,ν_7}_1."
        ),
      )
    )
  )

  sign_step = ProofStep(
    conclusion=SignIndeterminacyStatement(
      value=epsilon_3,
      representative=alpha,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  coset_step = ProofStep(
    conclusion=CosetMembershipStatement(
      element=epsilon_3,
      coset=Coset(
        representative=beta,
        subgroup=subgroup,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  rules = (
    zero_rule,
    defined_rule,
    membership_rule,
  )

  result = run_inference_until_stable_with_history(
    rules,
    (
      first_equality_step,
      second_equality_step,
      theorem_step,
      sign_step,
      coset_step,
    ),
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3

  terminal_round = derive_inference_round_result(
    rules,
    result.steps,
  )

  assert terminal_round.new_steps == ()


def test_phase19_toda_theorem_statement_is_outside_generic_equality_scope():
  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
        source="Toda",
        note=(
          "Literature-backed theorem for "
          "the current unindexed projection."
        ),
      )
    )
  )

  rule = equality_symmetry_inference_rule()

  match = find_inference_match(
    rule,
    (
      theorem_step,
    ),
  )

  assert match is None


def test_phase20_actual_epsilon3_toda_fact_preserves_index_one():
  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  statement = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
  )

  assert statement.element == epsilon_3

  assert statement.bracket == TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  assert statement.bracket.index == 1

  assert statement.bracket.second == (
    Suspension(
      nu_prime,
    )
  )


def test_phase20_actual_epsilon3_membership_fact_preserves_index():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  statement = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=TodaBracket(
      first=eta(3),
      second=Suspension(
        nu_prime,
      ),
      third=nu(7),
      index=1,
    ),
    source=reference,
    note=(
      "Known Toda membership fact "
      "{η_3,Eν′,ν_7}_1."
    ),
  )

  step = toda_bracket_membership_proof_step(
    statement
  )

  assert step.conclusion == statement
  assert step.conclusion.bracket.index == 1
  assert step.conclusion.source == reference

  assert step.conclusion.note == (
    "Known Toda membership fact "
    "{η_3,Eν′,ν_7}_1."
  )

  assert step.premises == ()
  assert step.rule == ProofRule.GIVEN
  assert step.inference_rule is None


def test_phase20_actual_epsilon3_theorem_fact_preserves_index():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  theorem = TodaBracketMembershipTheoremStatement(
    element=epsilon_3,
    bracket=TodaBracket(
      first=eta(3),
      second=Suspension(
        nu_prime,
      ),
      third=nu(7),
      index=1,
    ),
    source=reference,
    note=(
      "Literature-backed theorem for "
      "{η_3,Eν′,ν_7}_1."
    ),
  )

  step = (
    toda_bracket_membership_theorem_proof_step(
      theorem
    )
  )

  assert step.conclusion == theorem
  assert step.conclusion.bracket.index == 1
  assert step.conclusion.source == reference

  assert step.conclusion.note == (
    "Literature-backed theorem for "
    "{η_3,Eν′,ν_7}_1."
  )

  assert step.premises == ()
  assert step.rule == ProofRule.GIVEN
  assert step.inference_rule is None


def test_phase20_actual_epsilon3_indexed_bracket_is_not_unindexed_projection():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  indexed = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  unindexed = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
  )

  assert indexed.index == 1
  assert unindexed.index is None
  assert indexed != unindexed


def test_phase20_indexed_epsilon3_definedness_uses_underlying_compositions():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  first_condition = Relation(
    lhs=Composition(
      left=eta(3),
      right=Suspension(
        nu_prime,
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.EQUALITY,
  )

  second_condition = Relation(
    lhs=Composition(
      left=nu_prime,
      right=nu(6),
    ),
    rhs=Zero(),
    relation_type=RelationType.EQUALITY,
  )

  assert bracket.index == 1

  assert first_condition.lhs == Composition(
    left=eta(3),
    right=Suspension(
      nu_prime,
    ),
  )

  assert second_condition.lhs == Composition(
    left=nu_prime,
    right=nu(6),
  )

  assert second_condition.lhs != Composition(
    left=Suspension(
      nu_prime,
    ),
    right=nu(7),
  )


def test_phase20_current_unindexed_definedness_rule_does_not_match_indexed_conditions():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=eta(3),
        right=Suspension(
          nu_prime,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  second_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=nu_prime,
        right=nu(6),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  assert match is None


def test_phase20_adjacent_displayed_entries_do_not_establish_indexed_definedness():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  suspended_nu_prime = Suspension(
    nu_prime,
  )

  first_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=eta(3),
        right=suspended_nu_prime,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  second_zero_step = relation_proof_step(
    Relation(
      lhs=Composition(
        left=suspended_nu_prime,
        right=nu(7),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  unindexed_definedness = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=eta(3),
      second=suspended_nu_prime,
      third=nu(7),
    ),
  )

  indexed_definedness = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=eta(3),
      second=suspended_nu_prime,
      third=nu(7),
      index=1,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert unindexed_definedness in conclusions
  assert indexed_definedness not in conclusions


def test_phase21_8_type_compatibility_alone_does_not_establish_toda_definedness():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=5,
    source=7,
    target=5,
  )

  c = HomotopyElement(
    name="c",
    dimension=7,
    source=9,
    target=7,
  )

  bracket = TodaBracket(
    first=a,
    second=b,
    third=c,
  )

  assert (
    bracket
    .are_defining_compositions_type_compatible()
  )

  first_zero = Relation(
    lhs=Composition(
      left=a,
      right=b,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  second_zero = Relation(
    lhs=Composition(
      left=b,
      right=c,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  defined_statement = TodaBracketDefinedStatement(
    bracket=bracket,
  )

  zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      zero_rule,
      defined_rule,
    ),
    (),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert first_zero not in conclusions
  assert second_zero not in conclusions
  assert defined_statement not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_1_indexed_toda_theorem_fact_preserves_full_bracket():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="ε",
      index=3,
    ),
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
  )

  bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  statement = TodaBracketMembershipTheoremStatement(
    element=epsilon_3,
    bracket=bracket,
    source=reference,
    note=(
      "Literature-backed indexed Toda theorem fact "
      "for {η₃,Eν′,ν₇}_1."
    ),
  )

  assert statement.element == epsilon_3
  assert statement.bracket == bracket
  assert statement.bracket.index == 1
  assert statement.bracket.first == eta_3
  assert statement.bracket.second == Suspension(
    expression=nu_prime,
  )
  assert statement.bracket.third == nu_7
  assert statement.source == reference

  assert statement.note == (
    "Literature-backed indexed Toda theorem fact "
    "for {η₃,Eν′,ν₇}_1."
  )

  assert not isinstance(
    statement,
    TodaBracketMembershipStatement,
  )


def test_phase23_2_indexed_toda_theorem_bridge_matches_same_index():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=TodaBracket(
        first=eta(3),
        second=Suspension(
          expression=nu_prime,
        ),
        third=nu(7),
        index=1,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert match is not None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership in conclusions

  derived_step = next(
    step
    for step in result.steps
    if step.conclusion == membership
  )

  assert derived_step.premises == (
    theorem_step,
    defined_step,
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_2_indexed_toda_theorem_bridge_rejects_different_index():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  theorem_bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  defined_bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu(7),
    index=2,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=theorem_bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=defined_bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert theorem_bracket.index == 1
  assert defined_bracket.index == 2
  assert theorem_bracket != defined_bracket
  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=theorem_bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_2_indexed_toda_theorem_bridge_rejects_unindexed_bracket():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  indexed_bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu(7),
    index=1,
  )

  unindexed_bracket = TodaBracket(
    first=eta(3),
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu(7),
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=indexed_bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=unindexed_bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert indexed_bracket.index == 1
  assert unindexed_bracket.index is None
  assert indexed_bracket != unindexed_bracket
  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=indexed_bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_3_indexed_toda_theorem_bridge_matches_same_generator_structure():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="ε",
      index=3,
    ),
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
  )

  theorem_bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  defined_bracket = TodaBracket(
    first=HomotopyElement(
      name="η₃",
      dimension=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    ),
    second=Suspension(
      expression=HomotopyElement(
        name="ν′",
        dimension=3,
        generator=GeneratorSymbol(
          family="ν",
          decoration="′",
        ),
      ),
    ),
    third=HomotopyElement(
      name="ν₇",
      dimension=7,
      generator=GeneratorSymbol(
        family="ν",
        index=7,
      ),
    ),
    index=1,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=theorem_bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=defined_bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert theorem_bracket == defined_bracket
  assert match is not None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=theorem_bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_3_indexed_toda_theorem_bridge_rejects_generator_family_mismatch():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
  )

  theorem_eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  different_eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="μ",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
  )

  theorem_bracket = TodaBracket(
    first=theorem_eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  defined_bracket = TodaBracket(
    first=different_eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=theorem_bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=defined_bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert theorem_eta_3.name == different_eta_3.name
  assert theorem_eta_3.dimension == different_eta_3.dimension
  assert theorem_eta_3.generator != different_eta_3.generator

  assert theorem_bracket != defined_bracket
  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=theorem_bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_3_indexed_toda_theorem_bridge_rejects_generator_decoration_mismatch():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  theorem_nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  different_nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
    ),
  )

  nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
  )

  theorem_bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=theorem_nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  defined_bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=different_nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=theorem_bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=defined_bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert theorem_nu_prime.name == (
    different_nu_prime.name
  )

  assert theorem_nu_prime.dimension == (
    different_nu_prime.dimension
  )

  assert theorem_nu_prime.generator != (
    different_nu_prime.generator
  )

  assert theorem_bracket != defined_bracket
  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=theorem_bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_3_indexed_toda_theorem_bridge_rejects_generator_index_mismatch():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  theorem_nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
  )

  different_nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=8,
    ),
  )

  theorem_bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=theorem_nu_7,
    index=1,
  )

  defined_bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=different_nu_7,
    index=1,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=theorem_bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=defined_bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert theorem_nu_7.name == different_nu_7.name
  assert theorem_nu_7.dimension == (
    different_nu_7.dimension
  )

  assert theorem_nu_7.generator != (
    different_nu_7.generator
  )

  assert theorem_bracket != defined_bracket
  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=theorem_bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_4_indexed_theorem_requires_definedness():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="ε",
      index=3,
    ),
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
  )

  bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=epsilon_3,
        bracket=bracket,
      )
    )
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
    ),
  )

  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_4_indexed_theorem_and_definedness_derive_membership():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="ε",
      index=3,
    ),
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
  )

  bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  theorem_statement = (
    TodaBracketMembershipTheoremStatement(
      element=epsilon_3,
      bracket=bracket,
      source=reference,
      note=(
        "Literature-backed indexed Toda theorem fact "
        "for {η₃,Eν′,ν₇}_1."
      ),
    )
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      theorem_statement
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert match is not None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
    source=reference,
    note=(
      "Literature-backed indexed Toda theorem fact "
      "for {η₃,Eν′,ν₇}_1."
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership in conclusions

  derived_step = next(
    step
    for step in result.steps
    if step.conclusion == membership
  )

  assert derived_step.rule == ProofRule.INFERENCE

  assert derived_step.inference_rule == (
    rule
  )

  assert derived_step.premises == (
    theorem_step,
    defined_step,
  )

  assert derived_step.conclusion.bracket.index == 1

  assert derived_step.conclusion.source == (
    reference
  )

  assert derived_step.conclusion.note == (
    "Literature-backed indexed Toda theorem fact "
    "for {η₃,Eν′,ν₇}_1."
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_4_indexed_definedness_alone_does_not_derive_membership():
  epsilon_3 = HomotopyElement(
    name="ε₃",
    dimension=3,
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  nu_7 = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
  )

  bracket = TodaBracket(
    first=eta_3,
    second=Suspension(
      expression=nu_prime,
    ),
    third=nu_7,
    index=1,
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      defined_step,
    ),
  )

  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=epsilon_3,
    bracket=bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_5_consistent_indexed_data_allows_theorem_bridge():
  x = HomotopyElement(
    name="x",
    dimension=10,
  )

  a = HomotopyElement(
    name="a",
    dimension=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=4,
  )

  c = HomotopyElement(
    name="c",
    dimension=5,
  )

  bracket = TodaBracket(
    first=a,
    second=IteratedSuspension(
      expression=b,
      exponent=2,
    ),
    third=IteratedSuspension(
      expression=c,
      exponent=2,
    ),
    index=2,
  )

  indexed_data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=b,
    third_base=c,
    suspension_exponent=2,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=x,
        bracket=bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    indexed_toda_bracket_membership_from_theorem_inference_rule(
      indexed_data
    )
  )

  assert indexed_data.is_consistent()

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert match is not None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=x,
    bracket=bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership in conclusions

  derived_step = next(
    step
    for step in result.steps
    if step.conclusion == membership
  )

  assert derived_step.premises == (
    theorem_step,
    defined_step,
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_5_index_mismatch_rejects_indexed_theorem_bridge():
  x = HomotopyElement(
    name="x",
    dimension=10,
  )

  a = HomotopyElement(
    name="a",
    dimension=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=4,
  )

  c = HomotopyElement(
    name="c",
    dimension=5,
  )

  bracket = TodaBracket(
    first=a,
    second=IteratedSuspension(
      expression=b,
      exponent=2,
    ),
    third=IteratedSuspension(
      expression=c,
      exponent=2,
    ),
    index=1,
  )

  indexed_data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=b,
    third_base=c,
    suspension_exponent=2,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=x,
        bracket=bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    indexed_toda_bracket_membership_from_theorem_inference_rule(
      indexed_data
    )
  )

  assert theorem_step.conclusion.bracket == (
    defined_step.conclusion.bracket
  )

  assert not indexed_data.is_consistent()

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=x,
    bracket=bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase23_5_entry_mismatch_rejects_indexed_theorem_bridge():
  x = HomotopyElement(
    name="x",
    dimension=10,
  )

  a = HomotopyElement(
    name="a",
    dimension=3,
  )

  b = HomotopyElement(
    name="b",
    dimension=4,
  )

  different_b = HomotopyElement(
    name="different-b",
    dimension=4,
  )

  c = HomotopyElement(
    name="c",
    dimension=5,
  )

  bracket = TodaBracket(
    first=a,
    second=IteratedSuspension(
      expression=different_b,
      exponent=2,
    ),
    third=IteratedSuspension(
      expression=c,
      exponent=2,
    ),
    index=2,
  )

  indexed_data = IndexedTodaBracketData(
    bracket=bracket,
    second_base=b,
    third_base=c,
    suspension_exponent=2,
  )

  theorem_step = (
    toda_bracket_membership_theorem_proof_step(
      TodaBracketMembershipTheoremStatement(
        element=x,
        bracket=bracket,
      )
    )
  )

  defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=bracket,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    indexed_toda_bracket_membership_from_theorem_inference_rule(
      indexed_data
    )
  )

  assert theorem_step.conclusion.bracket == (
    defined_step.conclusion.bracket
  )

  assert bracket.index == 2
  assert indexed_data.suspension_exponent == 2

  assert not indexed_data.is_consistent()

  match = find_inference_match(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  assert match is None

  result = run_inference_until_stable_with_history(
    rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  membership = TodaBracketMembershipStatement(
    element=x,
    bracket=bracket,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )




