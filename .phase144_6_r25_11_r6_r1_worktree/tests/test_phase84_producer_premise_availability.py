from functools import lru_cache

import pytest

from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  analyze_producer_premise_availabilities,
  detect_goal_rule_missing_premises,
  find_missing_premise_producer_lookups,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase77_applicability_provenance import (
  build_phase77_6_data,
)
from toda_rules import (
  Toda36Lemma516BracketSumContainmentStatement,
  TodaLemma516BracketSumContainmentStatement,
  TodaLemma516ScaledCompositionBridgeStatement,
)


def _register_rule(
  catalog,
  key,
  rule,
  conclusion_type,
):
  catalog.register(
    InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=True,
    )
  )


@lru_cache(maxsize=1)
def build_phase84_3_data():
  phase77 = build_phase77_6_data()
  phase77_data = phase77[
    "data"
  ]
  phase77_5a = phase77_data[
    "phase77_5a"
  ]

  final_rule = phase77_data[
    "final_rule"
  ]
  composition_rule = phase77_data[
    "composition_rule"
  ]
  bracket_sum_rule = phase77_5a[
    "rule"
  ]

  first_term_step = phase77_5a[
    "first_term_step"
  ]
  second_term_step = phase77_5a[
    "second_term_step"
  ]
  suspension_bridge_step = phase77[
    "suspension_bridge_step"
  ]
  sigma_definition_step = phase77[
    "sigma_definition_step"
  ]

  repository = ProofRepository()

  for key, step in (
    (
      "phase84.first-term",
      first_term_step,
    ),
    (
      "phase84.second-term",
      second_term_step,
    ),
    (
      "phase84.suspension-bridge",
      suspension_bridge_step,
    ),
    (
      "phase84.sigma-definition",
      sigma_definition_step,
    ),
  ):
    repository.register(
      ProofRepositoryEntry(
        key=key,
        step=step,
        phase="84",
        theorem=(
          "Toda Lemma 5.16 producer "
          "premise availability"
        ),
      )
    )

  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase84.final",
    final_rule,
    TodaLemma516BracketSumContainmentStatement,
  )

  _register_rule(
    catalog,
    "phase84.composition-producer",
    composition_rule,
    TodaLemma516ScaledCompositionBridgeStatement,
  )

  _register_rule(
    catalog,
    "phase84.bracket-sum-producer",
    bracket_sum_rule,
    Toda36Lemma516BracketSumContainmentStatement,
  )

  goal = phase77[
    "final_step"
  ].conclusion

  initial_steps = repository_available_steps(
    repository
  )

  final_availability = (
    detect_goal_rule_missing_premises(
      repository,
      catalog,
      goal,
    )[
      0
    ]
  )

  lookups = (
    find_missing_premise_producer_lookups(
      final_availability,
      catalog,
    )
  )

  producer_availabilities = tuple(
    analyze_producer_premise_availabilities(
      lookup,
      initial_steps,
    )
    for lookup in lookups
  )

  return {
    "phase77": phase77,
    "repository": repository,
    "catalog": catalog,
    "goal": goal,
    "final_rule": final_rule,
    "composition_rule": composition_rule,
    "bracket_sum_rule": bracket_sum_rule,
    "initial_steps": initial_steps,
    "final_availability": (
      final_availability
    ),
    "lookups": lookups,
    "producer_availabilities": (
      producer_availabilities
    ),
  }


def test_phase84_3_final_rule_has_two_missing_premises():
  data = build_phase84_3_data()

  assert (
    data[
      "final_availability"
    ].missing_indices
    == (
      0,
      1,
    )
  )


def test_phase84_3_each_final_premise_has_one_producer_candidate():
  data = build_phase84_3_data()

  assert tuple(
    len(
      lookup.producer_rules
    )
    for lookup in data[
      "lookups"
    ]
  ) == (
    1,
    1,
  )


def test_phase84_3_analysis_preserves_candidate_order():
  data = build_phase84_3_data()

  assert tuple(
    tuple(
      availability.inference_rule
      for availability
      in availabilities
    )
    for availabilities
    in data[
      "producer_availabilities"
    ]
  ) == (
    (
      data[
        "bracket_sum_rule"
      ],
    ),
    (
      data[
        "composition_rule"
      ],
    ),
  )


def test_phase84_3_bracket_sum_producer_is_initially_complete():
  data = build_phase84_3_data()

  availability = data[
    "producer_availabilities"
  ][
    0
  ][
    0
  ]

  assert availability.is_complete
  assert availability.missing_indices == ()

  assert availability.matched_steps == (
    data[
      "phase77"
    ][
      "data"
    ][
      "phase77_5a"
    ][
      "first_term_step"
    ],
    data[
      "phase77"
    ][
      "data"
    ][
      "phase77_5a"
    ][
      "second_term_step"
    ],
  )


def test_phase84_3_composition_producer_is_initially_incomplete():
  data = build_phase84_3_data()

  availability = data[
    "producer_availabilities"
  ][
    1
  ][
    0
  ]

  assert not availability.is_complete

  assert availability.missing_indices == (
    0,
  )

  assert (
    availability.missing_patterns[
      0
    ].statement_type
    is Toda36Lemma516BracketSumContainmentStatement
  )


def test_phase84_3_composition_reuses_other_initial_premises():
  data = build_phase84_3_data()

  availability = data[
    "producer_availabilities"
  ][
    1
  ][
    0
  ]

  assert availability.matched_steps == (
    None,
    data[
      "phase77"
    ][
      "suspension_bridge_step"
    ],
    data[
      "phase77"
    ][
      "sigma_definition_step"
    ],
  )


def test_phase84_3_analysis_uses_only_initial_repository_steps():
  data = build_phase84_3_data()

  bracket_sum_conclusion = data[
    "phase77"
  ][
    "bracket_sum_step"
  ].conclusion

  assert all(
    step.conclusion
    != bracket_sum_conclusion
    for step in data[
      "initial_steps"
    ]
  )

  composition_availability = data[
    "producer_availabilities"
  ][
    1
  ][
    0
  ]

  assert (
    composition_availability
    .matched_steps[
      0
    ]
    is None
  )


def test_phase84_3_analysis_does_not_mutate_repository():
  data = build_phase84_3_data()

  assert (
    repository_available_steps(
      data[
        "repository"
      ]
    )
    == data[
      "initial_steps"
    ]
  )


def test_phase84_3_empty_candidate_lookup_returns_empty():
  data = build_phase84_3_data()

  lookup = data[
    "lookups"
  ][
    0
  ]

  empty_lookup = type(
    lookup
  )(
    inference_rule=(
      lookup.inference_rule
    ),
    premise_index=(
      lookup.premise_index
    ),
    premise_pattern=(
      lookup.premise_pattern
    ),
    producer_rules=(),
  )

  assert (
    analyze_producer_premise_availabilities(
      empty_lookup,
      data[
        "initial_steps"
      ],
    )
    == ()
  )


def test_phase84_3_rejects_wrong_lookup_type():
  data = build_phase84_3_data()

  with pytest.raises(
    TypeError,
    match=(
      "lookup must be a "
      "MissingPremiseProducerLookup"
    ),
  ):
    analyze_producer_premise_availabilities(
      object(),
      data[
        "initial_steps"
      ],
    )
