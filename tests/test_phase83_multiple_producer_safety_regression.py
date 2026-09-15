from copy import copy
from dataclasses import replace
from functools import lru_cache

from proof import PremisePattern
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
from test_phase83_actual_theorem_integration import (
  build_phase83_5_data,
)
from toda_rules import (
  Toda36Lemma516BracketSumContainmentStatement,
  Toda36Lemma516FirstBracketTermStatement,
  Toda36Lemma516SecondBracketTermStatement,
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


def _build_repository(
  data,
  *,
  include_bridge=True,
  include_setup=True,
  include_first=False,
):
  repository = ProofRepository()

  steps = []

  if include_bridge:
    steps.append(
      data[
        "bridge_step"
      ]
    )

  if include_setup:
    steps.append(
      data[
        "setup_step"
      ]
    )

  if include_first:
    steps.append(
      data[
        "original_first_step"
      ]
    )

  for index, step in enumerate(
    steps
  ):
    repository.register(
      ProofRepositoryEntry(
        key=(
          "phase83.safety.seed."
          f"{index}"
        ),
        step=step,
        phase="83",
        theorem=(
          "multiple-producer safety "
          "regression"
        ),
      )
    )

  return repository


def _build_catalog(
  data,
  *,
  include_first=True,
  include_second=True,
  first_safe=True,
  second_rule=None,
):
  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase83.safety.final",
    data[
      "final_rule"
    ],
    Toda36Lemma516BracketSumContainmentStatement,
  )

  if include_first:
    _register_rule(
      catalog,
      "phase83.safety.first",
      data[
        "first_rule"
      ],
      Toda36Lemma516FirstBracketTermStatement,
      fixed_point_safe=first_safe,
    )

  if include_second:
    if second_rule is None:
      second_rule = data[
        "second_rule"
      ]

    _register_rule(
      catalog,
      "phase83.safety.second",
      second_rule,
      Toda36Lemma516SecondBracketTermStatement,
    )

  return catalog


def _run(
  data,
  repository,
  catalog,
):
  return (
    derive_goal_from_repository_with_one_level_producers(
      repository,
      catalog,
      data[
        "goal"
      ],
    )
  )


def _steps_of_type(
  result,
  statement_type,
):
  return tuple(
    step
    for step in result.inference_result.steps
    if isinstance(
      step.conclusion,
      statement_type,
    )
  )


@lru_cache(maxsize=1)
def build_phase83_6_data():
  return build_phase83_5_data()


def test_phase83_6_missing_one_producer_blocks_all_producers():
  data = build_phase83_6_data()
  repository = _build_repository(
    data
  )
  catalog = _build_catalog(
    data,
    include_first=False,
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is None
  assert (
    _steps_of_type(
      result,
      Toda36Lemma516FirstBracketTermStatement,
    )
    == ()
  )
  assert (
    _steps_of_type(
      result,
      Toda36Lemma516SecondBracketTermStatement,
    )
    == ()
  )


def test_phase83_6_unsafe_one_producer_blocks_all_producers():
  data = build_phase83_6_data()
  repository = _build_repository(
    data
  )
  catalog = _build_catalog(
    data,
    first_safe=False,
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is None
  assert (
    _steps_of_type(
      result,
      Toda36Lemma516SecondBracketTermStatement,
    )
    == ()
  )


def test_phase83_6_ambiguous_one_producer_blocks_all_producers():
  data = build_phase83_6_data()
  repository = _build_repository(
    data
  )
  catalog = _build_catalog(
    data
  )

  _register_rule(
    catalog,
    "phase83.safety.first-second-rule",
    copy(
      data[
        "first_rule"
      ]
    ),
    Toda36Lemma516FirstBracketTermStatement,
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is None
  assert (
    _steps_of_type(
      result,
      Toda36Lemma516FirstBracketTermStatement,
    )
    == ()
  )
  assert (
    _steps_of_type(
      result,
      Toda36Lemma516SecondBracketTermStatement,
    )
    == ()
  )


def test_phase83_6_same_rule_alias_is_not_ambiguity():
  data = build_phase83_6_data()
  repository = _build_repository(
    data
  )
  catalog = _build_catalog(
    data
  )

  _register_rule(
    catalog,
    "phase83.safety.first-alias",
    data[
      "first_rule"
    ],
    Toda36Lemma516FirstBracketTermStatement,
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is not None
  assert len(
    _steps_of_type(
      result,
      Toda36Lemma516FirstBracketTermStatement,
    )
  ) == 1


def test_phase83_6_existing_first_premise_is_not_reproduced():
  data = build_phase83_6_data()
  repository = _build_repository(
    data,
    include_first=True,
  )
  catalog = _build_catalog(
    data
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  first_steps = _steps_of_type(
    result,
    Toda36Lemma516FirstBracketTermStatement,
  )

  assert result.goal_step is not None
  assert len(
    first_steps
  ) == 1
  assert (
    first_steps[
      0
    ]
    is data[
      "original_first_step"
    ]
  )


def test_phase83_6_unavailable_producer_premise_does_not_recurse():
  data = build_phase83_6_data()
  repository = _build_repository(
    data,
    include_setup=False,
  )
  catalog = _build_catalog(
    data
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is None
  assert (
    _steps_of_type(
      result,
      Toda36Lemma516FirstBracketTermStatement,
    )
    == ()
  )
  assert (
    _steps_of_type(
      result,
      Toda36Lemma516SecondBracketTermStatement,
    )
    == ()
  )


def test_phase83_6_partial_producer_application_does_not_create_goal():
  data = build_phase83_6_data()
  repository = _build_repository(
    data
  )

  blocked_second_rule = replace(
    data[
      "second_rule"
    ],
    premise_patterns=(
      data[
        "second_rule"
      ].premise_patterns
      + (
        PremisePattern(
          statement_type=dict,
        ),
      )
    ),
  )

  catalog = _build_catalog(
    data,
    second_rule=blocked_second_rule,
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is None
  assert len(
    _steps_of_type(
      result,
      Toda36Lemma516FirstBracketTermStatement,
    )
  ) == 1
  assert (
    _steps_of_type(
      result,
      Toda36Lemma516SecondBracketTermStatement,
    )
    == ()
  )


def test_phase83_6_incompatible_generated_branches_do_not_create_goal():
  data = build_phase83_6_data()
  repository = _build_repository(
    data
  )

  original_second = data[
    "original_second_step"
  ].conclusion
  wrong_beta = replace(
    original_second.beta,
    name="γ",
  )
  wrong_second = replace(
    original_second,
    beta=wrong_beta,
  )
  wrong_second_rule = replace(
    data[
      "second_rule"
    ],
    conclusion_builder=(
      lambda premises: wrong_second
    ),
  )

  catalog = _build_catalog(
    data,
    second_rule=wrong_second_rule,
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is None
  assert len(
    _steps_of_type(
      result,
      Toda36Lemma516FirstBracketTermStatement,
    )
  ) == 1
  assert len(
    _steps_of_type(
      result,
      Toda36Lemma516SecondBracketTermStatement,
    )
  ) == 1


def test_phase83_6_duplicate_final_rules_do_not_duplicate_conclusions():
  data = build_phase83_6_data()
  repository = _build_repository(
    data
  )
  catalog = _build_catalog(
    data
  )

  _register_rule(
    catalog,
    "phase83.safety.final-second-rule",
    copy(
      data[
        "final_rule"
      ]
    ),
    Toda36Lemma516BracketSumContainmentStatement,
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is not None
  assert len(
    _steps_of_type(
      result,
      Toda36Lemma516BracketSumContainmentStatement,
    )
  ) == 1
  assert len(
    _steps_of_type(
      result,
      Toda36Lemma516FirstBracketTermStatement,
    )
  ) == 1
  assert len(
    _steps_of_type(
      result,
      Toda36Lemma516SecondBracketTermStatement,
    )
  ) == 1


def test_phase83_6_repository_is_unchanged_after_failed_search():
  data = build_phase83_6_data()
  repository = _build_repository(
    data
  )
  before = repository_available_steps(
    repository
  )
  catalog = _build_catalog(
    data,
    include_first=False,
  )

  result = _run(
    data,
    repository,
    catalog,
  )

  assert result.goal_step is None
  assert (
    repository_available_steps(
      repository
    )
    == before
  )
