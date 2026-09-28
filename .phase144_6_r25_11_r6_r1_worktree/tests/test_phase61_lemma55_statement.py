from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
  ScalarSymbol,
  TodaBracket,
)
from toda_rules import (
  TodaLemma55BracketContainsUpToSignStatement,
)


def build_phase61_2_data():
  m = ScalarSymbol(
    name="m",
  )

  t = ScalarSymbol(
    name="t",
  )

  m_plus_two = ScalarSum(
    left=m,
    right=2,
  )

  m_plus_three = ScalarSum(
    left=m,
    right=3,
  )

  t_plus_two = ScalarSum(
    left=t,
    right=2,
  )

  t_plus_five = ScalarSum(
    left=t,
    right=5,
  )

  t_plus_six = ScalarSum(
    left=t,
    right=6,
  )

  beta = HomotopyElement(
    name="β",
    dimension=t_plus_two,
    source=t_plus_two,
    target=m,
  )

  eta_m_plus_two = HomotopyElement(
    name="η_(m+2)",
    dimension=m_plus_two,
    source=m_plus_three,
    target=m_plus_two,
    generator=GeneratorSymbol(
      family="η",
      index=m_plus_two,
    ),
  )

  eta_t_plus_five = HomotopyElement(
    name="η_(t+5)",
    dimension=t_plus_five,
    source=t_plus_six,
    target=t_plus_five,
    generator=GeneratorSymbol(
      family="η",
      index=t_plus_five,
    ),
  )

  nu4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  e3_beta = IteratedSuspension(
    expression=beta,
    exponent=3,
  )

  e2_beta = IteratedSuspension(
    expression=beta,
    exponent=2,
  )

  et_nu4 = IteratedSuspension(
    expression=nu4,
    exponent=t,
  )

  bracket = TodaBracket(
    first=eta_m_plus_two,
    second=e3_beta,
    third=eta_t_plus_five,
    index=3,
  )

  positive_value = Composition(
    left=e2_beta,
    right=et_nu4,
  )

  statement = (
    TodaLemma55BracketContainsUpToSignStatement(
      bracket=bracket,
      positive_value=positive_value,
    )
  )

  return {
    "m": m,
    "t": t,
    "m_plus_two": m_plus_two,
    "m_plus_three": m_plus_three,
    "t_plus_two": t_plus_two,
    "t_plus_five": t_plus_five,
    "t_plus_six": t_plus_six,
    "beta": beta,
    "eta_m_plus_two": eta_m_plus_two,
    "eta_t_plus_five": eta_t_plus_five,
    "nu4": nu4,
    "e3_beta": e3_beta,
    "e2_beta": e2_beta,
    "et_nu4": et_nu4,
    "bracket": bracket,
    "positive_value": positive_value,
    "statement": statement,
  }


def test_phase61_2_statement_is_first_class():
  data = build_phase61_2_data()

  assert isinstance(
    data[
      "statement"
    ],
    TodaLemma55BracketContainsUpToSignStatement,
  )


def test_phase61_2_statement_preserves_bracket():
  data = build_phase61_2_data()

  assert (
    data[
      "statement"
    ].bracket
    == data[
      "bracket"
    ]
  )


def test_phase61_2_statement_preserves_positive_value():
  data = build_phase61_2_data()

  assert (
    data[
      "statement"
    ].positive_value
    == data[
      "positive_value"
    ]
  )


def test_phase61_2_bracket_has_index_three():
  data = build_phase61_2_data()

  assert (
    data[
      "statement"
    ].bracket.index
    == 3
  )


def test_phase61_2_bracket_has_lemma55_entries():
  data = build_phase61_2_data()

  bracket = (
    data[
      "statement"
    ].bracket
  )

  assert (
    bracket.first
    == data[
      "eta_m_plus_two"
    ]
  )

  assert (
    bracket.second
    == IteratedSuspension(
      expression=data[
        "beta"
      ],
      exponent=3,
    )
  )

  assert (
    bracket.third
    == data[
      "eta_t_plus_five"
    ]
  )


def test_phase61_2_positive_value_is_e2_beta_composed_with_et_nu4():
  data = build_phase61_2_data()

  assert (
    data[
      "statement"
    ].positive_value
    == Composition(
      left=IteratedSuspension(
        expression=data[
          "beta"
        ],
        exponent=2,
      ),
      right=IteratedSuspension(
        expression=data[
          "nu4"
        ],
        exponent=data[
          "t"
        ],
      ),
    )
  )


def test_phase61_2_statement_distinguishes_different_bracket():
  data = build_phase61_2_data()

  wrong_bracket = TodaBracket(
    first=data[
      "eta_m_plus_two"
    ],
    second=data[
      "e3_beta"
    ],
    third=data[
      "eta_t_plus_five"
    ],
    index=2,
  )

  wrong_statement = (
    TodaLemma55BracketContainsUpToSignStatement(
      bracket=wrong_bracket,
      positive_value=data[
        "positive_value"
      ],
    )
  )

  assert (
    wrong_statement
    != data[
      "statement"
    ]
  )


def test_phase61_2_statement_distinguishes_different_positive_value():
  data = build_phase61_2_data()

  wrong_value = Composition(
    left=data[
      "e2_beta"
    ],
    right=IteratedSuspension(
      expression=data[
        "nu4"
      ],
      exponent=ScalarSum(
        left=data[
          "t"
        ],
        right=1,
      ),
    ),
  )

  wrong_statement = (
    TodaLemma55BracketContainsUpToSignStatement(
      bracket=data[
        "bracket"
      ],
      positive_value=wrong_value,
    )
  )

  assert (
    wrong_statement
    != data[
      "statement"
    ]
  )


