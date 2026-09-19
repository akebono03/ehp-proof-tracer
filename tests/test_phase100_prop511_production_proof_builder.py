import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from toda_proof_builders import (
  build_toda_prop511_proof_step,
)
from toda_rules import (
  TodaProp511FiniteDimensionalStatement,
)


def build_phase100_9_prop511_step():
  data = build_phase73_8e_data()

  step = build_toda_prop511_proof_step(
    data[
      "pi8_2_step"
    ],
    data[
      "pi9_3_zero_step"
    ],
    data[
      "pi10_4_step"
    ],
    data[
      "nu_squared_step"
    ],
  )

  return (
    data,
    step,
  )


def test_phase100_9_production_builder_derives_prop511():
  _, step = (
    build_phase100_9_prop511_step()
  )

  assert isinstance(
    step.conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase100_9_production_builder_matches_existing_phase73_conclusion():
  data, step = (
    build_phase100_9_prop511_step()
  )

  assert (
    step.conclusion
    == data[
      "final_step"
    ].conclusion
  )


def test_phase100_9_production_builder_preserves_exact_premise_identity_and_order():
  data, step = (
    build_phase100_9_prop511_step()
  )

  expected_premises = (
    data[
      "pi8_2_step"
    ],
    data[
      "pi9_3_zero_step"
    ],
    data[
      "pi10_4_step"
    ],
    data[
      "nu_squared_step"
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


def test_phase100_9_production_builder_preserves_inference_rule_semantics():
  data, step = (
    build_phase100_9_prop511_step()
  )

  existing_rule = (
    data[
      "final_step"
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


def test_phase100_9_production_builder_rejects_given_mathematical_premise():
  data = build_phase73_8e_data()

  given_pi10_4 = ProofStep(
    conclusion=(
      data[
        "pi10_4_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    ValueError,
    match=(
      "premises do not derive "
      "Toda Proposition 5.11"
    ),
  ):
    build_toda_prop511_proof_step(
      data[
        "pi8_2_step"
      ],
      data[
        "pi9_3_zero_step"
      ],
      given_pi10_4,
      data[
        "nu_squared_step"
      ],
    )


def test_phase100_9_production_builder_rejects_wrong_premise_role():
  data = build_phase73_8e_data()

  with pytest.raises(
    ValueError,
    match=(
      "premises do not derive "
      "Toda Proposition 5.11"
    ),
  ):
    build_toda_prop511_proof_step(
      data[
        "pi8_2_step"
      ],
      data[
        "pi9_3_zero_step"
      ],
      data[
        "pi9_3_zero_step"
      ],
      data[
        "nu_squared_step"
      ],
    )


def test_phase100_9_production_builder_does_not_mutate_premise_steps():
  data = build_phase73_8e_data()

  premise_steps = (
    data[
      "pi8_2_step"
    ],
    data[
      "pi9_3_zero_step"
    ],
    data[
      "pi10_4_step"
    ],
    data[
      "nu_squared_step"
    ],
  )

  original_conclusions = tuple(
    step.conclusion
    for step in premise_steps
  )

  build_toda_prop511_proof_step(
    *premise_steps
  )

  assert tuple(
    step.conclusion
    for step in premise_steps
  ) == original_conclusions
