from functools import lru_cache

import pytest

from expression import (
  GeneratorSymbol,
  IteratedSuspension,
  ScalarSum,
  ScalarSymbol,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase75_lemma514_sigma8 import (
  build_phase75_8a_data,
)
from toda_rules import (
  TodaLemma514Sigma8Statement,
  TodaSigmaFamilyDefinitionStatement,
  toda_lemma514_sigma_family_definition_inference_rule,
  toda_sigma_family_definition_statement,
)


@lru_cache(maxsize=1)
def build_phase75_8b_data():
  phase75_8a = (
    build_phase75_8a_data()
  )

  sigma8_step = (
    phase75_8a[
      "sigma8_step"
    ]
  )

  n = ScalarSymbol(
    name="n",
  )

  n_range = (
    ScalarGreaterEqualStatement(
      left=n,
      right=8,
    )
  )

  n_range_step = ProofStep(
    conclusion=n_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma514_sigma_family_definition_inference_rule()
  )

  premise_steps = (
    sigma8_step,
    n_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  expected_statement = (
    toda_sigma_family_definition_statement(
      n,
      sigma8_step.conclusion,
    )
  )

  definition_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase75_8a": phase75_8a,
    "sigma8_step": sigma8_step,
    "n": n,
    "n_range": n_range,
    "n_range_step": n_range_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_statement": (
      expected_statement
    ),
    "definition_step": (
      definition_step
    ),
  }


def test_phase75_8b_reuses_derived_sigma8():
  data = build_phase75_8b_data()

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


def test_phase75_8b_range_is_explicit_given():
  data = build_phase75_8b_data()

  assert (
    data[
      "n_range_step"
    ].conclusion
    == ScalarGreaterEqualStatement(
      left=(
        data[
          "n"
        ]
      ),
      right=8,
    )
  )

  assert (
    data[
      "n_range_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase75_8b_derives_sigma_family_definition():
  data = build_phase75_8b_data()

  assert isinstance(
    data[
      "definition_step"
    ].conclusion,
    TodaSigmaFamilyDefinitionStatement,
  )

  assert (
    data[
      "definition_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8b_symbolic_index_is_n():
  data = build_phase75_8b_data()

  assert (
    data[
      "definition_step"
    ].conclusion
    .index
    == data[
      "n"
    ]
  )


def test_phase75_8b_sigma_n_has_expected_group_dimensions():
  data = build_phase75_8b_data()

  n = (
    data[
      "n"
    ]
  )

  sigma_n = (
    data[
      "definition_step"
    ].conclusion
    .element
  )

  assert (
    sigma_n.dimension
    == n
  )

  assert (
    sigma_n.source
    == ScalarSum(
      left=n,
      right=7,
    )
  )

  assert (
    sigma_n.target
    == n
  )


def test_phase75_8b_sigma_n_has_expected_generator():
  data = build_phase75_8b_data()

  n = (
    data[
      "n"
    ]
  )

  sigma_n = (
    data[
      "definition_step"
    ].conclusion
    .element
  )

  assert (
    sigma_n.generator
    == GeneratorSymbol(
      family="σ",
      index=n,
    )
  )


def test_phase75_8b_definition_is_e_n_minus_8_sigma8():
  data = build_phase75_8b_data()

  statement = (
    data[
      "definition_step"
    ].conclusion
  )

  sigma8 = (
    data[
      "sigma8_step"
    ].conclusion
    .sigma8
  )

  assert (
    statement.iterated_suspension
    == IteratedSuspension(
      expression=sigma8,
      exponent=ScalarSum(
        left=(
          data[
            "n"
          ]
        ),
        right=-8,
      ),
    )
  )


def test_phase75_8b_preserves_sigma8_statement():
  data = build_phase75_8b_data()

  assert (
    data[
      "definition_step"
    ].conclusion
    .sigma8_statement
    == data[
      "sigma8_step"
    ].conclusion
  )


def test_phase75_8b_preserves_theorem36_provenance():
  data = build_phase75_8b_data()

  definition = (
    data[
      "definition_step"
    ].conclusion
  )

  assert (
    definition
    .sigma8_statement
    .theorem36_bridge
    == data[
      "sigma8_step"
    ].conclusion
    .theorem36_bridge
  )


def test_phase75_8b_uses_exact_dependencies():
  data = build_phase75_8b_data()

  assert (
    data[
      "definition_step"
    ].premises
    == (
      data[
        "sigma8_step"
      ],
      data[
        "n_range_step"
      ],
    )
  )


def test_phase75_8b_definition_not_present_initially():
  data = build_phase75_8b_data()

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_8b_rejects_given_sigma8():
  data = build_phase75_8b_data()

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
      data[
        "n_range_step"
      ],
    ),
  ) is None


def test_phase75_8b_rejects_n_at_least_7():
  data = build_phase75_8b_data()

  wrong_range_step = ProofStep(
    conclusion=(
      ScalarGreaterEqualStatement(
        left=(
          data[
            "n"
          ]
        ),
        right=7,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "sigma8_step"
      ],
      wrong_range_step,
    ),
  ) is None


def test_phase75_8b_concrete_n8_is_sigma8():
  data = build_phase75_8b_data()

  statement = (
    toda_sigma_family_definition_statement(
      8,
      data[
        "sigma8_step"
      ].conclusion,
    )
  )

  assert (
    statement.element
    == data[
      "sigma8_step"
    ].conclusion
    .sigma8
  )

  assert (
    statement.iterated_suspension
    == IteratedSuspension(
      expression=(
        data[
          "sigma8_step"
        ].conclusion
        .sigma8
      ),
      exponent=0,
    )
  )


def test_phase75_8b_concrete_n9_is_e_sigma8():
  data = build_phase75_8b_data()

  statement = (
    toda_sigma_family_definition_statement(
      9,
      data[
        "sigma8_step"
      ].conclusion,
    )
  )

  assert (
    statement.element.source
    == 16
  )

  assert (
    statement.element.target
    == 9
  )

  assert (
    statement.iterated_suspension
    == IteratedSuspension(
      expression=(
        data[
          "sigma8_step"
        ].conclusion
        .sigma8
      ),
      exponent=1,
    )
  )


def test_phase75_8b_rejects_concrete_n_below_8():
  data = build_phase75_8b_data()

  with pytest.raises(
    ValueError,
  ):
    toda_sigma_family_definition_statement(
      7,
      data[
        "sigma8_step"
      ].conclusion,
    )


def test_phase75_8b_rejects_invalid_index_type():
  data = build_phase75_8b_data()

  with pytest.raises(
    TypeError,
  ):
    toda_sigma_family_definition_statement(
      "n",
      data[
        "sigma8_step"
      ].conclusion,
    )


def test_phase75_8b_reaches_fixed_point():
  data = build_phase75_8b_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


