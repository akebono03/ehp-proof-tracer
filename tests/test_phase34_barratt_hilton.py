from typing import (
  get_args,
  get_type_hints,
)

from algebra import Subgroup
from expression import (
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
)
from generator_facts import (
  GeneratorAmbientGroupFact,
)
from set_rules import (
  ImageSubgroupReference,
  KernelSubgroupReference,
  MembershipStatement,
)


def test_phase34_1_concrete_homotopy_element_typing_can_represent_concrete_membership():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  assert a.source == 5
  assert a.target == 3

  assert a.generator is None


def test_phase34_1_concrete_barratt_hilton_parameter_instance_is_representable():
  p = 3
  k = 2

  a = HomotopyElement(
    name="a",
    dimension=p,
    source=p + k,
    target=p,
  )

  assert a.source == p + k
  assert a.target == p


def test_phase34_1_symbolic_p_plus_k_is_representable_as_scalar_structure():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  p_plus_k = ScalarSum(
    left=p,
    right=k,
  )

  assert p_plus_k == ScalarSum(
    left=ScalarSymbol(
      name="p",
    ),
    right=ScalarSymbol(
      name="k",
    ),
  )


def test_phase34_1_homotopy_element_source_target_remain_concrete_integer_typing():
  type_hints = get_type_hints(
    HomotopyElement
  )

  assert type_hints["source"] == (
    int | None
  )

  assert type_hints["target"] == (
    int | None
  )


def test_phase34_1_generator_ambient_group_fact_is_generator_specific():
  type_hints = get_type_hints(
    GeneratorAmbientGroupFact
  )

  assert "generator" in type_hints
  assert "group_dimension" in type_hints
  assert "sphere_dimension" in type_hints

  assert "element" not in type_hints


def test_phase34_1_generator_ambient_group_dimensions_remain_concrete():
  type_hints = get_type_hints(
    GeneratorAmbientGroupFact
  )

  assert (
    type_hints["group_dimension"]
    is int
  )

  assert (
    type_hints["sphere_dimension"]
    is int
  )


def test_phase34_1_generic_membership_statement_is_subgroup_membership():
  type_hints = get_type_hints(
    MembershipStatement
  )

  subgroup_type = (
    type_hints["subgroup"]
  )

  assert set(
    get_args(
      subgroup_type
    )
  ) == {
    Subgroup,
    ImageSubgroupReference,
    KernelSubgroupReference,
  }


def test_phase34_1_current_membership_statement_has_no_homotopy_group_dimensions():
  type_hints = get_type_hints(
    MembershipStatement
  )

  assert "group_dimension" not in type_hints
  assert "sphere_dimension" not in type_hints


def test_phase34_1_symbolic_barratt_hilton_applicability_needs_additional_representation():
  homotopy_type_hints = get_type_hints(
    HomotopyElement
  )

  ambient_type_hints = get_type_hints(
    GeneratorAmbientGroupFact
  )

  membership_type_hints = get_type_hints(
    MembershipStatement
  )

  assert homotopy_type_hints["source"] == (
    int | None
  )

  assert ambient_type_hints[
    "group_dimension"
  ] is int

  assert "element" not in (
    ambient_type_hints
  )

  assert set(
    get_args(
      membership_type_hints[
        "subgroup"
      ]
    )
  ) == {
    Subgroup,
    ImageSubgroupReference,
    KernelSubgroupReference,
  }

  assert "group_dimension" not in (
    membership_type_hints
  )

  assert "sphere_dimension" not in (
    membership_type_hints
  )



