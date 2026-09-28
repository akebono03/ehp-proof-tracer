import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  TodaBracket,
)
from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_toda_membership_exploration import (
  RepositoryTodaBracketMembershipOccurrence,
  TodaBracketMembershipKind,
  TodaBracketPosition,
  find_repository_toda_bracket_membership_occurrences,
)
from test_phase99_actual_repository_element_lookup_validation import (
  build_phase99_5_actual_repository,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


def nu_prime_generator():
  return GeneratorSymbol(
    family="ν",
    decoration="′",
  )


def nu_prime_element():
  return HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator(),
  )


def eta(
  index,
):
  return HomotopyElement(
    name=f"η{index}",
    dimension=index,
    generator=GeneratorSymbol(
      family="η",
      index=index,
    ),
  )


def make_membership_entry(
  key,
  statement,
):
  return ProofRepositoryEntry(
    key=key,
    step=ProofStep(
      conclusion=statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase102_3_actual_theorem_membership_finds_nu_prime_in_second_position():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_toda_bracket_membership_occurrences(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  assert len(
    result
  ) == 1

  occurrence = result[
    0
  ]

  assert isinstance(
    occurrence,
    RepositoryTodaBracketMembershipOccurrence,
  )

  assert (
    occurrence
    .source_pattern_occurrence
    .source_occurrence
    .entry
    is data[
      "theorem_entry"
    ]
  )

  assert (
    occurrence.statement
    is data[
      "theorem_step"
    ].conclusion
  )

  assert (
    occurrence.kind
    is TodaBracketMembershipKind.THEOREM
  )

  assert occurrence.positions == (
    TodaBracketPosition.SECOND,
  )


def test_phase102_3_actual_non_membership_nu_prime_occurrences_are_excluded():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_toda_bracket_membership_occurrences(
      data[
        "repository"
      ],
      nu_prime_generator(),
    )
  )

  assert tuple(
    (
      occurrence
      .source_pattern_occurrence
      .source_occurrence
      .entry
    )
    for occurrence in result
  ) == (
    data[
      "theorem_entry"
    ],
  )


def test_phase102_3_position_filter_distinguishes_first_second_and_third():
  repository = ProofRepository()

  first_entry = make_membership_entry(
    "phase102.first",
    TodaBracketMembershipStatement(
      element=eta(
        2
      ),
      bracket=TodaBracket(
        first=nu_prime_element(),
        second=eta(
          3
        ),
        third=eta(
          4
        ),
      ),
    ),
  )

  second_entry = make_membership_entry(
    "phase102.second",
    TodaBracketMembershipStatement(
      element=eta(
        2
      ),
      bracket=TodaBracket(
        first=eta(
          3
        ),
        second=nu_prime_element(),
        third=eta(
          4
        ),
      ),
    ),
  )

  third_entry = make_membership_entry(
    "phase102.third",
    TodaBracketMembershipStatement(
      element=eta(
        2
      ),
      bracket=TodaBracket(
        first=eta(
          3
        ),
        second=eta(
          4
        ),
        third=nu_prime_element(),
      ),
    ),
  )

  for entry in (
    first_entry,
    second_entry,
    third_entry,
  ):
    repository.register(
      entry
    )

  assert tuple(
    (
      occurrence
      .source_pattern_occurrence
      .source_occurrence
      .entry
    )
    for occurrence
    in find_repository_toda_bracket_membership_occurrences(
      repository,
      nu_prime_generator(),
      position=TodaBracketPosition.FIRST,
    )
  ) == (
    first_entry,
  )

  assert tuple(
    (
      occurrence
      .source_pattern_occurrence
      .source_occurrence
      .entry
    )
    for occurrence
    in find_repository_toda_bracket_membership_occurrences(
      repository,
      nu_prime_generator(),
      position=TodaBracketPosition.SECOND,
    )
  ) == (
    second_entry,
  )

  assert tuple(
    (
      occurrence
      .source_pattern_occurrence
      .source_occurrence
      .entry
    )
    for occurrence
    in find_repository_toda_bracket_membership_occurrences(
      repository,
      nu_prime_generator(),
      position=TodaBracketPosition.THIRD,
    )
  ) == (
    third_entry,
  )


def test_phase102_3_ordinary_membership_kind_is_preserved():
  repository = ProofRepository()

  statement = TodaBracketMembershipStatement(
    element=eta(
      2
    ),
    bracket=TodaBracket(
      first=eta(
        3
      ),
      second=nu_prime_element(),
      third=eta(
        4
      ),
    ),
  )

  entry = make_membership_entry(
    "phase102.ordinary",
    statement,
  )

  repository.register(
    entry
  )

  result = (
    find_repository_toda_bracket_membership_occurrences(
      repository,
      nu_prime_generator(),
      kind=TodaBracketMembershipKind.MEMBERSHIP,
    )
  )

  assert len(
    result
  ) == 1

  assert (
    result[
      0
    ].statement
    is statement
  )

  assert (
    result[
      0
    ].kind
    is TodaBracketMembershipKind.MEMBERSHIP
  )


def test_phase102_3_theorem_kind_filter_excludes_ordinary_membership():
  repository = ProofRepository()

  repository.register(
    make_membership_entry(
      "phase102.ordinary",
      TodaBracketMembershipStatement(
        element=eta(
          2
        ),
        bracket=TodaBracket(
          first=eta(
            3
          ),
          second=nu_prime_element(),
          third=eta(
            4
          ),
        ),
      ),
    )
  )

  result = (
    find_repository_toda_bracket_membership_occurrences(
      repository,
      nu_prime_generator(),
      kind=TodaBracketMembershipKind.THEOREM,
    )
  )

  assert result == ()


def test_phase102_3_generator_only_in_membership_element_is_not_bracket_match():
  repository = ProofRepository()

  repository.register(
    make_membership_entry(
      "phase102.element-only",
      TodaBracketMembershipStatement(
        element=nu_prime_element(),
        bracket=TodaBracket(
          first=eta(
            2
          ),
          second=eta(
            3
          ),
          third=eta(
            4
          ),
        ),
      ),
    )
  )

  result = (
    find_repository_toda_bracket_membership_occurrences(
      repository,
      nu_prime_generator(),
    )
  )

  assert result == ()


def test_phase102_3_unknown_generator_returns_empty_tuple():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_toda_bracket_membership_occurrences(
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


def test_phase102_3_builder_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be a ProofRepository"
    ),
  ):
    find_repository_toda_bracket_membership_occurrences(
      "not-a-repository",
      nu_prime_generator(),
    )


def test_phase102_3_builder_rejects_non_generator():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    find_repository_toda_bracket_membership_occurrences(
      ProofRepository(),
      "ν′",
    )


def test_phase102_3_builder_rejects_invalid_position():
  with pytest.raises(
    TypeError,
    match=(
      "position must be a TodaBracketPosition "
      "or None"
    ),
  ):
    find_repository_toda_bracket_membership_occurrences(
      ProofRepository(),
      nu_prime_generator(),
      position="second",
    )


def test_phase102_3_builder_rejects_invalid_kind():
  with pytest.raises(
    TypeError,
    match=(
      "kind must be a TodaBracketMembershipKind "
      "or None"
    ),
  ):
    find_repository_toda_bracket_membership_occurrences(
      ProofRepository(),
      nu_prime_generator(),
      kind="theorem",
    )
