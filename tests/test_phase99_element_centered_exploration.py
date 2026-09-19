import pytest

from expression import GeneratorSymbol
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
import repository_element_exploration
from repository_element_exploration import (
  RepositoryGeneratorExplorationResult,
  build_repository_generator_exploration,
)
from repository_element_lookup import (
  RepositoryGeneratorOccurrence,
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


def test_phase99_15_result_accepts_valid_empty_aggregate():
  generator = nu_prime_generator()

  result = RepositoryGeneratorExplorationResult(
    generator=generator,
    occurrences=(),
    toda_bracket_occurrences=(),
    map_input_occurrences=(),
    group_generator_occurrences=(),
    composition_left_occurrences=(),
    composition_right_occurrences=(),
  )

  assert result.generator is generator
  assert result.occurrences == ()


def test_phase99_15_result_rejects_non_generator():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    RepositoryGeneratorExplorationResult(
      generator="ν′",
      occurrences=(),
      toda_bracket_occurrences=(),
      map_input_occurrences=(),
      group_generator_occurrences=(),
      composition_left_occurrences=(),
      composition_right_occurrences=(),
    )


def test_phase99_15_result_rejects_non_tuple_occurrence_field():
  with pytest.raises(
    TypeError,
    match=(
      "occurrences must be a tuple"
    ),
  ):
    RepositoryGeneratorExplorationResult(
      generator=nu_prime_generator(),
      occurrences=[],
      toda_bracket_occurrences=(),
      map_input_occurrences=(),
      group_generator_occurrences=(),
      composition_left_occurrences=(),
      composition_right_occurrences=(),
    )


def test_phase99_15_result_rejects_non_occurrence_member():
  with pytest.raises(
    TypeError,
    match=(
      "group_generator_occurrences "
      "must contain only "
      "RepositoryGeneratorOccurrence values"
    ),
  ):
    RepositoryGeneratorExplorationResult(
      generator=nu_prime_generator(),
      occurrences=(),
      toda_bracket_occurrences=(),
      map_input_occurrences=(),
      group_generator_occurrences=(
        "not-an-occurrence",
      ),
      composition_left_occurrences=(),
      composition_right_occurrences=(),
    )


def test_phase99_15_actual_repository_aggregates_all_occurrences():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence in result.occurrences
  ) == (
    data[
      "theorem_entry"
    ],
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


def test_phase99_15_actual_repository_aggregates_toda_bracket_occurrences():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence
    in result.toda_bracket_occurrences
  ) == (
    data[
      "theorem_entry"
    ],
  )

  assert (
    GeneratorOccurrenceRole.TODA_BRACKET_SECOND
    in result.toda_bracket_occurrences[
      0
    ].roles
  )


def test_phase99_15_actual_repository_aggregates_group_generator_occurrences():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence
    in result.group_generator_occurrences
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


def test_phase99_15_actual_repository_aggregates_composition_sides():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence
    in result.composition_left_occurrences
  ) == (
    data[
      "phase68_entry"
    ],
    data[
      "phase70_entry"
    ],
  )

  assert tuple(
    occurrence.entry
    for occurrence
    in result.composition_right_occurrences
  ) == (
    data[
      "phase67_entry"
    ],
  )


def test_phase99_15_map_input_aggregate_works_for_actual_equation57():
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

  assert len(
    result.occurrences
  ) == 1

  assert tuple(
    occurrence.entry
    for occurrence
    in result.map_input_occurrences
  ) == (
    entry,
  )

  assert (
    GeneratorOccurrenceRole.MAP_INPUT
    in result.map_input_occurrences[
      0
    ].roles
  )


def test_phase99_15_category_views_reuse_occurrence_object_identity():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  phase68_occurrence = result.occurrences[
    2
  ]

  assert (
    result.group_generator_occurrences[
      1
    ]
    is phase68_occurrence
  )

  assert (
    result.composition_left_occurrences[
      0
    ]
    is phase68_occurrence
  )


def test_phase99_15_builder_calls_occurrence_lookup_once(
  monkeypatch,
):
  data = build_phase99_5_actual_repository()

  calls = []

  real_lookup = (
    repository_element_exploration
    .find_repository_generator_occurrences
  )

  def counting_lookup(
    repository,
    generator,
  ):
    calls.append(
      (
        repository,
        generator,
      )
    )

    return real_lookup(
      repository,
      generator,
    )

  monkeypatch.setattr(
    repository_element_exploration,
    "find_repository_generator_occurrences",
    counting_lookup,
  )

  generator = nu_prime_generator()

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      generator,
    )
  )

  assert len(
    result.occurrences
  ) == 4

  assert calls == [
    (
      data[
        "repository"
      ],
      generator,
    ),
  ]


def test_phase99_15_unknown_generator_returns_empty_result():
  data = build_phase99_5_actual_repository()

  generator = GeneratorSymbol(
    family="ζ",
    index=999,
  )

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      generator,
    )
  )

  assert result.generator is generator
  assert result.occurrences == ()
  assert result.toda_bracket_occurrences == ()
  assert result.map_input_occurrences == ()
  assert result.group_generator_occurrences == ()
  assert result.composition_left_occurrences == ()
  assert result.composition_right_occurrences == ()


def test_phase99_15_plain_nu_remains_distinct_from_nu_prime():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_generator_exploration(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
      ),
    )
  )

  assert all(
    occurrence.entry
    not in (
      data[
        "theorem_entry"
      ],
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
    for occurrence in result.occurrences
  )


def test_phase99_15_builder_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be a ProofRepository"
    ),
  ):
    build_repository_generator_exploration(
      "not-a-repository",
      nu_prime_generator(),
    )


def test_phase99_15_builder_rejects_non_generator():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    build_repository_generator_exploration(
      ProofRepository(),
      "ν′",
    )
