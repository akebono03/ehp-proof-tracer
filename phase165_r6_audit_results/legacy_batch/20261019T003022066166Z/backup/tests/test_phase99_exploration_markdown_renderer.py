import pytest

from expression import GeneratorSymbol
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_element_exploration import (
  build_repository_generator_exploration,
)
from repository_element_presentation import (
  build_repository_generator_exploration_presentation,
)
from repository_element_renderer import (
  render_repository_generator_exploration_markdown,
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


def build_actual_nu_prime_presentation():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      result
    )
  )

  return {
    "data": data,
    "result": result,
    "presentation": presentation,
  }


def test_phase99_21_actual_nu_prime_markdown_has_generator_heading_and_count():
  actual = (
    build_actual_nu_prime_presentation()
  )

  rendered = (
    render_repository_generator_exploration_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert rendered.startswith(
    "# $\\nu'$"
  )
  assert "Occurrences: 4" in rendered


def test_phase99_21_actual_nu_prime_markdown_has_grouped_sections_in_fixed_order():
  actual = (
    build_actual_nu_prime_presentation()
  )

  rendered = (
    render_repository_generator_exploration_markdown(
      actual[
        "presentation"
      ]
    )
  )

  sections = (
    "## Toda brackets",
    "## Group generators",
    "## Composition left",
    "## Composition right",
  )

  positions = tuple(
    rendered.index(
      section
    )
    for section in sections
  )

  assert positions == tuple(
    sorted(
      positions
    )
  )

  assert "## Map inputs" not in rendered
  assert "## Other occurrences" not in rendered


def test_phase99_21_actual_toda_section_contains_full_conclusion_role_and_metadata():
  actual = (
    build_actual_nu_prime_presentation()
  )

  rendered = (
    render_repository_generator_exploration_markdown(
      actual[
        "presentation"
      ]
    )
  )

  theorem_occurrence = (
    actual[
      "presentation"
    ]
    .toda_bracket_occurrences[
      0
    ]
  )

  assert (
    "$"
    + theorem_occurrence.conclusion_latex
    + "$"
  ) in rendered

  assert (
    "Roles: Toda bracket second entry"
    in rendered
  )

  theorem_entry = (
    actual[
      "data"
    ][
      "theorem_entry"
    ]
  )

  assert (
    "Phase: "
    + theorem_entry.phase
  ) in rendered

  assert (
    "Theorem: "
    + theorem_entry.theorem
  ) in rendered


def test_phase99_21_group_generator_section_contains_actual_phase68_relation_and_all_roles():
  actual = (
    build_actual_nu_prime_presentation()
  )

  rendered = (
    render_repository_generator_exploration_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert (
    r"$\pi_{7}^{3} = "
    r"\mathbb{Z}/2\{\nu'\eta_{6}\}$"
    in rendered
  )

  assert (
    "Roles: relation right-hand side, "
    "group generator, "
    "composition left factor"
    in rendered
  )


def test_phase99_21_actual_map_input_section_renders_equation57():
  phase65 = build_phase65_3_data()

  repository = ProofRepository()

  entry = ProofRepositoryEntry(
    key="phase65.equation57",
    step=phase65[
      "equation57_step"
    ],
    phase="65",
    theorem="Toda Equation (5.7)",
  )

  repository.register(
    entry
  )

  result = (
    build_repository_generator_exploration(
      repository,
      nu_prime_generator(),
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      result
    )
  )

  rendered = (
    render_repository_generator_exploration_markdown(
      presentation
    )
  )

  assert "## Map inputs" in rendered
  assert r"H\left(" in rendered
  assert (
    "Roles: relation left-hand side, "
    "map input, "
    "composition left factor"
    in rendered
  )
  assert "Phase: 65" in rendered
  assert "Theorem: Toda Equation (5.7)" in rendered


def test_phase99_21_empty_exploration_omits_all_occurrence_sections():
  data = build_phase99_5_actual_repository()

  result = (
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
      result
    )
  )

  rendered = (
    render_repository_generator_exploration_markdown(
      presentation
    )
  )

  assert rendered.startswith(
    "# $ζ_{999}$"
  )
  assert "Occurrences: 0" in rendered
  assert "## " not in rendered


def test_phase99_21_renderer_is_deterministic():
  actual = (
    build_actual_nu_prime_presentation()
  )

  first = (
    render_repository_generator_exploration_markdown(
      actual[
        "presentation"
      ]
    )
  )
  second = (
    render_repository_generator_exploration_markdown(
      actual[
        "presentation"
      ]
    )
  )

  assert first == second


def test_phase99_21_renderer_does_not_mutate_repository():
  actual = (
    build_actual_nu_prime_presentation()
  )

  repository = (
    actual[
      "data"
    ][
      "repository"
    ]
  )

  before = (
    repository.entries()
  )

  render_repository_generator_exploration_markdown(
    actual[
      "presentation"
    ]
  )

  assert repository.entries() == before

  for (
    before_entry,
    after_entry,
  ) in zip(
    before,
    repository.entries(),
  ):
    assert after_entry is before_entry


def test_phase99_21_renderer_rejects_non_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "RepositoryGeneratorExplorationPresentation"
    ),
  ):
    render_repository_generator_exploration_markdown(
      "not-a-presentation"
    )
