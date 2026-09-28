from proof import (
  InferenceRule,
  PremisePattern,
)
from repository_generator_applicability_presentation import (
  ApplicabilityRuleFamilyPresentation,
  build_repository_generator_applicability_presentation,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


def test_phase103_6c3_same_rule_name_forms_one_family_within_source():
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
    first_source.rule_families
  ) == 2

  assert (
    first_source
    .rule_families[
      0
    ]
    .name
    == "first grouped rule"
  )


def test_phase103_6c3_family_preserves_catalog_entry_identity_and_order():
  data = build_grouped_fixture()

  first_node = data[
    "first_node"
  ]

  first_rule_clone = InferenceRule(
    name="first grouped rule",
    premise_patterns=(
      PremisePattern(),
    ),
  )

  clone_entry = (
    InferenceRuleCatalogEntry(
      key="phase103.grouped.first.clone",
      rule=first_rule_clone,
      conclusion_type=object,
      fixed_point_safe=False,
    )
  )

  clone_candidate = (
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=first_node,
      candidate=(
        InferenceRuleApplicabilityCandidate(
          catalog_entry=clone_entry,
          premise_index=0,
          premise_pattern=(
            first_rule_clone
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

  source_result = data[
    "result"
  ]

  extended_result = type(
    source_result
  )(
    proof_scope_exploration=(
      source_result
      .proof_scope_exploration
    ),
    candidates=(
      source_result.candidates
      + (
        clone_candidate,
      )
    ),
  )

  presentation = (
    build_repository_generator_applicability_presentation(
      extended_result
    )
  )

  first_family = (
    presentation
    .source_groups[
      0
    ]
    .rule_families[
      0
    ]
  )

  assert isinstance(
    first_family,
    ApplicabilityRuleFamilyPresentation,
  )

  assert tuple(
    entry.key
    for entry in (
      first_family.catalog_entries
    )
  ) == (
    "phase103.grouped.first",
    "phase103.grouped.first.clone",
  )

  assert (
    first_family
    .rule_groups[
      0
    ]
    .catalog_entry
    is data[
      "first_entry"
    ]
  )

  assert (
    first_family
    .rule_groups[
      1
    ]
    .catalog_entry
    is clone_entry
  )


def test_phase103_6c3_family_preserves_every_candidate_identity():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  family_candidates = tuple(
    candidate
    for source_group
    in presentation.source_groups
    for family
    in source_group.rule_families
    for candidate
    in family.candidates
  )

  assert len(
    family_candidates
  ) == len(
    data[
      "candidates"
    ]
  )

  assert {
    id(
      candidate
    )
    for candidate
    in family_candidates
  } == {
    id(
      candidate
    )
    for candidate
    in data[
      "candidates"
    ]
  }


def test_phase103_6c3_family_is_presentation_only_not_semantic_dedupe():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  first_family = (
    presentation
    .source_groups[
      0
    ]
    .rule_families[
      0
    ]
  )

  assert (
    len(
      first_family.rule_groups
    )
    == 1
  )

  assert (
    first_family.raw_candidate_count
    == 2
  )

  assert (
    first_family.candidates[
      0
    ]
    is data[
      "candidates"
    ][
      0
    ]
  )

  assert (
    first_family.candidates[
      1
    ]
    is data[
      "candidates"
    ][
      1
    ]
  )


def test_phase103_6c3_rule_family_count_is_separate_from_rule_group_count():
  data = build_grouped_fixture()

  presentation = (
    build_repository_generator_applicability_presentation(
      data[
        "result"
      ]
    )
  )

  assert (
    presentation.rule_group_count
    == 3
  )

  assert (
    presentation.rule_family_count
    == 3
  )
