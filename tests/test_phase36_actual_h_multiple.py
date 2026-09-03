from expression import (
  MapApplication,
  Multiple,
)
from homomorphism_rules import (
  HomomorphismStatement,
  homomorphism_preserves_multiple_inference_rule,
)
from hopf_facts import (
  ETA_2,
  ETA_2_HOPF_INVARIANT_FACT,
  IOTA_3,
)
from hopf_rules import (
  ehp_h_homomorphism_proof_step,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
)
from map_facts import (
  EHP_H_MAP,
  EHP_H_MAP_ISOMORPHISM_FACT,
)
from map_property_rules import (
  IsomorphismStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_preserved_under_multiple_inference_rule,
  equality_transitivity_inference_rule,
)


def test_phase36_1_four_eta_2_is_representable_as_multiple():
  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  assert four_eta_2 == Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  assert four_eta_2.coefficient == 4
  assert four_eta_2.expression == ETA_2


def test_phase36_1_generic_multiple_rule_accepts_explicit_actual_h_homomorphism():
  homomorphism_step = ProofStep(
    conclusion=HomomorphismStatement(
      map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=4,
      expression=ETA_2,
    )
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Multiple(
        coefficient=4,
        expression=ETA_2,
      ),
    ),
    rhs=Multiple(
      coefficient=4,
      expression=MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_phase36_1_actual_h_isomorphism_fact_materializes_as_isomorphism_not_homomorphism():
  step = (
    EHP_H_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  assert step.conclusion == (
    IsomorphismStatement(
      map=EHP_H_MAP,
    )
  )

  assert step.conclusion != (
    HomomorphismStatement(
      map=EHP_H_MAP,
    )
  )


def test_phase36_1_multiple_rule_does_not_accept_actual_h_isomorphism_directly():
  isomorphism_step = (
    EHP_H_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=4,
      expression=ETA_2,
    )
  )

  match = find_inference_match(
    rule,
    (
      isomorphism_step,
    ),
  )

  assert match is None


def test_phase36_2_actual_h_homomorphism_materializes_as_given_proof_step():
  step = (
    ehp_h_homomorphism_proof_step()
  )

  assert step.conclusion == (
    HomomorphismStatement(
      map=EHP_H_MAP,
    )
  )

  assert step.rule == ProofRule.GIVEN
  assert step.premises == ()
  assert step.inference_rule is None

  assert step.conclusion.map is (
    EHP_H_MAP
  )


def test_phase36_2_actual_h_homomorphism_connects_to_generic_multiple_rule():
  homomorphism_step = (
    ehp_h_homomorphism_proof_step()
  )

  rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=4,
      expression=ETA_2,
    )
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
    ),
  )

  assert match is not None


def test_phase36_3_h_four_eta_2_equals_four_h_eta_2():
  homomorphism_step = (
    ehp_h_homomorphism_proof_step()
  )

  rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=4,
      expression=ETA_2,
    )
  )

  match = find_inference_match(
    rule,
    (
      homomorphism_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Multiple(
        coefficient=4,
        expression=ETA_2,
      ),
    ),
    rhs=Multiple(
      coefficient=4,
      expression=MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule == rule

  assert step.premises == (
    homomorphism_step,
  )


def test_phase36_4_h_eta_2_equality_substitutes_under_four_multiple():
  hopf_fact_step = (
    hopf_invariant_proof_step(
      ETA_2_HOPF_INVARIANT_FACT
    )
  )

  bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  bridge_match = find_inference_match(
    bridge_rule,
    (
      hopf_fact_step,
    ),
  )

  assert bridge_match is not None

  h_eta_2_step = apply_inference_match(
    bridge_match
  )

  assert h_eta_2_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=ETA_2,
    ),
    rhs=IOTA_3,
    relation_type=RelationType.EQUALITY,
  )

  multiple_rule = (
    equality_preserved_under_multiple_inference_rule(
      coefficient=4,
    )
  )

  multiple_match = find_inference_match(
    multiple_rule,
    (
      h_eta_2_step,
    ),
  )

  assert multiple_match is not None

  step = apply_inference_match(
    multiple_match
  )

  assert step.conclusion == Relation(
    lhs=Multiple(
      coefficient=4,
      expression=MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    ),
    rhs=Multiple(
      coefficient=4,
      expression=IOTA_3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule == (
    multiple_rule
  )

  assert step.premises == (
    h_eta_2_step,
  )

  assert (
    h_eta_2_step.premises
    == (
      hopf_fact_step,
    )
  )

  assert (
    hopf_fact_step.conclusion.source
    == ETA_2_HOPF_INVARIANT_FACT.source
  )


def test_phase36_5_h_four_eta_2_equals_four_iota_3_by_transitivity():
  homomorphism_step = (
    ehp_h_homomorphism_proof_step()
  )

  h_multiple_rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=4,
      expression=ETA_2,
    )
  )

  h_multiple_match = find_inference_match(
    h_multiple_rule,
    (
      homomorphism_step,
    ),
  )

  assert h_multiple_match is not None

  h_four_eta_2_step = (
    apply_inference_match(
      h_multiple_match
    )
  )

  assert h_four_eta_2_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Multiple(
        coefficient=4,
        expression=ETA_2,
      ),
    ),
    rhs=Multiple(
      coefficient=4,
      expression=MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  hopf_fact_step = (
    hopf_invariant_proof_step(
      ETA_2_HOPF_INVARIANT_FACT
    )
  )

  hopf_bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  hopf_bridge_match = find_inference_match(
    hopf_bridge_rule,
    (
      hopf_fact_step,
    ),
  )

  assert hopf_bridge_match is not None

  h_eta_2_step = apply_inference_match(
    hopf_bridge_match
  )

  multiple_rule = (
    equality_preserved_under_multiple_inference_rule(
      coefficient=4,
    )
  )

  multiple_match = find_inference_match(
    multiple_rule,
    (
      h_eta_2_step,
    ),
  )

  assert multiple_match is not None

  four_h_eta_2_step = (
    apply_inference_match(
      multiple_match
    )
  )

  assert four_h_eta_2_step.conclusion == Relation(
    lhs=Multiple(
      coefficient=4,
      expression=MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    ),
    rhs=Multiple(
      coefficient=4,
      expression=IOTA_3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      h_four_eta_2_step,
      four_h_eta_2_step,
    ),
  )

  assert transitivity_match is not None

  final_step = apply_inference_match(
    transitivity_match
  )

  assert final_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Multiple(
        coefficient=4,
        expression=ETA_2,
      ),
    ),
    rhs=Multiple(
      coefficient=4,
      expression=IOTA_3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert final_step.inference_rule == (
    transitivity_rule
  )

  assert final_step.premises == (
    h_four_eta_2_step,
    four_h_eta_2_step,
  )


def test_phase36_6_h_four_eta_2_equals_four_iota_3_end_to_end():
  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  four_iota_3 = Multiple(
    coefficient=4,
    expression=IOTA_3,
  )

  homomorphism_step = (
    ehp_h_homomorphism_proof_step()
  )

  assert homomorphism_step.conclusion == (
    HomomorphismStatement(
      map=EHP_H_MAP,
    )
  )

  h_multiple_rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=4,
      expression=ETA_2,
    )
  )

  h_multiple_match = find_inference_match(
    h_multiple_rule,
    (
      homomorphism_step,
    ),
  )

  assert h_multiple_match is not None

  h_four_eta_2_step = (
    apply_inference_match(
      h_multiple_match
    )
  )

  assert h_four_eta_2_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    rhs=Multiple(
      coefficient=4,
      expression=MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  hopf_fact_step = (
    hopf_invariant_proof_step(
      ETA_2_HOPF_INVARIANT_FACT
    )
  )

  hopf_bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  hopf_bridge_match = find_inference_match(
    hopf_bridge_rule,
    (
      hopf_fact_step,
    ),
  )

  assert hopf_bridge_match is not None

  h_eta_2_step = (
    apply_inference_match(
      hopf_bridge_match
    )
  )

  assert h_eta_2_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=ETA_2,
    ),
    rhs=IOTA_3,
    relation_type=RelationType.EQUALITY,
  )

  multiple_rule = (
    equality_preserved_under_multiple_inference_rule(
      coefficient=4,
    )
  )

  multiple_match = find_inference_match(
    multiple_rule,
    (
      h_eta_2_step,
    ),
  )

  assert multiple_match is not None

  four_h_eta_2_step = (
    apply_inference_match(
      multiple_match
    )
  )

  assert four_h_eta_2_step.conclusion == Relation(
    lhs=Multiple(
      coefficient=4,
      expression=MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  final_match = find_inference_match(
    transitivity_rule,
    (
      h_four_eta_2_step,
      four_h_eta_2_step,
    ),
  )

  assert final_match is not None

  final_step = apply_inference_match(
    final_match
  )

  assert final_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert final_step.inference_rule == (
    transitivity_rule
  )

  assert final_step.premises == (
    h_four_eta_2_step,
    four_h_eta_2_step,
  )

  assert h_four_eta_2_step.premises == (
    homomorphism_step,
  )

  assert four_h_eta_2_step.premises == (
    h_eta_2_step,
  )

  assert h_eta_2_step.premises == (
    hopf_fact_step,
  )

  assert (
    hopf_fact_step.conclusion.source
    == ETA_2_HOPF_INVARIANT_FACT.source
  )







