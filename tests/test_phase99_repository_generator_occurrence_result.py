import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Sum,
)
from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_element_lookup import (
  RepositoryGeneratorOccurrence,
  find_repository_entries_by_conclusion_generator,
  find_repository_generator_occurrences,
)
from test_phase99_actual_repository_element_lookup_validation import (
  build_phase99_5_actual_repository,
)


def make_entry(
  key,
  conclusion,
):
  return ProofRepositoryEntry(
    key=key,
    step=ProofStep(
      conclusion=conclusion,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase99_8_occurrence_result_accepts_valid_root_path():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  entry = make_entry(
    "phase99.root",
    generator,
  )

  result = RepositoryGeneratorOccurrence(
    entry=entry,
    path=(),
    matched_generator=generator,
  )

  assert result.entry is entry
  assert result.path == ()
  assert (
    result.matched_generator
    is generator
  )


def test_phase99_8_occurrence_result_rejects_non_entry():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  with pytest.raises(
    TypeError,
    match=(
      "entry must be a ProofRepositoryEntry"
    ),
  ):
    RepositoryGeneratorOccurrence(
      entry="not-an-entry",
      path=(),
      matched_generator=generator,
    )


def test_phase99_8_occurrence_result_rejects_non_tuple_path():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  entry = make_entry(
    "phase99.path",
    generator,
  )

  with pytest.raises(
    TypeError,
    match="path must be a tuple",
  ):
    RepositoryGeneratorOccurrence(
      entry=entry,
      path=[
        "generator",
      ],
      matched_generator=generator,
    )


def test_phase99_8_occurrence_result_rejects_non_string_path_segment():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  entry = make_entry(
    "phase99.segment",
    generator,
  )

  with pytest.raises(
    TypeError,
    match=(
      "path must contain only str segments"
    ),
  ):
    RepositoryGeneratorOccurrence(
      entry=entry,
      path=(
        0,
      ),
      matched_generator=generator,
    )


def test_phase99_8_occurrence_result_rejects_non_generator_match():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  entry = make_entry(
    "phase99.generator",
    generator,
  )

  with pytest.raises(
    TypeError,
    match=(
      "matched_generator must be "
      "a GeneratorSymbol"
    ),
  ):
    RepositoryGeneratorOccurrence(
      entry=entry,
      path=(),
      matched_generator="ν′",
    )


def test_phase99_8_empty_repository_returns_no_occurrences():
  repository = ProofRepository()

  result = (
    find_repository_generator_occurrences(
      repository,
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert result == ()


def test_phase99_8_single_entry_returns_path_and_original_generator_identity():
  repository = ProofRepository()

  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  element = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=generator,
  )

  entry = make_entry(
    "phase99.single",
    element,
  )

  repository.register(
    entry
  )

  result = (
    find_repository_generator_occurrences(
      repository,
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert len(
    result
  ) == 1

  occurrence = result[
    0
  ]

  assert occurrence.entry is entry
  assert occurrence.path == (
    "generator",
  )
  assert (
    occurrence.matched_generator
    is generator
  )


def test_phase99_8_same_entry_multiple_occurrences_return_multiple_results():
  repository = ProofRepository()

  shared_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  left = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=shared_generator,
  )

  right_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  right = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=right_generator,
  )

  entry = make_entry(
    "phase99.multiple",
    Sum(
      left=left,
      right=right,
    ),
  )

  repository.register(
    entry
  )

  result = (
    find_repository_generator_occurrences(
      repository,
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert tuple(
    occurrence.path
    for occurrence in result
  ) == (
    (
      "left",
      "generator",
    ),
    (
      "right",
      "generator",
    ),
  )

  assert all(
    occurrence.entry
    is entry
    for occurrence in result
  )

  assert (
    result[
      0
    ].matched_generator
    is shared_generator
  )

  assert (
    result[
      1
    ].matched_generator
    is right_generator
  )


def test_phase99_8_occurrences_preserve_repository_registration_order():
  repository = ProofRepository()

  first_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  second_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  first_entry = make_entry(
    "phase99.first",
    HomotopyElement(
      name="ν′",
      dimension=3,
      generator=first_generator,
    ),
  )

  unrelated_entry = make_entry(
    "phase99.eta",
    HomotopyElement(
      name="η₃",
      dimension=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    ),
  )

  second_entry = make_entry(
    "phase99.second",
    HomotopyElement(
      name="ν′",
      dimension=3,
      generator=second_generator,
    ),
  )

  repository.register(
    first_entry
  )
  repository.register(
    unrelated_entry
  )
  repository.register(
    second_entry
  )

  result = (
    find_repository_generator_occurrences(
      repository,
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence in result
  ) == (
    first_entry,
    second_entry,
  )


def test_phase99_8_entry_only_lookup_remains_one_entry_for_multiple_occurrences():
  repository = ProofRepository()

  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  entry = make_entry(
    "phase99.entry_only",
    Sum(
      left=HomotopyElement(
        name="ν′",
        dimension=3,
        generator=generator,
      ),
      right=HomotopyElement(
        name="ν′",
        dimension=3,
        generator=GeneratorSymbol(
          family="ν",
          decoration="′",
        ),
      ),
    ),
  )

  repository.register(
    entry
  )

  assert (
    find_repository_entries_by_conclusion_generator(
      repository,
      generator,
    )
    == (
      entry,
    )
  )

  assert len(
    find_repository_generator_occurrences(
      repository,
      generator,
    )
  ) == 2


def test_phase99_8_actual_repository_occurrence_paths_are_representative():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_generator_occurrences(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert tuple(
    occurrence.entry
    for occurrence in result
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
    occurrence.path
    for occurrence in result
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


def test_phase99_8_occurrence_lookup_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be a ProofRepository"
    ),
  ):
    find_repository_generator_occurrences(
      "not-a-repository",
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )


def test_phase99_8_occurrence_lookup_rejects_non_generator():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    find_repository_generator_occurrences(
      repository,
      "ν′",
    )
