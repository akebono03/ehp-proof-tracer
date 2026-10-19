import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepositoryEntry,
)
from repository_generator_applicability_execution_orchestration import (
  FirstQualifiedProductionApplicabilityExecutionResult,
)
from repository_generator_applicability_facade import (
  explore_standard_repository_generator_applicability_input,
)
from repository_generator_qualified_execution_selection import (
  select_qualified_repository_generator_applicability_candidates,
)
from repository_generator_standard_qualified_execution_facade import (
  StandardRepositoryGeneratorQualifiedExecutionFacadeResult,
  execute_standard_repository_generator_applicability_result_by_root_and_source,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


def _standard_phase105_17_fixture():
  applicability_result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime"
    )
  )

  qualified_selection = (
    select_qualified_repository_generator_applicability_candidates(
      applicability_result
    )
  )

  prop58_candidates = tuple(
    candidate
    for candidate
    in qualified_selection.candidates
    if (
      candidate.root_entry.key
      == "standard.toda.prop58"
    )
  )

  prop58_scope_nodes = tuple(
    node
    for node
    in applicability_result.scope.nodes
    if (
      node.root_entry.key
      == "standard.toda.prop58"
    )
  )

  for candidate in prop58_candidates:
    source_step = (
      candidate.candidate.source_step
    )

    phase66_steps = tuple(
      node.proof_step
      for node
      in prop58_scope_nodes
      if (
        isinstance(
          node.proof_step.conclusion,
          TodaDeltaImageUpToSignStatement,
        )
        and node.proof_step.premises
        == (
          source_step,
        )
      )
    )

    if len(
      phase66_steps
    ) != 1:
      continue

    return {
      "applicability_result": applicability_result,
      "root_entry": candidate.root_entry,
      "source_step": source_step,
      "goal": phase66_steps[
        0
      ].conclusion,
      "existing_phase66_step": phase66_steps[
        0
      ],
    }

  raise AssertionError(
    "could not locate the standard Prop.5.8 "
    "pi_7^4 -> Delta(iota_9) source/goal pair"
  )


def test_phase105_17_standard_result_runs_full_facade_to_execution():
  data = _standard_phase105_17_fixture()

  result = (
    execute_standard_repository_generator_applicability_result_by_root_and_source(
      data[
        "applicability_result"
      ],
      data[
        "root_entry"
      ],
      data[
        "source_step"
      ],
      data[
        "goal"
      ],
    )
  )

  assert isinstance(
    result,
    StandardRepositoryGeneratorQualifiedExecutionFacadeResult,
  )
  assert result.executed is True
  assert isinstance(
    result.execution,
    FirstQualifiedProductionApplicabilityExecutionResult,
  )


def test_phase105_17_preserves_identity_across_all_integration_layers():
  data = _standard_phase105_17_fixture()

  result = (
    execute_standard_repository_generator_applicability_result_by_root_and_source(
      data[
        "applicability_result"
      ],
      data[
        "root_entry"
      ],
      data[
        "source_step"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.qualified_selection.applicability_result
    is data[
      "applicability_result"
    ]
  )
  assert (
    result.family_grouping.selection
    is result.qualified_selection
  )
  assert (
    result.family_selection.grouping
    is result.family_grouping
  )
  assert (
    result.execution.candidate
    is result.representative
  )


def test_phase105_17_selected_group_matches_explicit_root_and_source():
  data = _standard_phase105_17_fixture()

  result = (
    execute_standard_repository_generator_applicability_result_by_root_and_source(
      data[
        "applicability_result"
      ],
      data[
        "root_entry"
      ],
      data[
        "source_step"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.selected_group.root_entry
    is data[
      "root_entry"
    ]
  )
  assert (
    result.selected_group.source_step
    is data[
      "source_step"
    ]
  )


def test_phase105_17_execution_uses_family_representative_identity():
  data = _standard_phase105_17_fixture()

  result = (
    execute_standard_repository_generator_applicability_result_by_root_and_source(
      data[
        "applicability_result"
      ],
      data[
        "root_entry"
      ],
      data[
        "source_step"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.execution.candidate
    is result.family_selection.representative
  )
  assert (
    result.execution.candidate
    is result.selected_group.representative
  )


def test_phase105_17_execution_reaches_existing_standard_phase66_goal():
  data = _standard_phase105_17_fixture()

  result = (
    execute_standard_repository_generator_applicability_result_by_root_and_source(
      data[
        "applicability_result"
      ],
      data[
        "root_entry"
      ],
      data[
        "source_step"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.execution.goal
    == data[
      "existing_phase66_step"
    ].conclusion
  )


def test_phase105_17_rejects_foreign_root_identity():
  data = _standard_phase105_17_fixture()

  foreign_root = ProofRepositoryEntry(
    key="phase105.17.foreign.root",
    step=ProofStep(
      conclusion="foreign root",
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  with pytest.raises(
    ValueError,
    match=(
      "root_entry must be an original root entry "
      "from grouping"
    ),
  ):
    execute_standard_repository_generator_applicability_result_by_root_and_source(
      data[
        "applicability_result"
      ],
      foreign_root,
      data[
        "source_step"
      ],
      data[
        "goal"
      ],
    )


def test_phase105_17_rejects_foreign_source_identity():
  data = _standard_phase105_17_fixture()

  foreign_source = ProofStep(
    conclusion="foreign source",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    ValueError,
    match=(
      "source_step must be an original source step "
      "from grouping"
    ),
  ):
    execute_standard_repository_generator_applicability_result_by_root_and_source(
      data[
        "applicability_result"
      ],
      data[
        "root_entry"
      ],
      foreign_source,
      data[
        "goal"
      ],
    )


def test_phase105_17_rejects_non_applicability_result():
  data = _standard_phase105_17_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    ),
  ):
    execute_standard_repository_generator_applicability_result_by_root_and_source(
      object(),
      data[
        "root_entry"
      ],
      data[
        "source_step"
      ],
      data[
        "goal"
      ],
    )
