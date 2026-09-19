import pytest

from expression import GeneratorSymbol
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
)
from repository_element_exploration import (
  build_repository_generator_exploration,
)
from repository_element_presentation import (
  build_repository_generator_exploration_presentation,
)
from repository_element_renderer import (
  render_generator_occurrence_role_label,
)
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase99_actual_repository_element_lookup_validation import (
  build_phase99_5_actual_repository,
)


def nu_prime_generator():
  return GeneratorSymbol(
    family="ν",
    decoration="′",
  )


def test_phase99_20_toda_bracket_view_reuses_existing_presentation_identity():
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

  assert (
    presentation.toda_bracket_occurrences
    == (
      presentation.occurrences[
        0
      ],
    )
  )

  assert (
    presentation.toda_bracket_occurrences[
      0
    ]
    is presentation.occurrences[
      0
    ]
  )


def test_phase99_20_group_generator_view_preserves_source_grouping_order():
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
    occurrence.source_occurrence.entry
    for occurrence
    in presentation.group_generator_occurrences
  ) == (
    data[
      "phase67_entry"
    ],
    data[
      "phase68_entry"
    ],
    data[
      "phase70_entry"
    ],
  )


def test_phase99_20_composition_views_reuse_existing_presentation_objects():
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

  assert (
    presentation.composition_left_occurrences
    == (
      presentation.occurrences[
        2
      ],
      presentation.occurrences[
        3
      ],
    )
  )

  assert (
    presentation.composition_right_occurrences
    == (
      presentation.occurrences[
        1
      ],
    )
  )


def test_phase99_20_map_input_view_uses_source_result_semantic_grouping():
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

  source_result = (
    build_repository_generator_exploration(
      repository,
      nu_prime_generator(),
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      source_result
    )
  )

  assert len(
    presentation.map_input_occurrences
  ) == 1

  assert (
    presentation.map_input_occurrences[
      0
    ]
    is presentation.occurrences[
      0
    ]
  )

  assert (
    presentation.map_input_occurrences[
      0
    ].source_occurrence.entry
    is entry
  )


def test_phase99_20_empty_source_categories_produce_empty_presentation_views():
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

  assert presentation.toda_bracket_occurrences == ()
  assert presentation.map_input_occurrences == ()
  assert presentation.group_generator_occurrences == ()
  assert presentation.composition_left_occurrences == ()
  assert presentation.composition_right_occurrences == ()


@pytest.mark.parametrize(
  (
    "role",
    "expected",
  ),
  (
    (
      GeneratorOccurrenceRole.RELATION_LHS,
      "relation left-hand side",
    ),
    (
      GeneratorOccurrenceRole.RELATION_RHS,
      "relation right-hand side",
    ),
    (
      GeneratorOccurrenceRole.GROUP_GENERATOR,
      "group generator",
    ),
    (
      GeneratorOccurrenceRole.COMPOSITION_LEFT,
      "composition left factor",
    ),
    (
      GeneratorOccurrenceRole.COMPOSITION_RIGHT,
      "composition right factor",
    ),
    (
      GeneratorOccurrenceRole.MAP_INPUT,
      "map input",
    ),
    (
      GeneratorOccurrenceRole.TODA_BRACKET_FIRST,
      "Toda bracket first entry",
    ),
    (
      GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
      "Toda bracket second entry",
    ),
    (
      GeneratorOccurrenceRole.TODA_BRACKET_THIRD,
      "Toda bracket third entry",
    ),
  ),
)
def test_phase99_20_role_label_renderer_covers_current_taxonomy(
  role,
  expected,
):
  assert (
    render_generator_occurrence_role_label(
      role
    )
    == expected
  )


def test_phase99_20_role_label_renderer_rejects_string_role():
  with pytest.raises(
    TypeError,
    match=(
      "role must be a GeneratorOccurrenceRole"
    ),
  ):
    render_generator_occurrence_role_label(
      "group_generator"
    )
