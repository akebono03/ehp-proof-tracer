import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from toda_proof_builders import (
  build_toda_prop56_proof_step,
)
from toda_rules import (
  TodaProp56FiniteDimensionalStatement,
)


def build_phase100_7_prop56_step():
  data = build_phase65_9_data()

  step = build_toda_prop56_proof_step(
    data[
      "pi5_2_step"
    ],
    data[
      "pi6_3_step"
    ],
    data[
      "pi7_4_step"
    ],
    data[
      "pi8_5_step"
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


def test_phase100_7_production_builder_derives_prop56():
  _, step = (
    build_phase100_7_prop56_step()
  )

  assert isinstance(
    step.conclusion,
    TodaProp56FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase100_7_production_builder_matches_existing_phase65_conclusion():
  data, step = (
    build_phase100_7_prop56_step()
  )

  assert (
    step.conclusion
    == data[
      "integration_step"
    ].conclusion
  )


def test_phase100_7_production_builder_preserves_exact_premise_identity_and_order():
  data, step = (
    build_phase100_7_prop56_step()
  )

  expected_premises = (
    data[
      "pi5_2_step"
    ],
    data[
      "pi6_3_step"
    ],
    data[
      "pi7_4_step"
    ],
    data[
      "pi8_5_step"
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


def test_phase100_7_production_builder_preserves_inference_rule_semantics():
  data, step = (
    build_phase100_7_prop56_step()
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


def test_phase100_7_production_builder_rejects_given_mathematical_premise():
  data = build_phase65_9_data()

  given_pi8_5 = ProofStep(
    conclusion=(
      data[
        "pi8_5_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    ValueError,
    match=(
      "premises do not derive "
      "Toda Proposition 5.6"
    ),
  ):
    build_toda_prop56_proof_step(
      data[
        "pi5_2_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "pi7_4_step"
      ],
      given_pi8_5,
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    )


def test_phase100_7_production_builder_rejects_wrong_premise_role():
  data = build_phase65_9_data()

  with pytest.raises(
    ValueError,
    match=(
      "premises do not derive "
      "Toda Proposition 5.6"
    ),
  ):
    build_toda_prop56_proof_step(
      data[
        "pi5_2_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "pi7_4_step"
      ],
      data[
        "pi7_4_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    )


def test_phase100_7_production_builder_does_not_mutate_premise_steps():
  data = build_phase65_9_data()

  premise_steps = (
    data[
      "pi5_2_step"
    ],
    data[
      "pi6_3_step"
    ],
    data[
      "pi7_4_step"
    ],
    data[
      "pi8_5_step"
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

  build_toda_prop56_proof_step(
    *premise_steps
  )

  assert tuple(
    step.conclusion
    for step in premise_steps
  ) == original_conclusions
