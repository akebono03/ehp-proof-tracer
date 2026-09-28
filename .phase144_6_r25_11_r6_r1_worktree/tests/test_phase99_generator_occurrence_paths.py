from dataclasses import dataclass

import pytest

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Sum,
  Suspension,
  TodaBracket,
)
from proof import Relation
from structural_containment import (
  contains_generator_symbol,
  find_generator_occurrence_paths,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


def test_phase99_7_direct_generator_occurrence_has_root_path():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert (
    find_generator_occurrence_paths(
      generator,
      generator,
    )
    == (
      (),
    )
  )


def test_phase99_7_homotopy_element_occurrence_ends_at_generator_field():
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

  assert (
    find_generator_occurrence_paths(
      element,
      generator,
    )
    == (
      (
        "generator",
      ),
    )
  )


def test_phase99_7_typed_and_untyped_elements_have_same_occurrence_path():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  typed = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=generator,
  )

  untyped = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=generator,
  )

  expected = (
    (
      "generator",
    ),
  )

  assert (
    find_generator_occurrence_paths(
      typed,
      generator,
    )
    == expected
  )

  assert (
    find_generator_occurrence_paths(
      untyped,
      generator,
    )
    == expected
  )


def test_phase99_7_plain_nu_does_not_match_nu_prime_path():
  plain_nu = HomotopyElement(
    name="ν",
    dimension=3,
    generator=GeneratorSymbol(
      family="ν",
    ),
  )

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert (
    find_generator_occurrence_paths(
      plain_nu,
      nu_prime_generator,
    )
    == ()
  )


def test_phase99_7_toda_bracket_membership_reports_nested_second_entry_path():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  membership = (
    TodaBracketMembershipStatement(
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
  )

  assert (
    find_generator_occurrence_paths(
      membership,
      nu_prime_generator,
    )
    == (
      (
        "bracket",
        "second",
        "expression",
        "generator",
      ),
    )
  )


def test_phase99_7_relation_composition_reports_deep_structural_path():
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
      left=eta_3,
      right=Suspension(
        expression=HomotopyElement(
          name="ν′",
          dimension=3,
          generator=nu_prime_generator,
        ),
      ),
    ),
  )

  assert (
    find_generator_occurrence_paths(
      relation,
      nu_prime_generator,
    )
    == (
      (
        "rhs",
        "right",
        "expression",
        "generator",
      ),
    )
  )


def test_phase99_7_tuple_indices_are_string_path_segments():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  values = (
    HomotopyElement(
      name="η₃",
      dimension=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    ),
    (
      HomotopyElement(
        name="ν′",
        dimension=3,
        generator=nu_prime_generator,
      ),
    ),
  )

  assert (
    find_generator_occurrence_paths(
      values,
      nu_prime_generator,
    )
    == (
      (
        "1",
        "0",
        "generator",
      ),
    )
  )


def test_phase99_7_returns_every_occurrence_in_one_structure():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  left = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator,
  )

  right = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  expression = Sum(
    left=left,
    right=right,
  )

  assert (
    find_generator_occurrence_paths(
      expression,
      nu_prime_generator,
    )
    == (
      (
        "left",
        "generator",
      ),
      (
        "right",
        "generator",
      ),
    )
  )


def test_phase99_7_shared_object_is_reported_at_each_distinct_path():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  shared = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator,
  )

  expression = Sum(
    left=shared,
    right=shared,
  )

  assert (
    find_generator_occurrence_paths(
      expression,
      nu_prime_generator,
    )
    == (
      (
        "left",
        "generator",
      ),
      (
        "right",
        "generator",
      ),
    )
  )


@dataclass
class CyclicNode:
  value: object = None
  child: object = None


def test_phase99_7_cycle_guard_does_not_discard_noncyclic_match():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  root = CyclicNode(
    value=HomotopyElement(
      name="ν′",
      dimension=3,
      generator=nu_prime_generator,
    ),
  )

  root.child = root

  assert (
    find_generator_occurrence_paths(
      root,
      nu_prime_generator,
    )
    == (
      (
        "value",
        "generator",
      ),
    )
  )


def test_phase99_7_existing_contains_predicate_remains_compatible():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  element = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator,
  )

  assert contains_generator_symbol(
    element,
    nu_prime_generator,
  )

  assert not contains_generator_symbol(
    element,
    GeneratorSymbol(
      family="ν",
    ),
  )


def test_phase99_7_rejects_non_generator_search_target():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    find_generator_occurrence_paths(
      HomotopyElement(
        name="ν′",
        dimension=3,
      ),
      "ν′",
    )
