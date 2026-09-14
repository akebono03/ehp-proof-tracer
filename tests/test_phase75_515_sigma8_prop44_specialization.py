from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase75_lemma514_sigma8 import (
  build_phase75_8a_data,
)
from toda_rules import (
  Toda515Sigma8Prop44SpecializationStatement,
  TodaLemma514Sigma8Statement,
  toda_prop515_sigma8_prop44_specialization_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_8e1_data():
  phase75_8a = (
    build_phase75_8a_data()
  )

  sigma8_step = (
    phase75_8a[
      "sigma8_step"
    ]
  )

  rule = (
    toda_prop515_sigma8_prop44_specialization_inference_rule()
  )

  premise_steps = (
    sigma8_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  specialization_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda515Sigma8Prop44SpecializationStatement,
    )
  )

  return {
    "phase75_8a": phase75_8a,
    "sigma8_step": sigma8_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "specialization_step": (
      specialization_step
    ),
  }


def test_phase75_8e1_reuses_derived_sigma8_statement():
  data = build_phase75_8e1_data()

  assert isinstance(
    data[
      "sigma8_step"
    ].conclusion,
    TodaLemma514Sigma8Statement,
  )

  assert (
    data[
      "sigma8_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8e1_derives_prop44_specialization():
  data = build_phase75_8e1_data()

  assert isinstance(
    data[
      "specialization_step"
    ].conclusion,
    Toda515Sigma8Prop44SpecializationStatement,
  )

  assert (
    data[
      "specialization_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8e1_specialization_has_n8():
  data = build_phase75_8e1_data()

  assert (
    data[
      "specialization_step"
    ].conclusion
    .n
    == 8
  )


def test_phase75_8e1_specialization_reuses_same_sigma8():
  data = build_phase75_8e1_data()

  assert (
    data[
      "specialization_step"
    ].conclusion
    .alpha
    == data[
      "sigma8_step"
    ].conclusion
    .sigma8
  )


def test_phase75_8e1_sigma8_membership_is_pi15_8():
  data = build_phase75_8e1_data()

  statement = (
    data[
      "specialization_step"
    ].conclusion
  )

  assert (
    statement.membership
    == TodaPrimaryGroupMembershipStatement(
      element=statement.alpha,
      group=TodaPrimaryGroup(
        group_dimension=15,
        sphere_dimension=8,
      ),
    )
  )


def test_phase75_8e1_sigma8_is_critical_degree_element():
  data = build_phase75_8e1_data()

  statement = (
    data[
      "specialization_step"
    ].conclusion
  )

  group = (
    statement
    .membership
    .group
  )

  assert (
    group.group_dimension
    == 2 * group.sphere_dimension - 1
  )


def test_phase75_8e1_hopf_sigma8_is_iota15():
  data = build_phase75_8e1_data()

  statement = (
    data[
      "specialization_step"
    ].conclusion
  )

  iota_15 = HomotopyElement(
    name="ι_15",
    dimension=15,
    generator=GeneratorSymbol(
      family="ι",
      index=15,
    ),
  )

  assert (
    statement.hopf_relation
    == Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=statement.alpha,
      ),
      rhs=iota_15,
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase75_8e1_preserves_sigma8_statement_provenance():
  data = build_phase75_8e1_data()

  assert (
    data[
      "specialization_step"
    ].conclusion
    .sigma8_statement
    == data[
      "sigma8_step"
    ].conclusion
  )


def test_phase75_8e1_uses_exact_dependency():
  data = build_phase75_8e1_data()

  assert (
    data[
      "specialization_step"
    ].premises
    == (
      data[
        "sigma8_step"
      ],
    )
  )


def test_phase75_8e1_statement_not_present_initially():
  data = build_phase75_8e1_data()

  assert (
    data[
      "specialization_step"
    ].conclusion
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_8e1_rejects_given_sigma8_statement():
  data = build_phase75_8e1_data()

  given = ProofStep(
    conclusion=(
      data[
        "sigma8_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      given,
    ),
  ) is None


def test_phase75_8e1_rejects_wrong_sigma8():
  data = build_phase75_8e1_data()

  sigma8_statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  wrong_sigma8 = HomotopyElement(
    name="σ₈",
    dimension=8,
    source=16,
    target=8,
    generator=GeneratorSymbol(
      family="σ",
      index=8,
    ),
  )

  wrong_statement = replace(
    sigma8_statement,
    sigma8=wrong_sigma8,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase75_8e1_rejects_wrong_hopf_relation():
  data = build_phase75_8e1_data()

  sigma8_statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  wrong_iota = HomotopyElement(
    name="ι_14",
    dimension=14,
    generator=GeneratorSymbol(
      family="ι",
      index=14,
    ),
  )

  wrong_statement = replace(
    sigma8_statement,
    hopf_relation=Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=(
          sigma8_statement.sigma8
        ),
      ),
      rhs=wrong_iota,
      relation_type=RelationType.EQUALITY,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase75_8e1_reaches_fixed_point():
  data = build_phase75_8e1_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )




