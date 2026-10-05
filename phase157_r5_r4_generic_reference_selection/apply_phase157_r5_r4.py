
from __future__ import annotations

import csv
from pathlib import Path


REFERENCES = Path("toda_group_proof_narrative_references.py")
CONTRIBUTION = Path("toda_group_proof_narrative_contribution_renderer.py")
RENDERER = Path("toda_group_proof_narrative_renderer.py")
PLAN = Path("phase157_r5_r3_output") / "phase157_r5_r3_classification_plan.csv"
TEST = Path("tests/test_phase157_r5_r4_generic_reference_selection.py")
OUTPUT_DIR = Path("phase157_r5_r4_output")

GENERIC_FILTER_NAME = (
  "filter_toda_group_proof_narrative_reference_entries_"
  "by_fixed_statement_boundary"
)
R4_FILTER_NAME = (
  "filter_phase157_r4_representative_reference_entries_"
  "by_fixed_statement_boundary"
)
GENERIC_RESTORE_NAME = (
  "restore_toda_group_proof_narrative_fixed_reference_entries_"
  "after_body_usage"
)
R4_RESTORE_NAME = (
  "restore_phase157_r4_representative_fixed_reference_entries_"
  "after_body_usage"
)

GENERIC_FILTER_FUNCTION = r'''
def filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  root_step: ProofStep,
) -> tuple[
  TodaGroupProofNarrativeReferenceEntry,
  ...,
]:
  if not isinstance(
    entries,
    tuple,
  ):
    raise TypeError(
      "entries must be a tuple"
    )

  if not all(
    isinstance(
      entry,
      TodaGroupProofNarrativeReferenceEntry,
    )
    for entry in entries
  ):
    raise TypeError(
      "entries must contain only "
      "TodaGroupProofNarrativeReferenceEntry objects"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  root_boundary = (
    classify_toda_literature_statement_step(
      root_step
    )
  )

  target_reference_locator = (
    None
    if root_boundary is None
    else root_boundary.reference_locator
  )
  target_component_key = (
    None
    if root_boundary is None
    else root_boundary.component_key
  )

  retained_entries = []

  for entry in entries:
    retained_steps = []

    for proof_step in entry.proof_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is None
        or boundary.classification
        != TodaLiteratureStatementClassification.FIXED_STATEMENT
        or boundary.component_key is None
      ):
        continue

      component = (
        get_toda_fixed_statement_component(
          boundary.reference_locator,
          boundary.component_key,
        )
      )

      if component is None:
        continue

      if (
        target_reference_locator is not None
        and target_component_key is not None
        and not is_toda_fixed_statement_component_reference_eligible(
          component,
          target_reference_locator,
          target_component_key,
        )
      ):
        continue

      retained_steps.append(
        proof_step
      )

    if not retained_steps:
      continue

    retained_entries.append(
      replace(
        entry,
        number=len(
          retained_entries
        ) + 1,
        proof_steps=tuple(
          retained_steps
        ),
      )
    )

  return tuple(
    retained_entries
  )
'''

GENERIC_RESTORE_FUNCTION = r'''
def restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(
  original_entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  original_statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  filtered_entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  filtered_statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  body_markdown: str,
  root_step: ProofStep,
  used_step_ids: frozenset[
    int
  ],
) -> tuple[
  tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  str,
]:
  if not isinstance(
    original_entries,
    tuple,
  ):
    raise TypeError(
      "original_entries must be a tuple"
    )

  if not isinstance(
    original_statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "original_statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    filtered_entries,
    tuple,
  ):
    raise TypeError(
      "filtered_entries must be a tuple"
    )

  if not isinstance(
    filtered_statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "filtered_statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  if not isinstance(
    used_step_ids,
    frozenset,
  ):
    raise TypeError(
      "used_step_ids must be a frozenset"
    )

  retained_reference_keys = {
    (
      entry.reference.locator,
      entry.reference.label,
      tuple(
        id(
          proof_step
        )
        for proof_step in entry.proof_steps
      ),
    )
    for entry in filtered_entries
  }

  desired_entries = []

  for entry in original_entries:
    has_selected_statement = (
      entry.number
      in original_statement_lines_by_reference_number
      and bool(
        original_statement_lines_by_reference_number[
          entry.number
        ]
      )
    )
    is_used_fixed_reference = (
      has_selected_statement
      and any(
        id(
          proof_step
        )
        in used_step_ids
        for proof_step in entry.proof_steps
      )
    )

    entry_key = (
      entry.reference.locator,
      entry.reference.label,
      tuple(
        id(
          proof_step
        )
        for proof_step in entry.proof_steps
      ),
    )

    if (
      entry_key
      in retained_reference_keys
      or is_used_fixed_reference
    ):
      desired_entries.append(
        entry
      )

  if len(
    desired_entries
  ) == len(
    filtered_entries
  ):
    return (
      filtered_entries,
      filtered_statement_lines_by_reference_number,
      body_markdown,
    )

  number_map = {
    entry.number: new_number
    for new_number, entry in enumerate(
      desired_entries,
      start=1,
    )
  }

  restored_entries = tuple(
    replace(
      entry,
      number=number_map[
        entry.number
      ],
    )
    for entry in desired_entries
  )

  restored_statement_lines = {
    number_map[
      entry.number
    ]: original_statement_lines_by_reference_number[
      entry.number
    ]
    for entry in desired_entries
    if (
      entry.number
      in original_statement_lines_by_reference_number
    )
  }

  filtered_original_number_by_new_number = {}

  for filtered_entry in filtered_entries:
    filtered_key = (
      filtered_entry.reference.locator,
      filtered_entry.reference.label,
      tuple(
        id(
          proof_step
        )
        for proof_step in filtered_entry.proof_steps
      ),
    )

    matching_original_entry = next(
      (
        original_entry
        for original_entry in original_entries
        if (
          (
            original_entry.reference.locator,
            original_entry.reference.label,
            tuple(
              id(
                proof_step
              )
              for proof_step
              in original_entry.proof_steps
            ),
          )
          == filtered_key
        )
      ),
      None,
    )

    if matching_original_entry is not None:
      filtered_original_number_by_new_number[
        filtered_entry.number
      ] = matching_original_entry.number

  marker_placeholders = {}

  def placeholder_marker(
    match,
  ):
    old_number = int(
      match.group(
        1
      )
    )
    original_number = (
      filtered_original_number_by_new_number.get(
        old_number
      )
    )

    if original_number is None:
      return match.group(
        0
      )

    new_number = number_map.get(
      original_number
    )

    if new_number is None:
      return match.group(
        0
      )

    placeholder = (
      "__PHASE157_R5_R4_REFERENCE_"
      + str(
        len(
          marker_placeholders
        )
      )
      + "__"
    )
    marker_placeholders[
      placeholder
    ] = (
      "[R"
      + str(
        new_number
      )
      + "]"
    )
    return placeholder

  remapped_body = re.sub(
    r"\[R([0-9]+)\]",
    placeholder_marker,
    body_markdown,
  )

  for placeholder, marker in marker_placeholders.items():
    remapped_body = remapped_body.replace(
      placeholder,
      marker,
    )

  return (
    restored_entries,
    restored_statement_lines,
    remapped_body,
  )
'''


def _insert_before_function(
  text: str,
  function_name: str,
  insertion: str,
) -> str:
  marker = "\ndef " + function_name + "(\n"
  index = text.find(
    marker
  )

  if index < 0:
    raise SystemExit(
      "function insertion anchor not found: "
      + function_name
    )

  return (
    text[:index]
    + "\n"
    + insertion.strip()
    + "\n"
    + text[index:]
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


def _pick_test_rows(
  rows,
):
  fixed_row = next(
    (
      row
      for row in rows
      if (
        row[
          "r5_r3_classification"
        ]
        == "FIXED_STATEMENT"
        and row[
          "r5_r3_component_key"
        ]
      )
    ),
    None,
  )

  internal_row = next(
    (
      row
      for row in rows
      if row[
        "r5_r3_classification"
      ] == "PROOF_INTERNAL"
    ),
    None,
  )

  aggregate_row = next(
    (
      row
      for row in rows
      if row[
        "boundary_status"
      ] == "FIXED_STATEMENT_WITHOUT_COMPONENT"
    ),
    None,
  )

  if (
    fixed_row is None
    or internal_row is None
    or aggregate_row is None
  ):
    raise SystemExit(
      "R5-R3 plan lacks fixed/internal/aggregate test rows"
    )

  return (
    fixed_row,
    internal_row,
    aggregate_row,
  )


def _test_text(
  fixed_row,
  internal_row,
  aggregate_row,
):
  template = '''from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage,
)


def _reference(
  locator: str,
) -> LiteratureReference:
  return LiteratureReference(
    label="Toda " + locator,
    locator=locator,
  )


def _step(
  rule_name: str,
  locator: str | None,
  conclusion: str,
  premises=(),
) -> ProofStep:
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=rule_name,
      literature_reference=(
        None
        if locator is None
        else _reference(
          locator
        )
      ),
    ),
  )


def test_phase157_r5_r4_generic_filter_applies_without_representative_target_guard():
  root_step = _step(
    "Phase157 R5-R4 arbitrary root",
    None,
    "arbitrary non-representative target",
  )

  fixed_step = _step(
    __FIXED_RULE__,
    __FIXED_LOCATOR__,
    "fixed candidate",
  )
  internal_step = _step(
    __INTERNAL_RULE__,
    __INTERNAL_LOCATOR__,
    "proof-internal candidate",
  )
  aggregate_step = _step(
    __AGGREGATE_RULE__,
    __AGGREGATE_LOCATOR__,
    "aggregate fixed statement without component",
  )

  fixed_entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=_reference(
      __FIXED_LOCATOR__
    ),
    proof_steps=(
      fixed_step,
    ),
  )
  internal_entry = TodaGroupProofNarrativeReferenceEntry(
    number=2,
    reference=_reference(
      __INTERNAL_LOCATOR__
    ),
    proof_steps=(
      internal_step,
    ),
  )
  aggregate_entry = TodaGroupProofNarrativeReferenceEntry(
    number=3,
    reference=_reference(
      __AGGREGATE_LOCATOR__
    ),
    proof_steps=(
      aggregate_step,
    ),
  )

  filtered = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      (
        fixed_entry,
        internal_entry,
        aggregate_entry,
      ),
      root_step,
    )
  )

  assert len(
    filtered
  ) == 1
  assert filtered[
    0
  ].number == 1
  assert filtered[
    0
  ].proof_steps == (
    fixed_step,
  )


def test_phase157_r5_r4_generic_restore_applies_without_representative_target_guard():
  used_step = _step(
    __FIXED_RULE__,
    __FIXED_LOCATOR__,
    "used fixed candidate",
  )
  retained_step = _step(
    __FIXED_RULE__,
    __FIXED_LOCATOR__,
    "retained fixed candidate",
  )
  root_step = _step(
    "Phase157 R5-R4 arbitrary root",
    None,
    "arbitrary non-representative target",
    premises=(
      used_step,
      retained_step,
    ),
  )

  used_entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=_reference(
      __FIXED_LOCATOR__
    ),
    proof_steps=(
      used_step,
    ),
  )
  retained_entry = TodaGroupProofNarrativeReferenceEntry(
    number=2,
    reference=_reference(
      __FIXED_LOCATOR__
    ),
    proof_steps=(
      retained_step,
    ),
  )
  filtered_retained_entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=retained_entry.reference,
    proof_steps=retained_entry.proof_steps,
  )

  (
    restored_entries,
    restored_lines,
    restored_body,
  ) = (
    restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(
      (
        used_entry,
        retained_entry,
      ),
      {
        1: (
          "used fixed",
        ),
        2: (
          "retained fixed",
        ),
      },
      (
        filtered_retained_entry,
      ),
      {
        1: (
          "retained fixed",
        ),
      },
      "uses [R1]",
      root_step,
      frozenset(
        {
          id(
            used_step
          ),
          id(
            retained_step
          ),
        }
      ),
    )
  )

  assert len(
    restored_entries
  ) == 2
  assert tuple(
    entry.number
    for entry in restored_entries
  ) == (
    1,
    2,
  )
  assert restored_lines == {
    1: (
      "used fixed",
    ),
    2: (
      "retained fixed",
    ),
  }
  assert restored_body == "uses [R2]"
'''

  replacements = {
    "__FIXED_RULE__": repr(
      fixed_row[
        "selected_rule"
      ]
    ),
    "__FIXED_LOCATOR__": repr(
      fixed_row[
        "reference"
      ]
    ),
    "__INTERNAL_RULE__": repr(
      internal_row[
        "selected_rule"
      ]
    ),
    "__INTERNAL_LOCATOR__": repr(
      internal_row[
        "reference"
      ]
    ),
    "__AGGREGATE_RULE__": repr(
      aggregate_row[
        "selected_rule"
      ]
    ),
    "__AGGREGATE_LOCATOR__": repr(
      aggregate_row[
        "reference"
      ]
    ),
  }

  for old, new in replacements.items():
    template = template.replace(
      old,
      new,
    )

  return template


def _replace_import_and_calls(
  text: str,
  old_name: str,
  new_name: str,
) -> str:
  if old_name not in text:
    raise SystemExit(
      "expected existing helper name not found: "
      + old_name
    )

  return text.replace(
    old_name,
    new_name,
  )


def _extract_import_block(
  text: str,
  module_name: str,
) -> str:
  marker = (
    "from "
    + module_name
    + " import (\n"
  )
  start = text.find(
    marker
  )

  if start < 0:
    return ""

  end = text.find(
    ")\n",
    start,
  )

  if end < 0:
    return ""

  return text[
    start:
    end + 2
  ]


def main():
  for path in (
    REFERENCES,
    CONTRIBUTION,
    RENDERER,
  ):
    if not path.exists():
      raise SystemExit(
        "target not found: "
        + str(
          path
        )
      )

  plan_rows = _read_plan()
  (
    fixed_row,
    internal_row,
    aggregate_row,
  ) = _pick_test_rows(
    plan_rows
  )

  references_text = REFERENCES.read_text(
    encoding="utf-8"
  )

  generic_filter_signature = (
    "def "
    + GENERIC_FILTER_NAME
    + "(\n"
  )
  if generic_filter_signature not in references_text:
    references_text = _insert_before_function(
      references_text,
      R4_FILTER_NAME,
      GENERIC_FILTER_FUNCTION,
    )

  generic_restore_signature = (
    "def "
    + GENERIC_RESTORE_NAME
    + "(\n"
  )
  if generic_restore_signature not in references_text:
    references_text = _insert_before_function(
      references_text,
      R4_RESTORE_NAME,
      GENERIC_RESTORE_FUNCTION,
    )

  REFERENCES.write_text(
    references_text,
    encoding="utf-8",
    newline="\n",
  )

  contribution_text = CONTRIBUTION.read_text(
    encoding="utf-8"
  )
  contribution_text = _replace_import_and_calls(
    contribution_text,
    R4_FILTER_NAME,
    GENERIC_FILTER_NAME,
  )
  contribution_text = _replace_import_and_calls(
    contribution_text,
    R4_RESTORE_NAME,
    GENERIC_RESTORE_NAME,
  )
  CONTRIBUTION.write_text(
    contribution_text,
    encoding="utf-8",
    newline="\n",
  )

  renderer_text = RENDERER.read_text(
    encoding="utf-8"
  )
  renderer_text = _replace_import_and_calls(
    renderer_text,
    R4_FILTER_NAME,
    GENERIC_FILTER_NAME,
  )
  RENDERER.write_text(
    renderer_text,
    encoding="utf-8",
    newline="\n",
  )

  TEST.write_text(
    _test_text(
      fixed_row,
      internal_row,
      aggregate_row,
    ),
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    OUTPUT_DIR
    / "contribution_reference_import_after.txt"
  ).write_text(
    _extract_import_block(
      contribution_text,
      "toda_group_proof_narrative_references",
    ),
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "renderer_reference_import_after.txt"
  ).write_text(
    _extract_import_block(
      renderer_text,
      "toda_group_proof_narrative_references",
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R4 generic Reference selection applied."
  )
  print(
    "updated: "
    + str(
      REFERENCES.resolve()
    )
  )
  print(
    "updated: "
    + str(
      CONTRIBUTION.resolve()
    )
  )
  print(
    "updated: "
    + str(
      RENDERER.resolve()
    )
  )
  print(
    "added: "
    + str(
      TEST.resolve()
    )
  )
  print(
    "R4 representative helpers remain available for compatibility."
  )
  print(
    "Generic renderer/contribution paths now use the generic helpers."
  )


if __name__ == "__main__":
  main()
