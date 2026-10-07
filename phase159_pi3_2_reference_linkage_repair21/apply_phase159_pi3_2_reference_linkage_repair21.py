from __future__ import annotations

import ast
import shutil
from pathlib import Path


CONTRIBUTION = Path(
  "toda_group_proof_narrative_contribution_renderer.py"
)
REFERENCES = Path(
  "toda_group_proof_narrative_references.py"
)
RENDERER = Path(
  "toda_group_proof_narrative_renderer.py"
)
LOCALITY_TEST = Path(
  "tests/test_phase159_pi3_2_public_definition_premise_locality.py"
)
BACKUP_DIR = Path(
  "phase159_pi3_2_reference_linkage_repair21_backup"
)


SPECIALIZED_STATEMENT_LINES = r"""def _toda_group_proof_narrative_reference_statement_lines_by_number(
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


REFERENCE_RENDERER = r"""def render_toda_group_proof_narrative_reference_entries_markdown(
  entries: tuple[TodaGroupProofNarrativeReferenceEntry, ...],
  statement_lines_by_reference_number: (
    dict[
      int,
      tuple[
        str,
        ...,
      ],
    ]
    | None
  ) = None,
) -> str:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")

  if (
    statement_lines_by_reference_number is not None
    and not isinstance(
      statement_lines_by_reference_number,
      dict,
    )
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be "
      "a dict or None"
    )

  if statement_lines_by_reference_number is not None:
    for reference_number, statement_lines in (
      statement_lines_by_reference_number.items()
    ):
      if (
        isinstance(
          reference_number,
          bool,
        )
        or not isinstance(
          reference_number,
          int,
        )
      ):
        raise TypeError(
          "statement_lines_by_reference_number keys "
          "must be integers"
        )

      if not isinstance(
        statement_lines,
        tuple,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must be tuples"
        )

      if not all(
        isinstance(
          line,
          str,
        )
        for line in statement_lines
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

  if not entries:
    return ""

  lines = []

  for entry in entries:
    if not isinstance(entry, TodaGroupProofNarrativeReferenceEntry):
      raise TypeError(
        "entries must contain only "
        "TodaGroupProofNarrativeReferenceEntry objects"
      )

    title = entry.reference.locator or entry.reference.label
    lines.append(f"**[R{entry.number}] {title}.**")

    if entry.reference.locator == "(5.1)":
      component_keys = {
        boundary.component_key
        for proof_step in entry.proof_steps
        for boundary in (
          classify_toda_literature_statement_step(
            proof_step
          ),
        )
        if (
          boundary is not None
          and boundary.classification
          == TodaLiteratureStatementClassification.FIXED_STATEMENT
          and boundary.reference_locator
          == "(5.1)"
          and boundary.component_key is not None
        )
      }

      if "circle_higher_homotopy_zero" in component_keys:
        lines.append(
          r"$\pi_{i}^{1} = 0\ (i > 1)$."
        )

      if "sphere_connectivity_zero" in component_keys:
        component = (
          get_toda_fixed_statement_component(
            "(5.1)",
            "sphere_connectivity_zero",
          )
        )

        if (
          component is not None
          and component
          .range_is_explicit_in_current_aggregate
        ):
          lines.append(
            r"$\pi_{i}^{n} = 0\ (i < n)$."
          )

      if "diagonal_identity_group" in component_keys:
        lines.append(
          (
            r"$\pi_{n}^{n} = "
            r"\mathbb{Z}\{\iota_{n}\}$."
          )
        )

      continue

    statement_lines = (
      ()
      if statement_lines_by_reference_number is None
      else statement_lines_by_reference_number.get(
        entry.number,
        (),
      )
    )

    for statement_line in statement_lines:
      lines.append(
        statement_line
      )

  return "\n".join(lines)
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


def wrap_public_renderer_return(
  source: str,
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
        == "render_toda_group_proof_narrative_markdown"
      )
    ),
    None,
  )

  if target is None:
    raise RuntimeError(
      "public renderer not found"
    )

  final_return = next(
    (
      node
      for node in reversed(
        target.body
      )
      if isinstance(
        node,
        ast.Return,
      )
    ),
    None,
  )

  if final_return is None:
    raise RuntimeError(
      "public renderer final return not found"
    )

  segment = ast.get_source_segment(
    source,
    final_return.value,
  )

  if segment is None:
    raise RuntimeError(
      "could not read final return expression"
    )

  if (
    "_phase159_r1_6d_finalize_reference_and_linkage"
    in segment
  ):
    return source

  newline = (
    "\r\n"
    if "\r\n" in source
    else "\n"
  )

  inner_lines = segment.splitlines()
  inner = newline.join(
    "      " + line
    for line in inner_lines
  )
  replacement = (
    "  return ("
    + newline
    + "    _phase159_r1_6d_finalize_reference_and_linkage("
    + newline
    + "      presentation,"
    + newline
    + inner
    + ","
    + newline
    + "    )"
    + newline
    + "  )"
  )

  lines = source.splitlines(
    keepends=True
  )

  return (
    "".join(
      lines[
        :final_return.lineno - 1
      ]
    )
    + replacement
    + newline
    + "".join(
      lines[
        final_return.end_lineno:
      ]
    )
  )


def normalize_locality_test_spacing(
  source: str,
) -> str:
  return source.replace(
    "[R1]より, ",
    "[R1] より, ",
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
    CONTRIBUTION,
    REFERENCES,
    RENDERER,
    LOCALITY_TEST,
  ):
    if not path.exists():
      raise FileNotFoundError(
        "Run from repository root; missing: "
        + str(
          path
        )
      )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  for path in (
    CONTRIBUTION,
    REFERENCES,
    RENDERER,
    LOCALITY_TEST,
  ):
    backup(
      path
    )

  contribution_source = (
    CONTRIBUTION.read_text(
      encoding="utf-8"
    )
  )
  references_source = (
    REFERENCES.read_text(
      encoding="utf-8"
    )
  )
  renderer_source = (
    RENDERER.read_text(
      encoding="utf-8"
    )
  )
  test_source = (
    LOCALITY_TEST.read_text(
      encoding="utf-8"
    )
  )

  contribution_updated = (
    replace_top_level_function(
      contribution_source,
      "_toda_group_proof_narrative_reference_statement_lines_by_number",
      SPECIALIZED_STATEMENT_LINES,
    )
  )
  references_updated = (
    replace_top_level_function(
      references_source,
      "render_toda_group_proof_narrative_reference_entries_markdown",
      REFERENCE_RENDERER,
    )
  )
  renderer_updated = (
    wrap_public_renderer_return(
      renderer_source
    )
  )
  test_updated = (
    normalize_locality_test_spacing(
      test_source
    )
  )

  for source in (
    contribution_updated,
    references_updated,
    renderer_updated,
    test_updated,
  ):
    ast.parse(
      source
    )

  CONTRIBUTION.write_text(
    contribution_updated,
    encoding="utf-8",
  )
  REFERENCES.write_text(
    references_updated,
    encoding="utf-8",
  )
  RENDERER.write_text(
    renderer_updated,
    encoding="utf-8",
  )
  LOCALITY_TEST.write_text(
    test_updated,
    encoding="utf-8",
  )

  print(
    "Applied Phase 159 pi3_2 reference-linkage repair21."
  )
  print(
    "Linkage statement lines restored to specialized form."
  )
  print(
    "Toda (5.1) generalization moved to Reference rendering only."
  )
  print(
    "Existing R1-6d finalization reconnected to public renderer."
  )


if __name__ == "__main__":
  main()
