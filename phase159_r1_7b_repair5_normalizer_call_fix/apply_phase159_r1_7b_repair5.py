from __future__ import annotations

import ast
from pathlib import Path
import shutil


ROOT = Path.cwd()
RENDERER = (
  ROOT
  / "toda_group_proof_narrative_renderer.py"
)
BACKUP_DIR = (
  ROOT
  / "phase159_r1_7b_repair5_backup_before_apply"
)


def _is_named_call(
  node,
  function_name: str,
) -> bool:
  return (
    isinstance(
      node,
      ast.Call,
    )
    and isinstance(
      node.func,
      ast.Name,
    )
    and node.func.id
    == function_name
  )


def _function_def(
  tree: ast.Module,
  function_name: str,
) -> ast.FunctionDef | None:
  return next(
    (
      node
      for node in tree.body
      if (
        isinstance(
          node,
          ast.FunctionDef,
        )
        and node.name
        == function_name
      )
    ),
    None,
  )


def _assignment_calls(
  assignment: ast.Assign,
  function_name: str,
) -> bool:
  return (
    len(
      assignment.targets
    )
    == 1
    and isinstance(
      assignment.targets[
        0
      ],
      ast.Name,
    )
    and assignment.targets[
      0
    ].id
    == "proof_body"
    and _is_named_call(
      assignment.value,
      function_name,
    )
  )


def _contract_already_calls_normalizer(
  contract_function: ast.FunctionDef,
) -> bool:
  return any(
    (
      isinstance(
        node,
        ast.Assign,
      )
      and _assignment_calls(
        node,
        "_phase159_r1_7b_normalize_public_exact_sequences",
      )
    )
    for node in contract_function.body
  )


def insert_normalizer_call(
  source: str,
) -> str:
  tree = ast.parse(
    source
  )

  helper_function = _function_def(
    tree,
    "_phase159_r1_7b_normalize_public_exact_sequences",
  )

  if helper_function is None:
    raise RuntimeError(
      "R1-7b normalizer helper definition is missing; "
      "repair3 must have been applied first"
    )

  contract_function = _function_def(
    tree,
    "_phase158_normalize_public_narrative_contract",
  )

  if contract_function is None:
    raise RuntimeError(
      "public narrative contract function not found"
    )

  if _contract_already_calls_normalizer(
    contract_function
  ):
    print(
      "R1-7b normalizer call already present; "
      "no production edit needed."
    )
    return source

  equation_assignment = next(
    (
      node
      for node in contract_function.body
      if (
        isinstance(
          node,
          ast.Assign,
        )
        and _assignment_calls(
          node,
          "_phase158_normalize_public_equation_numbers",
        )
      )
    ),
    None,
  )

  if equation_assignment is None:
    raise RuntimeError(
      "proof_body equation-number normalization "
      "assignment not found in public contract"
    )

  if equation_assignment.end_lineno is None:
    raise RuntimeError(
      "equation-number normalization assignment "
      "has no end line"
    )

  lines = source.splitlines(
    keepends=True
  )
  insert_index = (
    equation_assignment.end_lineno
  )

  insertion = (
    "  proof_body = (\n"
    "    _phase159_r1_7b_normalize_public_exact_sequences(\n"
    "      presentation,\n"
    "      proof_body,\n"
    "    )\n"
    "  )\n"
  )

  lines.insert(
    insert_index,
    insertion,
  )

  updated = "".join(
    lines
  )

  verification_tree = ast.parse(
    updated
  )
  verification_contract = _function_def(
    verification_tree,
    "_phase158_normalize_public_narrative_contract",
  )

  if (
    verification_contract is None
    or not _contract_already_calls_normalizer(
      verification_contract
    )
  ):
    raise RuntimeError(
      "failed to insert R1-7b normalizer call"
    )

  return updated


def main() -> int:
  if not RENDERER.exists():
    raise RuntimeError(
      f"missing renderer: {RENDERER}"
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    RENDERER,
    BACKUP_DIR
    / RENDERER.name,
  )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )
  updated = insert_normalizer_call(
    source
  )

  RENDERER.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Phase 159-R1-7b repair5 applied."
  )
  print(
    "Production file: "
    "toda_group_proof_narrative_renderer.py"
  )
  print(
    "Change: call existing R1-7b normalizer "
    "from public Narrative contract."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
