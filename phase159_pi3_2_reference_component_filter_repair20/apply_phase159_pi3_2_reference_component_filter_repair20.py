from __future__ import annotations

import ast
import shutil
from pathlib import Path


REFERENCES = Path(
  "toda_group_proof_narrative_references.py"
)
CONTRIBUTION_RENDERER = Path(
  "toda_group_proof_narrative_contribution_renderer.py"
)
NARRATIVE_RENDERER = Path(
  "toda_group_proof_narrative_renderer.py"
)
TEST_FILE = Path(
  "tests/test_phase159_r1_6c_source_faithful_reference_linkage.py"
)
BACKUP_DIR = Path(
  "phase159_pi3_2_reference_component_filter_repair20_backup"
)


NEW_FIXED_BOUNDARY_FILTER = r'''def filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
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

      if not (
        component
        .range_is_explicit_in_current_aggregate
      ):
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
'''


NEW_CANONICAL_FIXED_REFERENCE_LINE = r'''def _phase157_r20_canonical_fixed_reference_line(
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
'''


NEW_TEST = r'''def test_phase159_r1_6c_toda_51_reference_is_source_faithful():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6c_pi3_2_presentation()
    )
  )
  reference = (
    rendered.split(
      "## 使用する結果\n\n",
      1,
    )[1].split(
      "\n---\n",
      1,
    )[0]
  )

  assert "**[R1] (5.1).**" in reference
  assert (
    r"$\pi_{i}^{1} = 0\ (i > 1)$."
    in reference
  )
  assert (
    r"$\pi_{n}^{n} = "
    r"\mathbb{Z}\{\iota_{n}\}$."
    in reference
  )

  assert (
    r"$\pi_{i}^{n} = 0\ (i < n)$."
    not in reference
  )
  assert r"\langle" not in reference
  assert r"\rangle" not in reference
  assert r"\pi_{2}^{1} = 0" not in reference
  assert r"\pi_{3}^{3}" not in reference
  assert (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$"
    not in reference
  )
'''


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


def unwrap_repair19_reference_postprocessor(
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
      "public narrative renderer not found"
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
      "public narrative final return not found"
    )

  call = final_return.value

  if not (
    isinstance(
      call,
      ast.Call,
    )
    and isinstance(
      call.func,
      ast.Name,
    )
    and call.func.id
    == "_phase159_r1_6c_canonicalize_toda_51_reference"
    and len(
      call.args
    ) == 1
    and not call.keywords
  ):
    return source

  inner = ast.get_source_segment(
    source,
    call.args[
      0
    ],
  )

  if inner is None:
    raise RuntimeError(
      "could not recover pre-repair19 return value"
    )

  newline = (
    "\r\n"
    if "\r\n" in source
    else "\n"
  )
  inner_lines = (
    inner.splitlines()
  )
  indented = newline.join(
    "    " + line
    for line in inner_lines
  )
  replacement = (
    "  return ("
    + newline
    + indented
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


def backup_file(
  path: Path,
) -> None:
  backup_path = (
    BACKUP_DIR
    / path
  )
  backup_path.parent.mkdir(
    parents=True,
    exist_ok=True,
  )

  if not backup_path.exists():
    shutil.copy2(
      path,
      backup_path,
    )


def main() -> None:
  for path in (
    REFERENCES,
    CONTRIBUTION_RENDERER,
    NARRATIVE_RENDERER,
    TEST_FILE,
  ):
    if not path.exists():
      raise FileNotFoundError(
        "Run from repository root; "
        "missing: "
        + str(
          path
        )
      )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  for path in (
    REFERENCES,
    CONTRIBUTION_RENDERER,
    NARRATIVE_RENDERER,
    TEST_FILE,
  ):
    backup_file(
      path
    )

  references_source = (
    REFERENCES.read_text(
      encoding="utf-8"
    )
  )
  contribution_source = (
    CONTRIBUTION_RENDERER.read_text(
      encoding="utf-8"
    )
  )
  renderer_source = (
    NARRATIVE_RENDERER.read_text(
      encoding="utf-8"
    )
  )
  test_source = (
    TEST_FILE.read_text(
      encoding="utf-8"
    )
  )

  references_updated = (
    replace_top_level_function(
      references_source,
      "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary",
      NEW_FIXED_BOUNDARY_FILTER,
    )
  )
  contribution_updated = (
    replace_top_level_function(
      contribution_source,
      "_phase157_r20_canonical_fixed_reference_line",
      NEW_CANONICAL_FIXED_REFERENCE_LINE,
    )
  )
  renderer_updated = (
    unwrap_repair19_reference_postprocessor(
      renderer_source
    )
  )
  test_updated = (
    replace_top_level_function(
      test_source,
      "test_phase159_r1_6c_toda_51_reference_is_source_faithful",
      NEW_TEST,
    )
  )

  for source in (
    references_updated,
    contribution_updated,
    renderer_updated,
    test_updated,
  ):
    ast.parse(
      source
    )

  REFERENCES.write_text(
    references_updated,
    encoding="utf-8",
  )
  CONTRIBUTION_RENDERER.write_text(
    contribution_updated,
    encoding="utf-8",
  )
  NARRATIVE_RENDERER.write_text(
    renderer_updated,
    encoding="utf-8",
  )
  TEST_FILE.write_text(
    test_updated,
    encoding="utf-8",
  )

  print(
    "Applied Phase 159 pi3_2 "
    "Reference component-filter repair20."
  )
  print(
    "Reference rendering now uses "
    "selected fixed-statement components."
  )
  print(
    "repair19 post-processing wrapper "
    "removed when present."
  )


if __name__ == "__main__":
  main()
