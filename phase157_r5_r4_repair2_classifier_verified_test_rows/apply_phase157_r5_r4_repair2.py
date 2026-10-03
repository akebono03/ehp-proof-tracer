
from __future__ import annotations

import csv
from pathlib import Path
import sys

PLAN = Path("phase157_r5_r3_output") / "phase157_r5_r3_classification_plan.csv"
TEST = Path("tests/test_phase157_r5_r4_generic_reference_selection.py")

REPOSITORY_ROOT = Path.cwd()
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)


def _reference(locator: str) -> LiteratureReference:
  return LiteratureReference(
    label="Toda " + locator,
    locator=locator,
  )


def _step_from_row(row) -> ProofStep:
  return ProofStep(
    conclusion="phase157-r5-r4-repair2",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=row["selected_rule"],
      literature_reference=_reference(
        row["reference"]
      ),
    ),
  )


def _read_rows():
  if not PLAN.exists():
    raise SystemExit(
      "classification plan not found: " + str(PLAN)
    )

  with PLAN.open(
    "r",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    return list(csv.DictReader(handle))


def _classify_row(row):
  return classify_toda_literature_statement_step(
    _step_from_row(row)
  )


def _pick_rows(rows):
  fixed_row = None
  internal_row = None
  aggregate_row = None

  for row in rows:
    boundary = _classify_row(row)

    if boundary is None:
      continue

    if (
      fixed_row is None
      and boundary.classification
      == TodaLiteratureStatementClassification.FIXED_STATEMENT
      and boundary.component_key is not None
    ):
      fixed_row = row

    if (
      internal_row is None
      and boundary.classification
      == TodaLiteratureStatementClassification.PROOF_INTERNAL
    ):
      internal_row = row

    if (
      aggregate_row is None
      and boundary.classification
      == TodaLiteratureStatementClassification.FIXED_STATEMENT
      and boundary.component_key is None
    ):
      aggregate_row = row

  if fixed_row is None:
    raise SystemExit(
      "no classifier-verified fixed component row found"
    )

  if internal_row is None:
    raise SystemExit(
      "no classifier-verified proof-internal row found"
    )

  if aggregate_row is None:
    raise SystemExit(
      "no classifier-verified fixed aggregate row found"
    )

  return fixed_row, internal_row, aggregate_row


def _test_text(
  fixed_row,
  internal_row,
  aggregate_row,
):
  lines = [
    "from proof import (",
    "  InferenceRule,",
    "  LiteratureReference,",
    "  ProofRule,",
    "  ProofStep,",
    ")",
    "from toda_group_proof_narrative_references import (",
    "  TodaGroupProofNarrativeReferenceEntry,",
    "  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,",
    "  restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage,",
    ")",
    "",
    "",
    "def _reference(",
    "  locator: str,",
    ") -> LiteratureReference:",
    "  return LiteratureReference(",
    '    label="Toda " + locator,',
    "    locator=locator,",
    "  )",
    "",
    "",
    "def _step(",
    "  rule_name: str,",
    "  locator: str | None,",
    "  conclusion: str,",
    "  premises=(),",
    ") -> ProofStep:",
    "  return ProofStep(",
    "    conclusion=conclusion,",
    "    premises=premises,",
    "    rule=ProofRule.INFERENCE,",
    "    inference_rule=InferenceRule(",
    "      name=rule_name,",
    "      literature_reference=(",
    "        None",
    "        if locator is None",
    "        else _reference(",
    "          locator",
    "        )",
    "      ),",
    "    ),",
    "  )",
    "",
    "",
    "def test_phase157_r5_r4_generic_filter_applies_without_representative_target_guard():",
    "  root_step = _step(",
    '    "Phase157 R5-R4 arbitrary root",',
    "    None,",
    '    "arbitrary non-representative target",',
    "  )",
    "",
    "  fixed_step = _step(",
    "    " + repr(fixed_row["selected_rule"]) + ",",
    "    " + repr(fixed_row["reference"]) + ",",
    '    "fixed candidate",',
    "  )",
    "  internal_step = _step(",
    "    " + repr(internal_row["selected_rule"]) + ",",
    "    " + repr(internal_row["reference"]) + ",",
    '    "proof-internal candidate",',
    "  )",
    "  aggregate_step = _step(",
    "    " + repr(aggregate_row["selected_rule"]) + ",",
    "    " + repr(aggregate_row["reference"]) + ",",
    '    "aggregate fixed statement without component",',
    "  )",
    "",
    "  fixed_entry = TodaGroupProofNarrativeReferenceEntry(",
    "    number=1,",
    "    reference=_reference(",
    "      " + repr(fixed_row["reference"]),
    "    ),",
    "    proof_steps=(",
    "      fixed_step,",
    "    ),",
    "  )",
    "  internal_entry = TodaGroupProofNarrativeReferenceEntry(",
    "    number=2,",
    "    reference=_reference(",
    "      " + repr(internal_row["reference"]),
    "    ),",
    "    proof_steps=(",
    "      internal_step,",
    "    ),",
    "  )",
    "  aggregate_entry = TodaGroupProofNarrativeReferenceEntry(",
    "    number=3,",
    "    reference=_reference(",
    "      " + repr(aggregate_row["reference"]),
    "    ),",
    "    proof_steps=(",
    "      aggregate_step,",
    "    ),",
    "  )",
    "",
    "  filtered = (",
    "    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(",
    "      (",
    "        fixed_entry,",
    "        internal_entry,",
    "        aggregate_entry,",
    "      ),",
    "      root_step,",
    "    )",
    "  )",
    "",
    "  assert len(",
    "    filtered",
    "  ) == 1",
    "  assert filtered[",
    "    0",
    "  ].number == 1",
    "  assert filtered[",
    "    0",
    "  ].proof_steps == (",
    "    fixed_step,",
    "  )",
    "",
    "",
    "def test_phase157_r5_r4_generic_restore_applies_without_representative_target_guard():",
    "  used_step = _step(",
    "    " + repr(fixed_row["selected_rule"]) + ",",
    "    " + repr(fixed_row["reference"]) + ",",
    '    "used fixed candidate",',
    "  )",
    "  retained_step = _step(",
    "    " + repr(fixed_row["selected_rule"]) + ",",
    "    " + repr(fixed_row["reference"]) + ",",
    '    "retained fixed candidate",',
    "  )",
    "  root_step = _step(",
    '    "Phase157 R5-R4 arbitrary root",',
    "    None,",
    '    "arbitrary non-representative target",',
    "    premises=(",
    "      used_step,",
    "      retained_step,",
    "    ),",
    "  )",
    "",
    "  used_entry = TodaGroupProofNarrativeReferenceEntry(",
    "    number=1,",
    "    reference=_reference(",
    "      " + repr(fixed_row["reference"]),
    "    ),",
    "    proof_steps=(",
    "      used_step,",
    "    ),",
    "  )",
    "  retained_entry = TodaGroupProofNarrativeReferenceEntry(",
    "    number=2,",
    "    reference=_reference(",
    "      " + repr(fixed_row["reference"]),
    "    ),",
    "    proof_steps=(",
    "      retained_step,",
    "    ),",
    "  )",
    "  filtered_retained_entry = TodaGroupProofNarrativeReferenceEntry(",
    "    number=1,",
    "    reference=retained_entry.reference,",
    "    proof_steps=retained_entry.proof_steps,",
    "  )",
    "",
    "  (",
    "    restored_entries,",
    "    restored_lines,",
    "    restored_body,",
    "  ) = (",
    "    restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(",
    "      (",
    "        used_entry,",
    "        retained_entry,",
    "      ),",
    "      {",
    "        1: (",
    '          "used fixed",',
    "        ),",
    "        2: (",
    '          "retained fixed",',
    "        ),",
    "      },",
    "      (",
    "        filtered_retained_entry,",
    "      ),",
    "      {",
    "        1: (",
    '          "retained fixed",',
    "        ),",
    "      },",
    '      "uses [R1]",',
    "      root_step,",
    "      frozenset(",
    "        {",
    "          id(",
    "            used_step",
    "          ),",
    "          id(",
    "            retained_step",
    "          ),",
    "        }",
    "      ),",
    "    )",
    "  )",
    "",
    "  assert len(",
    "    restored_entries",
    "  ) == 2",
    "  assert tuple(",
    "    entry.number",
    "    for entry in restored_entries",
    "  ) == (",
    "    1,",
    "    2,",
    "  )",
    "  assert restored_lines == {",
    "    1: (",
    '      "used fixed",',
    "    ),",
    "    2: (",
    '      "retained fixed",',
    "    ),",
    "  }",
    '  assert restored_body == "uses [R2]"',
  ]

  return "\n".join(lines) + "\n"


def main() -> None:
  rows = _read_rows()
  fixed_row, internal_row, aggregate_row = _pick_rows(rows)

  fixed_boundary = _classify_row(fixed_row)
  aggregate_boundary = _classify_row(aggregate_row)

  print("Classifier-verified test rows:")
  print("  fixed:")
  print("    locator=" + fixed_row["reference"])
  print("    rule=" + fixed_row["selected_rule"])
  print("    component=" + str(fixed_boundary.component_key))
  print("  internal:")
  print("    locator=" + internal_row["reference"])
  print("    rule=" + internal_row["selected_rule"])
  print("  aggregate:")
  print("    locator=" + aggregate_row["reference"])
  print("    rule=" + aggregate_row["selected_rule"])
  print("    component=" + str(aggregate_boundary.component_key))

  TEST.write_text(
    _test_text(
      fixed_row,
      internal_row,
      aggregate_row,
    ),
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R5-R4 repair2 applied.")
  print("Production code changes: none")
  print("updated: " + str(TEST.resolve()))


if __name__ == "__main__":
  main()
