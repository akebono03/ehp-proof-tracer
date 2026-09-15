from dataclasses import dataclass
from functools import lru_cache

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  derive_goal_from_repository_with_catalog,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_goal_compatible_rule_entries,
  find_goal_compatible_rules,
)
from test_phase81_actual_theorem_integration import (
  build_phase81_5_data,
)


@dataclass(frozen=True)
class MissingPremiseStatement:
  value: str


@dataclass(frozen=True)
class UnrelatedConclusionStatement:
  value: str


def _collect_ancestors(
  step,
):
  ancestors = []
  seen = set()
  stack = list(
    step.premises
  )

  while stack:
    current = stack.pop()

    current_id = id(
      current
    )

    if current_id in seen:
      continue

    seen.add(
      current_id
    )

    ancestors.append(
      current
    )

    stack.extend(
      current.premises
    )

  return tuple(
    ancestors
  )


def _proof_graph_is_acyclic(
  step,
):
  visited = set()
  active = set()

  def visit(
    current,
  ):
    current_id = id(
      current
    )

    if current_id in active:
      return False

    if current_id in visited:
      return True

    active.add(
      current_id
    )

    for premise in current.premises:
      if not visit(
        premise
      ):
        return False

    active.remove(
      current_id
    )

    visited.add(
      current_id
    )

    return True

  return visit(
    step
  )


def _all_matches(
  inference_result,
):
  return tuple(
    match
    for round_result
    in inference_result.round_results
    for match
    in round_result.matches
  )


def _all_application_results(
  inference_result,
):
  return tuple(
    application_result
    for round_result
    in inference_result.round_results
    for application_result
    in round_result.application_results
  )


@lru_cache(maxsize=1)
def build_phase81_6_data():
  phase81_5 = (
    build_phase81_5_data()
  )

  phase80 = phase81_5[
    "phase80"
  ]

  repository = phase80[
    "repository"
  ]

  goal = phase80[
    "goal"
  ]

  final_rule = phase80[
    "final_rule"
  ]

  bracket_sum_type = type(
    phase80[
      "bracket_sum_step"
    ].conclusion
  )

  composition_type = type(
    phase80[
      "composition_step"
    ].conclusion
  )

  goal_type = type(
    goal
  )

  def build_actual_goal(
    premises,
  ):
    return goal

  wrong_guard_rule = (
    InferenceRule(
      name=(
        "Phase 81 wrong-instance "
        "Toda Lemma 5.16 candidate"
      ),
      premise_patterns=(
        PremisePattern(
          proof_rule=(
            ProofRule.INFERENCE
          ),
          statement_type=(
            bracket_sum_type
          ),
        ),
        PremisePattern(
          proof_rule=(
            ProofRule.INFERENCE
          ),
          statement_type=(
            composition_type
          ),
        ),
      ),
      conclusion_builder=(
        build_actual_goal
      ),
      match_guard=(
        lambda premises, bindings: False
      ),
    )
  )

  missing_premise_rule = (
    InferenceRule(
      name=(
        "Phase 81 missing-premise "
        "Toda Lemma 5.16 candidate"
      ),
      premise_patterns=(
        PremisePattern(
          proof_rule=(
            ProofRule.INFERENCE
          ),
          statement_type=(
            MissingPremiseStatement
          ),
        ),
      ),
      conclusion_builder=(
        build_actual_goal
      ),
    )
  )

  unsafe_rule = (
    InferenceRule(
      name=(
        "Phase 81 unsafe "
        "Toda Lemma 5.16 candidate"
      ),
      premise_patterns=(
        PremisePattern(
          proof_rule=(
            ProofRule.INFERENCE
          ),
          statement_type=(
            bracket_sum_type
          ),
        ),
        PremisePattern(
          proof_rule=(
            ProofRule.INFERENCE
          ),
          statement_type=(
            composition_type
          ),
        ),
      ),
      conclusion_builder=(
        build_actual_goal
      ),
    )
  )

  unrelated_rule = (
    InferenceRule(
      name=(
        "Phase 81 unrelated candidate"
      ),
      conclusion_builder=(
        lambda premises: (
          UnrelatedConclusionStatement(
            value="unrelated",
          )
        )
      ),
    )
  )

  catalog = (
    InferenceRuleCatalog()
  )

  correct_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase77."
        "toda_lemma516_final"
      ),
      rule=final_rule,
      conclusion_type=goal_type,
      fixed_point_safe=True,
    )
  )

  alias_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase77."
        "toda_lemma516_final.alias"
      ),
      rule=final_rule,
      conclusion_type=goal_type,
      fixed_point_safe=True,
    )
  )

  wrong_guard_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase81."
        "wrong_instance"
      ),
      rule=wrong_guard_rule,
      conclusion_type=goal_type,
      fixed_point_safe=True,
    )
  )

  missing_premise_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase81."
        "missing_premise"
      ),
      rule=missing_premise_rule,
      conclusion_type=goal_type,
      fixed_point_safe=True,
    )
  )

  unsafe_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase81."
        "unsafe_candidate"
      ),
      rule=unsafe_rule,
      conclusion_type=goal_type,
      fixed_point_safe=False,
    )
  )

  unrelated_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase81."
        "unrelated_candidate"
      ),
      rule=unrelated_rule,
      conclusion_type=(
        UnrelatedConclusionStatement
      ),
      fixed_point_safe=True,
    )
  )

  for entry in (
    correct_entry,
    alias_entry,
    wrong_guard_entry,
    missing_premise_entry,
    unsafe_entry,
    unrelated_entry,
  ):
    catalog.register(
      entry
    )

  compatible_entries = (
    find_goal_compatible_rule_entries(
      catalog,
      goal,
    )
  )

  compatible_rules = (
    find_goal_compatible_rules(
      catalog,
      goal,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      goal,
    )
  )

  goal_step = result.goal_step

  if goal_step is None:
    raise RuntimeError(
      "Phase 81-6 actual Toda "
      "Lemma 5.16 goal was not derived"
    )

  ancestors = (
    _collect_ancestors(
      goal_step
    )
  )

  matches = (
    _all_matches(
      result.inference_result
    )
  )

  application_results = (
    _all_application_results(
      result.inference_result
    )
  )

  return {
    "phase81_5": phase81_5,
    "phase80": phase80,
    "repository": repository,
    "goal": goal,
    "final_rule": final_rule,
    "catalog": catalog,
    "correct_entry": correct_entry,
    "alias_entry": alias_entry,
    "wrong_guard_entry": (
      wrong_guard_entry
    ),
    "missing_premise_entry": (
      missing_premise_entry
    ),
    "unsafe_entry": unsafe_entry,
    "unrelated_entry": (
      unrelated_entry
    ),
    "wrong_guard_rule": (
      wrong_guard_rule
    ),
    "missing_premise_rule": (
      missing_premise_rule
    ),
    "unsafe_rule": unsafe_rule,
    "unrelated_rule": (
      unrelated_rule
    ),
    "compatible_entries": (
      compatible_entries
    ),
    "compatible_rules": (
      compatible_rules
    ),
    "result": result,
    "goal_step": goal_step,
    "ancestors": ancestors,
    "matches": matches,
    "application_results": (
      application_results
    ),
  }


def test_phase81_6_goal_filter_keeps_safe_same_type_candidates():
  data = build_phase81_6_data()

  assert (
    data[
      "compatible_entries"
    ]
    == (
      data[
        "correct_entry"
      ],
      data[
        "alias_entry"
      ],
      data[
        "wrong_guard_entry"
      ],
      data[
        "missing_premise_entry"
      ],
    )
  )


def test_phase81_6_goal_filter_excludes_unsafe_candidate():
  data = build_phase81_6_data()

  assert (
    data[
      "unsafe_entry"
    ]
    not in data[
      "compatible_entries"
    ]
  )

  assert (
    data[
      "unsafe_rule"
    ]
    not in data[
      "compatible_rules"
    ]
  )


def test_phase81_6_goal_filter_excludes_unrelated_conclusion_type():
  data = build_phase81_6_data()

  assert (
    data[
      "unrelated_entry"
    ]
    not in data[
      "compatible_entries"
    ]
  )

  assert (
    data[
      "unrelated_rule"
    ]
    not in data[
      "compatible_rules"
    ]
  )


def test_phase81_6_rule_alias_is_deduplicated_before_execution():
  data = build_phase81_6_data()

  assert (
    data[
      "compatible_rules"
    ].count(
      data[
        "final_rule"
      ]
    )
    == 1
  )

  assert (
    data[
      "compatible_rules"
    ][0]
    is data[
      "final_rule"
    ]
  )


def test_phase81_6_wrong_guard_candidate_is_selected_but_not_applicable():
  data = build_phase81_6_data()

  assert (
    data[
      "wrong_guard_rule"
    ]
    in data[
      "compatible_rules"
    ]
  )

  assert all(
    match.inference_rule
    is not data[
      "wrong_guard_rule"
    ]
    for match in data[
      "matches"
    ]
  )


def test_phase81_6_missing_premise_candidate_is_selected_but_not_applicable():
  data = build_phase81_6_data()

  assert (
    data[
      "missing_premise_rule"
    ]
    in data[
      "compatible_rules"
    ]
  )

  assert all(
    match.inference_rule
    is not data[
      "missing_premise_rule"
    ]
    for match in data[
      "matches"
    ]
  )


def test_phase81_6_unsafe_candidate_never_reaches_matching():
  data = build_phase81_6_data()

  assert all(
    match.inference_rule
    is not data[
      "unsafe_rule"
    ]
    for match in data[
      "matches"
    ]
  )


def test_phase81_6_correct_actual_rule_derives_goal_under_ambiguity():
  data = build_phase81_6_data()

  assert (
    data[
      "goal_step"
    ].conclusion
    == data[
      "goal"
    ]
  )

  assert (
    data[
      "goal_step"
    ].inference_rule
    is data[
      "final_rule"
    ]
  )

  assert (
    data[
      "goal_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase81_6_only_correct_rule_produces_accepted_goal():
  data = build_phase81_6_data()

  accepted_goal_results = tuple(
    application_result
    for application_result
    in data[
      "application_results"
    ]
    if (
      application_result.accepted
      and (
        application_result
        .candidate_step
        .conclusion
        == data[
          "goal"
        ]
      )
    )
  )

  assert (
    len(
      accepted_goal_results
    )
    == 1
  )

  assert (
    accepted_goal_results[
      0
    ]
    .match
    .inference_rule
    is data[
      "final_rule"
    ]
  )


def test_phase81_6_alias_does_not_create_duplicate_accepted_goal():
  data = build_phase81_6_data()

  derived_goal_steps = tuple(
    step
    for step
    in data[
      "result"
    ]
    .inference_result
    .steps
    if (
      step.conclusion
      == data[
        "goal"
      ]
    )
  )

  assert (
    len(
      derived_goal_steps
    )
    == 1
  )

  assert (
    derived_goal_steps[0]
    is data[
      "goal_step"
    ]
  )


def test_phase81_6_goal_is_absent_from_derived_ancestry():
  data = build_phase81_6_data()

  assert all(
    ancestor.conclusion
    != data[
      "goal"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase81_6_derived_graph_remains_acyclic():
  data = build_phase81_6_data()

  assert (
    _proof_graph_is_acyclic(
      data[
        "goal_step"
      ]
    )
  )


def test_phase81_6_repository_remains_unchanged():
  data = build_phase81_6_data()

  assert (
    data[
      "repository"
    ].find_by_conclusion(
      data[
        "goal"
      ]
    )
    == ()
  )


def test_phase81_6_seed_goal_is_distinguished_from_derived_goal():
  data = build_phase81_6_data()

  given_goal_step = (
    ProofStep(
      conclusion=data[
        "goal"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    )
  )

  repository = (
    ProofRepository()
  )

  repository.register(
    ProofRepositoryEntry(
      key=(
        "phase81."
        "given_goal_seed"
      ),
      step=given_goal_step,
      phase="81",
      theorem=(
        "seed-goal-regression"
      ),
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.goal_step
    is given_goal_step
  )

  assert (
    result.goal_step.rule
    == ProofRule.GIVEN
  )

  assert (
    result.goal_step.inference_rule
    is None
  )


