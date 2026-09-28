import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from toda_proof_builders import (
  build_toda_prop58_proof_step,
)
from toda_rules import (
  TodaProp58FiniteDimensionalStatement,
)


def build_phase100_8_prop58_step():
  data = build_phase68_11_data()

  step = build_toda_prop58_proof_step(
    data[
      "pi6_2_step"
    ],
    data[
      "pi7_3_step"
    ],
    data[
      "pi8_4_step"
    ],
    data[
      "pi9_5_step"
    ],
    data[
      "higher_zero_step"
    ],
    data[
      "higher_range_step"
    ],
  )

  return (
    data,
    step,
  )


def test_phase100_8_production_builder_derives_prop58():
  _, step = (
    build_phase100_8_prop58_step()
  )

  assert isinstance(
    step.conclusion,
    TodaProp58FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase100_8_production_builder_matches_existing_phase68_conclusion():
  data, step = (
    build_phase100_8_prop58_step()
  )

  assert (
    step.conclusion
    == data[
      "integration_step"
    ].conclusion
  )


def test_phase100_8_production_builder_preserves_exact_premise_identity_and_order():
  data, step = (
    build_phase100_8_prop58_step()
  )

  expected_premises = (
    data[
      "pi6_2_step"
    ],
    data[
      "pi7_3_step"
    ],
    data[
      "pi8_4_step"
    ],
    data[
      "pi9_5_step"
    ],
    data[
      "higher_zero_step"
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


def test_phase100_8_production_builder_preserves_inference_rule_semantics():
  data, step = (
    build_phase100_8_prop58_step()
  )

  existing_rule = (
    data[
      "integration_step"
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


def test_phase100_8_production_builder_rejects_given_mathematical_premise():
  data = build_phase68_11_data()

  given_pi9_5 = ProofStep(
    conclusion=(
      data[
        "pi9_5_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    ValueError,
    match=(
      "premises do not derive "
      "Toda Proposition 5.8"
    ),
  ):
    build_toda_prop58_proof_step(
      data[
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      given_pi9_5,
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    )


def test_phase100_8_production_builder_rejects_wrong_premise_role():
  data = build_phase68_11_data()

  with pytest.raises(
    ValueError,
    match=(
      "premises do not derive "
      "Toda Proposition 5.8"
    ),
  ):
    build_toda_prop58_proof_step(
      data[
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    )


def test_phase100_8_production_builder_does_not_mutate_premise_steps():
  data = build_phase68_11_data()

  premise_steps = (
    data[
      "pi6_2_step"
    ],
    data[
      "pi7_3_step"
    ],
    data[
      "pi8_4_step"
    ],
    data[
      "pi9_5_step"
    ],
    data[
      "higher_zero_step"
    ],
    data[
      "higher_range_step"
    ],
  )

  original_conclusions = tuple(
    step.conclusion
    for step in premise_steps
  )

  build_toda_prop58_proof_step(
    *premise_steps
  )

  assert tuple(
    step.conclusion
    for step in premise_steps
  ) == original_conclusions
