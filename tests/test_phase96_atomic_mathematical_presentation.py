import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from test_phase90_known_group_lookup import (
  make_entry,
  make_generator,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_group_result import (
  normalize_toda_group_result,
)
from toda_presentation import (
  TodaGeneratorOrderKind,
  TodaGeneratorOrderPresentation,
  TodaGeneratorPresentation,
  TodaGroupResultPresentation,
  TodaGroupStructureKind,
  TodaGroupStructurePresentation,
  TodaTargetPresentation,
  build_toda_generator_order_presentation,
  build_toda_generator_presentation,
  build_toda_group_result_presentation,
  build_toda_group_structure_presentation,
  build_toda_target_presentation,
)


def test_phase96_3_target_presentation_preserves_target_identity():
  target = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  presentation = (
    build_toda_target_presentation(
      target
    )
  )

  assert isinstance(
    presentation,
    TodaTargetPresentation,
  )
  assert (
    presentation.source_target
    is target
  )
  assert (
    presentation.group_dimension
    == 9
  )
  assert (
    presentation.sphere_dimension
    == 5
  )


def test_phase96_3_infinite_order_is_first_class_presentation():
  presentation = (
    build_toda_generator_order_presentation(
      None
    )
  )

  assert (
    presentation.kind
    is TodaGeneratorOrderKind.INFINITE
  )
  assert presentation.value is None


def test_phase96_3_finite_order_is_first_class_presentation():
  presentation = (
    build_toda_generator_order_presentation(
      8
    )
  )

  assert (
    presentation.kind
    is TodaGeneratorOrderKind.FINITE
  )
  assert presentation.value == 8


def test_phase96_3_generator_presentation_preserves_expression_identity():
  generator = make_generator(
    name="nu4_squared",
    family="nu^2",
    index=4,
    dimension=10,
  )

  presentation = (
    build_toda_generator_presentation(
      generator,
      8,
    )
  )

  assert isinstance(
    presentation,
    TodaGeneratorPresentation,
  )
  assert (
    presentation.source_generator
    is generator
  )
  assert (
    presentation.order.kind
    is TodaGeneratorOrderKind.FINITE
  )
  assert presentation.order.value == 8


def test_phase96_3_free_cyclic_structure_preserves_generator_and_infinite_order():
  generator = make_generator(
    name="iota_5",
    family="iota",
    index=5,
    dimension=5,
  )
  source = FreeCyclicGroup(
    generator=generator,
  )

  presentation = (
    build_toda_group_structure_presentation(
      source
    )
  )

  assert (
    presentation.kind
    is TodaGroupStructureKind.FREE_CYCLIC
  )
  assert (
    presentation.source_structure
    is source
  )
  assert (
    presentation.generator
    .source_generator
    is generator
  )
  assert (
    presentation.generator
    .order
    .kind
    is TodaGeneratorOrderKind.INFINITE
  )
  assert presentation.summands == ()


def test_phase96_3_actual_pi9_5_finite_cyclic_structure_and_order():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  group_result = (
    candidate.group_result
  )

  presentation = (
    build_toda_group_result_presentation(
      group_result
    )
  )

  assert isinstance(
    presentation,
    TodaGroupResultPresentation,
  )
  assert (
    presentation.source_group_result
    is group_result
  )
  assert (
    presentation.target.source_target
    is group_result.target
  )
  assert (
    presentation.group_structure.kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  )
  assert (
    presentation.group_structure.source_structure
    is group_result.group_structure
  )
  assert len(
    presentation.generators
  ) == 1
  assert (
    presentation.generators[
      0
    ].source_generator
    is group_result.generators[
      0
    ]
  )
  assert (
    presentation.generators[
      0
    ].order.kind
    is TodaGeneratorOrderKind.FINITE
  )
  assert (
    presentation.generators[
      0
    ].order.value
    == 2
  )


def test_phase96_3_actual_pi7_4_direct_sum_preserves_summand_order_and_identity():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi7_4"
    ]
  )

  group_result = (
    candidate.group_result
  )

  presentation = (
    build_toda_group_result_presentation(
      group_result
    )
  )

  structure = (
    presentation.group_structure
  )

  assert (
    structure.kind
    is TodaGroupStructureKind.DIRECT_SUM
  )
  assert (
    structure.source_structure
    is group_result.group_structure
  )
  assert len(
    structure.summands
  ) == 2

  assert (
    structure.summands[
      0
    ].kind
    is TodaGroupStructureKind.FREE_CYCLIC
  )
  assert (
    structure.summands[
      1
    ].kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  )

  assert (
    structure.summands[
      0
    ].source_structure
    is (
      group_result
      .group_structure
      .summands[
        0
      ]
    )
  )
  assert (
    structure.summands[
      1
    ].source_structure
    is (
      group_result
      .group_structure
      .summands[
        1
      ]
    )
  )

  assert tuple(
    generator.order.kind
    for generator in (
      presentation.generators
    )
  ) == (
    TodaGeneratorOrderKind.INFINITE,
    TodaGeneratorOrderKind.FINITE,
  )

  assert tuple(
    generator.order.value
    for generator in (
      presentation.generators
    )
  ) == (
    None,
    4,
  )


def test_phase96_3_actual_pi9_2_zero_group_is_explicit_presentation():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_2"
    ]
  )

  group_result = (
    candidate.group_result
  )

  presentation = (
    build_toda_group_result_presentation(
      group_result
    )
  )

  assert (
    presentation.group_structure.kind
    is TodaGroupStructureKind.ZERO
  )
  assert (
    presentation
    .group_structure
    .source_structure
    is None
  )
  assert (
    presentation
    .group_structure
    .generator
    is None
  )
  assert (
    presentation
    .group_structure
    .summands
    == ()
  )
  assert presentation.generators == ()


def test_phase96_3_manual_free_group_result_preserves_source_identity():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )
  generator = HomotopyElement(
    name="iota_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="iota",
      index=5,
    ),
  )
  relation = Relation(
    lhs=target,
    rhs=FreeCyclicGroup(
      generator=generator,
    ),
    relation_type=RelationType.EQUALITY,
  )
  entry = make_entry(
    key="phase96.free",
    conclusion=relation,
    rule=ProofRule.GIVEN,
  )
  group_result = (
    normalize_toda_group_result(
      entry
    )
  )

  presentation = (
    build_toda_group_result_presentation(
      group_result
    )
  )

  assert (
    presentation.source_group_result
    is group_result
  )
  assert (
    presentation.generators[
      0
    ].source_generator
    is generator
  )
  assert (
    presentation.generators[
      0
    ].order.kind
    is TodaGeneratorOrderKind.INFINITE
  )


def test_phase96_3_nested_direct_sum_is_recursive_without_flattening_structure():
  first_generator = make_generator(
    name="a",
    family="a",
    index=1,
    dimension=1,
  )
  second_generator = make_generator(
    name="b",
    family="b",
    index=1,
    dimension=1,
  )
  third_generator = make_generator(
    name="c",
    family="c",
    index=1,
    dimension=1,
  )

  nested = DirectSumGroup(
    summands=(
      FreeCyclicGroup(
        generator=first_generator,
      ),
      DirectSumGroup(
        summands=(
          FiniteCyclicGroup(
            order=2,
            generator=second_generator,
          ),
          FiniteCyclicGroup(
            order=4,
            generator=third_generator,
          ),
        ),
      ),
    ),
  )

  presentation = (
    build_toda_group_structure_presentation(
      nested
    )
  )

  assert (
    presentation.kind
    is TodaGroupStructureKind.DIRECT_SUM
  )
  assert (
    presentation.summands[
      1
    ].kind
    is TodaGroupStructureKind.DIRECT_SUM
  )
  assert tuple(
    summand.generator.order.value
    for summand in (
      presentation.summands[
        1
      ].summands
    )
  ) == (
    2,
    4,
  )


def test_phase96_3_order_builder_rejects_bool():
  with pytest.raises(
    TypeError,
    match=(
      "order must be a positive int "
      "or None"
    ),
  ):
    build_toda_generator_order_presentation(
      True
    )


def test_phase96_3_order_builder_rejects_non_positive_int():
  with pytest.raises(
    ValueError,
    match="order must be positive",
  ):
    build_toda_generator_order_presentation(
      0
    )


def test_phase96_3_target_builder_rejects_non_target():
  with pytest.raises(
    TypeError,
    match=(
      "target must be a TodaPrimaryGroup"
    ),
  ):
    build_toda_target_presentation(
      "not-a-target"
    )


def test_phase96_3_generator_builder_rejects_non_expression():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be an Expression"
    ),
  ):
    build_toda_generator_presentation(
      "not-an-expression",
      2,
    )


def test_phase96_3_group_structure_builder_rejects_unsupported_structure():
  with pytest.raises(
    TypeError,
    match=(
      "group_structure must be "
      "FreeCyclicGroup, "
      "FiniteCyclicGroup, "
      "DirectSumGroup, or None"
    ),
  ):
    build_toda_group_structure_presentation(
      "not-a-group-structure"
    )


def test_phase96_3_group_result_builder_rejects_non_group_result():
  with pytest.raises(
    TypeError,
    match=(
      "group_result must be "
      "a TodaGroupResult"
    ),
  ):
    build_toda_group_result_presentation(
      "not-a-group-result"
    )


def test_phase96_3_order_presentation_rejects_infinite_value():
  with pytest.raises(
    ValueError,
    match=(
      "infinite order must have "
      "value None"
    ),
  ):
    TodaGeneratorOrderPresentation(
      kind=(
        TodaGeneratorOrderKind
        .INFINITE
      ),
      value=2,
    )


def test_phase96_3_finite_structure_rejects_wrong_order():
  generator = make_generator(
    name="nu",
    family="nu",
    index=5,
    dimension=8,
  )
  source = FiniteCyclicGroup(
    order=8,
    generator=generator,
  )

  with pytest.raises(
    ValueError,
    match=(
      "finite cyclic generator order "
      "must match source_structure"
    ),
  ):
    TodaGroupStructurePresentation(
      kind=(
        TodaGroupStructureKind
        .FINITE_CYCLIC
      ),
      source_structure=source,
      generator=(
        TodaGeneratorPresentation(
          source_generator=generator,
          order=(
            TodaGeneratorOrderPresentation(
              kind=(
                TodaGeneratorOrderKind
                .FINITE
              ),
              value=4,
            )
          ),
        )
      ),
    )
