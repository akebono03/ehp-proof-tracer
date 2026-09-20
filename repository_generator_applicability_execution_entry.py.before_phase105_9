from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


_FIRST_QUALIFIED_PRODUCTION_EXECUTION_FACTORY = (
  "toda_58_delta_iota9_nu4_nu_prime_inference_rule"
)


def _candidate_inference_rule_factory_name(
  candidate,
):
  inference_rule = (
    candidate
    .candidate
    .inference_rule
  )

  conclusion_builder = (
    inference_rule.conclusion_builder
  )

  if not callable(
    conclusion_builder
  ):
    return None

  qualname = getattr(
    conclusion_builder,
    "__qualname__",
    "",
  )

  marker = ".<locals>."

  if marker not in qualname:
    return None

  factory_qualname = qualname.split(
    marker,
    1,
  )[
    0
  ]

  return factory_qualname.rsplit(
    ".",
    1,
  )[
    -1
  ]


def build_first_qualified_production_execution_entry(
  candidate,
  goal,
) -> InferenceRuleCatalogEntry:
  if not isinstance(
    candidate,
    RepositoryProofScopeApplicabilityCandidate,
  ):
    raise TypeError(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    )

  factory_name = (
    _candidate_inference_rule_factory_name(
      candidate
    )
  )

  if (
    factory_name
    != _FIRST_QUALIFIED_PRODUCTION_EXECUTION_FACTORY
  ):
    raise ValueError(
      "candidate rule is not the first qualified "
      "production execution rule"
    )

  discovery_entry = (
    candidate
    .candidate
    .catalog_entry
  )

  return InferenceRuleCatalogEntry(
    key=(
      "standard.production.execution."
      "toda58.delta-iota9-nu-expression"
    ),
    rule=discovery_entry.rule,
    conclusion_type=discovery_entry.conclusion_type,
    fixed_point_safe=True,
    goal_compatibility=(
      lambda candidate_goal:
      candidate_goal == goal
    ),
    relevance_category=(
      discovery_entry.relevance_category
    ),
  )


def build_first_qualified_production_execution_catalog(
  candidate,
  goal,
) -> InferenceRuleCatalog:
  execution_entry = (
    build_first_qualified_production_execution_entry(
      candidate,
      goal,
    )
  )

  catalog = InferenceRuleCatalog()
  catalog.register(
    execution_entry
  )

  return catalog
