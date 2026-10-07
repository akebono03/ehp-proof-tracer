from __future__ import annotations

import ast
import shutil
from pathlib import Path


REFERENCES = Path(
  "toda_group_proof_narrative_references.py"
)
CONTRIBUTION = Path(
  "toda_group_proof_narrative_contribution_renderer.py"
)
BACKUP_DIR = Path(
  "phase159_pi3_2_reference_component_filter_repair20a_backup"
)


ORIGINAL_REFERENCE_FILTER = r"""def filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
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
      ):
        continue

      if boundary.component_key is None:
        fixed_components = (
          get_toda_fixed_statement_components(
            boundary.reference_locator
          )
        )

        if fixed_components:
          retained_steps.append(
            proof_step
          )

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

  retained_entries = sorted(
    retained_entries,
    key=lambda entry: (
      0
      if entry.reference.locator
      == "(5.1)"
      else 1
    ),
  )

  return tuple(
    replace(
      entry,
      number=number,
    )
    for number, entry in enumerate(
      retained_entries,
      start=1,
    )
  )
"""


NEW_STATEMENT_LINES = r"""def _toda_group_proof_narrative_reference_statement_lines_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    str,
    ...,
  ],
]:
  statement_lines_by_reference_number = {}

  for entry in reference_entries:
    candidate_steps = []
    rendered_by_step_id = {}
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is not None
        and boundary.classification
        is TodaLiteratureStatementClassification.FIXED_STATEMENT
        and boundary.component_key is not None
      ):
        component = (
          get_toda_fixed_statement_component(
            boundary.reference_locator,
            boundary.component_key,
          )
        )

        if not (
          component
          .range_is_explicit_in_current_aggregate
        ):
          continue

      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )
      rendered_statement = (
        _phase157_r20_canonical_fixed_reference_line(
          proof_step,
          rendered_statement,
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if (
        rendered_statement
        in seen_rendered_statements
      ):
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )
      rendered_by_step_id[
        id(
          proof_step
        )
      ] = rendered_statement

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    aggregate_specializations = tuple(
      (
        proof_step,
        _phase153_r6_reference_aggregate_component(
          presentation,
          entry,
          proof_step,
        ),
      )
      for proof_step in selected_steps
      if is_dataclass(
        proof_step.conclusion
      )
    )
    aggregate_specializations = tuple(
      pair
      for pair in aggregate_specializations
      if pair[
        1
      ] is not None
    )

    if len(
      aggregate_specializations
    ) == 1:
      selected_steps = (
        aggregate_specializations[
          0
        ][
          0
        ],
      )

    rendered_selected_by_step_id = {
      id(
        proof_step
      ): (
        _phase157_r20_canonical_fixed_reference_line(
          proof_step,
          _phase153_r6_render_reference_statement(
            presentation,
            entry,
            proof_step,
            rendered_by_step_id[
              id(
                proof_step
              )
            ],
          ),
        )
      )
      for proof_step in selected_steps
    }

    statement_lines = (
      _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines(
        selected_steps,
        rendered_selected_by_step_id,
      )
    )

    if statement_lines:
      statement_lines_by_reference_number[
        entry.number
      ] = statement_lines

  return statement_lines_by_reference_number
"""


def replace_top_level_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )
  target = next(
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

  if target is None:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  lines = source.splitlines(
    keepends=True
  )
  newline = (
    "\r\n"
    if "\r\n" in source
    else "\n"
  )

  return (
    "".join(
      lines[
        :target.lineno - 1
      ]
    )
    + replacement.strip(
      "\n"
    ).replace(
      "\n",
      newline,
    )
    + newline
    + "".join(
      lines[
        target.end_lineno:
      ]
    )
  )


def ensure_boundary_import(
  source: str,
) -> str:
  old = """from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)
"""
  new = """from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_component,
)
"""

  if new in source:
    return source

  if old not in source:
    raise RuntimeError(
      "expected literature boundary import "
      "block not found"
    )

  return source.replace(
    old,
    new,
    1,
  )


def backup(
  path: Path,
) -> None:
  destination = (
    BACKUP_DIR
    / path
  )
  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


def main() -> None:
  for path in (
    REFERENCES,
    CONTRIBUTION,
  ):
    if not path.exists():
      raise FileNotFoundError(
        "Run this script from repository root; "
        "missing: "
        + str(
          path
        )
      )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  backup(
    REFERENCES
  )
  backup(
    CONTRIBUTION
  )

  references_source = (
    REFERENCES.read_text(
      encoding="utf-8"
    )
  )
  contribution_source = (
    CONTRIBUTION.read_text(
      encoding="utf-8"
    )
  )

  references_updated = (
    replace_top_level_function(
      references_source,
      "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary",
      ORIGINAL_REFERENCE_FILTER,
    )
  )

  contribution_updated = (
    ensure_boundary_import(
      contribution_source
    )
  )
  contribution_updated = (
    replace_top_level_function(
      contribution_updated,
      "_toda_group_proof_narrative_reference_statement_lines_by_number",
      NEW_STATEMENT_LINES,
    )
  )

  ast.parse(
    references_updated
  )
  ast.parse(
    contribution_updated
  )

  REFERENCES.write_text(
    references_updated,
    encoding="utf-8",
  )
  CONTRIBUTION.write_text(
    contribution_updated,
    encoding="utf-8",
  )

  print(
    "Applied Phase 159 pi3_2 "
    "Reference component-filter repair20a."
  )
  print(
    "Reference entry proof_steps restored."
  )
  print(
    "Display-only component filtering moved "
    "to statement-line rendering."
  )


if __name__ == "__main__":
  main()
