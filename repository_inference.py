from dataclasses import dataclass
from enum import Enum

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


@dataclass(frozen=True)
class MissingPremiseProducerLookup:
  inference_rule: InferenceRule
  premise_index: int
  premise_pattern: PremisePattern
  producer_rules: tuple[
    InferenceRule,
    ...,
  ]


@dataclass(frozen=True)
class BoundedProducerSearchNode:
  requesting_rule: InferenceRule
  premise_index: int
  premise_pattern: PremisePattern
  producer_rule: InferenceRule
  producer_availability: (
    PremiseAvailability
  )
  depths: tuple[
    int,
    ...,
  ]
  dependencies: tuple[
    "BoundedProducerSearchNode",
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.requesting_rule,
      InferenceRule,
    ):
      raise TypeError(
        "requesting_rule must be an "
        "InferenceRule"
      )

    if (
      isinstance(
        self.premise_index,
        bool,
      )
      or not isinstance(
        self.premise_index,
        int,
      )
    ):
      raise TypeError(
        "premise_index must be an int"
      )

    if (
      self.premise_index < 0
      or self.premise_index
      >= len(
        self.requesting_rule
        .premise_patterns
      )
    ):
      raise ValueError(
        "premise_index must identify a "
        "requesting_rule premise"
      )

    if not isinstance(
      self.premise_pattern,
      PremisePattern,
    ):
      raise TypeError(
        "premise_pattern must be a "
        "PremisePattern"
      )

    if (
      self.requesting_rule
      .premise_patterns[
        self.premise_index
      ]
      != self.premise_pattern
    ):
      raise ValueError(
        "premise_pattern must match the "
        "requesting_rule premise"
      )

    if not isinstance(
      self.producer_rule,
      InferenceRule,
    ):
      raise TypeError(
        "producer_rule must be an "
        "InferenceRule"
      )

    if not isinstance(
      self.producer_availability,
      PremiseAvailability,
    ):
      raise TypeError(
        "producer_availability must be a "
        "PremiseAvailability"
      )

    if (
      self.producer_availability
      .inference_rule
      is not self.producer_rule
    ):
      raise ValueError(
        "producer_availability must "
        "describe producer_rule"
      )

    if not isinstance(
      self.depths,
      tuple,
    ):
      raise TypeError(
        "depths must be a tuple"
      )

    if not self.depths:
      raise ValueError(
        "depths must not be empty"
      )

    if any(
      isinstance(
        depth,
        bool,
      )
      or not isinstance(
        depth,
        int,
      )
      for depth in self.depths
    ):
      raise TypeError(
        "depths must contain only ints"
      )

    if any(
      depth < 1
      for depth in self.depths
    ):
      raise ValueError(
        "depths must contain only "
        "positive values"
      )

    if (
      self.depths
      != tuple(
        sorted(
          set(
            self.depths
          )
        )
      )
    ):
      raise ValueError(
        "depths must be unique and sorted"
      )

    if not isinstance(
      self.dependencies,
      tuple,
    ):
      raise TypeError(
        "dependencies must be a tuple"
      )

    if any(
      not isinstance(
        dependency,
        BoundedProducerSearchNode,
      )
      for dependency
      in self.dependencies
    ):
      raise TypeError(
        "dependencies must contain only "
        "BoundedProducerSearchNode objects"
      )

  @property
  def minimum_depth(
    self,
  ) -> int:
    return min(
      self.depths
    )

  @property
  def maximum_depth(
    self,
  ) -> int:
    return max(
      self.depths
    )

  @property
  def is_shared(
    self,
  ) -> bool:
    return len(
      self.depths
    ) > 1


@dataclass(frozen=True)
class BoundedProducerSearchResult:
  goal: object
  final_rule: InferenceRule
  final_availability: (
    PremiseAvailability
  )
  producer_nodes: tuple[
    BoundedProducerSearchNode,
    ...,
  ]
  max_depth: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.final_rule,
      InferenceRule,
    ):
      raise TypeError(
        "final_rule must be an "
        "InferenceRule"
      )

    if not isinstance(
      self.final_availability,
      PremiseAvailability,
    ):
      raise TypeError(
        "final_availability must be a "
        "PremiseAvailability"
      )

    if (
      self.final_availability
      .inference_rule
      is not self.final_rule
    ):
      raise ValueError(
        "final_availability must describe "
        "final_rule"
      )

    if not isinstance(
      self.producer_nodes,
      tuple,
    ):
      raise TypeError(
        "producer_nodes must be a tuple"
      )

    if any(
      not isinstance(
        node,
        BoundedProducerSearchNode,
      )
      for node in self.producer_nodes
    ):
      raise TypeError(
        "producer_nodes must contain only "
        "BoundedProducerSearchNode objects"
      )

    if (
      isinstance(
        self.max_depth,
        bool,
      )
      or not isinstance(
        self.max_depth,
        int,
      )
    ):
      raise TypeError(
        "max_depth must be an int"
      )

    if self.max_depth < 1:
      raise ValueError(
        "max_depth must be positive"
      )

  @property
  def is_within_depth_limit(
    self,
  ) -> bool:
    return all(
      node.maximum_depth
      <= self.max_depth
      for node in self.producer_nodes
    )


class BoundedProducerSearchStatus(Enum):
  SUCCESS = "success"
  GOAL_ALREADY_AVAILABLE = (
    "goal_already_available"
  )
  NO_FINAL_RULE = "no_final_rule"
  AMBIGUOUS_FINAL_RULE = (
    "ambiguous_final_rule"
  )
  NO_PRODUCER = "no_producer"
  UNSAFE_PRODUCER = "unsafe_producer"
  AMBIGUOUS_PRODUCER = (
    "ambiguous_producer"
  )
  CYCLE_DETECTED = "cycle_detected"
  DEPTH_LIMIT = "depth_limit"
  PRODUCER_NOT_APPLICABLE = (
    "producer_not_applicable"
  )
  PRODUCER_OUTPUT_NOT_USABLE = (
    "producer_output_not_usable"
  )
  FINAL_RULE_NOT_APPLICABLE = (
    "final_rule_not_applicable"
  )
  GOAL_NOT_DERIVED = "goal_not_derived"


@dataclass(frozen=True)
class BoundedProducerSearchDiagnostic:
  status: BoundedProducerSearchStatus
  goal: object
  final_rule: InferenceRule | None = None
  requesting_rule: InferenceRule | None = None
  premise_index: int | None = None
  premise_pattern: PremisePattern | None = None
  current_depth: int | None = None
  required_next_depth: int | None = None
  producer_candidates: tuple[
    InferenceRule,
    ...,
  ] = ()
  unsafe_producer_candidates: tuple[
    InferenceRule,
    ...,
  ] = ()
  ancestor_rules: tuple[
    InferenceRule,
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.status,
      BoundedProducerSearchStatus,
    ):
      raise TypeError(
        "status must be a "
        "BoundedProducerSearchStatus"
      )

    if self.status in (
      BoundedProducerSearchStatus.SUCCESS,
      BoundedProducerSearchStatus
      .GOAL_ALREADY_AVAILABLE,
    ):
      raise ValueError(
        "diagnostic status must describe "
        "a failure"
      )

    for name, rule in (
      (
        "final_rule",
        self.final_rule,
      ),
      (
        "requesting_rule",
        self.requesting_rule,
      ),
    ):
      if (
        rule is not None
        and not isinstance(
          rule,
          InferenceRule,
        )
      ):
        raise TypeError(
          f"{name} must be an "
          "InferenceRule or None"
        )

    premise_context = (
      self.requesting_rule,
      self.premise_index,
      self.premise_pattern,
    )

    if (
      any(
        value is None
        for value in premise_context
      )
      and any(
        value is not None
        for value in premise_context
      )
    ):
      raise ValueError(
        "requesting_rule, premise_index, "
        "and premise_pattern must be "
        "provided together"
      )

    if self.premise_index is not None:
      if (
        isinstance(
          self.premise_index,
          bool,
        )
        or not isinstance(
          self.premise_index,
          int,
        )
      ):
        raise TypeError(
          "premise_index must be an int "
          "or None"
        )

      if (
        self.premise_index < 0
        or self.premise_index
        >= len(
          self.requesting_rule
          .premise_patterns
        )
      ):
        raise ValueError(
          "premise_index must identify a "
          "requesting_rule premise"
        )

      if not isinstance(
        self.premise_pattern,
        PremisePattern,
      ):
        raise TypeError(
          "premise_pattern must be a "
          "PremisePattern or None"
        )

      if (
        self.requesting_rule
        .premise_patterns[
          self.premise_index
        ]
        != self.premise_pattern
      ):
        raise ValueError(
          "premise_pattern must match the "
          "requesting_rule premise"
        )

    for name, depth in (
      (
        "current_depth",
        self.current_depth,
      ),
      (
        "required_next_depth",
        self.required_next_depth,
      ),
    ):
      if depth is None:
        continue

      if (
        isinstance(
          depth,
          bool,
        )
        or not isinstance(
          depth,
          int,
        )
      ):
        raise TypeError(
          f"{name} must be an int or None"
        )

      if depth < 0:
        raise ValueError(
          f"{name} must be non-negative"
        )

    if (
      self.current_depth is not None
      and self.required_next_depth
      is not None
      and self.required_next_depth
      <= self.current_depth
    ):
      raise ValueError(
        "required_next_depth must be "
        "greater than current_depth"
      )

    for name, rules in (
      (
        "producer_candidates",
        self.producer_candidates,
      ),
      (
        "unsafe_producer_candidates",
        self.unsafe_producer_candidates,
      ),
      (
        "ancestor_rules",
        self.ancestor_rules,
      ),
    ):
      if not isinstance(
        rules,
        tuple,
      ):
        raise TypeError(
          f"{name} must be a tuple"
        )

      if any(
        not isinstance(
          rule,
          InferenceRule,
        )
        for rule in rules
      ):
        raise TypeError(
          f"{name} must contain only "
          "InferenceRule objects"
        )


@dataclass(frozen=True)
class BoundedProducerSearchReport:
  status: BoundedProducerSearchStatus
  goal: object
  search_result: (
    BoundedProducerSearchResult | None
  ) = None
  diagnostic: (
    BoundedProducerSearchDiagnostic | None
  ) = None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.status,
      BoundedProducerSearchStatus,
    ):
      raise TypeError(
        "status must be a "
        "BoundedProducerSearchStatus"
      )

    if (
      self.search_result is not None
      and not isinstance(
        self.search_result,
        BoundedProducerSearchResult,
      )
    ):
      raise TypeError(
        "search_result must be a "
        "BoundedProducerSearchResult or "
        "None"
      )

    if (
      self.diagnostic is not None
      and not isinstance(
        self.diagnostic,
        BoundedProducerSearchDiagnostic,
      )
    ):
      raise TypeError(
        "diagnostic must be a "
        "BoundedProducerSearchDiagnostic "
        "or None"
      )

    if (
      self.search_result is not None
      and self.search_result.goal
      != self.goal
    ):
      raise ValueError(
        "search_result goal must match "
        "report goal"
      )

    if (
      self.diagnostic is not None
      and self.diagnostic.goal
      != self.goal
    ):
      raise ValueError(
        "diagnostic goal must match "
        "report goal"
      )

    if self.status is (
      BoundedProducerSearchStatus.SUCCESS
    ):
      if self.search_result is None:
        raise ValueError(
          "successful report requires a "
          "search_result"
        )

      if self.diagnostic is not None:
        raise ValueError(
          "successful report must not "
          "contain a diagnostic"
        )

      return

    if self.status is (
      BoundedProducerSearchStatus
      .GOAL_ALREADY_AVAILABLE
    ):
      if (
        self.search_result is not None
        or self.diagnostic is not None
      ):
        raise ValueError(
          "goal-already-available report "
          "must not contain search or "
          "diagnostic data"
        )

      return

    if self.diagnostic is None:
      raise ValueError(
        "failure report requires a "
        "diagnostic"
      )

    if self.diagnostic.status is not (
      self.status
    ):
      raise ValueError(
        "diagnostic status must match "
        "report status"
      )


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


def find_missing_premise_producer_lookups(
  availability,
  rule_catalog,
) -> tuple[
  MissingPremiseProducerLookup,
  ...,
]:
  if not isinstance(
    availability,
    PremiseAvailability,
  ):
    raise TypeError(
      "availability must be a "
      "PremiseAvailability"
    )

  if not isinstance(
    rule_catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "rule_catalog must be an "
      "InferenceRuleCatalog"
    )

  return tuple(
    MissingPremiseProducerLookup(
      inference_rule=(
        availability.inference_rule
      ),
      premise_index=index,
      premise_pattern=(
        availability.inference_rule
        .premise_patterns[index]
      ),
      producer_rules=(
        find_premise_producer_rules(
          rule_catalog,
          availability.inference_rule
          .premise_patterns[index],
        )
      ),
    )
    for index
    in availability.missing_indices
  )


def analyze_producer_premise_availabilities(
  lookup,
  available_steps,
) -> tuple[
  PremiseAvailability,
  ...,
]:
  if not isinstance(
    lookup,
    MissingPremiseProducerLookup,
  ):
    raise TypeError(
      "lookup must be a "
      "MissingPremiseProducerLookup"
    )

  return tuple(
    detect_missing_premises(
      producer_rule,
      available_steps,
    )
    for producer_rule
    in lookup.producer_rules
  )


def all_missing_premises_uniquely_producible(
  lookups,
) -> bool:
  if not isinstance(
    lookups,
    (tuple, list),
  ):
    raise TypeError(
      "lookups must be a tuple/list of "
      "MissingPremiseProducerLookup"
    )

  normalized_lookups = tuple(
    lookups
  )

  for lookup in normalized_lookups:
    if not isinstance(
      lookup,
      MissingPremiseProducerLookup,
    ):
      raise TypeError(
        "lookups must contain only "
        "MissingPremiseProducerLookup "
        "objects"
      )

  if not normalized_lookups:
    return False

  return all(
    len(
      lookup.producer_rules
    ) == 1
    for lookup in normalized_lookups
  )


def select_unique_depth_two_producer_chain(
  repository,
  rule_catalog,
  goal,
) -> BoundedProducerSearchResult | None:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
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

  if len(
    final_rules
  ) != 1:
    return None

  final_rule = final_rules[
    0
  ]

  final_availability = (
    detect_missing_premises(
      final_rule,
      initial_steps,
    )
  )

  direct_lookups = (
    find_missing_premise_producer_lookups(
      final_availability,
      rule_catalog,
    )
  )

  if not (
    all_missing_premises_uniquely_producible(
      direct_lookups
    )
  ):
    return None

  node_specs = {}
  dependency_rule_ids = {}
  direct_rule_ids = []

  def register_node_spec(
    requesting_rule,
    premise_index,
    premise_pattern,
    producer_rule,
    producer_availability,
    depth,
  ):
    producer_rule_id = id(
      producer_rule
    )

    if producer_rule_id not in node_specs:
      node_specs[
        producer_rule_id
      ] = {
        "requesting_rule": (
          requesting_rule
        ),
        "premise_index": premise_index,
        "premise_pattern": (
          premise_pattern
        ),
        "producer_rule": producer_rule,
        "producer_availability": (
          producer_availability
        ),
        "depths": set(),
      }

      dependency_rule_ids[
        producer_rule_id
      ] = []

    node_specs[
      producer_rule_id
    ][
      "depths"
    ].add(
      depth
    )

    return producer_rule_id

  for direct_lookup in direct_lookups:
    direct_rule = (
      direct_lookup.producer_rules[
        0
      ]
    )

    direct_availability = (
      analyze_producer_premise_availabilities(
        direct_lookup,
        initial_steps,
      )[
        0
      ]
    )

    direct_rule_id = register_node_spec(
      final_rule,
      direct_lookup.premise_index,
      direct_lookup.premise_pattern,
      direct_rule,
      direct_availability,
      1,
    )

    direct_rule_ids.append(
      direct_rule_id
    )

    if direct_availability.is_complete:
      continue

    nested_lookups = (
      find_missing_premise_producer_lookups(
        direct_availability,
        rule_catalog,
      )
    )

    if not (
      all_missing_premises_uniquely_producible(
        nested_lookups
      )
    ):
      return None

    for nested_lookup in nested_lookups:
      nested_rule = (
        nested_lookup.producer_rules[
          0
        ]
      )

      nested_availability = (
        analyze_producer_premise_availabilities(
          nested_lookup,
          initial_steps,
        )[
          0
        ]
      )

      if not nested_availability.is_complete:
        return None

      nested_rule_id = register_node_spec(
        direct_rule,
        nested_lookup.premise_index,
        nested_lookup.premise_pattern,
        nested_rule,
        nested_availability,
        2,
      )

      if (
        nested_rule_id
        not in dependency_rule_ids[
          direct_rule_id
        ]
      ):
        dependency_rule_ids[
          direct_rule_id
        ].append(
          nested_rule_id
        )

  nodes_by_rule_id = {}

  for producer_rule_id, spec in (
    node_specs.items()
  ):
    if dependency_rule_ids[
      producer_rule_id
    ]:
      continue

    nodes_by_rule_id[
      producer_rule_id
    ] = BoundedProducerSearchNode(
      requesting_rule=spec[
        "requesting_rule"
      ],
      premise_index=spec[
        "premise_index"
      ],
      premise_pattern=spec[
        "premise_pattern"
      ],
      producer_rule=spec[
        "producer_rule"
      ],
      producer_availability=spec[
        "producer_availability"
      ],
      depths=tuple(
        sorted(
          spec[
            "depths"
          ]
        )
      ),
    )

  for producer_rule_id, spec in (
    node_specs.items()
  ):
    if producer_rule_id in nodes_by_rule_id:
      continue

    dependencies = tuple(
      nodes_by_rule_id.get(
        dependency_rule_id
      )
      for dependency_rule_id
      in dependency_rule_ids[
        producer_rule_id
      ]
    )

    if any(
      dependency is None
      for dependency in dependencies
    ):
      return None

    nodes_by_rule_id[
      producer_rule_id
    ] = BoundedProducerSearchNode(
      requesting_rule=spec[
        "requesting_rule"
      ],
      premise_index=spec[
        "premise_index"
      ],
      premise_pattern=spec[
        "premise_pattern"
      ],
      producer_rule=spec[
        "producer_rule"
      ],
      producer_availability=spec[
        "producer_availability"
      ],
      depths=tuple(
        sorted(
          spec[
            "depths"
          ]
        )
      ),
      dependencies=dependencies,
    )

  producer_nodes = []
  seen_producer_rule_ids = set()

  for direct_rule_id in direct_rule_ids:
    direct_node = nodes_by_rule_id[
      direct_rule_id
    ]

    for dependency in direct_node.dependencies:
      dependency_rule_id = id(
        dependency.producer_rule
      )

      if (
        dependency_rule_id
        in seen_producer_rule_ids
      ):
        continue

      seen_producer_rule_ids.add(
        dependency_rule_id
      )
      producer_nodes.append(
        dependency
      )

    if (
      direct_rule_id
      in seen_producer_rule_ids
    ):
      continue

    seen_producer_rule_ids.add(
      direct_rule_id
    )
    producer_nodes.append(
      direct_node
    )

  return BoundedProducerSearchResult(
    goal=goal,
    final_rule=final_rule,
    final_availability=(
      final_availability
    ),
    producer_nodes=tuple(
      producer_nodes
    ),
    max_depth=2,
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

    lookups = (
      find_missing_premise_producer_lookups(
        availability,
        rule_catalog,
      )
    )

    if not (
      all_missing_premises_uniquely_producible(
        lookups
      )
    ):
      continue

    for lookup in lookups:
      producer_rule = (
        lookup.producer_rules[
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


def derive_goal_from_repository_with_depth_two_producers(
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
      "repository must be a ProofRepository"
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

  search_result = (
    select_unique_depth_two_producer_chain(
      repository,
      rule_catalog,
      goal,
    )
  )

  if search_result is None:
    inference_result = (
      run_inference_until_stable_with_history(
        (),
        initial_steps,
        max_rounds=max_rounds,
      )
    )

    return RepositoryInferenceResult(
      inference_result=inference_result,
      goal_step=find_goal_step(
        inference_result.steps,
        goal,
      ),
    )

  current_steps = initial_steps

  for node in search_result.producer_nodes:
    producer_result = (
      run_inference_until_stable_with_history(
        (
          node.producer_rule,
        ),
        current_steps,
        max_rounds=1,
      )
    )

    current_steps = producer_result.steps

  final_result = (
    run_inference_until_stable_with_history(
      (
        search_result.final_rule,
      ),
      current_steps,
      max_rounds=max_rounds,
    )
  )

  return RepositoryInferenceResult(
    inference_result=final_result,
    goal_step=find_goal_step(
      final_result.steps,
      goal,
    ),
  )
