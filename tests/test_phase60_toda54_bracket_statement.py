from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  TodaBracket,
)
from toda_rules import (
  Toda54BracketUpToSignStatement,
)


def build_phase60_2_data():
  n = ScalarSymbol(
    name="n",
  )

  t = ScalarSymbol(
    name="t",
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  eta_n = HomotopyElement(
    name="η_n",
    dimension=n,
    source=n_plus_one,
    target=n,
    generator=GeneratorSymbol(
      family="η",
      index=n,
    ),
  )

  eta_n_plus_one = HomotopyElement(
    name="η_(n+1)",
    dimension=n_plus_one,
    source=ScalarSum(
      left=n,
      right=2,
    ),
    target=n_plus_one,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_one,
    ),
  )

  iota_n_plus_one = HomotopyElement(
    name="ι_(n+1)",
    dimension=n_plus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=n_plus_one,
    ),
  )

  bracket = TodaBracket(
    first=eta_n,
    second=Multiple(
      coefficient=2,
      expression=iota_n_plus_one,
    ),
    third=eta_n_plus_one,
    index=t,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  exponent = ScalarSum(
    left=n,
    right=ScalarProduct(
      left=-1,
      right=3,
    ),
  )

  positive_value = IteratedSuspension(
    expression=nu_prime,
    exponent=exponent,
  )

  statement = Toda54BracketUpToSignStatement(
    bracket=bracket,
    positive_value=positive_value,
  )

  return {
    "n": n,
    "t": t,
    "n_plus_one": n_plus_one,
    "eta_n": eta_n,
    "eta_n_plus_one": eta_n_plus_one,
    "iota_n_plus_one": iota_n_plus_one,
    "bracket": bracket,
    "nu_prime": nu_prime,
    "exponent": exponent,
    "positive_value": positive_value,
    "statement": statement,
  }


def test_phase60_2_statement_is_first_class():
  data = build_phase60_2_data()

  assert isinstance(
    data[
      "statement"
    ],
    Toda54BracketUpToSignStatement,
  )


def test_phase60_2_statement_preserves_bracket():
  data = build_phase60_2_data()

  assert (
    data[
      "statement"
    ].bracket
    == data[
      "bracket"
    ]
  )


def test_phase60_2_bracket_has_symbolic_t_index():
  data = build_phase60_2_data()

  assert (
    data[
      "statement"
    ].bracket.index
    == data[
      "t"
    ]
  )


def test_phase60_2_bracket_has_expected_entries():
  data = build_phase60_2_data()

  bracket = (
    data[
      "statement"
    ].bracket
  )

  assert (
    bracket.first
    == data[
      "eta_n"
    ]
  )

  assert (
    bracket.second
    == Multiple(
      coefficient=2,
      expression=data[
        "iota_n_plus_one"
      ],
    )
  )

  assert (
    bracket.third
    == data[
      "eta_n_plus_one"
    ]
  )


def test_phase60_2_positive_value_is_iterated_suspension_n_minus_3():
  data = build_phase60_2_data()

  value = (
    data[
      "statement"
    ].positive_value
  )

  assert isinstance(
    value,
    IteratedSuspension,
  )

  assert (
    value.expression
    == data[
      "nu_prime"
    ]
  )

  assert (
    value.exponent
    == data[
      "exponent"
    ]
  )

  assert (
    value.exponent
    == ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=3,
      ),
    )
  )


def test_phase60_2_statement_distinguishes_different_bracket_index():
  data = build_phase60_2_data()

  other_t = ScalarSymbol(
    name="u",
  )

  other_bracket = TodaBracket(
    first=data[
      "eta_n"
    ],
    second=Multiple(
      coefficient=2,
      expression=data[
        "iota_n_plus_one"
      ],
    ),
    third=data[
      "eta_n_plus_one"
    ],
    index=other_t,
  )

  other_statement = Toda54BracketUpToSignStatement(
    bracket=other_bracket,
    positive_value=data[
      "positive_value"
    ],
  )

  assert (
    other_statement
    != data[
      "statement"
    ]
  )


def test_phase60_2_statement_distinguishes_different_positive_value():
  data = build_phase60_2_data()

  wrong_value = IteratedSuspension(
    expression=data[
      "nu_prime"
    ],
    exponent=ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=2,
      ),
    ),
  )

  wrong_statement = Toda54BracketUpToSignStatement(
    bracket=data[
      "bracket"
    ],
    positive_value=wrong_value,
  )

  assert (
    wrong_statement
    != data[
      "statement"
    ]
  )


