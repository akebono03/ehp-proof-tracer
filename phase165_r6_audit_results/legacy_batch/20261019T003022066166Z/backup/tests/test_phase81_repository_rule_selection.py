from dataclasses import dataclass

from proof import (
  InferenceRule,
  InferenceTerminationReason,
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
)


@dataclass(frozen=True)
class SeedStatement:
  value: str


@dataclass(frozen=True)
class GoalStatement:
  value: str


@dataclass(frozen=True)
class UnrelatedStatement:
  value: str


def make_seed_step(
  value="target",
):
  return ProofStep(
    conclusion=SeedStatement(
      value=value,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )


def make_goal_rule(
  name="goal rule",
):
  def build_conclusion(
    premises,
  ):
    return GoalStatement(
      value=(
        premises[0]
        .conclusion
        .value
      ),
    )

  return InferenceRule(
    name=name,
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=SeedStatement,
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )


def make_unrelated_rule(
  name="unrelated rule",
):
  def build_conclusion(
    premises,
  ):
    return UnrelatedStatement(
      value=(
        premises[0]
        .conclusion
        .value
      ),
    )

  return InferenceRule(
    name=name,
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=SeedStatement,
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
  )


def make_repository(
  seed_step,
):
  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="phase81.seed",
      step=seed_step,
      phase="81",
      theorem="synthetic",
    )
  )

  return repository


def test_catalog_repository_inference_derives_goal_without_explicit_rule():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  goal_rule = make_goal_rule()

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.goal",
      rule=goal_rule,
      conclusion_type=GoalStatement,
      fixed_point_safe=True,
    )
  )

  goal = GoalStatement(
    value="target",
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      goal,
    )
  )

  assert (
    result.goal_step
    is not None
  )

  assert (
    result.goal_step.conclusion
    == goal
  )

  assert (
    result.goal_step.rule
    == ProofRule.INFERENCE
  )


def test_catalog_repository_inference_uses_selected_rule():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  goal_rule = make_goal_rule()

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.goal",
      rule=goal_rule,
      conclusion_type=GoalStatement,
      fixed_point_safe=True,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      GoalStatement(
        value="target",
      ),
    )
  )

  assert (
    result.goal_step
    is not None
  )

  assert (
    result.goal_step.inference_rule
    is goal_rule
  )


def test_catalog_repository_inference_preserves_repository_premise_identity():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  goal_rule = make_goal_rule()

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.goal",
      rule=goal_rule,
      conclusion_type=GoalStatement,
      fixed_point_safe=True,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      GoalStatement(
        value="target",
      ),
    )
  )

  assert (
    result.goal_step
    is not None
  )

  assert (
    result.goal_step.premises
    == (
      seed_step,
    )
  )

  assert (
    result.goal_step.premises[0]
    is seed_step
  )


def test_catalog_repository_inference_reaches_fixed_point():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.goal",
      rule=make_goal_rule(),
      conclusion_type=GoalStatement,
      fixed_point_safe=True,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      GoalStatement(
        value="target",
      ),
    )
  )

  assert (
    result
    .inference_result
    .termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_catalog_repository_inference_ignores_unrelated_rule():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  goal_rule = make_goal_rule()

  unrelated_rule = (
    make_unrelated_rule()
  )

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.unrelated",
      rule=unrelated_rule,
      conclusion_type=UnrelatedStatement,
      fixed_point_safe=True,
    )
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.goal",
      rule=goal_rule,
      conclusion_type=GoalStatement,
      fixed_point_safe=True,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      GoalStatement(
        value="target",
      ),
    )
  )

  assert (
    result.goal_step
    is not None
  )

  assert (
    result.goal_step.inference_rule
    is goal_rule
  )

  assert all(
    step.inference_rule
    is not unrelated_rule
    for step in result.inference_result.steps
  )


def test_catalog_repository_inference_excludes_unsafe_matching_rule():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  unsafe_rule = make_goal_rule(
    "unsafe goal rule"
  )

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.unsafe",
      rule=unsafe_rule,
      conclusion_type=GoalStatement,
      fixed_point_safe=False,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      GoalStatement(
        value="target",
      ),
    )
  )

  assert (
    result.goal_step
    is None
  )

  assert all(
    step.inference_rule
    is not unsafe_rule
    for step in result.inference_result.steps
  )


def test_catalog_repository_inference_returns_no_goal_when_no_compatible_rule():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.unrelated",
      rule=make_unrelated_rule(),
      conclusion_type=UnrelatedStatement,
      fixed_point_safe=True,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      GoalStatement(
        value="target",
      ),
    )
  )

  assert (
    result.goal_step
    is None
  )


def test_catalog_repository_inference_deduplicates_rule_alias_before_execution():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  goal_rule = make_goal_rule()

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.goal",
      rule=goal_rule,
      conclusion_type=GoalStatement,
      fixed_point_safe=True,
    )
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.goal.alias",
      rule=goal_rule,
      conclusion_type=GoalStatement,
      fixed_point_safe=True,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      GoalStatement(
        value="target",
      ),
    )
  )

  assert (
    result.goal_step
    is not None
  )

  derived_goal_steps = tuple(
    step
    for step
    in result.inference_result.steps
    if isinstance(
      step.conclusion,
      GoalStatement,
    )
  )

  assert (
    len(
      derived_goal_steps
    )
    == 1
  )


def test_catalog_repository_inference_does_not_mutate_repository():
  seed_step = make_seed_step()

  repository = make_repository(
    seed_step
  )

  entries_before = (
    repository.entries()
  )

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase81.goal",
      rule=make_goal_rule(),
      conclusion_type=GoalStatement,
      fixed_point_safe=True,
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      repository,
      catalog,
      GoalStatement(
        value="target",
      ),
    )
  )

  assert (
    result.goal_step
    is not None
  )

  assert (
    repository.entries()
    == entries_before
  )

  assert (
    len(
      repository.entries()
    )
    == 1
  )

  assert (
    repository.entries()[0].step
    is seed_step
  )


