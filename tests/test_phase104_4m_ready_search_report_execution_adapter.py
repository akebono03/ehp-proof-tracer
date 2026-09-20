from dataclasses import dataclass

import pytest

import repository_generator_applicability_handoff as handoff_module
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
from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityCandidateHandoff,
  RepositoryGeneratorApplicabilityHandoffExecutionResult,
  RepositoryGeneratorApplicabilityHandoffSearchReport,
  RepositoryGeneratorApplicabilityHandoffValidationStatus,
  build_repository_generator_applicability_handoff_search_report,
  execute_repository_generator_applicability_handoff_search_report,
  validate_repository_generator_applicability_handoff,
)
from repository_inference import (
  BoundedProducerExecutionResult,
  BoundedProducerSearchDiagnostic,
  BoundedProducerSearchReport,
  BoundedProducerSearchStatus,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase1044MSeed:
  value: str


@dataclass(frozen=True)
class Phase1044MMiddle:
  value: str


@dataclass(frozen=True)
class Phase1044MGoal:
  value: str


def _build_fixture(
  *,
  goal_already_available=False,
):
  seed = Phase1044MSeed(
    value="seed",
  )
  middle = Phase1044MMiddle(
    value="middle",
  )
  goal = Phase1044MGoal(
    value="goal",
  )

  source_step = ProofStep(
    conclusion=seed,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  root_entry = ProofRepositoryEntry(
    key="phase104.4m.root",
    step=source_step,
  )

  repository = ProofRepository()
  repository.register(
    root_entry
  )

  seed_pattern = PremisePattern(
    statement_type=Phase1044MSeed,
    statement_pattern=seed,
  )
  middle_pattern = PremisePattern(
    statement_type=Phase1044MMiddle,
    statement_pattern=middle,
  )

  producer_rule = InferenceRule(
    name="phase104 4m producer",
    premise_patterns=(
      seed_pattern,
    ),
    conclusion_builder=(
      lambda premises:
      Phase1044MMiddle(
        value="middle",
      )
    ),
  )

  final_rule = InferenceRule(
    name="phase104 4m validated final rule",
    premise_patterns=(
      middle_pattern,
    ),
    conclusion_builder=(
      lambda premises:
      Phase1044MGoal(
        value="goal",
      )
    ),
  )

  discovery_entry = InferenceRuleCatalogEntry(
    key="phase104.4m.discovery",
    rule=final_rule,
    conclusion_type=Phase1044MGoal,
    fixed_point_safe=False,
  )

  scope_node = RepositoryProofScopeNode(
    root_entry=root_entry,
    proof_step=source_step,
    shortest_depth=0,
  )

  raw_candidate = InferenceRuleApplicabilityCandidate(
    catalog_entry=discovery_entry,
    premise_index=0,
    premise_pattern=middle_pattern,
    source_step=source_step,
    bindings=(),
  )

  candidate = (
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=scope_node,
      candidate=raw_candidate,
    )
  )

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=candidate,
      goal=goal,
    )
  )

  execution_catalog = InferenceRuleCatalog()

  producer_entry = InferenceRuleCatalogEntry(
    key="phase104.4m.producer",
    rule=producer_rule,
    conclusion_type=Phase1044MMiddle,
    fixed_point_safe=True,
  )
  execution_catalog.register(
    producer_entry
  )

  execution_entry = InferenceRuleCatalogEntry(
    key="phase104.4m.execution",
    rule=final_rule,
    conclusion_type=Phase1044MGoal,
    fixed_point_safe=True,
    goal_compatibility=(
      lambda candidate_goal:
      candidate_goal == goal
    ),
  )
  execution_catalog.register(
    execution_entry
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      execution_catalog,
    )
  )

  assert validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
  )

  if goal_already_available:
    goal_step = ProofStep(
      conclusion=goal,
      premises=(),
      rule=ProofRule.GIVEN,
    )
    repository.register(
      ProofRepositoryEntry(
        key="phase104.4m.goal",
        step=goal_step,
      )
    )

  search_report = (
    build_repository_generator_applicability_handoff_search_report(
      validation,
      repository,
      execution_catalog,
    )
  )

  return {
    "repository": repository,
    "goal": goal,
    "producer_rule": producer_rule,
    "final_rule": final_rule,
    "execution_catalog": execution_catalog,
    "validation": validation,
    "search_report": search_report,
  }


def test_phase104_4m_executes_prebuilt_search_report_without_research(
  monkeypatch,
):
  data = _build_fixture()

  def fail_if_search_is_rebuilt(*args, **kwargs):
    raise AssertionError(
      "execution must not rebuild the search report"
    )

  monkeypatch.setattr(
    handoff_module,
    "_build_bounded_producer_search_report_for_final_rule",
    fail_if_search_is_rebuilt,
  )

  result = (
    execute_repository_generator_applicability_handoff_search_report(
      data["search_report"],
      data["repository"],
    )
  )

  assert isinstance(
    result,
    RepositoryGeneratorApplicabilityHandoffExecutionResult,
  )
  assert isinstance(
    result.execution_result,
    BoundedProducerExecutionResult,
  )
  assert (
    result.search_report
    is data["search_report"]
  )
  assert (
    result.execution_result.report
    is data["search_report"].report
  )


def test_phase104_4m_executes_selected_producer_path_and_final_rule():
  data = _build_fixture()

  result = (
    execute_repository_generator_applicability_handoff_search_report(
      data["search_report"],
      data["repository"],
    )
  )

  search_result = (
    result.search_report.report.search_result
  )
  assert search_result is not None
  assert tuple(
    node.producer_rule
    for node in search_result.producer_nodes
  ) == (
    data["producer_rule"],
  )
  assert (
    search_result.final_rule
    is data["final_rule"]
  )

  repository_result = (
    result.execution_result.repository_inference_result
  )
  assert repository_result is not None

  executed_rules = tuple(
    step.inference_rule
    for step in repository_result.inference_result.steps
    if step.inference_rule is not None
  )

  assert data["producer_rule"] in executed_rules
  assert data["final_rule"] in executed_rules
  assert repository_result.goal_step is not None
  assert (
    repository_result.goal_step.conclusion
    == data["goal"]
  )


def test_phase104_4m_goal_already_available_executes_no_rule():
  data = _build_fixture(
    goal_already_available=True,
  )

  assert data["search_report"].report.status is (
    BoundedProducerSearchStatus.GOAL_ALREADY_AVAILABLE
  )

  result = (
    execute_repository_generator_applicability_handoff_search_report(
      data["search_report"],
      data["repository"],
    )
  )

  assert (
    result.execution_result.report
    is data["search_report"].report
  )

  repository_result = (
    result.execution_result.repository_inference_result
  )
  assert repository_result is not None
  assert repository_result.goal_step is not None
  assert all(
    step.inference_rule is None
    for step in repository_result.inference_result.steps
  )


def test_phase104_4m_failed_report_is_returned_without_execution():
  data = _build_fixture()

  failed_report = BoundedProducerSearchReport(
    status=BoundedProducerSearchStatus.NO_PRODUCER,
    goal=data["goal"],
    diagnostic=BoundedProducerSearchDiagnostic(
      status=BoundedProducerSearchStatus.NO_PRODUCER,
      goal=data["goal"],
      final_rule=data["final_rule"],
      ancestor_rules=(
        data["final_rule"],
      ),
    ),
  )

  failed_search_report = (
    RepositoryGeneratorApplicabilityHandoffSearchReport(
      validation=data["validation"],
      report=failed_report,
    )
  )

  result = (
    execute_repository_generator_applicability_handoff_search_report(
      failed_search_report,
      data["repository"],
    )
  )

  assert result.execution_result.report is failed_report
  assert (
    result.execution_result.repository_inference_result
    is None
  )


def test_phase104_4m_execution_wrapper_rejects_report_identity_drift():
  data = _build_fixture()

  execution_result = (
    execute_repository_generator_applicability_handoff_search_report(
      data["search_report"],
      data["repository"],
    )
    .execution_result
  )

  different_report = BoundedProducerSearchReport(
    status=BoundedProducerSearchStatus.GOAL_ALREADY_AVAILABLE,
    goal=data["goal"],
  )

  different_search_report = (
    RepositoryGeneratorApplicabilityHandoffSearchReport(
      validation=data["validation"],
      report=different_report,
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "execution_result.report must be "
      "search_report.report"
    ),
  ):
    RepositoryGeneratorApplicabilityHandoffExecutionResult(
      search_report=different_search_report,
      execution_result=execution_result,
    )


def test_phase104_4m_rejects_non_search_report_input():
  data = _build_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "search_report must be a "
      "RepositoryGeneratorApplicabilityHandoffSearchReport"
    ),
  ):
    execute_repository_generator_applicability_handoff_search_report(
      object(),
      data["repository"],
    )
