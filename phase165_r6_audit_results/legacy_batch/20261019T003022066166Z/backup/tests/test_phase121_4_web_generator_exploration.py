import pytest

from repository_element_facade import (
  explore_standard_repository_generator_input,
)
from web_generator_exploration import (
  WebGeneratorExplorationOccurrenceView,
  WebGeneratorExplorationView,
  build_standard_web_generator_exploration_view,
)


def test_phase121_4_nu_prime_returns_structured_web_exploration_view():
  view = (
    build_standard_web_generator_exploration_view(
      "nu_prime"
    )
  )

  assert isinstance(
    view,
    WebGeneratorExplorationView,
  )

  assert (
    view.generator_input
    == "nu_prime"
  )

  assert (
    view.generator_latex
    == r"\nu'"
  )

  assert (
    view.occurrence_count
    > 0
  )


def test_phase121_4_web_occurrence_count_matches_existing_explore_facade():
  report = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  view = (
    build_standard_web_generator_exploration_view(
      "nu_prime"
    )
  )

  assert (
    view.occurrence_count
    == len(
      report.presentation.occurrences
    )
  )


def test_phase121_4_nu_prime_preserves_existing_grouped_views():
  report = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  view = (
    build_standard_web_generator_exploration_view(
      "nu_prime"
    )
  )

  grouped_pairs = (
    (
      report.presentation.toda_bracket_occurrences,
      view.toda_bracket_occurrences,
    ),
    (
      report.presentation.map_input_occurrences,
      view.map_input_occurrences,
    ),
    (
      report.presentation.group_generator_occurrences,
      view.group_generator_occurrences,
    ),
    (
      report.presentation.composition_left_occurrences,
      view.composition_left_occurrences,
    ),
    (
      report.presentation.composition_right_occurrences,
      view.composition_right_occurrences,
    ),
  )

  for (
    presentation_occurrences,
    web_occurrences,
  ) in grouped_pairs:
    assert tuple(
      occurrence.conclusion_latex
      for occurrence
      in web_occurrences
    ) == tuple(
      occurrence.conclusion_latex
      for occurrence
      in presentation_occurrences
    )


def test_phase121_4_occurrence_view_preserves_latex_roles_phase_and_theorem():
  view = (
    build_standard_web_generator_exploration_view(
      "nu_prime"
    )
  )

  occurrence = (
    view.group_generator_occurrences[
      0
    ]
  )

  assert isinstance(
    occurrence,
    WebGeneratorExplorationOccurrenceView,
  )

  assert (
    occurrence.conclusion_latex
  )

  assert (
    "group generator"
    in occurrence.role_labels
  )

  assert (
    occurrence.phase
    != ""
  )

  assert (
    occurrence.theorem
    != ""
  )


def test_phase121_4_unknown_generator_is_normal_zero_result():
  view = (
    build_standard_web_generator_exploration_view(
      "eta_999"
    )
  )

  assert (
    view.generator_latex
    == r"\eta_{999}"
  )

  assert (
    view.occurrence_count
    == 0
  )

  assert (
    view.toda_bracket_occurrences
    == ()
  )
  assert (
    view.map_input_occurrences
    == ()
  )
  assert (
    view.group_generator_occurrences
    == ()
  )
  assert (
    view.composition_left_occurrences
    == ()
  )
  assert (
    view.composition_right_occurrences
    == ()
  )
  assert (
    view.other_occurrences
    == ()
  )


def test_phase121_4_blank_generator_is_rejected():
  with pytest.raises(
    ValueError,
    match="generator is required",
  ):
    build_standard_web_generator_exploration_view(
      "  "
    )


def test_phase121_4_non_string_generator_is_rejected():
  with pytest.raises(
    TypeError,
    match="generator_input must be a str",
  ):
    build_standard_web_generator_exploration_view(
      None
    )
