from __future__ import annotations

import ast
import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()

REFERENCES = (
  ROOT
  / "toda_group_proof_narrative_references.py"
)
RENDERER = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair6_descendant_reference_usage.py"
)

RESTORE_FUNCTION = 'def restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(\n  original_entries: tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  original_statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n  filtered_entries: tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  filtered_statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n  body_markdown: str,\n  root_step: ProofStep,\n  used_step_ids: frozenset[\n    int\n  ],\n  presentation: TodaGroupProofPresentation | None = None,\n) -> tuple[\n  tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n  str,\n]:\n  if not isinstance(\n    original_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "original_entries must be a tuple"\n    )\n\n  if not isinstance(\n    original_statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "original_statement_lines_by_reference_number must be a dict"\n    )\n\n  if not isinstance(\n    filtered_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "filtered_entries must be a tuple"\n    )\n\n  if not isinstance(\n    filtered_statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "filtered_statement_lines_by_reference_number must be a dict"\n    )\n\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  if not isinstance(\n    root_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "root_step must be a ProofStep"\n    )\n\n  if not isinstance(\n    used_step_ids,\n    frozenset,\n  ):\n    raise TypeError(\n      "used_step_ids must be a frozenset"\n    )\n\n  if (\n    presentation is not None\n    and not isinstance(\n      presentation,\n      TodaGroupProofPresentation,\n    )\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation or None"\n    )\n\n  retained_reference_keys = {\n    (\n      entry.reference.locator,\n      entry.reference.label,\n      tuple(\n        id(\n          proof_step\n        )\n        for proof_step in entry.proof_steps\n      ),\n    )\n    for entry in filtered_entries\n  }\n\n  reference_internal_step_ids = {\n    id(\n      proof_step\n    )\n    for entry in original_entries\n    for proof_step in entry.proof_steps\n    if proof_step is not root_step\n  }\n\n  consumers_by_step_id = {}\n\n  if presentation is not None:\n    for edge in presentation.edges:\n      consumers_by_step_id.setdefault(\n        id(\n          edge.premise_step\n        ),\n        [],\n      ).append(\n        edge.parent_step\n      )\n\n  def has_used_external_descendant(\n    proof_step: ProofStep,\n  ) -> bool:\n    proof_step_id = id(\n      proof_step\n    )\n\n    if (\n      proof_step_id\n      in used_step_ids\n      and proof_step_id\n      not in reference_internal_step_ids\n    ):\n      return True\n\n    if presentation is None:\n      return (\n        proof_step_id\n        in used_step_ids\n      )\n\n    frontier = list(\n      consumers_by_step_id.get(\n        proof_step_id,\n        (),\n      )\n    )\n    seen_step_ids = {\n      proof_step_id\n    }\n\n    while frontier:\n      consumer = frontier.pop(\n        0\n      )\n      consumer_id = id(\n        consumer\n      )\n\n      if consumer_id in seen_step_ids:\n        continue\n\n      seen_step_ids.add(\n        consumer_id\n      )\n\n      if (\n        consumer is root_step\n        or (\n          consumer_id\n          in used_step_ids\n          and consumer_id\n          not in reference_internal_step_ids\n        )\n      ):\n        return True\n\n      frontier.extend(\n        consumers_by_step_id.get(\n          consumer_id,\n          (),\n        )\n      )\n\n    return False\n\n  desired_entries = []\n\n  for entry in original_entries:\n    has_selected_statement = (\n      entry.number\n      in original_statement_lines_by_reference_number\n      and bool(\n        original_statement_lines_by_reference_number[\n          entry.number\n        ]\n      )\n    )\n\n    is_used_fixed_reference = (\n      has_selected_statement\n      and any(\n        has_used_external_descendant(\n          proof_step\n        )\n        for proof_step in entry.proof_steps\n      )\n    )\n\n    entry_key = (\n      entry.reference.locator,\n      entry.reference.label,\n      tuple(\n        id(\n          proof_step\n        )\n        for proof_step in entry.proof_steps\n      ),\n    )\n\n    if (\n      entry_key\n      in retained_reference_keys\n      or is_used_fixed_reference\n    ):\n      desired_entries.append(\n        entry\n      )\n\n  if len(\n    desired_entries\n  ) == len(\n    filtered_entries\n  ):\n    return (\n      filtered_entries,\n      filtered_statement_lines_by_reference_number,\n      body_markdown,\n    )\n\n  number_map = {\n    entry.number: new_number\n    for new_number, entry in enumerate(\n      desired_entries,\n      start=1,\n    )\n  }\n\n  restored_entries = tuple(\n    replace(\n      entry,\n      number=number_map[\n        entry.number\n      ],\n    )\n    for entry in desired_entries\n  )\n\n  restored_statement_lines = {\n    number_map[\n      entry.number\n    ]: original_statement_lines_by_reference_number[\n      entry.number\n    ]\n    for entry in desired_entries\n    if (\n      entry.number\n      in original_statement_lines_by_reference_number\n    )\n  }\n\n  filtered_original_number_by_new_number = {}\n\n  for filtered_entry in filtered_entries:\n    filtered_key = (\n      filtered_entry.reference.locator,\n      filtered_entry.reference.label,\n      tuple(\n        id(\n          proof_step\n        )\n        for proof_step in filtered_entry.proof_steps\n      ),\n    )\n\n    matching_original_entry = next(\n      (\n        original_entry\n        for original_entry in original_entries\n        if (\n          (\n            original_entry.reference.locator,\n            original_entry.reference.label,\n            tuple(\n              id(\n                proof_step\n              )\n              for proof_step\n              in original_entry.proof_steps\n            ),\n          )\n          == filtered_key\n        )\n      ),\n      None,\n    )\n\n    if matching_original_entry is not None:\n      filtered_original_number_by_new_number[\n        filtered_entry.number\n      ] = matching_original_entry.number\n\n  marker_placeholders = {}\n\n  def placeholder_marker(\n    match,\n  ):\n    old_number = int(\n      match.group(\n        1\n      )\n    )\n    original_number = (\n      filtered_original_number_by_new_number.get(\n        old_number\n      )\n    )\n\n    if original_number is None:\n      return match.group(\n        0\n      )\n\n    new_number = number_map.get(\n      original_number\n    )\n\n    if new_number is None:\n      return match.group(\n        0\n      )\n\n    placeholder = (\n      "__PHASE157_R20_REFERENCE_"\n      + str(\n        len(\n          marker_placeholders\n        )\n      )\n      + "__"\n    )\n\n    marker_placeholders[\n      placeholder\n    ] = (\n      "[R"\n      + str(\n        new_number\n      )\n      + "]"\n    )\n\n    return placeholder\n\n  remapped_body = re.sub(\n    r"\\[R([0-9]+)\\]",\n    placeholder_marker,\n    body_markdown,\n  )\n\n  for placeholder, marker in marker_placeholders.items():\n    remapped_body = remapped_body.replace(\n      placeholder,\n      marker,\n    )\n\n  return (\n    restored_entries,\n    restored_statement_lines,\n    remapped_body,\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_r20_repair6() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair6_used_reference_ancestry_keeps_required_references():\n  rendered = _render_pi6_3_r20_repair6()\n\n  required = (\n    "Proposition 5.6",\n    "(5.3)",\n    "Proposition 5.3",\n    "Proposition 5.1",\n    "Proposition 2.2",\n  )\n\n  for locator in required:\n    assert locator in rendered\n\n\ndef test_phase157_r20_repair6_has_no_target_specific_reference_recovery():\n  from pathlib import Path\n\n  reference_source = Path(\n    "toda_group_proof_narrative_references.py"\n  ).read_text(\n    encoding="utf-8"\n  )\n  renderer_source = Path(\n    "toda_group_proof_narrative_contribution_renderer.py"\n  ).read_text(\n    encoding="utf-8"\n  )\n\n  forbidden = (\n    "_phase157_r19_",\n    "is_pi6_3",\n    "_phase157_r3_restore_pi6_3_",\n    "filter_phase157_r3_pi6_3_reference_entries",\n    "_phase157_r3_is_pi6_3_root",\n    "restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage",\n  )\n\n  for token in forbidden:\n    assert token not in reference_source\n    assert token not in renderer_source\n'


def function_range(
  source: str,
  name: str,
) -> tuple[
  int,
  int,
]:
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        (
          ast.FunctionDef,
          ast.AsyncFunctionDef,
        ),
      )
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(line)
        for line in lines[
          :node.end_lineno
        ]
      )

      while (
        end < len(source)
        and source[
          end:
          end + 1
        ] == "\n"
      ):
        end += 1

      return (
        start,
        end,
      )

  raise RuntimeError(
    "function not found: "
    + name
  )


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    name,
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def remove_redundant_post_restore_body_filter(
  source: str,
) -> str:
  restore_call = (
    "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage("
  )
  restore_index = source.find(
    restore_call
  )

  if restore_index < 0:
    raise RuntimeError(
      "restore call not found in renderer"
    )

  post_restore = source[
    restore_index:
  ]

  pattern = re.compile(
    r"""
  if "\[R" in rendered:
    \(
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    \) = \(
      filter_toda_group_proof_narrative_reference_entries_by_body_usage\(
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
      \)
    \)

""",
    flags=(
      re.DOTALL
      | re.VERBOSE
    ),
  )

  match = pattern.search(
    post_restore
  )

  if match is None:
    return source

  absolute_start = (
    restore_index
    + match.start()
  )
  absolute_end = (
    restore_index
    + match.end()
  )

  return (
    source[
      :absolute_start
    ]
    + source[
      absolute_end:
    ]
  )


def main() -> int:
  for path in (
    REFERENCES,
    RENDERER,
  ):
    if not path.is_file():
      raise RuntimeError(
        "missing file: "
        + str(
          path
        )
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair6_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    REFERENCES,
    RENDERER,
  ):
    shutil.copy2(
      path,
      backup / path.name,
    )

  reference_source = (
    REFERENCES.read_text(
      encoding="utf-8"
    )
  )
  renderer_source = (
    RENDERER.read_text(
      encoding="utf-8"
    )
  )

  reference_source = replace_function(
    reference_source,
    "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage",
    RESTORE_FUNCTION,
  )

  renderer_source = (
    remove_redundant_post_restore_body_filter(
      renderer_source
    )
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
    "filter_phase157_r3_pi6_3_reference_entries",
    "_phase157_r3_is_pi6_3_root",
    "restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage",
  )

  for token in forbidden:
    if (
      token in reference_source
      or token in renderer_source
    ):
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    reference_source,
    str(
      REFERENCES
    ),
    "exec",
  )
  compile(
    renderer_source,
    str(
      RENDERER
    ),
    "exec",
  )
  compile(
    TEST_SOURCE,
    str(
      TEST
    ),
    "exec",
  )

  REFERENCES.write_text(
    reference_source,
    encoding="utf-8",
    newline="\n",
  )
  RENDERER.write_text(
    renderer_source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair6 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed:"
  )
  print(
    " ",
    REFERENCES,
  )
  print(
    " ",
    RENDERER,
  )
  print(
    " ",
    TEST,
  )
  print("")
  print(
    "Architecture preflight:"
  )

  for token in forbidden:
    print(
      " ",
      token,
      "=",
      reference_source.count(
        token
      )
      + renderer_source.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
