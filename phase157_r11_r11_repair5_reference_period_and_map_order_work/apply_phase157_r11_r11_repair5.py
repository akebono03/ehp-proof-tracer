from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair5"
BACKUP.mkdir(exist_ok=True)

CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R11_TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"


def backup(path: Path) -> None:
  destination = BACKUP / path.name

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


for path in (
  CONTRIBUTION,
  R11_TEST,
):
  backup(
    path
  )


def replace_once(
  path: Path,
  old: str,
  new: str,
  label: str,
) -> None:
  text = path.read_text(
    encoding="utf-8"
  )

  if new in text:
    print(
      f"Already applied: {label}"
    )
    return

  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"expected exactly one match for {label} "
      f"in {path}, found {count}"
    )

  path.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )

  print(
    f"Applied: {label}"
  )


def ensure_dependency_imports() -> None:
  text = CONTRIBUTION.read_text(
    encoding="utf-8"
  )

  import_block = '''from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)
'''

  if import_block in text:
    print(
      "Already applied: dependency role imports"
    )
    return

  anchor = '''from toda_literature_statement_boundary import (
'''

  if anchor not in text:
    raise RuntimeError(
      "could not locate contribution-renderer import anchor"
    )

  text = text.replace(
    anchor,
    import_block
    + anchor,
    1,
  )

  CONTRIBUTION.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "Applied: dependency role imports"
  )


ensure_dependency_imports()


old_reference_line_ending = '''    if index == len(
      ordered_steps
    ) - 1:
      lines.append(
        line
        + "."
      )
      continue

    lines.append(
      line
      + ","
    )
'''

new_reference_line_ending = '''    lines.append(
      line
      + "."
    )
'''

replace_once(
  CONTRIBUTION,
  old_reference_line_ending,
  new_reference_line_ending,
  "terminate every non-definition Reference statement with a period",
)


start_marker = (
  "def order_toda_group_proof_narrative_surjectivity_support(\n"
)
end_marker = (
  "\n\ndef insert_toda_group_proof_narrative_reference_map_values_before_surjectivity(\n"
)

text = CONTRIBUTION.read_text(
  encoding="utf-8"
)

start = text.find(
  start_marker
)
end = text.find(
  end_marker,
  start,
)

if (
  start < 0
  or end < 0
):
  raise RuntimeError(
    "could not locate surjectivity-support function"
  )

new_order_function = r'''def order_toda_group_proof_narrative_surjectivity_support(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    rendered_statement = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered_statement:
      return None

    target_key = (
      _phase157_r11_reference_statement_match_key(
        rendered_statement
      )
    )

    matching_indices = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if (
        _phase157_r11_reference_statement_match_key(
          paragraph
        )
        == target_key
      )
    )

    if len(
      matching_indices
    ) != 1:
      return None

    return matching_indices[
      0
    ]

  for node in presentation.nodes:
    map_step = node.proof_step

    if (
      classify_toda_proof_step_role(
        map_step
      )
      is not TodaProofDependencyRole.MAP_PROPERTY
    ):
      continue

    map_index = paragraph_index_for_step(
      map_step
    )

    if map_index is None:
      continue

    equality_premises = tuple(
      premise
      for premise in map_step.premises
      if (
        isinstance(
          premise.conclusion,
          Relation,
        )
        and premise.conclusion.relation_type
        is RelationType.EQUALITY
      )
    )

    if not equality_premises:
      continue

    support_steps = []

    for equality_premise in equality_premises:
      support_steps.extend(
        premise
        for premise in equality_premise.premises
        if (
          isinstance(
            premise.conclusion,
            Relation,
          )
          and premise.conclusion.relation_type
          is RelationType.EQUALITY
        )
      )
      support_steps.append(
        equality_premise
      )

    support_indices = tuple(
      index
      for proof_step in support_steps
      for index in (
        paragraph_index_for_step(
          proof_step
        ),
      )
      if index is not None
    )

    if not support_indices:
      continue

    first_support_index = min(
      support_indices
    )
    last_support_index = max(
      support_indices
    )

    if (
      first_support_index < map_index
      and last_support_index < map_index
    ):
      continue

    if (
      first_support_index
      <= map_index
      <= last_support_index
    ):
      continue

    support_block = paragraphs[
      first_support_index:
      last_support_index + 1
    ]

    del paragraphs[
      first_support_index:
      last_support_index + 1
    ]

    if first_support_index < map_index:
      map_index -= len(
        support_block
      )

    paragraphs[
      map_index:
      map_index
    ] = support_block

  for map_index, paragraph in enumerate(
    tuple(
      paragraphs
    )
  ):
    stripped = paragraph.strip()

    if (
      not stripped.startswith(
        "$H:"
      )
      or " は全射である." not in stripped
      or r"\to " not in stripped
    ):
      continue

    target_fragment = stripped.split(
      r"\to ",
      1,
    )[1].split(
      "$",
      1,
    )[0].strip()

    group_index = next(
      (
        index
        for index in range(
          map_index + 1,
          len(
            paragraphs
          ),
        )
        if paragraphs[
          index
        ].strip().startswith(
          "$"
          + target_fragment
          + " = "
        )
      ),
      None,
    )

    if group_index is None:
      continue

    group_paragraph = paragraphs.pop(
      group_index
    )
    paragraphs.insert(
      map_index,
      group_paragraph,
    )

  return "\n\n".join(
    paragraphs
  )
'''

text = (
  text[
    :start
  ]
  + new_order_function
  + text[
    end:
  ]
)

CONTRIBUTION.write_text(
  text,
  encoding="utf-8",
)

print(
  "Applied: graph-backed map-property equality support ordering"
)


old_call = '''  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      rendered
    )
  )
'''

new_call = '''  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
    )
  )
'''

replace_once(
  CONTRIBUTION,
  old_call,
  new_call,
  "pass presentation into map-property support ordering",
)


def update_tests() -> None:
  text = R11_TEST.read_text(
    encoding="utf-8"
  )

  test_name = (
    "def test_phase157_r11_r11_reference_non_definition_lines_end_with_period():"
  )

  if test_name not in text:
    new_test = r'''


def test_phase157_r11_r11_reference_non_definition_lines_end_with_period():
  reference, _ = _reference_and_body()

  assert (
    r"$\nu' \in \pi_{6}^{3}$."
    in reference
  )
  assert (
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = E^{2}\eta_{3}$."
    in reference
  )
'''
    text = (
      text.rstrip()
      + new_test
      + "\n"
    )

  R11_TEST.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "Updated: Reference period regression test"
  )


update_tests()

print("")
print("Phase157 R11-R11 repair5 applied successfully.")
