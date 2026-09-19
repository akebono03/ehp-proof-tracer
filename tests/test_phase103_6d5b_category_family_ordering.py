from proof import (
  InferenceRule,
  PremisePattern,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_applicability_presentation import (
  build_repository_generator_applicability_presentation,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
  RuleRelevanceCategory,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


def _build_ordering_result(
  family_specs,
):
  data = build_grouped_fixture()

  source_result = data[
    "result"
  ]

  first_node = data[
    "first_node"
  ]

  candidates = []

  for index, (
    name,
    category,
  ) in enumerate(
    family_specs
  ):
    rule = InferenceRule(
      name=name,
      premise_patterns=(
        PremisePattern(),
      ),
    )

    entry = InferenceRuleCatalogEntry(
      key=(
        "phase103.6d5b."
        f"{index:02d}"
      ),
      rule=rule,
      conclusion_type=object,
      fixed_point_safe=False,
      relevance_category=category,
    )

    candidates.append(
      RepositoryProofScopeApplicabilityCandidate(
        scope_node=first_node,
        candidate=(
          InferenceRuleApplicabilityCandidate(
            catalog_entry=entry,
            premise_index=0,
            premise_pattern=(
              rule.premise_patterns[
                0
              ]
            ),
            source_step=(
              first_node.proof_step
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
      candidates=tuple(
        candidates
      ),
    )
  )


def test_phase103_6d5b_rule_families_follow_explicit_category_order():
  result = _build_ordering_result(
    (
      (
        "generic rule",
        RuleRelevanceCategory.GENERIC_RELATION,
      ),
      (
        "unclassified rule",
        RuleRelevanceCategory.UNCLASSIFIED,
      ),
      (
        "bridge rule",
        RuleRelevanceCategory.BRIDGE,
      ),
      (
        "theorem rule",
        RuleRelevanceCategory.THEOREM_SPECIFIC,
      ),
      (
        "structural rule",
        RuleRelevanceCategory.STRUCTURAL,
      ),
      (
        "map rule",
        RuleRelevanceCategory.MAP_PROPERTY,
      ),
    )
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  family_names = tuple(
    family.name
    for family in (
      presentation
      .source_groups[
        0
      ]
      .rule_families
    )
  )

  assert family_names == (
    "theorem rule",
    "map rule",
    "structural rule",
    "bridge rule",
    "generic rule",
    "unclassified rule",
  )


def test_phase103_6d5b_same_category_preserves_first_seen_family_order():
  result = _build_ordering_result(
    (
      (
        "generic first",
        RuleRelevanceCategory.GENERIC_RELATION,
      ),
      (
        "theorem first",
        RuleRelevanceCategory.THEOREM_SPECIFIC,
      ),
      (
        "theorem second",
        RuleRelevanceCategory.THEOREM_SPECIFIC,
      ),
      (
        "generic second",
        RuleRelevanceCategory.GENERIC_RELATION,
      ),
    )
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  family_names = tuple(
    family.name
    for family in (
      presentation
      .source_groups[
        0
      ]
      .rule_families
    )
  )

  assert family_names == (
    "theorem first",
    "theorem second",
    "generic first",
    "generic second",
  )


def test_phase103_6d5b_rule_group_order_is_not_changed():
  result = _build_ordering_result(
    (
      (
        "generic rule",
        RuleRelevanceCategory.GENERIC_RELATION,
      ),
      (
        "theorem rule",
        RuleRelevanceCategory.THEOREM_SPECIFIC,
      ),
      (
        "bridge rule",
        RuleRelevanceCategory.BRIDGE,
      ),
    )
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  group_names = tuple(
    rule_group.inference_rule.name
    for rule_group in (
      presentation
      .source_groups[
        0
      ]
      .rule_groups
    )
  )

  assert group_names == (
    "generic rule",
    "theorem rule",
    "bridge rule",
  )


def test_phase103_6d5b_raw_candidate_identity_and_order_are_unchanged():
  result = _build_ordering_result(
    (
      (
        "generic rule",
        RuleRelevanceCategory.GENERIC_RELATION,
      ),
      (
        "theorem rule",
        RuleRelevanceCategory.THEOREM_SPECIFIC,
      ),
      (
        "unclassified rule",
        RuleRelevanceCategory.UNCLASSIFIED,
      ),
    )
  )

  original_candidates = (
    result.candidates
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  assert (
    result.candidates
    == original_candidates
  )

  grouped_candidates = tuple(
    candidate
    for source_group
    in presentation.source_groups
    for candidate
    in source_group.candidates
  )

  assert grouped_candidates == (
    original_candidates
  )


def test_phase103_6d5b_mixed_category_family_falls_back_to_unclassified_order():
  data = build_grouped_fixture()

  source_result = data[
    "result"
  ]

  first_node = data[
    "first_node"
  ]

  def build_candidate(
    key,
    name,
    category,
  ):
    rule = InferenceRule(
      name=name,
      premise_patterns=(
        PremisePattern(),
      ),
    )

    entry = InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=object,
      fixed_point_safe=False,
      relevance_category=category,
    )

    return (
      RepositoryProofScopeApplicabilityCandidate(
        scope_node=first_node,
        candidate=(
          InferenceRuleApplicabilityCandidate(
            catalog_entry=entry,
            premise_index=0,
            premise_pattern=(
              rule.premise_patterns[
                0
              ]
            ),
            source_step=(
              first_node.proof_step
            ),
            bindings=(),
          )
        ),
      )
    )

  result = (
    RepositoryGeneratorApplicabilityExplorationResult(
      proof_scope_exploration=(
        source_result
        .proof_scope_exploration
      ),
      candidates=(
        build_candidate(
          "phase103.6d5b.mixed.generic",
          "mixed family",
          RuleRelevanceCategory.GENERIC_RELATION,
        ),
        build_candidate(
          "phase103.6d5b.theorem",
          "theorem family",
          RuleRelevanceCategory.THEOREM_SPECIFIC,
        ),
        build_candidate(
          "phase103.6d5b.mixed.map",
          "mixed family",
          RuleRelevanceCategory.MAP_PROPERTY,
        ),
      ),
    )
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      result
    )
  )

  family_names = tuple(
    family.name
    for family in (
      presentation
      .source_groups[
        0
      ]
      .rule_families
    )
  )

  assert family_names == (
    "theorem family",
    "mixed family",
  )
