from __future__ import annotations

import csv
from pathlib import Path


TARGET = Path(
  "toda_literature_statement_boundary.py"
)
CANDIDATES = Path(
  "phase157_r5_r2_inventory_output"
) / "phase157_r5_r2_catalog_candidates.csv"
OUTPUT_DIR = Path(
  "phase157_r5_r3_output"
)
TEST_PATH = Path(
  "tests/test_phase157_r5_r3_boundary_catalog_expansion.py"
)

EXTENSION_MARKER = (
  "# Phase157-R5-R3 boundary catalog expansion"
)

TRACKED_ANCHOR = (
  "\n_TRACKED_REFERENCE_LOCATORS = frozenset(\n"
)

OLD_LOCATOR_FUNCTION_START = (
  "def _proof_step_reference_locator(\n"
)

CLASSIFY_FUNCTION_START = (
  "\ndef classify_toda_literature_statement_step(\n"
)


COMPONENT_EXTENSION = r'''
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
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Equation 5.7": (
    TodaFixedStatementComponent(
      reference_locator="Equation 5.7",
      component_key="nu_prime_eta6_hopf_relation",
      statement_role=TodaLiteratureStatementRole.MAP_VALUE,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,
    ),
  ),
  "Equation 5.8": (
    TodaFixedStatementComponent(
      reference_locator="Equation 5.8",
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


_PHASE157_R5_R3_AGGREGATE_COMPONENTS = {
  "Proposition 5.1": "finite_dimensional_aggregate",
  "Proposition 5.3": "finite_dimensional_aggregate",
  "Proposition 5.6": "finite_dimensional_aggregate",
  "Proposition 5.11": "finite_dimensional_aggregate",
}

for (
  _phase157_r5_r3_locator,
  _phase157_r5_r3_component_key,
) in _PHASE157_R5_R3_AGGREGATE_COMPONENTS.items():
  _phase157_r5_r3_components = (
    _FIXED_COMPONENTS_BY_REFERENCE.get(
      _phase157_r5_r3_locator,
      (),
    )
  )

  if not any(
    component.component_key
    == _phase157_r5_r3_component_key
    for component in _phase157_r5_r3_components
  ):
    _FIXED_COMPONENTS_BY_REFERENCE[
      _phase157_r5_r3_locator
    ] = (
      *_phase157_r5_r3_components,
      TodaFixedStatementComponent(
        reference_locator=(
          _phase157_r5_r3_locator
        ),
        component_key=(
          _phase157_r5_r3_component_key
        ),
        statement_role=(
          TodaLiteratureStatementRole.OTHER
        ),
        order=None,
        range_text=None,
        range_is_explicit_in_current_aggregate=True,
      ),
    )


_PHASE157_R5_R3_INTERNAL_RULE_LOCATORS = {
__INTERNAL_RULE_LOCATORS__
}


_FIXED_RULE_COMPONENT_KEYS.update(
  {
__FIXED_RULE_COMPONENT_KEYS__
  }
)


_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.update(
  {
__FIXED_RULE_LOCATORS__
  }
)
'''


NEW_LOCATOR_FUNCTION = r'''def _proof_step_reference_locator(
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
'''


def _read_candidate_rows():
  if not CANDIDATES.exists():
    raise SystemExit(
      "R5-R2 catalog candidates not found: "
      + str(
        CANDIDATES
      )
    )

  with CANDIDATES.open(
    "r",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    return list(
      csv.DictReader(
        handle
      )
    )


def _normalized(
  text: str,
) -> str:
  return (
    text
    .replace(" ", "")
    .replace("\\left", "")
    .replace("\\right", "")
  )


def _prop58_component(
  statement: str,
) -> str | None:
  normalized = _normalized(
    statement
  )

  if (
    "\\pi_{6}^{2}" in normalized
    and "\\pi_{7}^{3}" in normalized
  ):
    return "finite_dimensional_aggregate"

  if "\\pi_{6}^{2}" in normalized:
    return "pi6_2_group_relation"

  if "\\pi_{7}^{3}" in normalized:
    return "pi7_3_group_relation"

  if "\\pi_{8}^{4}" in normalized:
    return "pi8_4_group_relation"

  if "\\pi_{9}^{5}" in normalized:
    return "pi9_5_group_relation"

  if (
    "\\pi_{n+4}^{n}" in normalized
    and "=0" in normalized
  ):
    return "higher_four_stem_zero"

  return None


def _prop59_component(
  statement: str,
) -> str | None:
  normalized = _normalized(
    statement
  )

  if (
    "\\pi_{7}^{2}" in normalized
    and "\\pi_{8}^{3}" in normalized
  ):
    return "finite_dimensional_aggregate"

  if "\\pi_{7}^{2}" in normalized:
    return "pi7_2_group_relation"

  if "\\pi_{8}^{3}" in normalized:
    return "pi8_3_group_relation"

  if "\\pi_{9}^{4}" in normalized:
    return "pi9_4_group_relation"

  if "\\pi_{10}^{5}" in normalized:
    return "pi10_5_group_relation"

  if "\\pi_{11}^{6}" in normalized:
    return "pi11_6_group_relation"

  if (
    "\\pi_{n+5}^{n}" in normalized
    and "=0" in normalized
  ):
    return "higher_five_stem_zero"

  return None


def _classify_candidate(
  row,
):
  locator = row[
    "reference"
  ]
  status = row[
    "boundary_status"
  ]
  rule = row[
    "selected_rule"
  ]
  statement = row[
    "sample_statement"
  ]
  normalized = _normalized(
    statement
  )

  if status == "FIXED_STATEMENT_WITHOUT_COMPONENT":
    aggregate_key = {
      "Proposition 5.1": "finite_dimensional_aggregate",
      "Proposition 5.3": "finite_dimensional_aggregate",
      "Proposition 5.6": "finite_dimensional_aggregate",
      "Proposition 5.11": "finite_dimensional_aggregate",
    }.get(
      locator
    )

    if aggregate_key is None:
      return (
        "UNDECIDED",
        None,
      )

    return (
      "FIXED_STATEMENT",
      aggregate_key,
    )

  if status != "UNTRACKED":
    return (
      "UNDECIDED",
      None,
    )

  if locator == "(4.5)":
    if (
      "同型写像" in statement
      or "isomorphism" in rule.lower()
    ):
      return (
        "FIXED_STATEMENT",
        "stable_range_suspension_isomorphism",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "(5.2)":
    if (
      "同型写像" in statement
      or "isomorphism" in rule.lower()
    ):
      return (
        "FIXED_STATEMENT",
        "eta2_composition_isomorphism",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "(5.5)":
    if (
      "\\nu_{n}" in statement
      and "E^" in statement
      and "4\\nu" in statement
    ):
      return (
        "FIXED_STATEMENT",
        "nu_family_relations",
      )

    if "nu-family" in rule.lower():
      return (
        "FIXED_STATEMENT",
        "nu_family_relations",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Equation 5.7":
    if (
      "H" in statement
      and "\\nu'" in statement
      and "\\eta_{6}" in statement
    ):
      return (
        "FIXED_STATEMENT",
        "nu_prime_eta6_hopf_relation",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Equation 5.8":
    if (
      "\\Delta" in statement
      and "\\iota_{9}" in statement
    ):
      return (
        "FIXED_STATEMENT",
        "delta_iota9_relation",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Lemma 5.4":
    if (
      "\\nu_{4}\\in" in normalized
      or "H(\\nu_{4})" in normalized
      or "2E\\nu_{4}=E^{2}\\nu'" in normalized
      or "Lemma 5.4" in rule
      and (
        "nu_4" in rule
        or "nu4" in rule
      )
    ):
      return (
        "FIXED_STATEMENT",
        "nu4_statement",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Lemma 5.7":
    if (
      "\\Delta" in statement
      and "\\nu_{5}" in statement
    ):
      return (
        "FIXED_STATEMENT",
        "delta_nu5_relation",
      )

    if (
      "E(" in statement
      and "\\eta_{2}" in statement
      and "\\nu'" in statement
      and "=0" in normalized
    ):
      return (
        "FIXED_STATEMENT",
        "eta2_suspension_zero_statement",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Proposition 2.5":
    if (
      "\\Delta" in statement
      and "\\eta_{9}" in statement
    ):
      return (
        "FIXED_STATEMENT",
        "delta_composition_formula",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Proposition 3.1":
    if (
      "\\wedge" in statement
      or "Barratt" in rule
      or "Hilton" in rule
    ):
      return (
        "FIXED_STATEMENT",
        "barratt_hilton_formula",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Proposition 4.4":
    if (
      "同型写像" in statement
      or "isomorphism" in rule.lower()
    ):
      return (
        "FIXED_STATEMENT",
        "nu4_decomposition_isomorphism",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Proposition 5.8":
    component_key = _prop58_component(
      statement
    )

    if component_key is not None:
      return (
        "FIXED_STATEMENT",
        component_key,
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Proposition 5.9":
    component_key = _prop59_component(
      statement
    )

    if component_key is not None:
      return (
        "FIXED_STATEMENT",
        component_key,
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  if locator == "Lemma 5.14":
    if (
      "\\sigma''" in statement
      or "\\sigma'" in statement
      or "\\sigma_{8}" in statement
    ):
      if "\\sigma_{8}" in statement:
        return (
          "FIXED_STATEMENT",
          "sigma8_statement",
        )

      if "\\sigma''" in statement:
        return (
          "FIXED_STATEMENT",
          "sigma_double_prime_statement",
        )

      return (
        "FIXED_STATEMENT",
        "sigma_prime_statement",
      )

    return (
      "PROOF_INTERNAL",
      None,
    )

  return (
    "UNDECIDED",
    None,
  )


def _format_mapping_lines(
  mapping,
):
  lines = []

  for key in sorted(
    mapping
  ):
    value = mapping[
      key
    ]
    lines.append(
      "    "
      + repr(
        key
      )
      + ": "
      + repr(
        value
      )
      + ","
    )

  return "\n".join(
    lines
  )


def _replace_locator_function(
  text: str,
) -> str:
  start = text.find(
    OLD_LOCATOR_FUNCTION_START
  )

  if start < 0:
    raise SystemExit(
      "_proof_step_reference_locator start not found"
    )

  end = text.find(
    CLASSIFY_FUNCTION_START,
    start,
  )

  if end < 0:
    raise SystemExit(
      "classify function anchor not found"
    )

  return (
    text[
      :start
    ]
    + NEW_LOCATOR_FUNCTION
    + text[
      end:
    ]
  )


def _build_test_text(
  expectations,
):
  cases = []

  for (
    locator,
    rule,
    expected_classification,
    expected_component,
  ) in expectations:
    cases.append(
      "  (\n"
      + "    "
      + repr(
        locator
      )
      + ",\n"
      + "    "
      + repr(
        rule
      )
      + ",\n"
      + "    "
      + repr(
        expected_classification
      )
      + ",\n"
      + "    "
      + repr(
        expected_component
      )
      + ",\n"
      + "  ),"
    )

  case_text = "\n".join(
    cases
  )

  return '''from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)


CASES = (
''' + case_text + '''
)


def _step(
  locator: str,
  rule_name: str,
) -> ProofStep:
  return ProofStep(
    conclusion="phase157-r5-r3",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=rule_name,
      literature_reference=LiteratureReference(
        label="Toda " + locator,
        locator=locator,
      ),
    ),
  )


def test_phase157_r5_r3_all_r5_r2_catalog_candidates_are_classified():
  for (
    locator,
    rule_name,
    expected_classification,
    expected_component,
  ) in CASES:
    boundary = classify_toda_literature_statement_step(
      _step(
        locator,
        rule_name,
      )
    )

    assert boundary is not None
    assert (
      boundary.classification.value
      == expected_classification
    )
    assert (
      boundary.reference_locator
      == locator
    )
    assert (
      boundary.component_key
      == expected_component
    )
'''


def main():
  if not TARGET.exists():
    raise SystemExit(
      "target not found: "
      + str(
        TARGET
      )
    )

  rows = _read_candidate_rows()

  fixed_rule_components = {}
  fixed_rule_locators = {}
  internal_rule_locators = {}
  plan_rows = []
  undecided_rows = []
  expectations = []

  for row in rows:
    classification, component_key = (
      _classify_candidate(
        row
      )
    )

    locator = row[
      "reference"
    ]
    rule = row[
      "selected_rule"
    ]

    plan_row = dict(
      row
    )
    plan_row[
      "r5_r3_classification"
    ] = classification
    plan_row[
      "r5_r3_component_key"
    ] = (
      component_key
      or ""
    )
    plan_rows.append(
      plan_row
    )

    if classification == "UNDECIDED":
      undecided_rows.append(
        plan_row
      )
      continue

    if classification == "FIXED_STATEMENT":
      fixed_rule_components[
        rule
      ] = component_key
      fixed_rule_locators[
        rule
      ] = locator
      expectations.append(
        (
          locator,
          rule,
          "fixed_statement",
          component_key,
        )
      )
      continue

    if classification == "PROOF_INTERNAL":
      internal_rule_locators[
        rule
      ] = locator
      expectations.append(
        (
          locator,
          rule,
          "proof_internal",
          None,
        )
      )
      continue

    raise SystemExit(
      "unexpected classification: "
      + classification
    )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  plan_path = (
    OUTPUT_DIR
    / "phase157_r5_r3_classification_plan.csv"
  )

  fieldnames = tuple(
    plan_rows[
      0
    ].keys()
  ) if plan_rows else ()

  if fieldnames:
    with plan_path.open(
      "w",
      encoding="utf-8-sig",
      newline="",
    ) as handle:
      writer = csv.DictWriter(
        handle,
        fieldnames=fieldnames,
      )
      writer.writeheader()
      writer.writerows(
        plan_rows
      )

  if undecided_rows:
    print(
      "R5-R3 stopped before production changes."
    )
    print(
      "UNDECIDED locator/rule pairs: "
      + str(
        len(
          undecided_rows
        )
      )
    )

    for row in undecided_rows:
      print(
        "  "
        + row[
          "reference"
        ]
        + " :: "
        + row[
          "selected_rule"
        ]
      )

    print(
      "classification plan: "
      + str(
        plan_path.resolve()
      )
    )

    raise SystemExit(
      2
    )

  text = TARGET.read_text(
    encoding="utf-8"
  )

  if EXTENSION_MARKER in text:
    raise SystemExit(
      "Phase157-R5-R3 extension is already present"
    )

  extension = COMPONENT_EXTENSION
  extension = extension.replace(
    "__INTERNAL_RULE_LOCATORS__",
    _format_mapping_lines(
      internal_rule_locators
    ),
  )
  extension = extension.replace(
    "__FIXED_RULE_COMPONENT_KEYS__",
    _format_mapping_lines(
      fixed_rule_components
    ),
  )
  extension = extension.replace(
    "__FIXED_RULE_LOCATORS__",
    _format_mapping_lines(
      fixed_rule_locators
    ),
  )

  if TRACKED_ANCHOR not in text:
    raise SystemExit(
      "tracked-locator insertion anchor not found"
    )

  text = text.replace(
    TRACKED_ANCHOR,
    "\n"
    + extension
    + TRACKED_ANCHOR,
    1,
  )

  text = _replace_locator_function(
    text
  )

  TARGET.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  TEST_PATH.write_text(
    _build_test_text(
      expectations
    ),
    encoding="utf-8",
    newline="\n",
  )

  fixed_count = len(
    fixed_rule_components
  )
  internal_count = len(
    internal_rule_locators
  )

  print(
    "Phase157-R5-R3 boundary catalog expansion applied."
  )
  print(
    "catalog candidate pairs: "
    + str(
      len(
        rows
      )
    )
  )
  print(
    "fixed rule pairs: "
    + str(
      fixed_count
    )
  )
  print(
    "proof-internal rule pairs: "
    + str(
      internal_count
    )
  )
  print(
    "undecided rule pairs: 0"
  )
  print(
    "updated: "
    + str(
      TARGET.resolve()
    )
  )
  print(
    "generated test: "
    + str(
      TEST_PATH.resolve()
    )
  )
  print(
    "classification plan: "
    + str(
      plan_path.resolve()
    )
  )


if __name__ == "__main__":
  main()
