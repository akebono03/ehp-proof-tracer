import pytest

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Suspension,
  TodaBracket,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_element_lookup import (
  find_repository_entries_by_conclusion_generator,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


def make_entry(
  key,
  conclusion,
  premises=(),
):
  return ProofRepositoryEntry(
    key=key,
    step=ProofStep(
      conclusion=conclusion,
      premises=premises,
      rule=(
        ProofRule.INFERENCE
        if premises
        else ProofRule.GIVEN
      ),
    ),
  )


def test_phase99_4_empty_repository_returns_empty_tuple():
  repository = ProofRepository()

  result = (
    find_repository_entries_by_conclusion_generator(
      repository,
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert result == ()


def test_phase99_4_finds_typed_and_untyped_nu_prime_conclusions_in_registration_order():
  repository = ProofRepository()

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  typed_entry = make_entry(
    "phase99.typed",
    HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=nu_prime_generator,
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

  untyped_entry = make_entry(
    "phase99.untyped",
    HomotopyElement(
      name="ν′",
      dimension=3,
      generator=nu_prime_generator,
    ),
  )

  repository.register(
    typed_entry
  )
  repository.register(
    unrelated_entry
  )
  repository.register(
    untyped_entry
  )

  result = (
    find_repository_entries_by_conclusion_generator(
      repository,
      nu_prime_generator,
    )
  )

  assert result == (
    typed_entry,
    untyped_entry,
  )


def test_phase99_4_does_not_match_plain_nu_when_searching_for_nu_prime():
  repository = ProofRepository()

  plain_nu_entry = make_entry(
    "phase99.plain_nu",
    HomotopyElement(
      name="ν",
      dimension=3,
      generator=GeneratorSymbol(
        family="ν",
      ),
    ),
  )

  repository.register(
    plain_nu_entry
  )

  result = (
    find_repository_entries_by_conclusion_generator(
      repository,
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert result == ()


def test_phase99_4_finds_nu_prime_nested_in_toda_bracket_conclusion():
  repository = ProofRepository()

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  membership = TodaBracketMembershipStatement(
    element=HomotopyElement(
      name="ε₃",
      dimension=3,
      generator=GeneratorSymbol(
        family="ε",
        index=3,
      ),
    ),
    bracket=TodaBracket(
      first=HomotopyElement(
        name="η₃",
        dimension=3,
        generator=GeneratorSymbol(
          family="η",
          index=3,
        ),
      ),
      second=Suspension(
        expression=HomotopyElement(
          name="ν′",
          dimension=3,
          generator=nu_prime_generator,
        ),
      ),
      third=HomotopyElement(
        name="ν₇",
        dimension=7,
        generator=GeneratorSymbol(
          family="ν",
          index=7,
        ),
      ),
      index=1,
    ),
  )

  entry = make_entry(
    "phase99.bracket",
    membership,
  )

  repository.register(
    entry
  )

  result = (
    find_repository_entries_by_conclusion_generator(
      repository,
      nu_prime_generator,
    )
  )

  assert result == (
    entry,
  )


def test_phase99_4_finds_nu_prime_deep_inside_relation_conclusion():
  repository = ProofRepository()

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  relation = Relation(
    lhs=eta_3,
    rhs=Composition(
      left=Multiple(
        coefficient=2,
        expression=eta_3,
      ),
      right=Suspension(
        expression=HomotopyElement(
          name="ν′",
          dimension=3,
          source=6,
          target=3,
          generator=nu_prime_generator,
        ),
      ),
    ),
  )

  entry = make_entry(
    "phase99.relation",
    relation,
  )

  repository.register(
    entry
  )

  result = (
    find_repository_entries_by_conclusion_generator(
      repository,
      nu_prime_generator,
    )
  )

  assert result == (
    entry,
  )


def test_phase99_4_does_not_search_proof_premises():
  repository = ProofRepository()

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  premise_step = ProofStep(
    conclusion=HomotopyElement(
      name="ν′",
      dimension=3,
      generator=nu_prime_generator,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  final_entry = make_entry(
    "phase99.final",
    HomotopyElement(
      name="η₃",
      dimension=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    ),
    premises=(
      premise_step,
    ),
  )

  repository.register(
    final_entry
  )

  result = (
    find_repository_entries_by_conclusion_generator(
      repository,
      nu_prime_generator,
    )
  )

  assert result == ()


def test_phase99_4_preserves_multiple_repository_entries_for_same_matching_step():
  repository = ProofRepository()

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  step = ProofStep(
    conclusion=HomotopyElement(
      name="ν′",
      dimension=3,
      generator=nu_prime_generator,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_entry = ProofRepositoryEntry(
    key="phase99.first",
    step=step,
  )

  second_entry = ProofRepositoryEntry(
    key="phase99.second",
    step=step,
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    find_repository_entries_by_conclusion_generator(
      repository,
      nu_prime_generator,
    )
  )

  assert result == (
    first_entry,
    second_entry,
  )

  assert result[0].step is step
  assert result[1].step is step


def test_phase99_4_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be a ProofRepository"
    ),
  ):
    find_repository_entries_by_conclusion_generator(
      "not-a-repository",
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )


def test_phase99_4_rejects_non_generator():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    find_repository_entries_by_conclusion_generator(
      repository,
      "ν′",
    )


def test_phase99_4_lookup_does_not_mutate_repository_or_conclusion():
  repository = ProofRepository()

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  conclusion = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=nu_prime_generator,
  )

  entry = make_entry(
    "phase99.identity",
    conclusion,
  )

  repository.register(
    entry
  )

  entries_before = repository.entries()
  conclusion_before = entry.step.conclusion

  result = (
    find_repository_entries_by_conclusion_generator(
      repository,
      nu_prime_generator,
    )
  )

  assert result == (
    entry,
  )

  assert repository.entries() == (
    entries_before
  )

  assert entry.step.conclusion is (
    conclusion_before
  )

  assert result[0] is entry
