import pytest

from expression import GeneratorSymbol
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_element_lookup import (
  find_repository_generator_occurrences,
  find_repository_generator_occurrences_by_role,
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


def test_phase99_13_toda_bracket_second_filter_returns_only_theorem_occurrence():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_generator_occurrences_by_role(
      data[
        "repository"
      ],
      nu_prime_generator(),
      GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
    )
  )

  assert len(
    result
  ) == 1

  assert (
    result[
      0
    ].entry
    is data[
      "theorem_entry"
    ]
  )

  assert (
    result[
      0
    ].roles
    == (
      GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
    )
  )


def test_phase99_13_group_generator_filter_preserves_repository_order():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_generator_occurrences_by_role(
      data[
        "repository"
      ],
      nu_prime_generator(),
      GeneratorOccurrenceRole.GROUP_GENERATOR,
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence in result
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


def test_phase99_13_composition_left_filter_returns_phase68_and_phase70():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_generator_occurrences_by_role(
      data[
        "repository"
      ],
      nu_prime_generator(),
      GeneratorOccurrenceRole.COMPOSITION_LEFT,
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence in result
  ) == (
    data[
      "phase68_entry"
    ],
    data[
      "phase70_entry"
    ],
  )


def test_phase99_13_composition_right_filter_returns_phase67():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_generator_occurrences_by_role(
      data[
        "repository"
      ],
      nu_prime_generator(),
      GeneratorOccurrenceRole.COMPOSITION_RIGHT,
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence in result
  ) == (
    data[
      "phase67_entry"
    ],
  )


def test_phase99_13_map_input_filter_works_through_repository_lookup():
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
    find_repository_generator_occurrences_by_role(
      repository,
      nu_prime_generator(),
      GeneratorOccurrenceRole.MAP_INPUT,
    )
  )

  assert len(
    result
  ) == 1

  occurrence = result[
    0
  ]

  assert occurrence.entry is entry

  assert occurrence.roles == (
    GeneratorOccurrenceRole.RELATION_LHS,
    GeneratorOccurrenceRole.MAP_INPUT,
    GeneratorOccurrenceRole.COMPOSITION_LEFT,
  )


def test_phase99_13_role_filter_returns_original_occurrence_objects_semantics():
  data = build_phase99_5_actual_repository()

  all_occurrences = (
    find_repository_generator_occurrences(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  filtered = (
    find_repository_generator_occurrences_by_role(
      data[
        "repository"
      ],
      nu_prime_generator(),
      GeneratorOccurrenceRole.GROUP_GENERATOR,
    )
  )

  expected = tuple(
    occurrence
    for occurrence in all_occurrences
    if (
      GeneratorOccurrenceRole.GROUP_GENERATOR
      in occurrence.roles
    )
  )

  assert filtered == expected

  assert tuple(
    occurrence.entry
    for occurrence in filtered
  ) == tuple(
    occurrence.entry
    for occurrence in expected
  )


def test_phase99_13_missing_role_returns_empty_tuple():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_generator_occurrences_by_role(
      data[
        "repository"
      ],
      nu_prime_generator(),
      GeneratorOccurrenceRole.TODA_BRACKET_FIRST,
    )
  )

  assert result == ()


def test_phase99_13_plain_nu_does_not_match_nu_prime_role_filtered_results():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_generator_occurrences_by_role(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
      ),
      GeneratorOccurrenceRole.GROUP_GENERATOR,
    )
  )

  assert all(
    occurrence.entry
    not in (
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
    for occurrence in result
  )


def test_phase99_13_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be a ProofRepository"
    ),
  ):
    find_repository_generator_occurrences_by_role(
      "not-a-repository",
      nu_prime_generator(),
      GeneratorOccurrenceRole.GROUP_GENERATOR,
    )


def test_phase99_13_rejects_non_generator():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    find_repository_generator_occurrences_by_role(
      ProofRepository(),
      "ν′",
      GeneratorOccurrenceRole.GROUP_GENERATOR,
    )


def test_phase99_13_rejects_string_role():
  with pytest.raises(
    TypeError,
    match=(
      "role must be a GeneratorOccurrenceRole"
    ),
  ):
    find_repository_generator_occurrences_by_role(
      ProofRepository(),
      nu_prime_generator(),
      "group_generator",
    )
