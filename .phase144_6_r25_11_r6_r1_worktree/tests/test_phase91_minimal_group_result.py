from dataclasses import FrozenInstanceError

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
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult


def build_phase91_2_fixture():
  target = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=4,
  )

  free_generator = HomotopyElement(
    name="nu_4",
    dimension=7,
    generator=GeneratorSymbol(
      family="nu",
      index=4,
    ),
  )

  finite_generator = HomotopyElement(
    name="E_nu_prime",
    dimension=7,
    generator=GeneratorSymbol(
      family="E_nu_prime",
      index=4,
    ),
  )

  group_structure = DirectSumGroup(
    summands=(
      FreeCyclicGroup(
        generator=free_generator,
      ),
      FiniteCyclicGroup(
        order=4,
        generator=finite_generator,
      ),
    ),
  )

  conclusion = Relation(
    lhs=target,
    rhs=group_structure,
    relation_type=RelationType.EQUALITY,
  )

  proof_step = ProofStep(
    conclusion=conclusion,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  source_entry = ProofRepositoryEntry(
    key="phase91.fixture.pi7_4",
    step=proof_step,
    phase="91-2",
    theorem="Phase 91-2 fixture",
  )

  result = TodaGroupResult(
    target=target,
    group_structure=group_structure,
    generators=(
      free_generator,
      finite_generator,
    ),
    generator_orders=(
      None,
      4,
    ),
    source_entry=source_entry,
    proof_step=proof_step,
  )

  return {
    "target": target,
    "free_generator": free_generator,
    "finite_generator": finite_generator,
    "group_structure": group_structure,
    "conclusion": conclusion,
    "proof_step": proof_step,
    "source_entry": source_entry,
    "result": result,
  }


def test_phase91_2_represents_group_structure_generators_and_orders():
  data = build_phase91_2_fixture()

  result = data[
    "result"
  ]

  assert (
    result.target
    == data[
      "target"
    ]
  )
  assert (
    result.group_structure
    == data[
      "group_structure"
    ]
  )
  assert (
    result.generators
    == (
      data[
        "free_generator"
      ],
      data[
        "finite_generator"
      ],
    )
  )
  assert (
    result.generator_orders
    == (
      None,
      4,
    )
  )


def test_phase91_2_none_represents_free_generator_order():
  data = build_phase91_2_fixture()

  assert (
    data[
      "result"
    ].generator_orders[
      0
    ]
    is None
  )


def test_phase91_2_zero_group_uses_none_structure_and_empty_generator_tuples():
  target = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=2,
  )

  proof_step = ProofStep(
    conclusion=(
      TodaPrimaryGroupZeroStatement(
        group=target,
      )
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  source_entry = ProofRepositoryEntry(
    key="phase91.fixture.pi9_2",
    step=proof_step,
    phase="91-2",
    theorem="Phase 91-2 zero fixture",
  )

  result = TodaGroupResult(
    target=target,
    group_structure=None,
    generators=(),
    generator_orders=(),
    source_entry=source_entry,
    proof_step=proof_step,
  )

  assert result.group_structure is None
  assert result.generators == ()
  assert result.generator_orders == ()


def test_phase91_2_preserves_source_entry_and_proof_step_identity():
  data = build_phase91_2_fixture()

  result = data[
    "result"
  ]

  assert (
    result.source_entry
    is data[
      "source_entry"
    ]
  )
  assert (
    result.proof_step
    is data[
      "proof_step"
    ]
  )
  assert (
    result.proof_step
    is result.source_entry.step
  )


def test_phase91_2_requires_parallel_generator_and_order_tuples():
  data = build_phase91_2_fixture()

  with pytest.raises(
    ValueError,
    match=(
      "generators and generator_orders "
      "must have the same length"
    ),
  ):
    TodaGroupResult(
      target=data[
        "target"
      ],
      group_structure=data[
        "group_structure"
      ],
      generators=(
        data[
          "free_generator"
        ],
      ),
      generator_orders=(
        None,
        4,
      ),
      source_entry=data[
        "source_entry"
      ],
      proof_step=data[
        "proof_step"
      ],
    )


def test_phase91_2_rejects_nonpositive_finite_generator_order():
  data = build_phase91_2_fixture()

  with pytest.raises(
    ValueError,
    match=(
      "generator orders must be positive"
    ),
  ):
    TodaGroupResult(
      target=data[
        "target"
      ],
      group_structure=data[
        "group_structure"
      ],
      generators=(
        data[
          "free_generator"
        ],
      ),
      generator_orders=(
        0,
      ),
      source_entry=data[
        "source_entry"
      ],
      proof_step=data[
        "proof_step"
      ],
    )


def test_phase91_2_rejects_boolean_generator_order():
  data = build_phase91_2_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "generator orders must be "
      "positive ints or None"
    ),
  ):
    TodaGroupResult(
      target=data[
        "target"
      ],
      group_structure=data[
        "group_structure"
      ],
      generators=(
        data[
          "free_generator"
        ],
      ),
      generator_orders=(
        True,
      ),
      source_entry=data[
        "source_entry"
      ],
      proof_step=data[
        "proof_step"
      ],
    )


def test_phase91_2_zero_group_cannot_have_generators():
  data = build_phase91_2_fixture()

  with pytest.raises(
    ValueError,
    match=(
      "zero group result must have "
      "empty generators and "
      "generator_orders"
    ),
  ):
    TodaGroupResult(
      target=data[
        "target"
      ],
      group_structure=None,
      generators=(
        data[
          "free_generator"
        ],
      ),
      generator_orders=(
        None,
      ),
      source_entry=data[
        "source_entry"
      ],
      proof_step=data[
        "proof_step"
      ],
    )


def test_phase91_2_requires_proof_step_to_be_source_entry_step():
  data = build_phase91_2_fixture()

  other_step = ProofStep(
    conclusion=data[
      "conclusion"
    ],
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  with pytest.raises(
    ValueError,
    match=(
      "proof_step must be source_entry.step"
    ),
  ):
    TodaGroupResult(
      target=data[
        "target"
      ],
      group_structure=data[
        "group_structure"
      ],
      generators=(
        data[
          "free_generator"
        ],
        data[
          "finite_generator"
        ],
      ),
      generator_orders=(
        None,
        4,
      ),
      source_entry=data[
        "source_entry"
      ],
      proof_step=other_step,
    )


def test_phase91_2_result_is_frozen():
  data = build_phase91_2_fixture()

  with pytest.raises(
    FrozenInstanceError,
  ):
    data[
      "result"
    ].target = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=4,
    )
