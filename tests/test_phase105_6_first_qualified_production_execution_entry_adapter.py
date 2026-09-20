import pytest

from repository_generator_applicability_execution_entry import (
  build_first_qualified_production_execution_catalog,
  build_first_qualified_production_execution_entry,
)
from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityCandidateHandoff,
  RepositoryGeneratorApplicabilityHandoffValidationStatus,
  build_repository_generator_applicability_handoff_search_report,
  execute_repository_generator_applicability_handoff_search_report,
  validate_repository_generator_applicability_handoff,
)
from repository_inference import (
  BoundedProducerSearchStatus,
)
from rule_catalog import (
  InferenceRuleCatalog,
)
from test_phase105_5_minimal_production_execution_seed_adapter import (
  build_phase105_5_actual_data,
)


def test_phase105_6_execution_entry_preserves_discovery_rule_identity():
  data = build_phase105_5_actual_data()

  entry = (
    build_first_qualified_production_execution_entry(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    entry.rule
    is data[
      "candidate"
    ].candidate.inference_rule
  )
  assert (
    entry.rule
    is data[
      "candidate"
    ].candidate.catalog_entry.rule
  )


def test_phase105_6_execution_entry_qualifies_only_fixed_point_safety():
  data = build_phase105_5_actual_data()

  discovery_entry = (
    data[
      "candidate"
    ].candidate.catalog_entry
  )
  execution_entry = (
    build_first_qualified_production_execution_entry(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  assert discovery_entry.fixed_point_safe is False
  assert execution_entry.fixed_point_safe is True
  assert (
    execution_entry.conclusion_type
    is discovery_entry.conclusion_type
  )
  assert (
    execution_entry.relevance_category
    is discovery_entry.relevance_category
  )


def test_phase105_6_execution_entry_is_goal_specific():
  data = build_phase105_5_actual_data()

  execution_entry = (
    build_first_qualified_production_execution_entry(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    execution_entry.goal_compatibility(
      data[
        "goal"
      ]
    )
    is True
  )

  assert (
    execution_entry.goal_compatibility(
      object()
    )
    is False
  )


def test_phase105_6_execution_catalog_contains_only_qualified_entry():
  data = build_phase105_5_actual_data()

  catalog = (
    build_first_qualified_production_execution_catalog(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  assert isinstance(
    catalog,
    InferenceRuleCatalog,
  )
  assert len(
    catalog.entries()
  ) == 1
  assert (
    catalog.entries()[
      0
    ].rule
    is data[
      "candidate"
    ].candidate.inference_rule
  )


def test_phase105_6_actual_handoff_becomes_ready_with_adapter_catalog():
  data = build_phase105_5_actual_data()

  execution_catalog = (
    build_first_qualified_production_execution_catalog(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=data[
        "candidate"
      ],
      goal=data[
        "goal"
      ],
    )
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
  assert validation.execution_entry is (
    execution_catalog.entries()[
      0
    ]
  )


def test_phase105_6_adapter_catalog_executes_with_phase105_5_seed():
  data = build_phase105_5_actual_data()

  execution_catalog = (
    build_first_qualified_production_execution_catalog(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=data[
        "candidate"
      ],
      goal=data[
        "goal"
      ],
    )
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      execution_catalog,
    )
  )

  search_report = (
    build_repository_generator_applicability_handoff_search_report(
      validation,
      data[
        "seed_repository"
      ],
      execution_catalog,
    )
  )

  assert search_report.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert search_report.report.search_result is not None
  assert (
    search_report.report.search_result.producer_nodes
    == ()
  )

  result = (
    execute_repository_generator_applicability_handoff_search_report(
      search_report,
      data[
        "seed_repository"
      ],
    )
  )

  repository_result = (
    result
    .execution_result
    .repository_inference_result
  )
  assert repository_result is not None

  goal_step = repository_result.goal_step
  assert goal_step is not None
  assert goal_step.conclusion == data[
    "goal"
  ]

  execution_entry = (
    validation.execution_entry
  )
  assert execution_entry is not None

  assert (
    data[
      "candidate"
    ].candidate.inference_rule
    is execution_entry.rule
    is search_report.report.search_result.final_rule
    is goal_step.inference_rule
  )

  assert goal_step.premises == (
    data[
      "source_step"
    ],
  )


def test_phase105_6_rejects_non_candidate():
  data = build_phase105_5_actual_data()

  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    build_first_qualified_production_execution_entry(
      object(),
      data[
        "goal"
      ],
    )

