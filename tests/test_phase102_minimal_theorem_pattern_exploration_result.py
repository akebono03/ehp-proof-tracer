import pytest

from expression import GeneratorSymbol
from proof_repository import ProofRepository
from repository_element_lookup import (
  RepositoryGeneratorOccurrence,
)
from repository_theorem_pattern_exploration import (
  RepositoryTheoremPatternOccurrence,
  build_repository_theorem_pattern_occurrences,
)
from test_phase99_actual_repository_element_lookup_validation import (
  build_phase99_5_actual_repository,
)


def nu_prime_generator():
  return GeneratorSymbol(
    family="ν",
    decoration="′",
  )


def test_phase102_2_result_preserves_source_occurrence_and_statement_identity():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_theorem_pattern_occurrences(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  first = result[
    0
  ]

  assert isinstance(
    first,
    RepositoryTheoremPatternOccurrence,
  )

  assert isinstance(
    first.source_occurrence,
    RepositoryGeneratorOccurrence,
  )

  assert (
    first.statement
    is first.source_occurrence.entry.step.conclusion
  )

  assert (
    first.statement_type
    is type(
      first.statement
    )
  )


def test_phase102_2_actual_theorem_membership_statement_is_recovered_losslessly():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_theorem_pattern_occurrences(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  theorem_result = result[
    0
  ]

  assert (
    theorem_result.source_occurrence.entry
    is data[
      "theorem_entry"
    ]
  )

  assert (
    theorem_result.statement
    is data[
      "theorem_step"
    ].conclusion
  )

  assert (
    theorem_result.statement.bracket.second.expression.generator
    == nu_prime_generator()
  )


def test_phase102_2_builder_preserves_existing_occurrence_order_and_identity():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_theorem_pattern_occurrences(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  assert tuple(
    item.source_occurrence.entry
    for item in result
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

  assert tuple(
    item.source_occurrence.path
    for item in result
  ) == (
    (
      "bracket",
      "second",
      "expression",
      "generator",
    ),
    (
      "rhs",
      "generator",
      "right",
      "generator",
    ),
    (
      "rhs",
      "generator",
      "left",
      "generator",
    ),
    (
      "rhs",
      "generator",
      "left",
      "generator",
    ),
  )


def test_phase102_2_unknown_generator_returns_empty_tuple():
  data = build_phase99_5_actual_repository()

  result = (
    build_repository_theorem_pattern_occurrences(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ζ",
        index=999,
      ),
    )
  )

  assert result == ()


def test_phase102_2_result_rejects_non_occurrence():
  with pytest.raises(
    TypeError,
    match=(
      "source_occurrence must be a "
      "RepositoryGeneratorOccurrence"
    ),
  ):
    RepositoryTheoremPatternOccurrence(
      source_occurrence="not-an-occurrence",
      statement=object(),
    )


def test_phase102_2_result_rejects_statement_not_from_source_entry():
  data = build_phase99_5_actual_repository()

  source_occurrence = (
    build_repository_theorem_pattern_occurrences(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )[
      0
    ].source_occurrence
  )

  with pytest.raises(
    ValueError,
    match=(
      "statement must be the source occurrence "
      "entry conclusion"
    ),
  ):
    RepositoryTheoremPatternOccurrence(
      source_occurrence=source_occurrence,
      statement=object(),
    )


def test_phase102_2_builder_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be a ProofRepository"
    ),
  ):
    build_repository_theorem_pattern_occurrences(
      "not-a-repository",
      nu_prime_generator(),
    )


def test_phase102_2_builder_rejects_non_generator():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    build_repository_theorem_pattern_occurrences(
      ProofRepository(),
      "ν′",
    )
