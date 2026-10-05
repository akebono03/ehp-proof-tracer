from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MULTI = (
  ROOT
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)
NUMBERING = (
  ROOT
  / "toda_group_proof_narrative_equation_numbering.py"
)
RENDERER = (
  ROOT
  / "toda_group_proof_narrative_renderer.py"
)

OLD_BRANCH = '    if (\n      argument.conclusion_block.role\n      is TodaGroupProofNarrativeMathematicalBlockRole\n      .TARGET\n    ):\n      missing_evidence_blocks = tuple(\n        block\n        for block in blocks\n        if (\n          id(\n            block\n          ) in evidence_block_ids\n          and id(\n            block\n          ) not in local_body_block_ids\n        )\n      )\n\n      if missing_evidence_blocks:\n        conclusion_position = next(\n          (\n            index\n            for index, block in enumerate(\n              local_body_blocks\n            )\n            if block is argument.conclusion_block\n          ),\n          len(\n            local_body_blocks\n          ),\n        )\n        local_body_blocks = (\n          local_body_blocks[\n            :conclusion_position\n          ]\n          + missing_evidence_blocks\n          + local_body_blocks[\n            conclusion_position:\n          ]\n        )\n    else:\n      local_body_blocks = tuple(\n        block\n        for block in blocks\n        if (\n          id(\n            block\n          ) in local_body_block_ids\n          or id(\n            block\n          ) in evidence_block_ids\n        )\n      )\n'
NEW_BRANCH = '    missing_evidence_blocks = tuple(\n      block\n      for block in blocks\n      if (\n        id(\n          block\n        ) in evidence_block_ids\n        and id(\n          block\n        ) not in local_body_block_ids\n      )\n    )\n\n    if missing_evidence_blocks:\n      conclusion_position = next(\n        (\n          index\n          for index, block in enumerate(\n            local_body_blocks\n          )\n          if block is argument.conclusion_block\n        ),\n        len(\n          local_body_blocks\n        ),\n      )\n      local_body_blocks = (\n        local_body_blocks[\n          :conclusion_position\n        ]\n        + missing_evidence_blocks\n        + local_body_blocks[\n          conclusion_position:\n        ]\n      )\n'
NEW_NUMBERING = 'def number_toda_group_proof_narrative_equations(\n  markdown: str,\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n) -> str:\n  if not isinstance(markdown, str):\n    raise TypeError("markdown must be a string")\n\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(blocks, tuple):\n    raise TypeError("blocks must be a tuple")\n\n  transitions = (\n    extract_toda_group_proof_narrative_step_transitions(\n      presentation,\n      blocks,\n    )\n  )\n  sources_by_target = {}\n\n  for transition in transitions:\n    target_id = id(\n      transition.target_step\n    )\n    current = sources_by_target.get(\n      target_id,\n      (),\n    )\n\n    if any(\n      step is transition.source_step\n      for step in current\n    ):\n      continue\n\n    sources_by_target[\n      target_id\n    ] = (\n      *current,\n      transition.source_step,\n    )\n\n  step_by_id = {\n    id(\n      proof_step\n    ): proof_step\n    for block in blocks\n    for proof_step in block.steps\n  }\n  lines = markdown.splitlines()\n  plain_by_id = {\n    step_id: _render_generic_narrative_step(\n      proof_step\n    )\n    for step_id, proof_step in step_by_id.items()\n  }\n\n  reference_plans = []\n  line_index_by_id = {}\n\n  for target_id, source_steps in sources_by_target.items():\n    target_plain = plain_by_id.get(\n      target_id\n    )\n\n    if not target_plain:\n      continue\n\n    target_index = next(\n      (\n        index\n        for index, line in enumerate(\n          lines\n        )\n        if line == target_plain\n      ),\n      None,\n    )\n\n    if target_index is None:\n      continue\n\n    connector_index = next(\n      (\n        index\n        for index in range(\n          target_index - 1,\n          -1,\n          -1,\n        )\n        if lines[index] == "これらより, "\n      ),\n      None,\n    )\n\n    if connector_index is None:\n      continue\n\n    visible_source_ids = []\n\n    for source_step in source_steps:\n      source_id = id(\n        source_step\n      )\n      source_plain = plain_by_id.get(\n        source_id\n      )\n\n      if not source_plain:\n        continue\n\n      source_index = next(\n        (\n          index\n          for index in range(\n            connector_index - 1,\n            -1,\n            -1,\n          )\n          if lines[index] == source_plain\n        ),\n        None,\n      )\n\n      if source_index is None:\n        continue\n\n      visible_source_ids.append(\n        source_id\n      )\n      current_index = line_index_by_id.get(\n        source_id\n      )\n\n      if (\n        current_index is None\n        or source_index < current_index\n      ):\n        line_index_by_id[\n          source_id\n        ] = source_index\n\n    if not visible_source_ids:\n      continue\n\n    current_target_index = line_index_by_id.get(\n      target_id\n    )\n\n    if (\n      current_target_index is None\n      or target_index < current_target_index\n    ):\n      line_index_by_id[\n        target_id\n      ] = target_index\n\n    reference_plans.append(\n      (\n        connector_index,\n        tuple(\n          visible_source_ids\n        ),\n      )\n    )\n\n  ordered_step_ids = tuple(\n    step_id\n    for step_id, _line_index in sorted(\n      line_index_by_id.items(),\n      key=lambda item: item[1],\n    )\n  )\n  number_by_id = {\n    step_id: number\n    for number, step_id in enumerate(\n      ordered_step_ids,\n      start=1,\n    )\n  }\n\n  occupied_line_indices = set()\n\n  for step_id in ordered_step_ids:\n    line_index = line_index_by_id[\n      step_id\n    ]\n\n    if line_index in occupied_line_indices:\n      continue\n\n    proof_step = step_by_id.get(\n      step_id\n    )\n\n    if proof_step is None:\n      continue\n\n    tagged_line = _numbered_step_line(\n      proof_step,\n      number_by_id[\n        step_id\n      ],\n    )\n\n    if tagged_line == lines[\n      line_index\n    ]:\n      continue\n\n    lines[\n      line_index\n    ] = tagged_line\n    occupied_line_indices.add(\n      line_index\n    )\n\n  for connector_index, source_ids in reference_plans:\n    references = tuple(\n      toda_group_proof_narrative_equation_reference(\n        number_by_id[\n          source_id\n        ]\n      )\n      for source_id in source_ids\n      if (\n        source_id in number_by_id\n        and line_index_by_id[\n          source_id\n        ] < connector_index\n      )\n    )\n\n    if not references:\n      continue\n\n    if len(\n      references\n    ) == 1:\n      reference_text = references[\n        0\n      ]\n    else:\n      reference_text = (\n        ", ".join(\n          references[\n            :-1\n          ]\n        )\n        + " と "\n        + references[\n          -1\n        ]\n      )\n\n    lines[\n      connector_index\n    ] = (\n      reference_text\n      + " より, "\n    )\n\n  return "\\n".join(\n    lines\n  )\n'
NEW_PUBLIC_NUMBER_NORMALIZER = 'def _phase158_normalize_public_equation_numbers(\n  proof_body: list[\n    str\n  ],\n) -> list[\n  str\n]:\n  connector_numbers_by_index = {}\n  referenced_numbers = set()\n\n  for index, line in enumerate(\n    proof_body\n  ):\n    numbers = (\n      _phase158_public_equation_connector_numbers(\n        line\n      )\n    )\n\n    if numbers is None:\n      continue\n\n    connector_numbers_by_index[\n      index\n    ] = numbers\n    referenced_numbers.update(\n      numbers\n    )\n\n  derivation_target_numbers = set()\n\n  for connector_index in connector_numbers_by_index:\n    target_index = next(\n      (\n        index\n        for index in range(\n          connector_index + 1,\n          len(\n            proof_body\n          ),\n        )\n        if proof_body[\n          index\n        ].strip()\n      ),\n      None,\n    )\n\n    if target_index is None:\n      continue\n\n    target_number = (\n      _phase158_public_equation_tag_number(\n        proof_body[\n          target_index\n        ]\n      )\n    )\n\n    if target_number is not None:\n      derivation_target_numbers.add(\n        target_number\n      )\n\n  retained_numbers = (\n    referenced_numbers\n    | derivation_target_numbers\n  )\n  retained_old_numbers = []\n  seen_old_numbers = set()\n\n  for line in proof_body:\n    number = (\n      _phase158_public_equation_tag_number(\n        line\n      )\n    )\n\n    if (\n      number is None\n      or number not in retained_numbers\n      or number in seen_old_numbers\n    ):\n      continue\n\n    retained_old_numbers.append(\n      number\n    )\n    seen_old_numbers.add(\n      number\n    )\n\n  number_map = {\n    old_number: new_number\n    for new_number, old_number in enumerate(\n      retained_old_numbers,\n      start=1,\n    )\n  }\n\n  result = []\n  emitted_old_numbers = set()\n\n  for index, source_line in enumerate(\n    proof_body\n  ):\n    line = source_line\n    tag_number = (\n      _phase158_public_equation_tag_number(\n        line\n      )\n    )\n\n    if tag_number is not None:\n      old_marker = (\n        r"\\tag{"\n        + str(\n          tag_number\n        )\n        + "}"\n      )\n\n      if (\n        tag_number not in number_map\n        or tag_number in emitted_old_numbers\n      ):\n        line = line.replace(\n          old_marker,\n          "",\n          1,\n        )\n      else:\n        line = line.replace(\n          old_marker,\n          (\n            r"\\tag{"\n            + str(\n              number_map[\n                tag_number\n              ]\n            )\n            + "}"\n          ),\n          1,\n        )\n        emitted_old_numbers.add(\n          tag_number\n        )\n\n    connector_numbers = (\n      connector_numbers_by_index.get(\n        index\n      )\n    )\n\n    if connector_numbers is not None:\n      if all(\n        number in number_map\n        for number in connector_numbers\n      ):\n        line = (\n          _phase158_render_public_equation_connector(\n            tuple(\n              number_map[\n                number\n              ]\n              for number in connector_numbers\n            )\n          )\n        )\n      else:\n        line = (\n          "これより,"\n          if len(\n            connector_numbers\n          ) == 1\n          else "これらより,"\n        )\n\n    result.append(\n      line\n    )\n\n  return result\n'


def function_range(
  source: str,
  function_name: str,
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
        ast.FunctionDef,
      )
      and node.name == function_name
    ):
      start = sum(
        len(
          line
        )
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(
          line
        )
        for line in lines[
          :node.end_lineno
        ]
      )
      return (
        start,
        end,
      )

  raise RuntimeError(
    "function not found: "
    + function_name
  )


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    function_name,
  )
  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n\n"
    + source[
      end:
    ].lstrip(
      "\n"
    )
  )


def main() -> int:
  for path in (
    MULTI,
    NUMBERING,
    RENDERER,
  ):
    if not path.exists():
      raise RuntimeError(
        "missing expected file: "
        + str(
          path
        )
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase158_r5_5b_repair1v_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    MULTI,
    NUMBERING,
    RENDERER,
  ):
    shutil.copy2(
      path,
      backup_dir
      / path.name,
    )

  multi_source = MULTI.read_text(
    encoding="utf-8"
  )

  if OLD_BRANCH not in multi_source:
    raise RuntimeError(
      "expected Phase 158 TARGET-only local-body branch not found"
    )

  multi_updated = multi_source.replace(
    OLD_BRANCH,
    NEW_BRANCH,
    1,
  )
  ast.parse(
    multi_updated
  )
  MULTI.write_text(
    multi_updated,
    encoding="utf-8",
    newline="\n",
  )

  numbering_source = NUMBERING.read_text(
    encoding="utf-8"
  )
  numbering_updated = replace_function(
    numbering_source,
    "number_toda_group_proof_narrative_equations",
    NEW_NUMBERING,
  )
  ast.parse(
    numbering_updated
  )
  NUMBERING.write_text(
    numbering_updated,
    encoding="utf-8",
    newline="\n",
  )

  renderer_source = RENDERER.read_text(
    encoding="utf-8"
  )
  renderer_updated = replace_function(
    renderer_source,
    "_phase158_normalize_public_equation_numbers",
    NEW_PUBLIC_NUMBER_NORMALIZER,
  )
  ast.parse(
    renderer_updated
  )
  RENDERER.write_text(
    renderer_updated,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 158-R5-5b repair1v applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Changed: "
    + MULTI.name
  )
  print(
    "Changed: "
    + NUMBERING.name
  )
  print(
    "Changed: "
    + RENDERER.name
  )
  print(
    "Import changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
