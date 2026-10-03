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
    range_text=None,
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


_FIXED_COMPONENTS_BY_REFERENCE = {
  "Proposition 5.1": _PROPOSITION_51_COMPONENTS,
  "Proposition 5.3": _PROPOSITION_53_COMPONENTS,
  "Proposition 5.6": _PROPOSITION_56_COMPONENTS,
  "(5.3)": _EQUATION_53_COMPONENTS,
}


_FIXED_RULE_COMPONENT_KEYS = {
  "Toda Proposition 5.1 finite-dimensional integration": None,
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
  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": "(5.3)",
  "Toda 5.3 nu-prime Lemma 5.2 Hopf specialization": "(5.3)",
  "Toda 5.3 nu-prime Lemma 5.2 double specialization": "(5.3)",
}


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

  for locator in _TRACKED_REFERENCE_LOCATORS:
    if locator.startswith("Proposition "):
      if rule_name.startswith("Toda " + locator):
        return locator

  if rule_name.startswith("Toda 5.3 "):
    return "(5.3)"

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
