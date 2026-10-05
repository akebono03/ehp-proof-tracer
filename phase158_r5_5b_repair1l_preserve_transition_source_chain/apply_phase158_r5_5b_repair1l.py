from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = (
  ROOT
  / "toda_group_proof_narrative_argument_body_renderer.py"
)

NEW_FUNCTION = 'def _relocatable_toda_group_proof_narrative_direct_derivation_premises(\n  direct_derivation_premises: tuple[\n    ProofStep,\n    ...,\n  ],\n  sources_by_target_id: dict[\n    int,\n    tuple[\n      ProofStep,\n      ...,\n    ],\n  ],\n  conclusion_block: TodaGroupProofNarrativeBlock,\n) -> tuple[\n  ProofStep,\n  ...,\n]:\n  transition_source_step_ids = frozenset(\n    id(\n      source_step\n    )\n    for source_steps in sources_by_target_id.values()\n    for source_step in source_steps\n  )\n\n  return tuple(\n    premise_step\n    for premise_step in direct_derivation_premises\n    if (\n      premise_step not in conclusion_block.steps\n      and id(\n        premise_step\n      ) not in transition_source_step_ids\n      and not sources_by_target_id.get(\n        id(\n          premise_step\n        ),\n        (),\n      )\n      and not (\n        is_toda_group_proof_narrative_provenance_only_statement(\n          premise_step.conclusion\n        )\n      )\n    )\n  )\n'


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
  if not TARGET.exists():
    raise RuntimeError(
      "missing expected file: "
      + str(
        TARGET
      )
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase158_r5_5b_repair1l_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup_dir
    / TARGET.name,
  )

  source = TARGET.read_text(
    encoding="utf-8"
  )
  start, end = function_range(
    source,
    "_relocatable_toda_group_proof_narrative_direct_derivation_premises",
  )
  current = source[
    start:end
  ].rstrip()

  if current == NEW_FUNCTION.rstrip():
    status = "already applied"
    updated = source
  else:
    updated = replace_function(
      source,
      "_relocatable_toda_group_proof_narrative_direct_derivation_premises",
      NEW_FUNCTION,
    )
    ast.parse(
      updated
    )
    TARGET.write_text(
      updated,
      encoding="utf-8",
      newline="\n",
    )
    status = "applied now"

  print(
    "Phase 158-R5-5b repair1l applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Transition-source relocation guard: "
    + status
  )
  print(
    "Import changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
