import pytest

from expression import GeneratorSymbol
from proof import (
  Relation,
  RelationType,
)
from repository_element_exploration import (
  build_repository_generator_exploration,
)
from repository_element_presentation import (
  RepositoryGeneratorExplorationPresentation,
  RepositoryGeneratorOccurrencePresentation,
  build_repository_generator_exploration_presentation,
  render_repository_conclusion_latex,
)
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)
from test_phase99_actual_repository_element_lookup_validation import (
  build_phase99_5_actual_repository,
)


def nu_prime_generator():
  return GeneratorSymbol(
    family="ν",
    decoration="′",
  )


def test_phase99_18_actual_exploration_presentation_preserves_source_identity():
  data = build_phase99_5_actual_repository()

  source_result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      source_result
    )
  )

  assert isinstance(
    presentation,
    RepositoryGeneratorExplorationPresentation,
  )

  assert (
    presentation.source_result
    is source_result
  )


def test_phase99_18_actual_exploration_presentation_preserves_occurrence_identity_and_order():
  data = build_phase99_5_actual_repository()

  source_result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      source_result
    )
  )

  assert tuple(
    occurrence_presentation.source_occurrence
    for occurrence_presentation
    in presentation.occurrences
  ) == source_result.occurrences

  for (
    occurrence_presentation,
    source_occurrence,
  ) in zip(
    presentation.occurrences,
    source_result.occurrences,
  ):
    assert (
      occurrence_presentation.source_occurrence
      is source_occurrence
    )


def test_phase99_18_actual_toda_membership_conclusion_uses_existing_expression_renderer():
  data = build_phase99_5_actual_repository()

  source_result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      source_result
    )
  )

  theorem_presentation = (
    presentation.occurrences[
      0
    ]
  )

  assert (
    theorem_presentation.source_occurrence.entry
    is data[
      "theorem_entry"
    ]
  )

  assert r" \in " in (
    theorem_presentation.conclusion_latex
  )

  assert (
    r"\{"
    in theorem_presentation.conclusion_latex
  )

  assert (
    r"E\nu'"
    in theorem_presentation.conclusion_latex
  )


def test_phase99_18_actual_group_relation_renders_target_group_and_composition():
  data = build_phase99_5_actual_repository()

  source_result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      source_result
    )
  )

  phase68_presentation = (
    presentation.occurrences[
      2
    ]
  )

  assert (
    phase68_presentation.source_occurrence.entry
    is data[
      "phase68_entry"
    ]
  )

  assert (
    phase68_presentation.conclusion_latex
    == (
      r"\pi_{7}^{3} = "
      r"\mathbb{Z}/2\{\nu'\eta_{6}\}"
    )
  )


def test_phase99_18_equation57_relation_renders_map_application_via_existing_renderer():
  data = build_phase65_3_data()

  rendered = (
    render_repository_conclusion_latex(
      data[
        "equation57_step"
      ].conclusion
    )
  )

  assert r"H\left(" in rendered
  assert r"\nu'" in rendered
  assert " = " in rendered


def test_phase99_18_empty_exploration_builds_empty_presentation():
  data = build_phase99_5_actual_repository()

  source_result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ζ",
        index=999,
      ),
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      source_result
    )
  )

  assert presentation.source_result is source_result
  assert presentation.occurrences == ()


def test_phase99_18_occurrence_presentation_rejects_non_occurrence():
  with pytest.raises(
    TypeError,
    match=(
      "source_occurrence must be a "
      "RepositoryGeneratorOccurrence"
    ),
  ):
    RepositoryGeneratorOccurrencePresentation(
      source_occurrence="not-an-occurrence",
      conclusion_latex="x",
    )


def test_phase99_18_occurrence_presentation_rejects_non_string_latex():
  data = build_phase99_5_actual_repository()

  source_result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "conclusion_latex must be a str"
    ),
  ):
    RepositoryGeneratorOccurrencePresentation(
      source_occurrence=(
        source_result.occurrences[
          0
        ]
      ),
      conclusion_latex=123,
    )


def test_phase99_18_exploration_presentation_rejects_non_result():
  with pytest.raises(
    TypeError,
    match=(
      "source_result must be a "
      "RepositoryGeneratorExplorationResult"
    ),
  ):
    RepositoryGeneratorExplorationPresentation(
      source_result="not-a-result",
      occurrences=(),
    )


def test_phase99_18_builder_rejects_non_result():
  with pytest.raises(
    TypeError,
    match=(
      "result must be a "
      "RepositoryGeneratorExplorationResult"
    ),
  ):
    build_repository_generator_exploration_presentation(
      "not-a-result"
    )


def test_phase99_18_non_equality_relation_is_not_silently_given_new_rendering_semantics():
  relation = Relation(
    lhs=1,
    rhs=2,
    relation_type=RelationType.INEQUALITY,
  )

  with pytest.raises(
    ValueError,
    match=(
      "only equality Relation conclusions "
      "are supported in Phase 99-18"
    ),
  ):
    render_repository_conclusion_latex(
      relation
    )


def test_phase99_18_unsupported_conclusion_type_is_rejected():
  with pytest.raises(
    TypeError,
    match=(
      "unsupported repository conclusion "
      "for LaTeX rendering"
    ),
  ):
    render_repository_conclusion_latex(
      object()
    )
