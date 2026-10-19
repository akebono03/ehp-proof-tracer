from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
)
from tests.test_phase75_515_pi15_8_final_group import (
  build_phase75_8e4_data,
)
from toda_group_proof_narrative_group_structure_semantics import (
  toda_group_structure_narrative_semantic_key,
)


def test_phase143_59a_direct_sum_key_ignores_summand_order():
  data = build_phase75_8e4_data()

  free = data[
    "free_summand"
  ]
  torsion = data[
    "torsion_summand"
  ]

  first = DirectSumGroup(
    summands=(
      torsion,
      free,
    ),
  )
  second = DirectSumGroup(
    summands=(
      free,
      torsion,
    ),
  )

  assert (
    toda_group_structure_narrative_semantic_key(
      first
    )
    == toda_group_structure_narrative_semantic_key(
      second
    )
  )


def test_phase143_59a_transport_and_final_group_have_same_key():
  data = build_phase75_8e4_data()

  transported_group = (
    data[
      "transported_statement"
    ].transported_group
  )
  final_group = (
    data[
      "final_step"
    ].conclusion
    .rhs
  )

  assert (
    transported_group
    != final_group
  )
  assert (
    toda_group_structure_narrative_semantic_key(
      transported_group
    )
    == toda_group_structure_narrative_semantic_key(
      final_group
    )
  )


def test_phase143_59a_finite_cyclic_order_remains_semantic():
  data = build_phase75_8e4_data()

  torsion = data[
    "torsion_summand"
  ]
  wrong_order = FiniteCyclicGroup(
    order=4,
    generator=torsion.generator,
  )

  assert (
    toda_group_structure_narrative_semantic_key(
      torsion
    )
    != toda_group_structure_narrative_semantic_key(
      wrong_order
    )
  )


def test_phase143_59a_generator_remains_semantic():
  data = build_phase75_8e4_data()

  free = data[
    "free_summand"
  ]
  torsion = data[
    "torsion_summand"
  ]
  wrong_free = FreeCyclicGroup(
    generator=torsion.generator,
  )

  assert (
    toda_group_structure_narrative_semantic_key(
      free
    )
    != toda_group_structure_narrative_semantic_key(
      wrong_free
    )
  )


def test_phase143_59a_direct_sum_key_preserves_multiplicity():
  data = build_phase75_8e4_data()

  free = data[
    "free_summand"
  ]
  one_copy = DirectSumGroup(
    summands=(
      free,
    ),
  )
  two_copies = DirectSumGroup(
    summands=(
      free,
      free,
    ),
  )

  assert (
    toda_group_structure_narrative_semantic_key(
      one_copy
    )
    != toda_group_structure_narrative_semantic_key(
      two_copies
    )
  )


def test_phase143_59a_does_not_change_direct_sum_equality_semantics():
  data = build_phase75_8e4_data()

  transported_group = (
    data[
      "transported_statement"
    ].transported_group
  )
  final_group = (
    data[
      "final_step"
    ].conclusion
    .rhs
  )

  assert (
    transported_group
    != final_group
  )


def test_phase143_59a_rejects_unsupported_group_structure():
  try:
    toda_group_structure_narrative_semantic_key(
      object()
    )
  except TypeError as error:
    assert (
      str(
        error
      )
      == (
        "unsupported group structure for "
        "Narrative semantic key"
      )
    )
  else:
    raise AssertionError(
      "TypeError was not raised"
    )
