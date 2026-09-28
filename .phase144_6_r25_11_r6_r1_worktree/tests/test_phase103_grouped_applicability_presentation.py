from expression import (
  GeneratorSymbol,
)
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
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_applicability_presentation import (
  build_repository_generator_applicability_presentation,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  RepositoryProofScopeResult,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from repository_proof_scope_exploration import (
  RepositoryProofScopeGeneratorOccurrence,
)
from repository_proof_scope_facade import (
  RepositoryProofScopeExplorationResult,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
)


def build_grouped_fixture():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  first_step = ProofStep(
    conclusion=generator,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion=generator,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  root_step = ProofStep(
    conclusion="root",
    premises=(
      first_step,
      second_step,
    ),
    rule=ProofRule.GIVEN,
  )

  root_entry = ProofRepositoryEntry(
    key="phase103.grouped.root",
    step=root_step,
  )

  repository = ProofRepository()
  repository.register(
    root_entry
  )

  root_node = RepositoryProofScopeNode(
    root_entry=root_entry,
    proof_step=root_step,
    shortest_depth=0,
  )

  first_node = RepositoryProofScopeNode(
    root_entry=root_entry,
    proof_step=first_step,
    shortest_depth=1,
  )

  second_node = RepositoryProofScopeNode(
    root_entry=root_entry,
    proof_step=second_step,
    shortest_depth=1,
  )

  scope = RepositoryProofScopeResult(
    repository=repository,
    nodes=(
      root_node,
      first_node,
      second_node,
    ),
  )

  first_occurrence = (
    RepositoryProofScopeGeneratorOccurrence(
      scope_node=first_node,
      path=(),
      matched_generator=generator,
      roles=(),
    )
  )

  second_occurrence = (
    RepositoryProofScopeGeneratorOccurrence(
      scope_node=second_node,
      path=(),
      matched_generator=generator,
      roles=(),
    )
  )

  proof_scope_exploration = (
    RepositoryProofScopeExplorationResult(
      generator=generator,
      scope=scope,
      occurrences=(
        first_occurrence,
        second_occurrence,
      ),
      toda_memberships=(),
      map_relations=(),
    )
  )

  first_rule = InferenceRule(
    name="first grouped rule",
    premise_patterns=(
      PremisePattern(),
      PremisePattern(),
    ),
  )

  second_rule = InferenceRule(
    name="second grouped rule",
    premise_patterns=(
      PremisePattern(),
    ),
  )

  first_entry = InferenceRuleCatalogEntry(
    key="phase103.grouped.first",
    rule=first_rule,
    conclusion_type=object,
    fixed_point_safe=False,
  )

  second_entry = InferenceRuleCatalogEntry(
    key="phase103.grouped.second",
    rule=second_rule,
    conclusion_type=object,
    fixed_point_safe=True,
  )

  def wrap(
    node,
    entry,
    premise_index,
  ):
    pattern = (
      entry
      .rule
      .premise_patterns[
        premise_index
      ]
    )

    candidate = (
      InferenceRuleApplicabilityCandidate(
        catalog_entry=entry,
        premise_index=premise_index,
        premise_pattern=pattern,
        source_step=node.proof_step,
        bindings=(),
      )
    )

    return (
      RepositoryProofScopeApplicabilityCandidate(
        scope_node=node,
        candidate=candidate,
      )
    )

  candidates = (
    wrap(
      first_node,
      first_entry,
      0,
    ),
    wrap(
      first_node,
      first_entry,
      1,
    ),
    wrap(
      first_node,
      second_entry,
      0,
    ),
    wrap(
      second_node,
      first_entry,
      0,
    ),
  )

  result = (
    RepositoryGeneratorApplicabilityExplorationResult(
      proof_scope_exploration=(
        proof_scope_exploration
      ),
      candidates=candidates,
    )
  )

  return {
    "result": result,
    "candidates": candidates,
    "first_node": first_node,
    "second_node": second_node,
    "first_entry": first_entry,
    "second_entry": second_entry,
  }


def test_phase103_6c1_groups_candidates_by_source_node():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  assert len(
    presentation.source_groups
  ) == 2

  assert (
    presentation
    .source_groups[
      0
    ]
    .scope_node
    is data[
      "first_node"
    ]
  )

  assert (
    presentation
    .source_groups[
      1
    ]
    .scope_node
    is data[
      "second_node"
    ]
  )


def test_phase103_6c1_groups_same_catalog_entry_within_source():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  first_source = (
    presentation
    .source_groups[
      0
    ]
  )

  assert len(
    first_source.rule_groups
  ) == 2

  assert (
    first_source
    .rule_groups[
      0
    ]
    .catalog_entry
    is data[
      "first_entry"
    ]
  )

  assert (
    first_source
    .rule_groups[
      0
    ]
    .premise_indexes
    == (
      0,
      1,
    )
  )

  assert (
    first_source
    .rule_groups[
      1
    ]
    .catalog_entry
    is data[
      "second_entry"
    ]
  )


def test_phase103_6c1_preserves_every_raw_candidate_identity_once():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  grouped = tuple(
    candidate
    for source_group
    in presentation.source_groups
    for candidate
    in source_group.candidates
  )

  assert len(
    grouped
  ) == len(
    data[
      "candidates"
    ]
  )

  assert {
    id(
      candidate
    )
    for candidate in grouped
  } == {
    id(
      candidate
    )
    for candidate in data[
      "candidates"
    ]
  }


def test_phase103_6c1_preserves_first_seen_group_order():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  assert tuple(
    source_group.scope_node
    for source_group
    in presentation.source_groups
  ) == (
    data[
      "first_node"
    ],
    data[
      "second_node"
    ],
  )

  assert tuple(
    rule_group.catalog_entry
    for rule_group
    in presentation
    .source_groups[
      0
    ]
    .rule_groups
  ) == (
    data[
      "first_entry"
    ],
    data[
      "second_entry"
    ],
  )


def test_phase103_6c1_other_view_reuses_source_group_identity():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  assert (
    presentation
    .toda_membership_source_groups
    == ()
  )

  assert (
    presentation
    .map_relation_source_groups
    == ()
  )

  assert (
    presentation
    .other_source_groups
    == presentation.source_groups
  )

  assert (
    presentation
    .other_source_groups[
      0
    ]
    is presentation
    .source_groups[
      0
    ]
  )


def test_phase103_6c1_rule_group_count_is_grouped_not_raw_count():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  assert (
    len(
      data[
        "candidates"
      ]
    )
    == 4
  )

  assert (
    presentation.rule_group_count
    == 3
  )
