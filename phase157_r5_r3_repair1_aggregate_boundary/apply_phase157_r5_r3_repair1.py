from __future__ import annotations

import csv
from pathlib import Path
import re


TARGET = Path(
  "toda_literature_statement_boundary.py"
)
PLAN = Path(
  "phase157_r5_r3_output"
) / "phase157_r5_r3_classification_plan.csv"
TEST_PATH = Path(
  "tests/test_phase157_r5_r3_boundary_catalog_expansion.py"
)

AGGREGATE_BLOCK_START = (
  "_PHASE157_R5_R3_AGGREGATE_COMPONENTS = {"
)
AGGREGATE_BLOCK_END = (
  "\n\n_PHASE157_R5_R3_INTERNAL_RULE_LOCATORS = {"
)


def _read_plan():
  if not PLAN.exists():
    raise SystemExit(
      "R5-R3 classification plan not found: "
      + str(
        PLAN
      )
    )

  with PLAN.open(
    "r",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    return list(
      csv.DictReader(
        handle
      )
    )


def _remove_aggregate_component_block(
  text: str,
) -> str:
  start = text.find(
    AGGREGATE_BLOCK_START
  )
  end = text.find(
    AGGREGATE_BLOCK_END
  )

  if start < 0:
    raise SystemExit(
      "aggregate component block start not found"
    )

  if end < 0:
    raise SystemExit(
      "aggregate component block end not found"
    )

  return (
    text[
      :start
    ]
    + "_PHASE157_R5_R3_INTERNAL_RULE_LOCATORS = {"
    + text[
      end
      + len(
        AGGREGATE_BLOCK_END
      ):
    ]
  )


def _remove_mapping_line(
  text: str,
  rule_name: str,
) -> str:
  escaped = re.escape(
    repr(
      rule_name
    )
  )

  pattern = re.compile(
    r"^\s{4}"
    + escaped
    + r":\s*'finite_dimensional_aggregate',\s*$\n?",
    re.MULTILINE,
  )

  text, count = pattern.subn(
    "",
    text,
    count=1,
  )

  if count != 1:
    raise SystemExit(
      "aggregate component mapping not found for rule: "
      + rule_name
    )

  locator_pattern = re.compile(
    r"^\s{4}"
    + escaped
    + r":\s*'Proposition 5\.(?:1|3|6|11)',\s*$\n?",
    re.MULTILINE,
  )

  text, count = locator_pattern.subn(
    "",
    text,
    count=1,
  )

  if count != 1:
    raise SystemExit(
      "aggregate locator mapping not found for rule: "
      + rule_name
    )

  return text


def _build_test_text(
  rows,
):
  cases = []

  for row in rows:
    locator = row[
      "reference"
    ]
    rule = row[
      "selected_rule"
    ]
    original_status = row[
      "boundary_status"
    ]
    classification = row[
      "r5_r3_classification"
    ]
    component_key = row[
      "r5_r3_component_key"
    ]

    if (
      original_status
      == "FIXED_STATEMENT_WITHOUT_COMPONENT"
    ):
      expected_classification = "fixed_statement"
      expected_component = None
    elif classification == "FIXED_STATEMENT":
      expected_classification = "fixed_statement"
      expected_component = (
        component_key
        or None
      )
    elif classification == "PROOF_INTERNAL":
      expected_classification = "proof_internal"
      expected_component = None
    else:
      raise SystemExit(
        "unexpected classification plan row: "
        + str(
          row
        )
      )

    cases.append(
      (
        locator,
        rule,
        expected_classification,
        expected_component,
      )
    )

  lines = [
    "from proof import (",
    "  InferenceRule,",
    "  LiteratureReference,",
    "  ProofRule,",
    "  ProofStep,",
    ")",
    "from toda_literature_statement_boundary import (",
    "  classify_toda_literature_statement_step,",
    ")",
    "",
    "",
    "CASES = (",
  ]

  for (
    locator,
    rule,
    expected_classification,
    expected_component,
  ) in cases:
    lines.extend(
      (
        "  (",
        "    " + repr(
          locator
        ) + ",",
        "    " + repr(
          rule
        ) + ",",
        "    " + repr(
          expected_classification
        ) + ",",
        "    " + repr(
          expected_component
        ) + ",",
        "  ),",
      )
    )

  lines.extend(
    (
      ")",
      "",
      "",
      "def _step(",
      "  locator: str,",
      "  rule_name: str,",
      ") -> ProofStep:",
      "  return ProofStep(",
      '    conclusion="phase157-r5-r3",',
      "    premises=(),",
      "    rule=ProofRule.INFERENCE,",
      "    inference_rule=InferenceRule(",
      "      name=rule_name,",
      "      literature_reference=LiteratureReference(",
      '        label="Toda " + locator,',
      "        locator=locator,",
      "      ),",
      "    ),",
      "  )",
      "",
      "",
      "def test_phase157_r5_r3_all_r5_r2_catalog_candidates_are_classified():",
      "  for (",
      "    locator,",
      "    rule_name,",
      "    expected_classification,",
      "    expected_component,",
      "  ) in CASES:",
      "    boundary = classify_toda_literature_statement_step(",
      "      _step(",
      "        locator,",
      "        rule_name,",
      "      )",
      "    )",
      "",
      "    assert boundary is not None",
      "    assert (",
      "      boundary.classification.value",
      "      == expected_classification",
      "    )",
      "    assert (",
      "      boundary.reference_locator",
      "      == locator",
      "    )",
      "    assert (",
      "      boundary.component_key",
      "      == expected_component",
      "    )",
      "",
      "",
      "def test_phase157_r5_r3_aggregate_fixed_statements_do_not_expand_component_inventory():",
      "  aggregate_locators = (",
      '    "Proposition 5.1",',
      '    "Proposition 5.3",',
      '    "Proposition 5.6",',
      '    "Proposition 5.11",',
      "  )",
      "",
      "  for locator in aggregate_locators:",
      "    aggregate_cases = tuple(",
      "      case",
      "      for case in CASES",
      "      if (",
      "        case[0] == locator",
      "        and case[3] is None",
      "        and case[2] == \"fixed_statement\"",
      "      )",
      "    )",
      "",
      "    assert aggregate_cases",
    )
  )

  return "\n".join(
    lines
  ) + "\n"


def main():
  if not TARGET.exists():
    raise SystemExit(
      "target not found: "
      + str(
        TARGET
      )
    )

  rows = _read_plan()

  aggregate_rows = [
    row
    for row in rows
    if row[
      "boundary_status"
    ] == "FIXED_STATEMENT_WITHOUT_COMPONENT"
  ]

  if len(
    aggregate_rows
  ) != 4:
    raise SystemExit(
      "expected 4 aggregate rows, found "
      + str(
        len(
          aggregate_rows
        )
      )
    )

  text = TARGET.read_text(
    encoding="utf-8"
  )

  text = _remove_aggregate_component_block(
    text
  )

  for row in aggregate_rows:
    text = _remove_mapping_line(
      text,
      row[
        "selected_rule"
      ],
    )

  TARGET.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  TEST_PATH.write_text(
    _build_test_text(
      rows
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R3 repair1 applied."
  )
  print(
    "removed synthetic aggregate components: 4"
  )
  print(
    "removed forced aggregate rule mappings: 4"
  )
  print(
    "aggregate classification remains FIXED_STATEMENT with component_key=None"
  )
  print(
    "updated: "
    + str(
      TARGET.resolve()
    )
  )
  print(
    "updated test: "
    + str(
      TEST_PATH.resolve()
    )
  )


if __name__ == "__main__":
  main()
