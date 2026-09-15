from dataclasses import dataclass

from proof import (
  InferenceRule,
  InferenceRunResult,
  PremisePattern,
  ProofStep,
  find_goal_step,
  match_premise_pattern,
  merge_variable_bindings,
  run_inference_until_stable_with_history,
)
from proof_repository import ProofRepository
from rule_catalog import (
  InferenceRuleCatalog,
  find_goal_compatible_rules,
  find_premise_producer_rules,
)


@dataclass(frozen=True)
class RepositoryInferenceResult:
  inference_result: InferenceRunResult
  goal_step: ProofStep | None


@dataclass(frozen=True)
class PremiseAvailability:
  inference_rule: InferenceRule
  matched_steps: tuple[
    ProofStep | None,
    ...,
  ]
  missing_indices: tuple[
    int,
    ...,
  ]

  @property
  def missing_patterns(
    self,
  ) -> tuple[
    PremisePattern,
    ...,
  ]:
    return tuple(
      self.inference_rule.premise_patterns[
        index
      ]
      for index in self.missing_indices
    )

  @property
  def is_complete(
    self,
  ) -> bool:
    return not self.missing_indices


def repository_available_steps(
  repository: ProofRepository,
) -> tuple[
  ProofStep,
  ...,
]:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  steps = []
  seen_step_ids = set()

  for entry in repository.entries():
    step_id = id(
      entry.step
    )

    if step_id in seen_step_ids:
      continue

    seen_step_ids.add(
      step_id
    )
    steps.append(
      entry.step
    )

  return tuple(
    steps
  )


def detect_missing_premises(
  inference_rule,
  available_steps,
) -> PremiseAvailability:
  if not isinstance(
    inference_rule,
    InferenceRule,
  ):
    raise TypeError(
      "inference_rule must be an "
      "InferenceRule"
    )

  if isinstance(
    available_steps,
    ProofStep,
  ):
    normalized_steps = (
      available_steps,
    )
  elif isinstance(
    available_steps,
    (tuple, list),
  ):
    normalized_steps = tuple(
      available_steps
    )
  else:
    raise TypeError(
      "available_steps must be a "
      "ProofStep or tuple/list of "
      "ProofStep"
    )

  for step in normalized_steps:
    if not isinstance(
      step,
      ProofStep,
    ):
      raise TypeError(
        "available_steps must contain "
        "only ProofStep objects"
      )

  patterns = (
    inference_rule.premise_patterns
  )

  if not patterns:
    return PremiseAvailability(
      inference_rule=inference_rule,
      matched_steps=(),
      missing_indices=(),
    )

  best_matched_steps = None
  best_match_count = -1

  def search(
    pattern_index,
    matched_steps,
    used_indices,
    bindings,
  ):
    nonlocal best_matched_steps
    nonlocal best_match_count

    if pattern_index == len(
      patterns
    ):
      match_count = sum(
        step is not None
        for step in matched_steps
      )

      if (
        match_count
        > best_match_count
      ):
        best_match_count = (
          match_count
        )
        best_matched_steps = tuple(
          matched_steps
        )

      return

    pattern = patterns[
      pattern_index
    ]

    for index, step in enumerate(
      normalized_steps
    ):
      if index in used_indices:
        continue

      premise_bindings = (
        match_premise_pattern(
          pattern,
          step,
        )
      )

      if premise_bindings is None:
        continue

      merged_bindings = (
        merge_variable_bindings(
          bindings
          + premise_bindings
        )
      )

      if merged_bindings is None:
        continue

      search(
        pattern_index + 1,
        matched_steps + [
          step,
        ],
        used_indices
        | {
          index,
        },
        merged_bindings,
      )

    search(
      pattern_index + 1,
      matched_steps + [
        None,
      ],
      used_indices,
      bindings,
    )

  search(
    0,
    [],
    set(),
    (),
  )

  if best_matched_steps is None:
    best_matched_steps = tuple(
      None
      for _ in patterns
    )

  missing_indices = tuple(
    index
    for index, step
    in enumerate(
      best_matched_steps
    )
    if step is None
  )

  return PremiseAvailability(
    inference_rule=inference_rule,
    matched_steps=(
      best_matched_steps
    ),
    missing_indices=(
      missing_indices
    ),
  )


def detect_goal_rule_missing_premises(
  repository,
  rule_catalog,
  goal,
) -> tuple[
  PremiseAvailability,
  ...,
]:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a "
      "ProofRepository"
    )

  if not isinstance(
    rule_catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "rule_catalog must be an "
      "InferenceRuleCatalog"
    )

  available_steps = (
    repository_available_steps(
      repository
    )
  )

  inference_rules = (
    find_goal_compatible_rules(
      rule_catalog,
      goal,
    )
  )

  return tuple(
    detect_missing_premises(
      inference_rule,
      available_steps,
    )
    for inference_rule
    in inference_rules
  )


def derive_goal_from_repository(
  repository: ProofRepository,
  inference_rules,
  goal,
  max_rounds=None,
) -> RepositoryInferenceResult:
  available_steps = (
    repository_available_steps(
      repository
    )
  )

  inference_result = (
    run_inference_until_stable_with_history(
      inference_rules,
      available_steps,
      max_rounds=max_rounds,
    )
  )

  goal_step = find_goal_step(
    inference_result.steps,
    goal,
  )

  return RepositoryInferenceResult(
    inference_result=inference_result,
    goal_step=goal_step,
  )


def derive_goal_from_repository_with_catalog(
  repository: ProofRepository,
  rule_catalog: InferenceRuleCatalog,
  goal,
  max_rounds=None,
) -> RepositoryInferenceResult:
  inference_rules = (
    find_goal_compatible_rules(
      rule_catalog,
      goal,
    )
  )

  return derive_goal_from_repository(
    repository,
    inference_rules,
    goal,
    max_rounds=max_rounds,
  )


def derive_goal_from_repository_with_one_level_producers(
  repository: ProofRepository,
  rule_catalog: InferenceRuleCatalog,
  goal,
  max_rounds=None,
) -> RepositoryInferenceResult:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a "
      "ProofRepository"
    )

  if not isinstance(
    rule_catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "rule_catalog must be an "
      "InferenceRuleCatalog"
    )

  initial_steps = (
    repository_available_steps(
      repository
    )
  )

  final_rules = (
    find_goal_compatible_rules(
      rule_catalog,
      goal,
    )
  )

  producer_rules = []
  seen_producer_rule_ids = set()

  for final_rule in final_rules:
    availability = (
      detect_missing_premises(
        final_rule,
        initial_steps,
      )
    )

    if len(
      availability.missing_patterns
    ) != 1:
      continue

    missing_pattern = (
      availability.missing_patterns[
        0
      ]
    )

    candidate_producer_rules = (
      find_premise_producer_rules(
        rule_catalog,
        missing_pattern,
      )
    )

    if len(
      candidate_producer_rules
    ) != 1:
      continue

    producer_rule = (
      candidate_producer_rules[
        0
      ]
    )

    producer_rule_id = id(
      producer_rule
    )

    if (
      producer_rule_id
      in seen_producer_rule_ids
    ):
      continue

    seen_producer_rule_ids.add(
      producer_rule_id
    )
    producer_rules.append(
      producer_rule
    )

  if producer_rules:
    producer_result = (
      run_inference_until_stable_with_history(
        tuple(
          producer_rules
        ),
        initial_steps,
        max_rounds=1,
      )
    )

    final_available_steps = (
      producer_result.steps
    )
  else:
    final_available_steps = (
      initial_steps
    )

  final_result = (
    run_inference_until_stable_with_history(
      final_rules,
      final_available_steps,
      max_rounds=max_rounds,
    )
  )

  goal_step = find_goal_step(
    final_result.steps,
    goal,
  )

  return RepositoryInferenceResult(
    inference_result=final_result,
    goal_step=goal_step,
  )



