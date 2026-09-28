from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  Relation,
  RelationType,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaProp51FiniteDimensionalStatement,
)


from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  Relation,
  RelationType,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaProp51FiniteDimensionalStatement,
)


def build_phase55_2_statement():
  n = ScalarSymbol(
    name="n",
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )

  eta_n = HomotopyElement(
    name="η_n",
    dimension=n,
    source=ScalarSum(
      left=n,
      right=1,
    ),
    target=n,
    generator=GeneratorSymbol(
      family="η",
      index=n,
    ),
  )

  pi3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_n_plus_1_n = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=1,
    ),
    sphere_dimension=n,
  )

  pi3_2_group_relation = Relation(
    lhs=pi3_2,
    rhs=FreeCyclicGroup(
      generator=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  eta2_hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=eta_2,
    ),
    rhs=iota_3,
    relation_type=RelationType.EQUALITY,
  )

  delta_iota5_relation = (
    TodaDeltaImageUpToSignStatement(
      map=TodaDeltaMap(
        source_group=pi5_5,
        target_group=pi3_2,
      ),
      element=iota_5,
      positive_value=Multiple(
        coefficient=2,
        expression=eta_2,
      ),
    )
  )

  higher_eta_group_relation = Relation(
    lhs=pi_n_plus_1_n,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_n,
    ),
    relation_type=RelationType.EQUALITY,
  )

  statement = (
    TodaProp51FiniteDimensionalStatement(
      pi3_2_group_relation=(
        pi3_2_group_relation
      ),
      eta2_hopf_relation=(
        eta2_hopf_relation
      ),
      delta_iota5_relation=(
        delta_iota5_relation
      ),
      higher_eta_group_relation=(
        higher_eta_group_relation
      ),
    )
  )

  return {
    "n": n,
    "eta_2": eta_2,
    "iota_3": iota_3,
    "iota_5": iota_5,
    "eta_n": eta_n,
    "pi3_2_group_relation": (
      pi3_2_group_relation
    ),
    "eta2_hopf_relation": (
      eta2_hopf_relation
    ),
    "delta_iota5_relation": (
      delta_iota5_relation
    ),
    "higher_eta_group_relation": (
      higher_eta_group_relation
    ),
    "statement": statement,
  }


def test_phase55_2_finite_dimensional_statement_is_representable():
  data = build_phase55_2_statement()

  assert isinstance(
    data[
      "statement"
    ],
    TodaProp51FiniteDimensionalStatement,
  )


def test_phase55_2_statement_preserves_pi3_2_group_result():
  data = build_phase55_2_statement()

  assert (
    data[
      "statement"
    ].pi3_2_group_relation
    == data[
      "pi3_2_group_relation"
    ]
  )


def test_phase55_2_statement_preserves_eta2_hopf_result():
  data = build_phase55_2_statement()

  assert (
    data[
      "statement"
    ].eta2_hopf_relation
    == data[
      "eta2_hopf_relation"
    ]
  )


def test_phase55_2_statement_preserves_delta_iota5_result():
  data = build_phase55_2_statement()

  assert (
    data[
      "statement"
    ].delta_iota5_relation
    == data[
      "delta_iota5_relation"
    ]
  )


def test_phase55_2_statement_preserves_higher_eta_group_result():
  data = build_phase55_2_statement()

  assert (
    data[
      "statement"
    ].higher_eta_group_relation
    == data[
      "higher_eta_group_relation"
    ]
  )


