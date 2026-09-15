from copy import copy
from functools import lru_cache

from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  derive_goal_from_repository_with_one_level_producers,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase82_actual_theorem_integration import (
  build_phase82_5_data,
)


def _register_rule(
  catalog,
  key,
  rule,
  conclusion_type,
  fixed_point_safe=True,
):
  catalog.register(
    InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=(
        fixed_point_safe
      ),
    )
  )


def _build_catalog(
  data,
  *,
  include_producer=True,
  producer_safe=True,
):
  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase82.safety.final",
    data[
      "phase82_3"
    ][
      "final_rule"
    ],
    type(
      data[
        "goal"
      ]
    ),
  )

  if include_producer:
    _register_rule(
      catalog,
      "phase82.safety.producer",
      data[
        "phase82_3"
      ][
        "producer_rule"
      ],
      type(
        data[
          "intermediate_step"
        ].conclusion
      ),
      fixed_point_safe=(
        producer_safe
      ),
    )

  return catalog


def _build_repository(
  steps,
):
  repository = ProofRepository()

  for index, step in enumerate(
    steps
  ):
    repository.register(
      ProofRepositoryEntry(
        key=(
          "phase82.safety."
          f"seed.{index}"
        ),
        step=step,
        phase="82",
        theorem=(
          "Phase 82 search-safety "
          "regression"
        ),
      )
    )

  return repository


def _run(
  repository,
  catalog,
  goal,
):
  return (
    derive_goal_from_repository_with_one_level_producers(
      repository,
      catalog,
      goal,
    )
  )


@lru_cache(maxsize=1)
def build_phase82_6_data():
  phase82_5 = (
    build_phase82_5_data()
  )

  return {
    "phase82_5": phase82_5,
    "phase82_4": phase82_5[
      "phase82_4"
    ],
    "phase82_3": phase82_5[
      "phase82_3"
    ],
    "phase77": phase82_5[
      "phase77"
    ],
    "goal": phase82_5[
      "goal"
    ],
    "repository": phase82_5[
      "repository"
    ],
    "catalog": phase82_5[
      "catalog"
    ],
    "initial_steps": phase82_5[
      "initial_steps"
    ],
    "intermediate_step": (
      phase82_5[
        "intermediate_step"
      ]
    ),
    "final_step": (
      phase82_5[
        "final_step"
      ]
    ),
  }


def test_phase82_6_actual_success_path_still_works():
  data = build_phase82_6_data()

  result = _run(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is not None
  )

  assert (
    result.goal_step.conclusion
    == data[
      "goal"
    ]
  )


def test_phase82_6_missing_producer_returns_no_goal():
  data = build_phase82_6_data()

  catalog = _build_catalog(
    data,
    include_producer=False,
  )

  result = _run(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is None
  )


def test_phase82_6_unsafe_only_producer_returns_no_goal():
  data = build_phase82_6_data()

  catalog = _build_catalog(
    data,
    producer_safe=False,
  )

  result = _run(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is None
  )


def test_phase82_6_wrong_producer_is_rejected_by_applicability():
  data = build_phase82_6_data()

  catalog = InferenceRuleCatalog()

  final_rule = data[
    "phase82_3"
  ][
    "final_rule"
  ]

  _register_rule(
    catalog,
    "phase82.safety.final",
    final_rule,
    type(
      data[
        "goal"
      ]
    ),
  )

  _register_rule(
    catalog,
    "phase82.safety.wrong-producer",
    final_rule,
    type(
      data[
        "intermediate_step"
      ].conclusion
    ),
  )

  result = _run(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is None
  )


def test_phase82_6_self_dependent_producer_does_not_fire():
  data = build_phase82_6_data()

  catalog = InferenceRuleCatalog()

  final_rule = data[
    "phase82_3"
  ][
    "final_rule"
  ]

  intermediate_type = type(
    data[
      "intermediate_step"
    ].conclusion
  )

  _register_rule(
    catalog,
    "phase82.safety.final",
    final_rule,
    type(
      data[
        "goal"
      ]
    ),
  )

  _register_rule(
    catalog,
    "phase82.safety.self-dependent",
    final_rule,
    intermediate_type,
  )

  result = _run(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  intermediate_conclusion = (
    data[
      "intermediate_step"
    ].conclusion
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != intermediate_conclusion
    for step in result.inference_result.steps
  )


def test_phase82_6_distinct_producer_ambiguity_is_not_expanded():
  data = build_phase82_6_data()

  producer_rule = data[
    "phase82_3"
  ][
    "producer_rule"
  ]

  second_producer_rule = copy(
    producer_rule
  )

  assert (
    second_producer_rule
    is not producer_rule
  )

  catalog = _build_catalog(
    data,
    include_producer=False,
  )

  intermediate_type = type(
    data[
      "intermediate_step"
    ].conclusion
  )

  _register_rule(
    catalog,
    "phase82.safety.producer-a",
    producer_rule,
    intermediate_type,
  )

  _register_rule(
    catalog,
    "phase82.safety.producer-b",
    second_producer_rule,
    intermediate_type,
  )

  result = _run(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != data[
      "intermediate_step"
    ].conclusion
    for step in result.inference_result.steps
  )


def test_phase82_6_same_rule_alias_is_not_ambiguity():
  data = build_phase82_6_data()

  producer_rule = data[
    "phase82_3"
  ][
    "producer_rule"
  ]

  catalog = _build_catalog(
    data,
    include_producer=False,
  )

  intermediate_type = type(
    data[
      "intermediate_step"
    ].conclusion
  )

  _register_rule(
    catalog,
    "phase82.safety.producer",
    producer_rule,
    intermediate_type,
  )

  _register_rule(
    catalog,
    "phase82.safety.producer-alias",
    producer_rule,
    intermediate_type,
  )

  result = _run(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is not None
  )

  matching_intermediates = tuple(
    step
    for step
    in result.inference_result.steps
    if (
      step.conclusion
      ==
      data[
        "intermediate_step"
      ].conclusion
    )
  )

  assert len(
    matching_intermediates
  ) == 1


def test_phase82_6_duplicate_intermediate_is_not_created():
  data = build_phase82_6_data()

  result = _run(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  matching_intermediates = tuple(
    step
    for step
    in result.inference_result.steps
    if (
      step.conclusion
      ==
      data[
        "intermediate_step"
      ].conclusion
    )
  )

  assert len(
    matching_intermediates
  ) == 1


def test_phase82_6_existing_intermediate_is_not_reproduced():
  data = build_phase82_6_data()

  phase77 = data[
    "phase77"
  ]

  repository = _build_repository(
    (
      phase77[
        "bracket_sum_step"
      ],
      phase77[
        "composition_step"
      ],
      phase77[
        "suspension_bridge_step"
      ],
      phase77[
        "sigma_definition_step"
      ],
    )
  )

  result = _run(
    repository,
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is not None
  )

  matching_intermediates = tuple(
    step
    for step
    in result.inference_result.steps
    if (
      step.conclusion
      ==
      phase77[
        "composition_step"
      ].conclusion
    )
  )

  assert len(
    matching_intermediates
  ) == 1

  assert (
    matching_intermediates[
      0
    ]
    is phase77[
      "composition_step"
    ]
  )


def test_phase82_6_two_missing_final_premises_do_not_trigger_search():
  data = build_phase82_6_data()

  repository = ProofRepository()

  result = _run(
    repository,
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != data[
      "intermediate_step"
    ].conclusion
    for step in result.inference_result.steps
  )


def test_phase82_6_missing_producer_premise_does_not_recurse():
  data = build_phase82_6_data()

  phase77 = data[
    "phase77"
  ]

  repository = _build_repository(
    (
      phase77[
        "bracket_sum_step"
      ],
      phase77[
        "suspension_bridge_step"
      ],
    )
  )

  result = _run(
    repository,
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != data[
      "intermediate_step"
    ].conclusion
    for step in result.inference_result.steps
  )


def test_phase82_6_depth_two_rule_in_catalog_is_not_followed():
  data = build_phase82_6_data()

  phase77 = data[
    "phase77"
  ]

  repository = _build_repository(
    (
      phase77[
        "bracket_sum_step"
      ],
      phase77[
        "suspension_bridge_step"
      ],
    )
  )

  catalog = _build_catalog(
    data,
  )

  sigma_definition_rule = (
    phase77[
      "sigma_definition_step"
    ].inference_rule
  )

  assert (
    sigma_definition_rule
    is not None
  )

  _register_rule(
    catalog,
    "phase82.safety.depth-two",
    sigma_definition_rule,
    type(
      phase77[
        "sigma_definition_step"
      ].conclusion
    ),
  )

  result = _run(
    repository,
    catalog,
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != phase77[
      "sigma_definition_step"
    ].conclusion
    for step in result.inference_result.steps
  )


def test_phase82_6_cycle_shaped_catalog_is_not_traversed():
  data = build_phase82_6_data()

  phase77 = data[
    "phase77"
  ]

  repository = _build_repository(
    (
      phase77[
        "bracket_sum_step"
      ],
      phase77[
        "suspension_bridge_step"
      ],
    )
  )

  catalog = _build_catalog(
    data,
  )

  final_rule = data[
    "phase82_3"
  ][
    "final_rule"
  ]

  _register_rule(
    catalog,
    "phase82.safety.cycle-back",
    final_rule,
    type(
      phase77[
        "sigma_definition_step"
      ].conclusion
    ),
  )

  result = _run(
    repository,
    catalog,
    data[
      "goal"
    ],
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.conclusion
    != data[
      "intermediate_step"
    ].conclusion
    for step in result.inference_result.steps
  )


def test_phase82_6_repository_is_unchanged_after_failed_search():
  data = build_phase82_6_data()

  before = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  ambiguous_rule = copy(
    data[
      "phase82_3"
    ][
      "producer_rule"
    ]
  )

  catalog = _build_catalog(
    data,
  )

  _register_rule(
    catalog,
    "phase82.safety.extra-producer",
    ambiguous_rule,
    type(
      data[
        "intermediate_step"
      ].conclusion
    ),
  )

  result = _run(
    data[
      "repository"
    ],
    catalog,
    data[
      "goal"
    ],
  )

  after = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  assert (
    result.goal_step
    is None
  )

  assert (
    after
    == before
  )


