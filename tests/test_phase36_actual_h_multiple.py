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
)
from hopf_rules import (
  ehp_h_homomorphism_proof_step,
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






