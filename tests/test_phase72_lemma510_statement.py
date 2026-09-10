from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  TodaBracket,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from toda_rules import (
  TodaLemma510BracketModuloStatement,
  toda_eta_family_definition_statement,
  toda_nu_family_definition_statement,
)


def build_phase72_2_statement():
  nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )

  eta_9 = (
    toda_eta_family_definition_statement(
      9
    ).element
  )

  iota_10 = HomotopyElement(
    name="ι_10",
    dimension=10,
    generator=GeneratorSymbol(
      family="ι",
      index=10,
    ),
  )

  iota_13 = HomotopyElement(
    name="ι_13",
    dimension=13,
    generator=GeneratorSymbol(
      family="ι",
      index=13,
    ),
  )

  bracket = TodaBracket(
    first=nu_6,
    second=eta_9,
    third=Multiple(
      coefficient=2,
      expression=iota_10,
    ),
  )

  ambient_group = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  delta_iota_13 = MapApplication(
    map=EHP_DELTA_MAP,
    expression=iota_13,
  )

  statement = (
    TodaLemma510BracketModuloStatement(
      element=delta_iota_13,
      bracket=bracket,
      ambient_group=ambient_group,
      modulus=2,
    )
  )

  return {
    "statement": statement,
    "nu_6": nu_6,
    "eta_9": eta_9,
    "iota_10": iota_10,
    "iota_13": iota_13,
    "bracket": bracket,
    "ambient_group": ambient_group,
    "delta_iota_13": delta_iota_13,
  }


def test_phase72_2_statement_type():
  data = (
    build_phase72_2_statement()
  )

  assert isinstance(
    data[
      "statement"
    ],
    TodaLemma510BracketModuloStatement,
  )


def test_phase72_2_element_is_delta_iota13():
  data = (
    build_phase72_2_statement()
  )

  assert (
    data[
      "statement"
    ].element
    == data[
      "delta_iota_13"
    ]
  )

  assert (
    data[
      "statement"
    ].element.map
    == EHP_DELTA_MAP
  )

  assert (
    data[
      "statement"
    ].element.expression
    == data[
      "iota_13"
    ]
  )


def test_phase72_2_bracket_is_expected():
  data = (
    build_phase72_2_statement()
  )

  assert (
    data[
      "statement"
    ].bracket
    == TodaBracket(
      first=data[
        "nu_6"
      ],
      second=data[
        "eta_9"
      ],
      third=Multiple(
        coefficient=2,
        expression=data[
          "iota_10"
        ],
      ),
    )
  )


def test_phase72_2_bracket_is_unindexed():
  data = (
    build_phase72_2_statement()
  )

  assert (
    data[
      "statement"
    ].bracket.index
    is None
  )


def test_phase72_2_uses_canonical_nu6():
  data = (
    build_phase72_2_statement()
  )

  assert (
    data[
      "statement"
    ].bracket.first
    == toda_nu_family_definition_statement(
      6
    ).element
  )


def test_phase72_2_uses_canonical_eta9():
  data = (
    build_phase72_2_statement()
  )

  assert (
    data[
      "statement"
    ].bracket.second
    == toda_eta_family_definition_statement(
      9
    ).element
  )


def test_phase72_2_third_entry_is_two_iota10():
  data = (
    build_phase72_2_statement()
  )

  third = (
    data[
      "statement"
    ].bracket.third
  )

  assert isinstance(
    third,
    Multiple,
  )

  assert (
    third.coefficient
    == 2
  )

  assert (
    third.expression
    == data[
      "iota_10"
    ]
  )


def test_phase72_2_ambient_group_is_pi11_6():
  data = (
    build_phase72_2_statement()
  )

  assert (
    data[
      "statement"
    ].ambient_group
    == TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )


def test_phase72_2_modulus_is_two():
  data = (
    build_phase72_2_statement()
  )

  assert (
    data[
      "statement"
    ].modulus
    == 2
  )


def test_phase72_2_statement_structurally_represents_lemma510():
  data = (
    build_phase72_2_statement()
  )

  statement = (
    data[
      "statement"
    ]
  )

  assert (
    statement.element
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "iota_13"
      ],
    )
  )

  assert (
    statement.bracket
    == TodaBracket(
      first=data[
        "nu_6"
      ],
      second=data[
        "eta_9"
      ],
      third=Multiple(
        coefficient=2,
        expression=data[
          "iota_10"
        ],
      ),
    )
  )

  assert (
    statement.ambient_group
    == TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )

  assert (
    statement.modulus
    == 2
  )


