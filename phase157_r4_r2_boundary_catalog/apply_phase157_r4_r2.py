from pathlib import Path

TARGET = Path("toda_literature_statement_boundary.py")

COMPONENT_INSERT_ANCHOR = "\n_FIXED_COMPONENTS_BY_REFERENCE = {\n"

COMPONENTS = r'''
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
    reference_locator="Equation 5.13",
    component_key="delta_nu9_relation",
    statement_role=TodaLiteratureStatementRole.MAP_VALUE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Equation 5.13",
    component_key="delta_eta11_squared_zero",
    statement_role=TodaLiteratureStatementRole.MAP_VALUE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="Equation 5.13",
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

'''

DICT_OLD = '''_FIXED_COMPONENTS_BY_REFERENCE = {
  "Proposition 5.1": _PROPOSITION_51_COMPONENTS,
  "Proposition 5.3": _PROPOSITION_53_COMPONENTS,
  "Proposition 5.6": _PROPOSITION_56_COMPONENTS,
  "(5.3)": _EQUATION_53_COMPONENTS,
}'''

DICT_NEW = '''_FIXED_COMPONENTS_BY_REFERENCE = {
  "Proposition 5.1": _PROPOSITION_51_COMPONENTS,
  "Proposition 5.3": _PROPOSITION_53_COMPONENTS,
  "Proposition 5.6": _PROPOSITION_56_COMPONENTS,
  "Proposition 5.11": _PROPOSITION_511_COMPONENTS,
  "Proposition 5.15": _PROPOSITION_515_COMPONENTS,
  "Lemma 5.13": _LEMMA_513_COMPONENTS,
  "Lemma 5.14": _LEMMA_514_COMPONENTS,
  "Equation 5.13": _EQUATION_513_COMPONENTS,
  "(5.5)": _EQUATION_55_COMPONENTS,
  "(5.3)": _EQUATION_53_COMPONENTS,
}'''

RULE_ANCHOR = "_FIXED_RULE_COMPONENT_KEYS = {\n"
RULE_PREFIX = '''_FIXED_RULE_COMPONENT_KEYS = {
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
'''

LOCATOR_ANCHOR = "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {\n"
LOCATOR_PREFIX = '''_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {
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
  "Toda Equation 5.13 Delta nu_9": "Equation 5.13",
  "Toda Equation 5.13 Delta eta_11 squared zero": "Equation 5.13",
  "Toda Equation 5.13 Delta eta_13 zero": "Equation 5.13",
  "Toda (5.5) nu-family finite-dimensional integration": "(5.5)",
'''


def main():
  if not TARGET.exists():
    raise SystemExit(f"target not found: {TARGET}")

  text = TARGET.read_text(encoding="utf-8")

  if "_PROPOSITION_511_COMPONENTS" not in text:
    if COMPONENT_INSERT_ANCHOR not in text:
      raise SystemExit("component insertion anchor not found")
    text = text.replace(
      COMPONENT_INSERT_ANCHOR,
      "\n" + COMPONENTS + "_FIXED_COMPONENTS_BY_REFERENCE = {\n",
      1,
    )

  if DICT_OLD in text:
    text = text.replace(
      DICT_OLD,
      DICT_NEW,
      1,
    )
  elif DICT_NEW not in text:
    raise SystemExit("fixed component dictionary shape not recognized")

  if '"Toda Proposition 5.11 finite-dimensional integration"' not in text:
    if RULE_ANCHOR not in text:
      raise SystemExit("fixed rule dictionary anchor not found")
    text = text.replace(
      RULE_ANCHOR,
      RULE_PREFIX,
      1,
    )

  locator_marker = (
    '"Toda Proposition 5.11 finite-dimensional integration": '
    '"Proposition 5.11"'
  )
  if locator_marker not in text:
    if LOCATOR_ANCHOR not in text:
      raise SystemExit("fixed locator dictionary anchor not found")
    text = text.replace(
      LOCATOR_ANCHOR,
      LOCATOR_PREFIX,
      1,
    )

  TARGET.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R4-R2 boundary catalog expansion applied.")
  print(f"updated: {TARGET.resolve()}")


if __name__ == "__main__":
  main()
