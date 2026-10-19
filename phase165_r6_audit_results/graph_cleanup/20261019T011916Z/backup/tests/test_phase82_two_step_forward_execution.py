from functools import lru_cache

from proof import ProofRule
from repository_inference import (
  derive_goal_from_repository_with_one_level_producers,
  repository_available_steps,
)
from test_phase82_premise_rule_lookup import (
  build_phase82_3_data,
)


@lru_cache(maxsize=1)
def build_phase82_4_data():
  phase82_3 = (
    build_phase82_3_data()
  )

  phase82_2 = phase82_3[
    "phase82_2"
  ]

  phase77 = phase82_3[
    "phase77"
  ]

  repository = phase82_2[
    "repository"
  ]

  catalog = phase82_3[
    "catalog"
  ]

  goal = phase82_2[
    "goal"
  ]

  initial_steps = (
    repository_available_steps(
      repository
    )
  )

  result = (
    derive_goal_from_repository_with_one_level_producers(
      repository,
      catalog,
      goal,
    )
  )

  intermediate_step = next(
    (
      step
      for step
      in result.inference_result.steps
      if (
        step.conclusion
        ==
        phase77[
          "composition_step"
        ].conclusion
        and step.rule
        == ProofRule.INFERENCE
      )
    ),
    None,
  )

  return {
    "phase82_3": phase82_3,
    "phase82_2": phase82_2,
    "phase77": phase77,
    "repository": repository,
    "catalog": catalog,
    "goal": goal,
    "initial_steps": initial_steps,
    "result": result,
    "intermediate_step": (
      intermediate_step
    ),
  }


def test_phase82_4_goal_is_not_initially_available():
  data = build_phase82_4_data()

  assert all(
    step.conclusion
    != data[
      "goal"
    ]
    for step in data[
      "initial_steps"
    ]
  )


def test_phase82_4_intermediate_is_not_initially_available():
  data = build_phase82_4_data()

  composition_conclusion = (
    data[
      "phase77"
    ][
      "composition_step"
    ].conclusion
  )

  assert all(
    step.conclusion
    != composition_conclusion
    for step in data[
      "initial_steps"
    ]
  )


def test_phase82_4_automatically_derives_intermediate():
  data = build_phase82_4_data()

  assert (
    data[
      "intermediate_step"
    ]
    is not None
  )

  assert (
    data[
      "intermediate_step"
    ].conclusion
    ==
    data[
      "phase77"
    ][
      "composition_step"
    ].conclusion
  )


def test_phase82_4_intermediate_is_new_proof_step():
  data = build_phase82_4_data()

  assert (
    data[
      "intermediate_step"
    ]
    is not data[
      "phase77"
    ][
      "composition_step"
    ]
  )


def test_phase82_4_intermediate_reuses_existing_producer_rule():
  data = build_phase82_4_data()

  assert (
    data[
      "intermediate_step"
    ].inference_rule
    is data[
      "phase82_3"
    ][
      "producer_rule"
    ]
  )


def test_phase82_4_intermediate_is_inference():
  data = build_phase82_4_data()

  assert (
    data[
      "intermediate_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase82_4_intermediate_uses_exact_available_premises():
  data = build_phase82_4_data()

  original_premises = (
    data[
      "phase77"
    ][
      "composition_step"
    ].premises
  )

  derived_premises = (
    data[
      "intermediate_step"
    ].premises
  )

  assert len(
    derived_premises
  ) == len(
    original_premises
  )

  for (
    derived_premise,
    original_premise,
  ) in zip(
    derived_premises,
    original_premises,
  ):
    assert (
      derived_premise
      is original_premise
    )


def test_phase82_4_derives_actual_goal():
  data = build_phase82_4_data()

  assert (
    data[
      "result"
    ].goal_step
    is not None
  )

  assert (
    data[
      "result"
    ].goal_step.conclusion
    ==
    data[
      "goal"
    ]
  )


def test_phase82_4_final_is_new_proof_step():
  data = build_phase82_4_data()

  assert (
    data[
      "result"
    ].goal_step
    is not data[
      "phase77"
    ][
      "final_step"
    ]
  )


def test_phase82_4_final_reuses_existing_final_rule():
  data = build_phase82_4_data()

  assert (
    data[
      "result"
    ].goal_step.inference_rule
    is data[
      "phase82_3"
    ][
      "final_rule"
    ]
  )


def test_phase82_4_final_is_inference():
  data = build_phase82_4_data()

  assert (
    data[
      "result"
    ].goal_step.rule
    == ProofRule.INFERENCE
  )


def test_phase82_4_final_uses_repository_bracket_sum():
  data = build_phase82_4_data()

  final_step = data[
    "result"
  ].goal_step

  assert (
    final_step.premises[
      0
    ]
    is data[
      "phase77"
    ][
      "bracket_sum_step"
    ]
  )


def test_phase82_4_final_uses_new_intermediate():
  data = build_phase82_4_data()

  final_step = data[
    "result"
  ].goal_step

  assert (
    final_step.premises[
      1
    ]
    is data[
      "intermediate_step"
    ]
  )


def test_phase82_4_repository_is_not_mutated():
  data = build_phase82_4_data()

  after_steps = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  assert (
    after_steps
    == data[
      "initial_steps"
    ]
  )


def test_phase82_4_derived_intermediate_is_not_registered():
  data = build_phase82_4_data()

  intermediate = data[
    "intermediate_step"
  ]

  assert all(
    step
    is not intermediate
    for step
    in repository_available_steps(
      data[
        "repository"
      ]
    )
  )


def test_phase82_4_derived_final_is_not_registered():
  data = build_phase82_4_data()

  final_step = data[
    "result"
  ].goal_step

  assert all(
    step
    is not final_step
    for step
    in repository_available_steps(
      data[
        "repository"
      ]
    )
  )


