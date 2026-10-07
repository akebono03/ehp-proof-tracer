from __future__ import annotations

import ast
import shutil
from pathlib import Path


CONTRIBUTION = Path(
  "toda_group_proof_narrative_contribution_renderer.py"
)
BACKUP_DIR = Path(
  "phase159_pi3_2_reference_component_filter_repair20b_backup"
)


ORIGINAL_CANONICAL_HELPER = r"""def _phase157_r20_canonical_fixed_reference_line(
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(\alpha\circ E\beta)"
      r" = H(\alpha)\circ E\beta$."
    )

  return rendered_statement
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

  def reference_display_line(
    proof_step: ProofStep,
    rendered_statement: str,
  ) -> str:
    boundary = (
      classify_toda_literature_statement_step(
        proof_step
      )
    )

    if (
      boundary is not None
      and boundary.reference_locator
      == "(5.1)"
      and boundary.component_key
      == "circle_higher_homotopy_zero"
    ):
      return (
        r"$\pi_{i}^{1} = 0\ (i > 1)$."
      )

    if (
      boundary is not None
      and boundary.reference_locator
      == "(5.1)"
      and boundary.component_key
      == "sphere_connectivity_zero"
    ):
      return (
        r"$\pi_{i}^{n} = 0\ (i < n)$."
      )

    if (
      boundary is not None
      and boundary.reference_locator
      == "(5.1)"
      and boundary.component_key
      == "diagonal_identity_group"
    ):
      return (
        r"$\pi_{n}^{n} = "
        r"\mathbb{Z}\{\iota_{n}\}$."
      )

    return (
      _phase157_r20_canonical_fixed_reference_line(
        proof_step,
        rendered_statement,
      )
    )

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
        reference_display_line(
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
        reference_display_line(
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


def main() -> None:
  if not CONTRIBUTION.exists():
    raise FileNotFoundError(
      "Run this script from repository root; "
      "missing: "
      + str(
        CONTRIBUTION
      )
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  backup = (
    BACKUP_DIR
    / CONTRIBUTION.name
  )

  if not backup.exists():
    shutil.copy2(
      CONTRIBUTION,
      backup,
    )

  source = CONTRIBUTION.read_text(
    encoding="utf-8"
  )

  updated = replace_top_level_function(
    source,
    "_phase157_r20_canonical_fixed_reference_line",
    ORIGINAL_CANONICAL_HELPER,
  )
  updated = replace_top_level_function(
    updated,
    "_toda_group_proof_narrative_reference_statement_lines_by_number",
    NEW_STATEMENT_LINES,
  )

  ast.parse(
    updated
  )

  CONTRIBUTION.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Applied Phase 159 pi3_2 "
    "Reference component-filter repair20b."
  )
  print(
    "Shared canonical helper restored."
  )
  print(
    "Toda (5.1) generalization is now "
    "Reference-section-only."
  )


if __name__ == "__main__":
  main()
