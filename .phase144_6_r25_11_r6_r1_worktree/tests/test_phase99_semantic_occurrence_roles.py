import pytest

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  MapSymbol,
  Sum,
  Suspension,
  TodaBracket,
)
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
  classify_generator_occurrence_roles,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from structural_containment import (
  find_generator_occurrence_paths,
)
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)
from test_phase68_pi7_3_nu_prime_eta6 import (
  build_phase68_3_data,
)
from theorem_facts import (
  EPSILON_3_TODA_MEMBERSHIP_FACT,
)


def nu_prime():
  return HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )


def eta_6():
  return HomotopyElement(
    name="η₆",
    dimension=6,
    source=7,
    target=6,
    generator=GeneratorSymbol(
      family="η",
      index=6,
    ),
  )


def test_phase99_10_role_enum_has_minimal_taxonomy():
  assert tuple(
    GeneratorOccurrenceRole
  ) == (
    GeneratorOccurrenceRole.RELATION_LHS,
    GeneratorOccurrenceRole.RELATION_RHS,
    GeneratorOccurrenceRole.GROUP_GENERATOR,
    GeneratorOccurrenceRole.COMPOSITION_LEFT,
    GeneratorOccurrenceRole.COMPOSITION_RIGHT,
    GeneratorOccurrenceRole.MAP_INPUT,
    GeneratorOccurrenceRole.TODA_BRACKET_FIRST,
    GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
    GeneratorOccurrenceRole.TODA_BRACKET_THIRD,
  )


def test_phase99_10_direct_generator_has_no_semantic_role():
  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert (
    classify_generator_occurrence_roles(
      generator,
      (),
    )
    == ()
  )


def test_phase99_10_relation_rhs_group_generator_composition_left_roles():
  element = nu_prime()

  conclusion = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=element,
        right=eta_6(),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  path = (
    "rhs",
    "generator",
    "left",
    "generator",
  )

  assert (
    classify_generator_occurrence_roles(
      conclusion,
      path,
    )
    == (
      GeneratorOccurrenceRole.RELATION_RHS,
      GeneratorOccurrenceRole.GROUP_GENERATOR,
      GeneratorOccurrenceRole.COMPOSITION_LEFT,
    )
  )


def test_phase99_10_relation_rhs_group_generator_composition_right_roles():
  element = nu_prime()

  conclusion = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=2,
    ),
    rhs=FiniteCyclicGroup(
      order=4,
      generator=Composition(
        left=HomotopyElement(
          name="η₂",
          dimension=2,
          generator=GeneratorSymbol(
            family="η",
            index=2,
          ),
        ),
        right=element,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  path = (
    "rhs",
    "generator",
    "right",
    "generator",
  )

  assert (
    classify_generator_occurrence_roles(
      conclusion,
      path,
    )
    == (
      GeneratorOccurrenceRole.RELATION_RHS,
      GeneratorOccurrenceRole.GROUP_GENERATOR,
      GeneratorOccurrenceRole.COMPOSITION_RIGHT,
    )
  )


def test_phase99_10_relation_lhs_map_input_composition_left_roles():
  element = nu_prime()

  conclusion = Relation(
    lhs=MapApplication(
      map=MapSymbol(
        name="H",
      ),
      expression=Composition(
        left=element,
        right=eta_6(),
      ),
    ),
    rhs=eta_6(),
    relation_type=RelationType.EQUALITY,
  )

  path = (
    "lhs",
    "expression",
    "left",
    "generator",
  )

  assert (
    classify_generator_occurrence_roles(
      conclusion,
      path,
    )
    == (
      GeneratorOccurrenceRole.RELATION_LHS,
      GeneratorOccurrenceRole.MAP_INPUT,
      GeneratorOccurrenceRole.COMPOSITION_LEFT,
    )
  )


def test_phase99_10_toda_bracket_second_role_ignores_suspension_wrapper():
  element = nu_prime()

  bracket = TodaBracket(
    first=eta_6(),
    second=Suspension(
      expression=element,
    ),
    third=eta_6(),
    index=1,
  )

  path = (
    "second",
    "expression",
    "generator",
  )

  assert (
    classify_generator_occurrence_roles(
      bracket,
      path,
    )
    == (
      GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
    )
  )


def test_phase99_10_toda_bracket_first_and_third_are_distinct():
  first = nu_prime()
  third = nu_prime()

  bracket = TodaBracket(
    first=first,
    second=eta_6(),
    third=third,
    index=1,
  )

  assert (
    classify_generator_occurrence_roles(
      bracket,
      (
        "first",
        "generator",
      ),
    )
    == (
      GeneratorOccurrenceRole.TODA_BRACKET_FIRST,
    )
  )

  assert (
    classify_generator_occurrence_roles(
      bracket,
      (
        "third",
        "generator",
      ),
    )
    == (
      GeneratorOccurrenceRole.TODA_BRACKET_THIRD,
    )
  )


def test_phase99_10_sum_left_is_not_misclassified_as_composition_left():
  element = nu_prime()

  value = Sum(
    left=element,
    right=eta_6(),
  )

  assert (
    classify_generator_occurrence_roles(
      value,
      (
        "left",
        "generator",
      ),
    )
    == ()
  )


def test_phase99_10_nested_compositions_preserve_repeated_semantic_edges():
  element = nu_prime()

  value = Composition(
    left=Composition(
      left=element,
      right=eta_6(),
    ),
    right=eta_6(),
  )

  assert (
    classify_generator_occurrence_roles(
      value,
      (
        "left",
        "left",
        "generator",
      ),
    )
    == (
      GeneratorOccurrenceRole.COMPOSITION_LEFT,
      GeneratorOccurrenceRole.COMPOSITION_LEFT,
    )
  )


def test_phase99_10_tuple_segments_do_not_create_semantic_roles():
  element = nu_prime()

  value = (
    eta_6(),
    (
      element,
    ),
  )

  assert (
    classify_generator_occurrence_roles(
      value,
      (
        "1",
        "0",
        "generator",
      ),
    )
    == ()
  )


def test_phase99_10_actual_theorem_fact_is_toda_bracket_second():
  statement = (
    EPSILON_3_TODA_MEMBERSHIP_FACT
    .statement
  )

  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  paths = find_generator_occurrence_paths(
    statement,
    generator,
  )

  assert paths == (
    (
      "bracket",
      "second",
      "expression",
      "generator",
    ),
  )

  assert (
    classify_generator_occurrence_roles(
      statement,
      paths[
        0
      ],
    )
    == (
      GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
    )
  )


def test_phase99_10_actual_equation57_is_relation_lhs_map_input_composition_left():
  data = build_phase65_3_data()

  conclusion = data[
    "equation57_step"
  ].conclusion

  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  paths = find_generator_occurrence_paths(
    conclusion,
    generator,
  )

  assert len(
    paths
  ) == 1

  assert (
    classify_generator_occurrence_roles(
      conclusion,
      paths[
        0
      ],
    )
    == (
      GeneratorOccurrenceRole.RELATION_LHS,
      GeneratorOccurrenceRole.MAP_INPUT,
      GeneratorOccurrenceRole.COMPOSITION_LEFT,
    )
  )


def test_phase99_10_actual_phase68_group_result_is_rhs_group_generator_composition_left():
  data = build_phase68_3_data()

  conclusion = data[
    "final_step"
  ].conclusion

  generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  paths = find_generator_occurrence_paths(
    conclusion,
    generator,
  )

  assert len(
    paths
  ) == 1

  assert (
    classify_generator_occurrence_roles(
      conclusion,
      paths[
        0
      ],
    )
    == (
      GeneratorOccurrenceRole.RELATION_RHS,
      GeneratorOccurrenceRole.GROUP_GENERATOR,
      GeneratorOccurrenceRole.COMPOSITION_LEFT,
    )
  )


def test_phase99_10_rejects_non_tuple_path():
  with pytest.raises(
    TypeError,
    match="path must be a tuple",
  ):
    classify_generator_occurrence_roles(
      nu_prime(),
      [
        "generator",
      ],
    )


def test_phase99_10_rejects_non_string_path_segment():
  with pytest.raises(
    TypeError,
    match=(
      "path must contain only str segments"
    ),
  ):
    classify_generator_occurrence_roles(
      nu_prime(),
      (
        0,
      ),
    )


def test_phase99_10_rejects_path_not_resolving_to_generator():
  value = nu_prime()

  with pytest.raises(
    ValueError,
    match=(
      "path must resolve to a GeneratorSymbol"
    ),
  ):
    classify_generator_occurrence_roles(
      value,
      (),
    )


def test_phase99_10_rejects_invalid_structural_path():
  value = nu_prime()

  with pytest.raises(
    ValueError,
    match=(
      "path segment is not valid for value"
    ),
  ):
    classify_generator_occurrence_roles(
      value,
      (
        "missing",
      ),
    )
