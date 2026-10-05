
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair2"
BACKUP.mkdir(exist_ok=True)

CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST_PATH = ROOT / "tests" / "test_phase157_r11_r17_residual_narrative_defects.py"


def backup(
  path: Path,
) -> None:
  destination = BACKUP / path.name

  if path.exists() and not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


for path in (
  CONTRIBUTION,
  TEST_PATH,
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

  if start < 0 or end < 0:
    raise RuntimeError(
      f"could not locate {label}"
    )

  current = text[
    start:end
  ]

  if current == replacement:
    print(
      f"Already applied: {label}"
    )
    return

  path.write_text(
    text[
      :start
    ]
    + replacement
    + text[
      end:
    ],
    encoding="utf-8",
  )

  print(
    f"Applied: {label}"
  )


link_function = r'''def link_toda_group_proof_narrative_unmarked_reference_consumers(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  paragraphs = body_markdown.split(
    "\n\n"
  )
  consumers_by_step_id = {}

  for edge in presentation.edges:
    consumers_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  for entry in reference_entries:
    marker = (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )

    if marker in "\n\n".join(
      paragraphs
    ):
      continue

    visible_non_root_consumers = []
    visible_root_consumers = []

    for proof_step in entry.proof_steps:
      for consumer in consumers_by_step_id.get(
        id(
          proof_step
        ),
        (),
      ):
        rendered_consumer = (
          _render_generic_narrative_step(
            consumer
          )
        )

        if not rendered_consumer:
          continue

        matching_indices = tuple(
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if rendered_consumer in paragraph
        )

        if len(
          matching_indices
        ) != 1:
          continue

        consumer_index = matching_indices[
          0
        ]

        if consumer is presentation.root_step:
          visible_root_consumers.append(
            (
              id(
                consumer
              ),
              consumer_index,
            )
          )
          continue

        consumer_reference = (
          extract_toda_group_proof_step_literature_reference(
            consumer
          )
        )

        if consumer_reference is not None:
          continue

        visible_non_root_consumers.append(
          (
            id(
              consumer
            ),
            consumer_index,
          )
        )

    non_root_candidates = tuple(
      dict.fromkeys(
        visible_non_root_consumers
      )
    )
    root_candidates = tuple(
      dict.fromkeys(
        visible_root_consumers
      )
    )

    if len(
      non_root_candidates
    ) == 1:
      _, consumer_index = non_root_candidates[
        0
      ]
    elif (
      not non_root_candidates
      and len(
        root_candidates
      ) == 1
    ):
      _, consumer_index = root_candidates[
        0
      ]
    else:
      continue

    paragraph = paragraphs[
      consumer_index
    ]

    if marker in paragraph:
      continue

    paragraphs[
      consumer_index
    ] = (
      marker
      + "を用いて, "
      + paragraph
    )

  return "\n\n".join(
    paragraphs
  )


'''

replace_function(
  CONTRIBUTION,
  "def link_toda_group_proof_narrative_unmarked_reference_consumers(\n",
  "\n\ndef normalize_toda_group_proof_narrative_display_math_periods(\n",
  link_function,
  "ownership-aware unmarked Reference linkage",
)


text = CONTRIBUTION.read_text(
  encoding="utf-8"
)

old_tail = '''  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    _phase157_r3_restore_pi6_3_earlier_prop56_reference(
      presentation,
      phase157_r3_entries_before_usage_filter,
      phase157_r3_lines_before_usage_filter,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  reference_section = (
'''

new_tail = '''  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    _phase157_r3_restore_pi6_3_earlier_prop56_reference(
      presentation,
      phase157_r3_entries_before_usage_filter,
      phase157_r3_lines_before_usage_filter,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  if "[R" in rendered:
    (
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_body_usage(
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
      )
    )

  reference_section = (
'''

if new_tail not in text:
  count = text.count(
    old_tail
  )

  if count != 1:
    raise RuntimeError(
      "could not locate final ancestry-pruning filter anchor"
    )

  CONTRIBUTION.write_text(
    text.replace(
      old_tail,
      new_tail,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Applied: final body-usage filter after fixed Reference restoration"
  )
else:
  print(
    "Already applied: final body-usage filter after fixed Reference restoration"
  )


print("")
print("Phase157 R11-R17 repair2 applied successfully.")
