import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from test_phase75_prop515_integration import (
  build_phase75_9_data,
)
from toda_proof_builders import (
  build_toda_prop515_proof_step,
)
from toda_rules import (
  TodaProp515FiniteDimensionalStatement,
)


def build_phase100_10_prop515_step():
  data = build_phase75_9_data()

  step = build_toda_prop515_proof_step(
    data[
      "pi9_2_step"
    ],
    data[
      "pi10_3_step"
    ],
    data[
      "pi11_4_step"
    ],
    data[
      "pi12_5_step"
    ],
    data[
      "pi13_6_step"
    ],
    data[
      "pi14_7_step"
    ],
    data[
      "pi15_8_step"
    ],
    data[
      "higher_step"
    ],
    data[
      "higher_range_step"
    ],
  )

  return (
    data,
    step,
  )


def test_phase100_10_production_builder_derives_prop515():
  _, step = (
    build_phase100_10_prop515_step()
  )

  assert isinstance(
    step.conclusion,
    TodaProp515FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase100_10_production_builder_matches_existing_phase75_conclusion():
  data, step = (
    build_phase100_10_prop515_step()
  )

  assert (
    step.conclusion
    == data[
      "aggregate_step"
    ].conclusion
  )


def test_phase100_10_production_builder_preserves_exact_premise_identity_and_order():
  data, step = (
    build_phase100_10_prop515_step()
  )

  expected_premises = (
    data[
      "pi9_2_step"
    ],
    data[
      "pi10_3_step"
    ],
    data[
      "pi11_4_step"
    ],
    data[
      "pi12_5_step"
    ],
    data[
      "pi13_6_step"
    ],
    data[
      "pi14_7_step"
    ],
    data[
      "pi15_8_step"
    ],
    data[
      "higher_step"
    ],
    data[
      "higher_range_step"
    ],
  )

  assert (
    step.premises
    == expected_premises
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      step.premises,
      expected_premises,
    )
  )


def test_phase100_10_production_builder_preserves_inference_rule_semantics():
  data, step = (
    build_phase100_10_prop515_step()
  )

  existing_rule = (
    data[
      "aggregate_step"
    ].inference_rule
  )

  production_rule = (
    step.inference_rule
  )

  assert production_rule is not None
  assert existing_rule is not None

  assert (
    production_rule.name
    == existing_rule.name
  )

  assert (
    production_rule.description
    == existing_rule.description
  )

  assert (
    production_rule.premise_patterns
    == existing_rule.premise_patterns
  )

  assert (
    production_rule.conclusion_pattern
    == existing_rule.conclusion_pattern
  )


def test_phase100_10_production_builder_rejects_given_mathematical_premise():
  data = build_phase75_9_data()

  given_pi15_8 = ProofStep(
    conclusion=(
      data[
        "pi15_8_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    ValueError,
    match=(
      "premises do not derive "
      "Toda Proposition 5.15"
    ),
  ):
    build_toda_prop515_proof_step(
      data[
        "pi9_2_step"
      ],
      data[
        "pi10_3_step"
      ],
      data[
        "pi11_4_step"
      ],
      data[
        "pi12_5_step"
      ],
      data[
        "pi13_6_step"
      ],
      data[
        "pi14_7_step"
      ],
      given_pi15_8,
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    )


def test_phase100_10_production_builder_rejects_wrong_premise_role():
  data = build_phase75_9_data()

  with pytest.raises(
    ValueError,
    match=(
      "premises do not derive "
      "Toda Proposition 5.15"
    ),
  ):
    build_toda_prop515_proof_step(
      data[
        "pi9_2_step"
      ],
      data[
        "pi10_3_step"
      ],
      data[
        "pi11_4_step"
      ],
      data[
        "pi12_5_step"
      ],
      data[
        "pi13_6_step"
      ],
      data[
        "pi14_7_step"
      ],
      data[
        "pi14_7_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    )


def test_phase100_10_production_builder_does_not_mutate_premise_steps():
  data = build_phase75_9_data()

  premise_steps = (
    data[
      "pi9_2_step"
    ],
    data[
      "pi10_3_step"
    ],
    data[
      "pi11_4_step"
    ],
    data[
      "pi12_5_step"
    ],
    data[
      "pi13_6_step"
    ],
    data[
      "pi14_7_step"
    ],
    data[
      "pi15_8_step"
    ],
    data[
      "higher_step"
    ],
    data[
      "higher_range_step"
    ],
  )

  original_conclusions = tuple(
    step.conclusion
    for step in premise_steps
  )

  build_toda_prop515_proof_step(
    *premise_steps
  )

  assert tuple(
    step.conclusion
    for step in premise_steps
  ) == original_conclusions
