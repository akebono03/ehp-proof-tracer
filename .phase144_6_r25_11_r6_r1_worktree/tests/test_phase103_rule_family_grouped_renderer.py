from proof import (
  InferenceRule,
  PremisePattern,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_applicability_renderer import (
  render_repository_generator_applicability_markdown,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


def _build_same_name_multi_catalog_result():
  data = build_grouped_fixture()

  source_result = data[
    "result"
  ]

  first_node = data[
    "first_node"
  ]

  duplicate_name_rule = InferenceRule(
    name="first grouped rule",
    premise_patterns=(
      PremisePattern(),
    ),
  )

  duplicate_name_entry = (
    InferenceRuleCatalogEntry(
      key="phase103.grouped.first.second-catalog",
      rule=duplicate_name_rule,
      conclusion_type=object,
      fixed_point_safe=True,
    )
  )

  duplicate_name_candidate = (
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=first_node,
      candidate=(
        InferenceRuleApplicabilityCandidate(
          catalog_entry=(
            duplicate_name_entry
          ),
          premise_index=0,
          premise_pattern=(
            duplicate_name_rule
            .premise_patterns[
              0
            ]
          ),
          source_step=(
            first_node
            .proof_step
          ),
          bindings=(),
        )
      ),
    )
  )

  return (
    RepositoryGeneratorApplicabilityExplorationResult(
      proof_scope_exploration=(
        source_result
        .proof_scope_exploration
      ),
      candidates=(
        source_result.candidates
        + (
          duplicate_name_candidate,
        )
      ),
    )
  )


def test_phase103_6c3_renderer_prints_rule_family_name_once_per_source():
  result = (
    _build_same_name_multi_catalog_result()
  )

  markdown = (
    render_repository_generator_applicability_markdown(
      result
    )
  )

  first_source_block = (
    markdown.split(
      "#### Source statement: GeneratorSymbol"
    )[
      1
    ]
  )

  first_source_block = (
    first_source_block.split(
      "#### Source statement: GeneratorSymbol"
    )[
      0
    ]
  )

  assert (
    first_source_block.count(
      "Rule: first grouped rule"
    )
    == 1
  )

  assert (
    "Catalog entries: 2"
    in first_source_block
  )

  assert (
    "phase103.grouped.first"
    in first_source_block
  )

  assert (
    "phase103.grouped.first.second-catalog"
    in first_source_block
  )


def test_phase103_6c3_renderer_preserves_catalog_metadata_and_premise_matches():
  result = (
    _build_same_name_multi_catalog_result()
  )

  markdown = (
    render_repository_generator_applicability_markdown(
      result
    )
  )

  assert (
    "Fixed-point safe: no"
    in markdown
  )

  assert (
    "Fixed-point safe: yes"
    in markdown
  )

  assert (
    "Premise index: 0; Bindings: 0"
    in markdown
  )

  assert (
    "Premise index: 1; Bindings: 0"
    in markdown
  )


def test_phase103_6c3_renderer_reports_rule_family_count():
  result = (
    _build_same_name_multi_catalog_result()
  )

  markdown = (
    render_repository_generator_applicability_markdown(
      result
    )
  )

  assert (
    "Rule groups: 4"
    in markdown
  )

  assert (
    "Rule families: 3"
    in markdown
  )
