from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair6"
BACKUP.mkdir(exist_ok=True)

CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R5_R9_TEST = ROOT / "tests" / "test_phase157_r5_r9_fixed_definition_body_suppression.py"


def backup(path: Path) -> None:
  destination = BACKUP / path.name

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


for path in (
  CONTRIBUTION,
  R5_R9_TEST,
):
  backup(
    path
  )


def replace_function(
  path: Path,
  start_marker: str,
  end_marker: str,
  replacement: str,
  label: str,
) -> None:
  text = path.read_text(
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
      f"could not locate function boundaries for {label}"
    )

  path.write_text(
    text[:start]
    + replacement
    + text[end:],
    encoding="utf-8",
  )

  print(
    f"Applied: {label}"
  )


replacement_function = r'''def order_toda_group_proof_narrative_surjectivity_support(
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

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
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
      if paragraph_match_key(
        paragraph
      ) == target_key
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

    if len(
      support_indices
    ) != len(
      support_steps
    ):
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

replace_function(
  CONTRIBUTION,
  "def order_toda_group_proof_narrative_surjectivity_support(\n",
  "\n\ndef insert_toda_group_proof_narrative_reference_map_values_before_surjectivity(\n",
  replacement_function,
  "Reference-prefix-aware graph-backed map-property support ordering",
)


def update_historical_period_expectation() -> None:
  text = R5_R9_TEST.read_text(
    encoding="utf-8"
  )

  old = (
    '    r"$\\\\nu\\\' \\\\in \\\\pi_{6}^{3}$,"'
  )
  new = (
    '    r"$\\\\nu\\\' \\\\in \\\\pi_{6}^{3}$."'
  )

  if new in text:
    print(
      "Already applied: historical Reference period expectation"
    )
    return

  if old not in text:
    raise RuntimeError(
      "could not locate historical membership comma expectation"
    )

  R5_R9_TEST.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )

  print(
    "Updated: historical Reference membership expectation comma -> period"
  )


update_historical_period_expectation()

print("")
print("Phase157 R11-R11 repair6 applied successfully.")
