from dataclasses import dataclass
from enum import Enum

from proof import (
  LiteratureReference,
  ProofStep,
)


class TodaLiteratureStatementClassification(str, Enum):
  FIXED_STATEMENT = "fixed_statement"
  PROOF_INTERNAL = "proof_internal"


class TodaLiteratureStatementRole(str, Enum):
  GROUP_STRUCTURE = "group_structure"
  MEMBERSHIP = "membership"
  MAP_VALUE = "map_value"
  RELATION = "relation"
  OTHER = "other"


@dataclass(frozen=True)
class TodaFixedStatementComponent:
  reference_locator: str
  component_key: str
  statement_role: TodaLiteratureStatementRole
  order: int | None
  range_text: str | None
  range_is_explicit_in_current_aggregate: bool

  def __post_init__(self) -> None:
    if not isinstance(self.reference_locator, str):
      raise TypeError("reference_locator must be a str")
    if not self.reference_locator:
      raise ValueError("reference_locator must not be empty")
    if not isinstance(self.component_key, str):
      raise TypeError("component_key must be a str")
    if not self.component_key:
      raise ValueError("component_key must not be empty")
    if not isinstance(
      self.statement_role,
      TodaLiteratureStatementRole,
    ):
      raise TypeError(
        "statement_role must be a "
        "TodaLiteratureStatementRole"
      )
    if self.order is not None:
      if isinstance(self.order, bool) or not isinstance(self.order, int):
        raise TypeError("order must be an int or None")
      if self.order <= 0:
        raise ValueError("order must be positive")
    if self.range_text is not None and not isinstance(
      self.range_text,
      str,
    ):
      raise TypeError("range_text must be a str or None")
    if not isinstance(
      self.range_is_explicit_in_current_aggregate,
      bool,
    ):
      raise TypeError(
        "range_is_explicit_in_current_aggregate must be a bool"
      )


@dataclass(frozen=True)
class TodaLiteratureStatementBoundary:
  classification: TodaLiteratureStatementClassification
  reference_locator: str
  component_key: str | None = None

  def __post_init__(self) -> None:
    if not isinstance(
      self.classification,
      TodaLiteratureStatementClassification,
    ):
      raise TypeError(
        "classification must be a "
        "TodaLiteratureStatementClassification"
      )
    if not isinstance(self.reference_locator, str):
      raise TypeError("reference_locator must be a str")
    if not self.reference_locator:
      raise ValueError("reference_locator must not be empty")
    if self.component_key is not None and not isinstance(
      self.component_key,
      str,
    ):
      raise TypeError("component_key must be a str or None")



_PROPOSITION_22_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Proposition 2.2",
    component_key="hopf_right_composition_formula",
    statement_role=TodaLiteratureStatementRole.RELATION,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
)


_EQUATION_51_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="circle_higher_homotopy_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text="i > 1",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="sphere_connectivity_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text="i < n",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="stable_negative_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text="k < 0",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="diagonal_identity_group",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text="n >= 1",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="stable_zero_stem",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="diagonal_suspension_isomorphism",
    statement_role=TodaLiteratureStatementRole.OTHER,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=False,
  ),
)


_PROPOSITION_51_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.1",
    component_key="pi3_2_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=1,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.1",
    component_key="eta2_hopf_relation",
    statement_role=TodaLiteratureStatementRole.MAP_VALUE,
    order=2,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.1",
    component_key="delta_iota5_relation",
    statement_role=TodaLiteratureStatementRole.MAP_VALUE,
    order=3,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.1",
    component_key="higher_eta_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=4,
    range_text="n >= 3",
    range_is_explicit_in_current_aggregate=False,
  ),
)


_PROPOSITION_53_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.3",
    component_key="pi4_2_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=1,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.3",
    component_key="pi5_3_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=2,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.3",
    component_key="pi6_4_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=3,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.3",
    component_key="higher_eta_squared_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=4,
    range_text="n >= 5",
    range_is_explicit_in_current_aggregate=True,
  ),
)


_PROPOSITION_56_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.6",
    component_key="pi5_2_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=1,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.6",
    component_key="pi6_3_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=2,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.6",
    component_key="pi7_4_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=3,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.6",
    component_key="pi8_5_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=4,
    range_text="n = 5",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.6",
    component_key="higher_nu_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=5,
    range_text="n >= 6",
    range_is_explicit_in_current_aggregate=True,
  ),
)


_EQUATION_53_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.3)",
    component_key="nu_prime_bracket_definition",
    statement_role=TodaLiteratureStatementRole.MEMBERSHIP,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.3)",
    component_key="nu_prime_membership",
    statement_role=TodaLiteratureStatementRole.MEMBERSHIP,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.3)",
    component_key="nu_prime_hopf_relation",
    statement_role=TodaLiteratureStatementRole.MAP_VALUE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.3)",
    component_key="nu_prime_double_relation",
    statement_role=TodaLiteratureStatementRole.RELATION,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
)



_PROPOSITION_511_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.11",
    component_key="pi8_2_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=1,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.11",
    component_key="pi9_3_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=2,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.11",
    component_key="pi10_4_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=3,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.11",
    component_key="higher_nu_squared_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=4,
    range_text="n >= 5",
    range_is_explicit_in_current_aggregate=True,
  ),
)


_PROPOSITION_515_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.15",
    component_key="pi9_2_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=1,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.15",
    component_key="pi10_3_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=2,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.15",
    component_key="pi11_4_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=3,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.15",
    component_key="pi12_5_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=4,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.15",
    component_key="pi13_6_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=5,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.15",
    component_key="pi14_7_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=6,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.15",
    component_key="pi15_8_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=7,
    range_text="n = 8",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Proposition 5.15",
    component_key="higher_sigma_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=8,
    range_text="n >= 9",
    range_is_explicit_in_current_aggregate=True,
  ),
)


_LEMMA_513_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Lemma 5.13",
    component_key="sigma_triple_prime_statement",
    statement_role=TodaLiteratureStatementRole.OTHER,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
)


_LEMMA_514_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Lemma 5.14",
    component_key="sigma_double_prime_statement",
    statement_role=TodaLiteratureStatementRole.OTHER,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Lemma 5.14",
    component_key="sigma_prime_statement",
    statement_role=TodaLiteratureStatementRole.OTHER,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Lemma 5.14",
    component_key="sigma8_statement",
    statement_role=TodaLiteratureStatementRole.OTHER,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
)


_EQUATION_513_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.13)",
    component_key="delta_nu9_relation",
    statement_role=TodaLiteratureStatementRole.MAP_VALUE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.13)",
    component_key="delta_eta11_squared_zero",
    statement_role=TodaLiteratureStatementRole.MAP_VALUE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.13)",
    component_key="delta_eta13_zero",
    statement_role=TodaLiteratureStatementRole.MAP_VALUE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
)


_EQUATION_55_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.5)",
    component_key="nu_family_relations",
    statement_role=TodaLiteratureStatementRole.OTHER,
    order=None,
    range_text="n >= 5",
    range_is_explicit_in_current_aggregate=True,
  ),
)

_FIXED_COMPONENTS_BY_REFERENCE = {
  "(5.1)": _EQUATION_51_COMPONENTS,
  "Proposition 2.2": _PROPOSITION_22_COMPONENTS,
  "Proposition 5.1": _PROPOSITION_51_COMPONENTS,
  "Proposition 5.3": _PROPOSITION_53_COMPONENTS,
  "Proposition 5.6": _PROPOSITION_56_COMPONENTS,
  "Proposition 5.11": _PROPOSITION_511_COMPONENTS,
  "Proposition 5.15": _PROPOSITION_515_COMPONENTS,
  "Lemma 5.13": _LEMMA_513_COMPONENTS,
  "Lemma 5.14": _LEMMA_514_COMPONENTS,
  "(5.13)": _EQUATION_513_COMPONENTS,
  "(5.5)": _EQUATION_55_COMPONENTS,
  "(5.3)": _EQUATION_53_COMPONENTS,
}


_FIXED_COMPONENTS_BY_REFERENCE[
  "(5.1)"
] = _EQUATION_51_COMPONENTS

_FIXED_RULE_COMPONENT_KEYS = {
  "Toda Equation 5.7 nu-prime eta_6 Hopf value": "nu_prime_eta6_hopf_relation",
  "Toda (5.1) circle higher homotopy zero": "circle_higher_homotopy_zero",
  "Toda (5.1) diagonal identity group": "diagonal_identity_group",
  "Toda (5.1) low-dimensional suspension isomorphism": "diagonal_suspension_isomorphism",
  "Toda Proposition 5.1 pi_3^2 group relation": "pi3_2_group_relation",
  "Toda Proposition 5.1 Delta iota_5": "delta_iota5_relation",
  "Toda Prop.2.2 right formula": "hopf_right_composition_formula",
  "Toda Proposition 5.11 finite-dimensional integration": None,
  "Toda Proposition 5.11 pi_8^2 from Proposition 5.9 and Toda (5.2)": (
    "pi8_2_group_relation"
  ),
  "Toda Proposition 5.11 pi_9^3 zero": "pi9_3_zero",
  "Toda Proposition 5.11 pi_10^4 generated by nu_4 squared": (
    "pi10_4_group_relation"
  ),
  "Toda Proposition 5.11 nu-squared finite-dimensional integration": (
    "higher_nu_squared_group_relation"
  ),
  "Toda Proposition 5.11 pi_11^5 nu_5 squared": (
    "higher_nu_squared_group_relation"
  ),
  "Toda Proposition 5.11 pi_12^6 nu_6 squared": (
    "higher_nu_squared_group_relation"
  ),
  "Toda Proposition 5.11 pi_13^7 nu_7 squared": (
    "higher_nu_squared_group_relation"
  ),
  "Toda Proposition 5.11 pi_14^8 nu_8 squared": (
    "higher_nu_squared_group_relation"
  ),
  "Toda Proposition 5.15 finite-dimensional integration": None,
  "Toda Proposition 5.15 pi_9^2 zero from Toda (5.2)": "pi9_2_zero",
  "Toda Proposition 5.15 pi_10^3 zero": "pi10_3_zero",
  "Toda Proposition 5.15 pi_11^4 zero": "pi11_4_zero",
  "Toda Proposition 5.15 pi_12^5 finite cyclic": "pi12_5_group_relation",
  "Toda Proposition 5.15 pi_13^6 finite cyclic": "pi13_6_group_relation",
  "Toda Proposition 5.15 pi_14^7 finite cyclic": "pi14_7_group_relation",
  "Toda Proposition 5.15 pi_15^8 final decomposition": (
    "pi15_8_group_relation"
  ),
  "Toda Proposition 5.15 higher seven-stem finite-dimensional integration": (
    "higher_sigma_group_relation"
  ),
  "Toda Lemma 5.13 sigma triple-prime definition": (
    "sigma_triple_prime_statement"
  ),
  "Toda Lemma 5.14 sigma double-prime branch": (
    "sigma_double_prime_statement"
  ),
  "Toda Lemma 5.14 sigma-prime branch": "sigma_prime_statement",
  "Toda Lemma 5.14 sigma_8 branch": "sigma8_statement",
  "Toda Equation 5.13 Delta nu_9": "delta_nu9_relation",
  "Toda Equation 5.13 Delta eta_11 squared zero": (
    "delta_eta11_squared_zero"
  ),
  "Toda Equation 5.13 Delta eta_13 zero": "delta_eta13_zero",
  "Toda (5.5) nu-family finite-dimensional integration": (
    "nu_family_relations"
  ),
  "Toda Proposition 5.1 finite-dimensional integration": None,
  "Toda Proposition 5.1 higher eta group relation": "higher_eta_group_relation",
  "Toda Proposition 5.3 finite-dimensional integration": None,
  "Toda Proposition 5.3 n=3 pi_5^3 finite-cyclic transport": (
    "pi5_3_group_relation"
  ),
  "Toda Proposition 5.3 n=4 pi_6^4 finite-cyclic transport": (
    "pi6_4_group_relation"
  ),
  "Toda Proposition 5.3 higher eta-squared finite-cyclic generator bridge": (
    "higher_eta_squared_group_relation"
  ),
  "Toda Proposition 5.6 finite-dimensional integration": None,
  "Toda Proposition 5.6 pi_5^2 eta_2 cube": "pi5_2_group_relation",
  "Toda Proposition 5.6 pi_6^3 finite cyclic": "pi6_3_group_relation",
  "Toda Proposition 5.6 pi_7^4 decomposition": "pi7_4_group_relation",
  "Toda Proposition 5.6 pi_8^5 finite cyclic": "pi8_5_group_relation",
  "Toda Proposition 5.6 higher nu finite-cyclic generator bridge": (
    "higher_nu_group_relation"
  ),
  "Toda (5.3) nu-prime bracket definition": (
    "nu_prime_bracket_definition"
  ),
  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": (
    "nu_prime_membership"
  ),
  "Toda 5.3 nu-prime Lemma 5.2 Hopf specialization": (
    "nu_prime_hopf_relation"
  ),
  "Toda 5.3 nu-prime Lemma 5.2 double specialization": (
    "nu_prime_double_relation"
  ),
}


_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {
  "Toda Proposition 5.1 higher eta group relation": "Proposition 5.1",
  "Toda Equation 5.7 nu-prime eta_6 Hopf value": "(5.7)",
  "Toda (5.1) circle higher homotopy zero": "(5.1)",
  "Toda (5.1) diagonal identity group": "(5.1)",
  "Toda (5.1) low-dimensional suspension isomorphism": "(5.1)",
  "Toda Proposition 5.1 pi_3^2 group relation": "Proposition 5.1",
  "Toda Proposition 5.1 Delta iota_5": "Proposition 5.1",
  "Toda Prop.2.2 right formula": "Proposition 2.2",
  "Toda Proposition 5.11 finite-dimensional integration": "Proposition 5.11",
  "Toda Proposition 5.11 pi_8^2 from Proposition 5.9 and Toda (5.2)": (
    "Proposition 5.11"
  ),
  "Toda Proposition 5.11 pi_9^3 zero": "Proposition 5.11",
  "Toda Proposition 5.11 pi_10^4 generated by nu_4 squared": (
    "Proposition 5.11"
  ),
  "Toda Proposition 5.11 nu-squared finite-dimensional integration": (
    "Proposition 5.11"
  ),
  "Toda Proposition 5.11 pi_11^5 nu_5 squared": "Proposition 5.11",
  "Toda Proposition 5.11 pi_12^6 nu_6 squared": "Proposition 5.11",
  "Toda Proposition 5.11 pi_13^7 nu_7 squared": "Proposition 5.11",
  "Toda Proposition 5.11 pi_14^8 nu_8 squared": "Proposition 5.11",
  "Toda Proposition 5.15 finite-dimensional integration": "Proposition 5.15",
  "Toda Proposition 5.15 pi_9^2 zero from Toda (5.2)": "Proposition 5.15",
  "Toda Proposition 5.15 pi_10^3 zero": "Proposition 5.15",
  "Toda Proposition 5.15 pi_11^4 zero": "Proposition 5.15",
  "Toda Proposition 5.15 pi_12^5 finite cyclic": "Proposition 5.15",
  "Toda Proposition 5.15 pi_13^6 finite cyclic": "Proposition 5.15",
  "Toda Proposition 5.15 pi_14^7 finite cyclic": "Proposition 5.15",
  "Toda Proposition 5.15 pi_15^8 final decomposition": "Proposition 5.15",
  "Toda Proposition 5.15 higher seven-stem finite-dimensional integration": (
    "Proposition 5.15"
  ),
  "Toda Lemma 5.13 sigma triple-prime definition": "Lemma 5.13",
  "Toda Lemma 5.14 sigma double-prime branch": "Lemma 5.14",
  "Toda Lemma 5.14 sigma-prime branch": "Lemma 5.14",
  "Toda Lemma 5.14 sigma_8 branch": "Lemma 5.14",
  "Toda Equation 5.13 Delta nu_9": "(5.13)",
  "Toda Equation 5.13 Delta eta_11 squared zero": "(5.13)",
  "Toda Equation 5.13 Delta eta_13 zero": "(5.13)",
  "Toda (5.5) nu-family finite-dimensional integration": "(5.5)",
  "Toda Proposition 5.1 finite-dimensional integration": (
    "Proposition 5.1"
  ),
  "Toda Proposition 5.3 finite-dimensional integration": (
    "Proposition 5.3"
  ),
  "Toda Proposition 5.3 n=3 pi_5^3 finite-cyclic transport": (
    "Proposition 5.3"
  ),
  "Toda Proposition 5.3 n=4 pi_6^4 finite-cyclic transport": (
    "Proposition 5.3"
  ),
  "Toda Proposition 5.3 higher eta-squared finite-cyclic generator bridge": (
    "Proposition 5.3"
  ),
  "Toda Proposition 5.6 finite-dimensional integration": (
    "Proposition 5.6"
  ),
  "Toda Proposition 5.6 pi_5^2 eta_2 cube": "Proposition 5.6",
  "Toda Proposition 5.6 pi_6^3 finite cyclic": "Proposition 5.6",
  "Toda Proposition 5.6 pi_7^4 decomposition": "Proposition 5.6",
  "Toda Proposition 5.6 pi_8^5 finite cyclic": "Proposition 5.6",
  "Toda Proposition 5.6 higher nu finite-cyclic generator bridge": (
    "Proposition 5.6"
  ),
  "Toda (5.3) nu-prime bracket definition": "(5.3)",
  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": "(5.3)",
  "Toda 5.3 nu-prime Lemma 5.2 Hopf specialization": "(5.3)",
  "Toda 5.3 nu-prime Lemma 5.2 double specialization": "(5.3)",
}



# Phase157-R5-R3 boundary catalog expansion

_PHASE157_R5_R3_ADDITIONAL_COMPONENTS = {
  "(4.5)": (
    TodaFixedStatementComponent(
      reference_locator="(4.5)",
      component_key="stable_range_suspension_isomorphism",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "(5.2)": (
    TodaFixedStatementComponent(
      reference_locator="(5.2)",
      component_key="eta2_composition_isomorphism",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text="i >= 3",
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "(5.7)": (
    TodaFixedStatementComponent(
      reference_locator="(5.7)",
      component_key="nu_prime_eta6_hopf_relation",
      statement_role=TodaLiteratureStatementRole.MAP_VALUE,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "(5.8)": (
    TodaFixedStatementComponent(
      reference_locator="(5.8)",
      component_key="delta_iota9_relation",
      statement_role=TodaLiteratureStatementRole.MAP_VALUE,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Lemma 5.4": (
    TodaFixedStatementComponent(
      reference_locator="Lemma 5.4",
      component_key="nu4_statement",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Lemma 5.7": (
    TodaFixedStatementComponent(
      reference_locator="Lemma 5.7",
      component_key="eta2_suspension_zero_statement",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Lemma 5.7",
      component_key="delta_nu5_relation",
      statement_role=TodaLiteratureStatementRole.MAP_VALUE,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Proposition 2.5": (
    TodaFixedStatementComponent(
      reference_locator="Proposition 2.5",
      component_key="delta_composition_formula",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Proposition 3.1": (
    TodaFixedStatementComponent(
      reference_locator="Proposition 3.1",
      component_key="barratt_hilton_formula",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Proposition 4.4": (
    TodaFixedStatementComponent(
      reference_locator="Proposition 4.4",
      component_key="nu4_decomposition_isomorphism",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Proposition 5.8": (
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.8",
      component_key="pi6_2_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=1,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.8",
      component_key="pi7_3_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=2,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.8",
      component_key="pi8_4_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=3,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.8",
      component_key="pi9_5_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=4,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.8",
      component_key="higher_four_stem_zero",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=5,
      range_text="n >= 6",
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.8",
      component_key="finite_dimensional_aggregate",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Proposition 5.9": (
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.9",
      component_key="pi7_2_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=1,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.9",
      component_key="pi8_3_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=2,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.9",
      component_key="pi9_4_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=3,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.9",
      component_key="pi10_5_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=4,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.9",
      component_key="pi11_6_group_relation",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=5,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.9",
      component_key="higher_five_stem_zero",
      statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
      order=6,
      range_text="n >= 7",
      range_is_explicit_in_current_aggregate=True,
    ),
    TodaFixedStatementComponent(
      reference_locator="Proposition 5.9",
      component_key="finite_dimensional_aggregate",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
}

for (
  _phase157_r5_r3_locator,
  _phase157_r5_r3_components,
) in _PHASE157_R5_R3_ADDITIONAL_COMPONENTS.items():
  if (
    _phase157_r5_r3_locator
    not in _FIXED_COMPONENTS_BY_REFERENCE
  ):
    _FIXED_COMPONENTS_BY_REFERENCE[
      _phase157_r5_r3_locator
    ] = _phase157_r5_r3_components


_PHASE157_R5_R3_INTERNAL_RULE_LOCATORS = {
    'Toda Equation 5.7 nu-prime eta_6 Hopf value': '(5.7)',
    'Toda 4.5 pi_4^3 finite-cyclic transport': '(4.5)',
    'Toda 5.2 pi_4^2 finite-cyclic transport': '(5.2)',
    'Toda Lemma 5.14 sigma-family definition': 'Lemma 5.14',
    'Toda Lemma 5.4 pi_6^5 finite-cyclic specialization': 'Lemma 5.4',
    'Toda Lemma 5.7 pi_6^2 eta_2 nu-prime': 'Lemma 5.7',
    'Toda Proposition 3.1 nu_6 eta_9 zero consequence': 'Proposition 3.1',
    'Toda Proposition 4.4 eta_2 second-summand restriction': 'Proposition 4.4',
    'Toda Proposition 5.8 Delta eta_9 value': 'Proposition 5.8',
    'Toda Proposition 5.8 eta_6 nu_7 zero specialization': 'Proposition 5.8',
}


_FIXED_RULE_COMPONENT_KEYS.update(
  {
    'Toda 4.5 stable-range iterated suspension isomorphism': 'stable_range_suspension_isomorphism',
    'Toda 5.2 eta_2 composition isomorphism': 'eta2_composition_isomorphism',
    'Toda 5.5 nu-family finite-dimensional integration': 'nu_family_relations',
    'Toda Equation 5.8 integration': 'delta_iota9_relation',
    'Toda Lemma 5.4 integration': 'nu4_statement',
    'Toda Lemma 5.7 Delta nu_5 generator': 'delta_nu5_relation',
    'Toda Proposition 2.5 Delta eta_9 composition': 'delta_composition_formula',
    'Toda Proposition 4.4 eta_2 n=2 specialization': 'nu4_decomposition_isomorphism',
    'Toda Proposition 4.4 nu_4 n=4 decomposition specialization': 'nu4_decomposition_isomorphism',
    'Toda Proposition 5.15 sigma_8 n=8 Proposition 4.4 decomposition specialization': 'nu4_decomposition_isomorphism',
    'Toda Proposition 5.8 finite-dimensional integration': 'finite_dimensional_aggregate',
    'Toda Proposition 5.8 higher four-stem zero transport': 'higher_four_stem_zero',
    'Toda Proposition 5.8 pi_7^3 Hopf injective': 'pi7_3_group_relation',
    'Toda Proposition 5.8 pi_7^3 finite cyclic': 'pi7_3_group_relation',
    'Toda Proposition 5.8 pi_8^4 decomposition': 'pi8_4_group_relation',
    'Toda Proposition 5.8 pi_9^5 finite cyclic': 'pi9_5_group_relation',
    'Toda Proposition 5.9 finite-dimensional integration': 'finite_dimensional_aggregate',
    'Toda Proposition 5.9 higher five-stem zero transport': 'higher_five_stem_zero',
    'Toda Proposition 5.9 pi_11^6 Hopf injective': 'pi11_6_group_relation',
    'Toda Proposition 5.9 pi_13^13 Delta surjective': 'pi11_6_group_relation',
    'Toda Proposition 5.9 pi_8^3 Hopf injective': 'pi8_3_group_relation',
    'Toda Proposition 5.9 pi_8^3 finite cyclic': 'pi8_3_group_relation',
    'Toda Proposition 5.9 pi_9^4 decomposition': 'pi9_4_group_relation',
  }
)


_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.update(
  {
    'Toda 4.5 stable-range iterated suspension isomorphism': '(4.5)',
    'Toda 5.2 eta_2 composition isomorphism': '(5.2)',
    'Toda 5.5 nu-family finite-dimensional integration': '(5.5)',
    'Toda Equation 5.8 integration': '(5.8)',
    'Toda Lemma 5.4 integration': 'Lemma 5.4',
    'Toda Lemma 5.7 Delta nu_5 generator': 'Lemma 5.7',
    'Toda Proposition 2.5 Delta eta_9 composition': 'Proposition 2.5',
    'Toda Proposition 4.4 eta_2 n=2 specialization': 'Proposition 4.4',
    'Toda Proposition 4.4 nu_4 n=4 decomposition specialization': 'Proposition 4.4',
    'Toda Proposition 5.15 sigma_8 n=8 Proposition 4.4 decomposition specialization': 'Proposition 4.4',
    'Toda Proposition 5.8 finite-dimensional integration': 'Proposition 5.8',
    'Toda Proposition 5.8 higher four-stem zero transport': 'Proposition 5.8',
    'Toda Proposition 5.8 pi_7^3 Hopf injective': 'Proposition 5.8',
    'Toda Proposition 5.8 pi_7^3 finite cyclic': 'Proposition 5.8',
    'Toda Proposition 5.8 pi_8^4 decomposition': 'Proposition 5.8',
    'Toda Proposition 5.8 pi_9^5 finite cyclic': 'Proposition 5.8',
    'Toda Proposition 5.9 finite-dimensional integration': 'Proposition 5.9',
    'Toda Proposition 5.9 higher five-stem zero transport': 'Proposition 5.9',
    'Toda Proposition 5.9 pi_11^6 Hopf injective': 'Proposition 5.9',
    'Toda Proposition 5.9 pi_13^13 Delta surjective': 'Proposition 5.9',
    'Toda Proposition 5.9 pi_8^3 Hopf injective': 'Proposition 5.9',
    'Toda Proposition 5.9 pi_8^3 finite cyclic': 'Proposition 5.9',
    'Toda Proposition 5.9 pi_9^4 decomposition': 'Proposition 5.9',
  }
)

_FIXED_COMPONENTS_BY_REFERENCE[
  "(5.1)"
] = _EQUATION_51_COMPONENTS

_FIXED_RULE_COMPONENT_KEYS[
  "Toda (5.1) sphere connectivity zero"
] = "sphere_connectivity_zero"

_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME[
  "Toda (5.1) sphere connectivity zero"
] = "(5.1)"

_TRACKED_REFERENCE_LOCATORS = frozenset(
  _FIXED_COMPONENTS_BY_REFERENCE
)


def get_toda_fixed_statement_components(
  reference_locator: str,
) -> tuple[TodaFixedStatementComponent, ...]:
  if not isinstance(reference_locator, str):
    raise TypeError("reference_locator must be a str")

  return _FIXED_COMPONENTS_BY_REFERENCE.get(
    reference_locator,
    (),
  )


def get_toda_fixed_statement_component(
  reference_locator: str,
  component_key: str,
) -> TodaFixedStatementComponent:
  if not isinstance(reference_locator, str):
    raise TypeError("reference_locator must be a str")
  if not isinstance(component_key, str):
    raise TypeError("component_key must be a str")

  matches = tuple(
    component
    for component in get_toda_fixed_statement_components(
      reference_locator
    )
    if component.component_key == component_key
  )

  if len(matches) != 1:
    raise KeyError(
      "unknown fixed statement component: "
      f"{reference_locator} / {component_key}"
    )

  return matches[0]


def _proof_step_reference_locator(
  proof_step: ProofStep,
) -> str | None:
  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None

  reference = inference_rule.literature_reference
  if reference is not None:
    return reference.locator

  rule_name = inference_rule.name

  internal_locator = (
    _PHASE157_R5_R3_INTERNAL_RULE_LOCATORS.get(
      rule_name
    )
  )
  if internal_locator is not None:
    return internal_locator

  for locator in _TRACKED_REFERENCE_LOCATORS:
    if locator.startswith(
      (
        "Proposition ",
        "Lemma ",
        "Equation ",
      )
    ):
      if rule_name.startswith(
        "Toda " + locator
      ):
        return locator

  parenthesized_locators = tuple(
    locator
    for locator in _TRACKED_REFERENCE_LOCATORS
    if (
      locator.startswith("(")
      and locator.endswith(")")
    )
  )

  for locator in parenthesized_locators:
    number = locator[
      1:
      -1
    ]

    if (
      rule_name.startswith(
        "Toda " + locator
      )
      or rule_name.startswith(
        "Toda " + number + " "
      )
    ):
      return locator

  return None

def classify_toda_literature_statement_step(
  proof_step: ProofStep,
) -> TodaLiteratureStatementBoundary | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")

  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None

  rule_name = inference_rule.name
  fixed_locator = _REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.get(
    rule_name
  )

  if fixed_locator is not None:
    return TodaLiteratureStatementBoundary(
      classification=(
        TodaLiteratureStatementClassification.FIXED_STATEMENT
      ),
      reference_locator=fixed_locator,
      component_key=_FIXED_RULE_COMPONENT_KEYS[
        rule_name
      ],
    )

  locator = _proof_step_reference_locator(
    proof_step
  )

  if locator not in _TRACKED_REFERENCE_LOCATORS:
    return None

  return TodaLiteratureStatementBoundary(
    classification=(
      TodaLiteratureStatementClassification.PROOF_INTERNAL
    ),
    reference_locator=locator,
    component_key=None,
  )


def is_toda_fixed_statement_component_reference_eligible(
  component: TodaFixedStatementComponent,
  target_reference_locator: str,
  target_component_key: str,
) -> bool:
  if not isinstance(
    component,
    TodaFixedStatementComponent,
  ):
    raise TypeError(
      "component must be a TodaFixedStatementComponent"
    )
  if not isinstance(target_reference_locator, str):
    raise TypeError("target_reference_locator must be a str")
  if not isinstance(target_component_key, str):
    raise TypeError("target_component_key must be a str")

  if component.reference_locator != target_reference_locator:
    return True

  target_component = get_toda_fixed_statement_component(
    target_reference_locator,
    target_component_key,
  )

  if (
    component.statement_role
    != TodaLiteratureStatementRole.GROUP_STRUCTURE
    or target_component.statement_role
    != TodaLiteratureStatementRole.GROUP_STRUCTURE
  ):
    return component.component_key != target_component.component_key

  if component.order is None or target_component.order is None:
    raise ValueError(
      "same-theorem group-structure components must have order"
    )

  return component.order < target_component.order


def select_toda_fixed_statement_reference_components(
  reference_locator: str,
  target_reference_locator: str,
  target_component_key: str,
) -> tuple[TodaFixedStatementComponent, ...]:
  if not isinstance(reference_locator, str):
    raise TypeError("reference_locator must be a str")

  return tuple(
    component
    for component in get_toda_fixed_statement_components(
      reference_locator
    )
    if is_toda_fixed_statement_component_reference_eligible(
      component,
      target_reference_locator,
      target_component_key,
    )
  )
