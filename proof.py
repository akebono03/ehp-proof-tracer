from dataclasses import dataclass
from enum import Enum
from typing import Any


class RelationType(Enum):
  EQUALITY = "equality"
  ZERO = "zero"
  ORDER = "order"


@dataclass(frozen=True)
class LiteratureReference:
  label: str
  author: str | None = None
  title: str | None = None
  year: int | None = None
  locator: str | None = None


@dataclass(frozen=True)
class Relation:
  lhs: Any
  rhs: Any
  relation_type: RelationType = RelationType.EQUALITY
  source: LiteratureReference | str | None = None
  note: str | None = None


class ProofRule(Enum):
  GIVEN = "given"
  RELATION = "relation"
  INFERENCE = "inference"
  EXACTNESS = "exactness"
  EHP_EXACTNESS = "ehp_exactness"
  KERNEL_COMPUTATION = "kernel_computation"
  IMAGE_COMPUTATION = "image_computation"
  COKERNEL_COMPUTATION = "cokernel_computation"


@dataclass(frozen=True)
class PremisePattern:
  proof_rule: ProofRule | None = None
  statement_type: type | None = None
  relation_type: RelationType | None = None


@dataclass(frozen=True)
class PatternVariable:
  name: str

  def __post_init__(self):
    if not isinstance(
      self.name,
      str,
    ):
      raise TypeError(
        "name must be a str"
      )

    if not self.name:
      raise ValueError(
        "name must not be empty"
      )


@dataclass(frozen=True)
class InferenceRule:
  name: str
  description: str | None = None
  premise_patterns: tuple[PremisePattern, ...] = ()
  conclusion_builder: Any = None


@dataclass(frozen=True)
class ProofStep:
  conclusion: Any
  premises: tuple[Any, ...]
  rule: ProofRule
  note: str | None = None
  inference_rule: InferenceRule | None = None


@dataclass(frozen=True)
class InferenceMatch:
  inference_rule: InferenceRule
  premises: tuple[ProofStep, ...]


class InferenceRejectionReason(Enum):
  ALREADY_KNOWN = "already_known"
  SAME_ROUND_DUPLICATE = (
    "same_round_duplicate"
  )


@dataclass(frozen=True)
class InferenceApplicationResult:
  match: InferenceMatch
  candidate_step: ProofStep
  accepted: bool | None = None
  rejection_reason: (
    InferenceRejectionReason | None
  ) = None


class InferenceTerminationReason(Enum):
  FIXED_POINT = "fixed_point"
  MAX_ROUNDS = "max_rounds"


@dataclass(frozen=True)
class InferenceRoundResult:
  new_steps: tuple[ProofStep, ...]
  matches: tuple[InferenceMatch, ...] = ()
  candidate_steps: tuple[ProofStep, ...] = ()
  duplicate_rejected_steps: tuple[ProofStep, ...] = ()
  application_results: tuple[
    InferenceApplicationResult,
    ...
  ] = ()


@dataclass(frozen=True)
class InferenceRunResult:
  steps: tuple[ProofStep, ...]
  round_results: tuple[
    InferenceRoundResult,
    ...
  ]
  termination_reason: InferenceTerminationReason

  @property
  def round_history(self):
    return tuple(
      round_result.new_steps
      for round_result
      in self.round_results
    )

  @property
  def round_count(self):
    return len(
      self.round_results
    )


@dataclass
class Proof:
  conclusion: Any
  steps: list[ProofStep]


def matches_premise_pattern(
  pattern,
  step,
):
  if not isinstance(
    pattern,
    PremisePattern,
  ):
    raise TypeError(
      "pattern must be a PremisePattern"
    )

  if not isinstance(
    step,
    ProofStep,
  ):
    raise TypeError(
      "step must be a ProofStep"
    )

  if (
    pattern.proof_rule is not None
    and step.rule != pattern.proof_rule
  ):
    return False

  if (
    pattern.statement_type is not None
    and not isinstance(
      step.conclusion,
      pattern.statement_type,
    )
  ):
    return False

  if pattern.relation_type is not None:
    if not isinstance(
      step.conclusion,
      Relation,
    ):
      return False

    if (
      step.conclusion.relation_type
      != pattern.relation_type
    ):
      return False

  return True


def matches_inference_rule(
  inference_rule,
  steps,
):
  if not isinstance(
    inference_rule,
    InferenceRule,
  ):
    raise TypeError(
      "inference_rule must be "
      "an InferenceRule"
    )

  normalized_steps = (
    _normalize_proof_steps(
      steps,
      "steps",
    )
  )

  patterns = (
    inference_rule.premise_patterns
  )

  if len(patterns) != len(
    normalized_steps
  ):
    return False

  return all(
    matches_premise_pattern(
      pattern,
      step,
    )
    for pattern, step in zip(
      patterns,
      normalized_steps,
    )
  )


def find_matching_premises(
  inference_rule,
  available_steps,
):
  matches = (
    find_all_matching_premises(
      inference_rule,
      available_steps,
    )
  )

  if not matches:
    return None

  return matches[0]


def find_all_matching_premises(
  inference_rule,
  available_steps,
):
  if not isinstance(
    inference_rule,
    InferenceRule,
  ):
    raise TypeError(
      "inference_rule must be "
      "an InferenceRule"
    )

  normalized_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  patterns = (
    inference_rule.premise_patterns
  )

  if not patterns:
    return (
      (),
    )

  results = []

  def search(
    pattern_index,
    matched_steps,
    used_indices,
  ):
    if pattern_index == len(
      patterns
    ):
      results.append(
        tuple(
          matched_steps
        )
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

      if not matches_premise_pattern(
        pattern,
        step,
      ):
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
      )

  search(
    0,
    [],
    set(),
  )

  return tuple(
    results
  )


def is_inference_rule_applicable(
  inference_rule,
  available_steps,
):
  return (
    find_matching_premises(
      inference_rule,
      available_steps,
    )
    is not None
  )


def find_applicable_inference_rules(
  inference_rules,
  available_steps,
):
  normalized_rules = (
    _normalize_inference_rules(
      inference_rules
    )
  )

  normalized_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  return tuple(
    inference_rule
    for inference_rule
    in normalized_rules
    if is_inference_rule_applicable(
      inference_rule,
      normalized_steps,
    )
  )


def find_inference_match(
  inference_rule,
  available_steps,
):
  matches = (
    find_inference_matches_for_rule(
      inference_rule,
      available_steps,
    )
  )

  if not matches:
    return None

  return matches[0]


def find_inference_matches(
  inference_rules,
  available_steps,
):
  normalized_rules = (
    _normalize_inference_rules(
      inference_rules
    )
  )

  normalized_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  matches = []

  for inference_rule in (
    normalized_rules
  ):
    matches.extend(
      find_inference_matches_for_rule(
        inference_rule,
        normalized_steps,
      )
    )

  return tuple(
    matches
  )


def find_inference_matches_for_rule(
  inference_rule,
  available_steps,
):
  premise_assignments = (
    find_all_matching_premises(
      inference_rule,
      available_steps,
    )
  )

  return tuple(
    InferenceMatch(
      inference_rule=inference_rule,
      premises=premises,
    )
    for premises
    in premise_assignments
  )


def apply_inference_match(
  inference_match,
):
  if not isinstance(
    inference_match,
    InferenceMatch,
  ):
    raise TypeError(
      "inference_match must be "
      "an InferenceMatch"
    )

  inference_rule = (
    inference_match.inference_rule
  )

  conclusion_builder = (
    inference_rule.conclusion_builder
  )

  if conclusion_builder is None:
    raise ValueError(
      "inference rule must have "
      "a conclusion builder"
    )

  if not callable(
    conclusion_builder
  ):
    raise TypeError(
      "conclusion_builder must be "
      "callable"
    )

  conclusion = conclusion_builder(
    inference_match.premises
  )

  return ProofStep(
    conclusion=conclusion,
    premises=inference_match.premises,
    rule=ProofRule.INFERENCE,
    inference_rule=inference_rule,
  )


def apply_inference_matches(
  inference_matches,
):
  normalized_matches = (
    _normalize_inference_matches(
      inference_matches
    )
  )

  return tuple(
    apply_inference_match(
      inference_match
    )
    for inference_match
    in normalized_matches
  )


def apply_inference_matches_with_results(
  inference_matches,
):
  normalized_matches = (
    _normalize_inference_matches(
      inference_matches
    )
  )

  results = []

  for inference_match in (
    normalized_matches
  ):
    candidate_step = (
      apply_inference_match(
        inference_match
      )
    )

    results.append(
      InferenceApplicationResult(
        match=inference_match,
        candidate_step=(
          candidate_step
        ),
      )
    )

  return tuple(
    results
  )


def relation_proof_step(relation):
  if not isinstance(relation, Relation):
    raise TypeError(
      "relation must be a Relation"
    )

  return ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )


@dataclass(frozen=True)
class KernelStatement:
  group_map: Any
  structure: Any


@dataclass(frozen=True)
class ImageStatement:
  group_map: Any
  structure: Any


@dataclass(frozen=True)
class CokernelStatement:
  group_map: Any
  structure: Any


def kernel_proof_step(group_map):
  statement = KernelStatement(
    group_map=group_map,
    structure=group_map.kernel_structure(),
  )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.KERNEL_COMPUTATION,
  )


def image_proof_step(group_map):
  statement = ImageStatement(
    group_map=group_map,
    structure=group_map.image_structure(),
  )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.IMAGE_COMPUTATION,
  )


def cokernel_proof_step(group_map):
  statement = CokernelStatement(
    group_map=group_map,
    structure=group_map.cokernel_structure(),
  )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.COKERNEL_COMPUTATION,
  )


@dataclass(frozen=True)
class ExactnessStatement:
  first_map: Any
  second_map: Any
  is_exact: bool


def exactness_proof_step(
  exact_step,
  image_step,
  kernel_step,
):
  if not isinstance(
    image_step.conclusion,
    ImageStatement,
  ):
    raise TypeError(
      "image_step must conclude "
      "an ImageStatement"
    )

  if not isinstance(
    kernel_step.conclusion,
    KernelStatement,
  ):
    raise TypeError(
      "kernel_step must conclude "
      "a KernelStatement"
    )

  if (
    image_step.conclusion.group_map
    is not exact_step.first_map
  ):
    raise ValueError(
      "image_step must refer to first_map"
    )

  if (
    kernel_step.conclusion.group_map
    is not exact_step.second_map
  ):
    raise ValueError(
      "kernel_step must refer to second_map"
    )

  statement = ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=exact_step.is_exact(),
  )

  return ProofStep(
    conclusion=statement,
    premises=(
      image_step,
      kernel_step,
    ),
    rule=ProofRule.EXACTNESS,
  )


def ehp_exactness_proof_step(
  exact_step,
  image_step,
  kernel_step,
):
  exactness_step = exactness_proof_step(
    exact_step,
    image_step,
    kernel_step,
  )

  return ProofStep(
    conclusion=exactness_step.conclusion,
    premises=exactness_step.premises,
    rule=ProofRule.EHP_EXACTNESS,
  )


def ehp_exactness_proof(exact_step):
  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  exactness_step = (
    ehp_exactness_proof_step(
      exact_step,
      image_step,
      kernel_step,
    )
  )

  return Proof(
    conclusion=exactness_step.conclusion,
    steps=[
      image_step,
      kernel_step,
      exactness_step,
    ],
  )


def ehp_sphere_proof(segment):
  return ehp_exactness_proof(
    segment.exact_step_at_sphere()
  )


def ehp_hopf_target_proof(segment):
  return ehp_exactness_proof(
    segment.exact_step_at_hopf_target()
  )


def _normalize_proof_steps(
  steps,
  name,
):
  if isinstance(
    steps,
    ProofStep,
  ):
    return (
      steps,
    )

  if not isinstance(
    steps,
    (tuple, list),
  ):
    raise TypeError(
      f"{name} must be a ProofStep "
      "or a tuple/list of ProofStep"
    )

  normalized = tuple(
    steps
  )

  for step in normalized:
    if not isinstance(
      step,
      ProofStep,
    ):
      raise TypeError(
        f"{name} must contain "
        "only ProofStep objects"
      )

  return normalized


def _normalize_inference_rules(
  inference_rules,
):
  if isinstance(
    inference_rules,
    InferenceRule,
  ):
    return (
      inference_rules,
    )

  if not isinstance(
    inference_rules,
    (tuple, list),
  ):
    raise TypeError(
      "inference_rules must be "
      "an InferenceRule or a "
      "tuple/list of InferenceRule"
    )

  normalized = tuple(
    inference_rules
  )

  for inference_rule in normalized:
    if not isinstance(
      inference_rule,
      InferenceRule,
    ):
      raise TypeError(
        "inference_rules must contain "
        "only InferenceRule objects"
      )

  return normalized


def _normalize_inference_matches(
  inference_matches,
):
  if isinstance(
    inference_matches,
    InferenceMatch,
  ):
    return (
      inference_matches,
    )

  if not isinstance(
    inference_matches,
    (tuple, list),
  ):
    raise TypeError(
      "inference_matches must be "
      "an InferenceMatch or a "
      "tuple/list of InferenceMatch"
    )

  normalized = tuple(
    inference_matches
  )

  for inference_match in normalized:
    if not isinstance(
      inference_match,
      InferenceMatch,
    ):
      raise TypeError(
        "inference_matches must contain "
        "only InferenceMatch objects"
      )

  return normalized


def _normalize_inference_application_results(
  application_results,
):
  if isinstance(
    application_results,
    InferenceApplicationResult,
  ):
    return (
      application_results,
    )

  if not isinstance(
    application_results,
    (tuple, list),
  ):
    raise TypeError(
      "application_results must be "
      "an InferenceApplicationResult "
      "or a tuple/list of "
      "InferenceApplicationResult"
    )

  normalized = tuple(
    application_results
  )

  for application_result in (
    normalized
  ):
    if not isinstance(
      application_result,
      InferenceApplicationResult,
    ):
      raise TypeError(
        "application_results must "
        "contain only "
        "InferenceApplicationResult "
        "objects"
      )

  return normalized


def _normalize_relations(
  relations,
):
  if isinstance(
    relations,
    Relation,
  ):
    return (
      relations,
    )

  if not isinstance(
    relations,
    (tuple, list),
  ):
    raise TypeError(
      "relations must be a Relation "
      "or a tuple/list of Relation"
    )

  normalized = tuple(
    relations
  )

  for relation in normalized:
    if not isinstance(
      relation,
      Relation,
    ):
      raise TypeError(
        "relations must contain "
        "only Relation objects"
      )

  return normalized


def _validate_inference_rule(
  inference_rule,
):
  if (
    inference_rule is not None
    and not isinstance(
      inference_rule,
      InferenceRule,
    )
  ):
    raise TypeError(
      "inference_rule must be "
      "an InferenceRule or None"
    )


def relation_inference_proof_step(
  conclusion,
  relation_steps,
  premises=(),
  note=None,
  inference_rule=None,
):
  normalized_relation_steps = (
    _normalize_proof_steps(
      relation_steps,
      "relation_steps",
    )
  )

  if not normalized_relation_steps:
    raise ValueError(
      "relation_steps must not be empty"
    )

  for relation_step in (
    normalized_relation_steps
  ):
    if (
      relation_step.rule
      != ProofRule.RELATION
    ):
      raise ValueError(
        "relation_steps must use "
        "ProofRule.RELATION"
      )

    if not isinstance(
      relation_step.conclusion,
      Relation,
    ):
      raise ValueError(
        "relation_steps must conclude "
        "Relation objects"
      )

  normalized_premises = (
    _normalize_proof_steps(
      premises,
      "premises",
    )
  )

  _validate_inference_rule(
    inference_rule
  )

  return ProofStep(
    conclusion=conclusion,
    premises=(
      normalized_relation_steps
      + normalized_premises
    ),
    rule=ProofRule.RELATION,
    note=note,
    inference_rule=inference_rule,
  )


def relation_inference_proof(
  relations,
  conclusion,
  premises=(),
  note=None,
  inference_rule=None,
):
  normalized_relations = (
    _normalize_relations(
      relations
    )
  )

  if not normalized_relations:
    raise ValueError(
      "relations must not be empty"
    )

  relation_steps = tuple(
    relation_proof_step(
      relation
    )
    for relation
    in normalized_relations
  )

  normalized_premises = (
    _normalize_proof_steps(
      premises,
      "premises",
    )
  )

  _validate_inference_rule(
    inference_rule
  )

  inference_step = (
    relation_inference_proof_step(
      conclusion,
      relation_steps,
      premises=normalized_premises,
      note=note,
      inference_rule=inference_rule,
    )
  )

  return Proof(
    conclusion=inference_step.conclusion,
    steps=[
      *relation_steps,
      *normalized_premises,
      inference_step,
    ],
  )


def _validate_max_rounds(
  max_rounds,
):
  if max_rounds is None:
    return

  if (
    isinstance(
      max_rounds,
      bool,
    )
    or not isinstance(
      max_rounds,
      int,
    )
  ):
    raise TypeError(
      "max_rounds must be "
      "an int or None"
    )

  if max_rounds < 0:
    raise ValueError(
      "max_rounds must be "
      "non-negative"
    )


def derive_inference_steps(
  inference_rules,
  available_steps,
):
  matches = find_inference_matches(
    inference_rules,
    available_steps,
  )

  return apply_inference_matches(
    matches
  )


def merge_proof_steps(
  available_steps,
  derived_steps,
):
  normalized_available_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  normalized_derived_steps = (
    _normalize_proof_steps(
      derived_steps,
      "derived_steps",
    )
  )

  merged_steps = list(
    normalized_available_steps
  )

  known_conclusions = [
    step.conclusion
    for step in merged_steps
  ]

  for step in normalized_derived_steps:
    if any(
      step.conclusion
      == known_conclusion
      for known_conclusion
      in known_conclusions
    ):
      continue

    merged_steps.append(
      step
    )

    known_conclusions.append(
      step.conclusion
    )

  return tuple(
    merged_steps
  )


def partition_new_and_duplicate_proof_steps(
  available_steps,
  candidate_steps,
):
  normalized_available_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  normalized_candidate_steps = (
    _normalize_proof_steps(
      candidate_steps,
      "candidate_steps",
    )
  )

  seen_conclusions = [
    step.conclusion
    for step
    in normalized_available_steps
  ]

  new_steps = []
  duplicate_rejected_steps = []

  for step in normalized_candidate_steps:
    if any(
      step.conclusion
      == seen_conclusion
      for seen_conclusion
      in seen_conclusions
    ):
      duplicate_rejected_steps.append(
        step
      )
      continue

    new_steps.append(
      step
    )

    seen_conclusions.append(
      step.conclusion
    )

  return (
    tuple(new_steps),
    tuple(
      duplicate_rejected_steps
    ),
  )


def classify_inference_application_results(
  available_steps,
  application_results,
):
  normalized_available_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  normalized_application_results = (
    _normalize_inference_application_results(
      application_results
    )
  )

  known_before_round = [
    step.conclusion
    for step
    in normalized_available_steps
  ]

  accepted_in_round = []
  classified_results = []

  for application_result in (
    normalized_application_results
  ):
    candidate_step = (
      application_result.candidate_step
    )

    candidate_conclusion = (
      candidate_step.conclusion
    )

    if any(
      candidate_conclusion
      == known_conclusion
      for known_conclusion
      in known_before_round
    ):
      classified_results.append(
        InferenceApplicationResult(
          match=application_result.match,
          candidate_step=candidate_step,
          accepted=False,
          rejection_reason=(
            InferenceRejectionReason.ALREADY_KNOWN
          ),
        )
      )
      continue

    if any(
      candidate_conclusion
      == accepted_conclusion
      for accepted_conclusion
      in accepted_in_round
    ):
      classified_results.append(
        InferenceApplicationResult(
          match=application_result.match,
          candidate_step=candidate_step,
          accepted=False,
          rejection_reason=(
            InferenceRejectionReason
            .SAME_ROUND_DUPLICATE
          ),
        )
      )
      continue

    classified_results.append(
      InferenceApplicationResult(
        match=application_result.match,
        candidate_step=candidate_step,
        accepted=True,
        rejection_reason=None,
      )
    )

    accepted_in_round.append(
      candidate_conclusion
    )

  return tuple(
    classified_results
  )


def derive_inference_round_result(
  inference_rules,
  available_steps,
):
  normalized_rules = (
    _normalize_inference_rules(
      inference_rules
    )
  )

  normalized_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  matches = find_inference_matches(
    normalized_rules,
    normalized_steps,
  )

  raw_application_results = (
    apply_inference_matches_with_results(
      matches
    )
  )

  application_results = (
    classify_inference_application_results(
      normalized_steps,
      raw_application_results,
    )
  )

  candidate_steps = tuple(
    application_result.candidate_step
    for application_result
    in application_results
  )

  new_steps = tuple(
    application_result.candidate_step
    for application_result
    in application_results
    if application_result.accepted
  )

  duplicate_rejected_steps = tuple(
    application_result.candidate_step
    for application_result
    in application_results
    if (
      application_result.accepted
      is False
    )
  )

  return InferenceRoundResult(
    new_steps=new_steps,
    matches=matches,
    candidate_steps=candidate_steps,
    duplicate_rejected_steps=(
      duplicate_rejected_steps
    ),
    application_results=(
      application_results
    ),
  )


def derive_new_inference_steps(
  inference_rules,
  available_steps,
):
  round_result = (
    derive_inference_round_result(
      inference_rules,
      available_steps,
    )
  )

  return round_result.new_steps


def run_inference_round(
  inference_rules,
  available_steps,
):
  normalized_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  new_steps = derive_new_inference_steps(
    inference_rules,
    normalized_steps,
  )

  return (
    normalized_steps
    + new_steps
  )


def run_inference_until_stable_with_history(
  inference_rules,
  available_steps,
  max_rounds=None,
):
  normalized_rules = (
    _normalize_inference_rules(
      inference_rules
    )
  )

  current_steps = (
    _normalize_proof_steps(
      available_steps,
      "available_steps",
    )
  )

  _validate_max_rounds(
    max_rounds
  )

  round_results = []

  while True:
    if (
      max_rounds is not None
      and len(
        round_results
      ) >= max_rounds
    ):
      return InferenceRunResult(
        steps=current_steps,
        round_results=tuple(
          round_results
        ),
        termination_reason=(
          InferenceTerminationReason.MAX_ROUNDS
        ),
      )

    round_result = (
      derive_inference_round_result(
        normalized_rules,
        current_steps,
      )
    )

    new_steps = (
      round_result.new_steps
    )

    if not new_steps:
      return InferenceRunResult(
        steps=current_steps,
        round_results=tuple(
          round_results
        ),
        termination_reason=(
          InferenceTerminationReason.FIXED_POINT
        ),
      )

    round_results.append(
      round_result
    )

    current_steps = (
      current_steps
      + new_steps
    )


def run_inference_until_stable(
  inference_rules,
  available_steps,
  max_rounds=None,
):
  result = (
    run_inference_until_stable_with_history(
      inference_rules,
      available_steps,
      max_rounds=max_rounds,
    )
  )

  return result.steps








