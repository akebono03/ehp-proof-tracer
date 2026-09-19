import pytest

from expression import GeneratorSymbol
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_element_facade import (
  RepositoryGeneratorExplorationReport,
  explore_repository_generator,
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


def test_phase99_23_actual_nu_prime_facade_returns_structured_report():
  data = build_phase99_5_actual_repository()

  report = explore_repository_generator(
    data[
      "repository"
    ],
    nu_prime_generator(),
  )

  assert isinstance(
    report,
    RepositoryGeneratorExplorationReport,
  )

  assert (
    report.presentation.source_result
    is report.exploration
  )

  assert len(
    report.exploration.occurrences
  ) == 4

  assert len(
    report.presentation.occurrences
  ) == 4

  assert "Occurrences: 4" in report.markdown


def test_phase99_23_actual_nu_prime_facade_preserves_occurrence_identity_and_order():
  data = build_phase99_5_actual_repository()

  report = explore_repository_generator(
    data[
      "repository"
    ],
    nu_prime_generator(),
  )

  assert tuple(
    presented.source_occurrence
    for presented in (
      report
      .presentation
      .occurrences
    )
  ) == (
    report
    .exploration
    .occurrences
  )

  for (
    presented,
    source_occurrence,
  ) in zip(
    report.presentation.occurrences,
    report.exploration.occurrences,
  ):
    assert (
      presented.source_occurrence
      is source_occurrence
    )


def test_phase99_23_actual_nu_prime_facade_preserves_grouped_views_and_markdown():
  data = build_phase99_5_actual_repository()

  report = explore_repository_generator(
    data[
      "repository"
    ],
    nu_prime_generator(),
  )

  assert len(
    report.presentation.toda_bracket_occurrences
  ) == 1

  assert len(
    report.presentation.group_generator_occurrences
  ) == 3

  assert len(
    report.presentation.composition_left_occurrences
  ) == 2

  assert len(
    report.presentation.composition_right_occurrences
  ) == 1

  assert "## Toda brackets" in report.markdown
  assert "## Group generators" in report.markdown
  assert "## Composition left" in report.markdown
  assert "## Composition right" in report.markdown


def test_phase99_23_map_input_facade_preserves_equation57_semantics():
  phase65 = build_phase65_3_data()

  repository = ProofRepository()

  entry = ProofRepositoryEntry(
    key="phase99.facade.equation57",
    step=phase65[
      "equation57_step"
    ],
    phase="65",
    theorem="Toda Equation (5.7)",
  )

  repository.register(
    entry
  )

  report = explore_repository_generator(
    repository,
    nu_prime_generator(),
  )

  assert len(
    report
    .exploration
    .map_input_occurrences
  ) == 1

  assert len(
    report
    .presentation
    .map_input_occurrences
  ) == 1

  assert (
    report
    .presentation
    .map_input_occurrences[
      0
    ]
    .source_occurrence
    is report
    .exploration
    .map_input_occurrences[
      0
    ]
  )

  assert "## Map inputs" in report.markdown
  assert r"H\left(" in report.markdown
  assert "Toda Equation (5.7)" in report.markdown


def test_phase99_23_unknown_generator_returns_empty_normal_result():
  data = build_phase99_5_actual_repository()

  report = explore_repository_generator(
    data[
      "repository"
    ],
    GeneratorSymbol(
      family="ζ",
      index=999,
    ),
  )

  assert report.exploration.occurrences == ()
  assert report.presentation.occurrences == ()
  assert "Occurrences: 0" in report.markdown
  assert "## " not in report.markdown


def test_phase99_23_facade_does_not_mutate_repository():
  data = build_phase99_5_actual_repository()

  repository = data[
    "repository"
  ]

  before = repository.entries()

  explore_repository_generator(
    repository,
    nu_prime_generator(),
  )

  after = repository.entries()

  assert after == before

  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase99_23_facade_reuses_repository_validation():
  with pytest.raises(
    TypeError,
  ):
    explore_repository_generator(
      "not-a-repository",
      nu_prime_generator(),
    )


def test_phase99_23_facade_reuses_generator_validation():
  with pytest.raises(
    TypeError,
  ):
    explore_repository_generator(
      ProofRepository(),
      "not-a-generator",
    )


def test_phase99_23_report_rejects_non_exploration():
  data = build_phase99_5_actual_repository()

  report = explore_repository_generator(
    data[
      "repository"
    ],
    nu_prime_generator(),
  )

  with pytest.raises(
    TypeError,
    match=(
      "exploration must be a "
      "RepositoryGeneratorExplorationResult"
    ),
  ):
    RepositoryGeneratorExplorationReport(
      exploration="not-an-exploration",
      presentation=report.presentation,
      markdown=report.markdown,
    )


def test_phase99_23_report_rejects_non_presentation():
  data = build_phase99_5_actual_repository()

  report = explore_repository_generator(
    data[
      "repository"
    ],
    nu_prime_generator(),
  )

  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "RepositoryGeneratorExplorationPresentation"
    ),
  ):
    RepositoryGeneratorExplorationReport(
      exploration=report.exploration,
      presentation="not-a-presentation",
      markdown=report.markdown,
    )


def test_phase99_23_report_requires_presentation_source_identity():
  first = explore_repository_generator(
    ProofRepository(),
    GeneratorSymbol(
      family="ζ",
      index=1,
    ),
  )

  second = explore_repository_generator(
    ProofRepository(),
    GeneratorSymbol(
      family="ζ",
      index=2,
    ),
  )

  with pytest.raises(
    ValueError,
    match=(
      "presentation source identity must match "
      "exploration"
    ),
  ):
    RepositoryGeneratorExplorationReport(
      exploration=first.exploration,
      presentation=second.presentation,
      markdown=first.markdown,
    )


def test_phase99_23_report_rejects_non_string_markdown():
  data = build_phase99_5_actual_repository()

  report = explore_repository_generator(
    data[
      "repository"
    ],
    nu_prime_generator(),
  )

  with pytest.raises(
    TypeError,
    match="markdown must be a str",
  ):
    RepositoryGeneratorExplorationReport(
      exploration=report.exploration,
      presentation=report.presentation,
      markdown=123,
    )
