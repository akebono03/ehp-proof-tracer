
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair1"
BACKUP.mkdir(exist_ok=True)

CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
NARRATIVE = ROOT / "toda_group_proof_narrative_renderer.py"
PHASE156_TEST = ROOT / "tests" / "test_phase156_r6_canonical_connector_local_ordering.py"


def backup(
  path: Path,
) -> None:
  destination = BACKUP / path.name

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


for path in (
  CONTRIBUTION,
  NARRATIVE,
  PHASE156_TEST,
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


hidden_zero_function = r'''def insert_toda_group_proof_narrative_hidden_zero_map_premises(
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

  def visible_paragraph_index(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    target_key = (
      _phase157_r11_reference_statement_match_key(
        rendered
      )
    )

    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      ) == target_key
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  insertions = []

  for node in presentation.nodes:
    consumer_step = node.proof_step
    consumer_index = visible_paragraph_index(
      consumer_step
    )

    if consumer_index is None:
      continue

    for premise in consumer_step.premises:
      rendered_premise = (
        _render_generic_narrative_step(
          premise
        )
      )

      if (
        not rendered_premise
        or "零写像である."
        not in rendered_premise
        or visible_paragraph_index(
          premise
        )
        is not None
      ):
        continue

      insertion_index = consumer_index

      if (
        insertion_index > 0
        and (
          "零写像"
          in paragraphs[
            insertion_index - 1
          ]
          or "Δ=0"
          in paragraphs[
            insertion_index - 1
          ]
          or r"\Delta=0"
          in paragraphs[
            insertion_index - 1
          ]
        )
      ):
        insertion_index -= 1

      insertions.append(
        (
          insertion_index,
          rendered_premise,
        )
      )

  seen_lines = set()

  for insertion_index, rendered_premise in sorted(
    insertions,
    reverse=True,
  ):
    if rendered_premise in seen_lines:
      continue

    if any(
      paragraph_match_key(
        paragraph
      )
      == _phase157_r11_reference_statement_match_key(
        rendered_premise
      )
      for paragraph in paragraphs
    ):
      continue

    paragraphs.insert(
      insertion_index,
      rendered_premise,
    )
    seen_lines.add(
      rendered_premise
    )

  return "\n\n".join(
    paragraphs
  )
'''

replace_function(
  CONTRIBUTION,
  "def insert_toda_group_proof_narrative_hidden_zero_map_premises(\n",
  "\n\ndef trim_toda_group_proof_narrative_redundant_left_ehp_terms(\n",
  hidden_zero_function,
  "hidden zero-map premise visibility",
)


text = CONTRIBUTION.read_text(
  encoding="utf-8"
)

old_before_used_ids = '''  rendered = (
    normalize_toda_group_proof_narrative_repeated_numeric_equalities(
      rendered
    )
  )

  generic_used_step_ids = (
'''

new_before_used_ids = '''  rendered = (
    normalize_toda_group_proof_narrative_repeated_numeric_equalities(
      rendered
    )
  )
  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

  generic_used_step_ids = (
'''

if new_before_used_ids not in text:
  count = text.count(
    old_before_used_ids
  )

  if count != 1:
    raise RuntimeError(
      "could not locate early Reference linkage insertion point"
    )

  CONTRIBUTION.write_text(
    text.replace(
      old_before_used_ids,
      new_before_used_ids,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Applied: move unmarked Reference linkage before usage filter"
  )
else:
  print(
    "Already applied: early unmarked Reference linkage"
  )


text = CONTRIBUTION.read_text(
  encoding="utf-8"
)

late_block = '''  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
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

'''

if late_block in text:
  first_index = text.find(
    late_block
  )
  early_anchor_index = text.find(
    "generic_used_step_ids = ("
  )

  if (
    first_index >= 0
    and first_index > early_anchor_index
  ):
    CONTRIBUTION.write_text(
      text[
        :first_index
      ]
      + text[
        first_index
        + len(
          late_block
        ):
      ],
      encoding="utf-8",
    )
    print(
      "Applied: remove late Reference linkage/filter"
    )
else:
  print(
    "Already applied: late Reference linkage/filter absent"
  )


public_helpers = r'''def _phase157_r11_r17_normalize_public_connectors(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  paragraphs = rendered.split(
    "\n\n"
  )
  connectors = {
    "以上より,",
    "したがって,",
    "これより,",
  }
  index = 0

  while index < len(
    paragraphs
  ) - 1:
    stripped = paragraphs[
      index
    ].strip()

    if stripped not in connectors:
      index += 1
      continue

    next_paragraph = paragraphs[
      index + 1
    ]
    separator = (
      "\n"
      if next_paragraph.lstrip().startswith(
        r"\["
      )
      else " "
    )

    paragraphs[
      index:
      index + 2
    ] = [
      stripped
      + separator
      + next_paragraph,
    ]

  return "\n\n".join(
    paragraphs
  )


def _phase157_r11_r17_normalize_public_numeric_equalities(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  characters = []
  index = 0

  while index < len(
    rendered
  ):
    if rendered[
      index
    ] != "=":
      characters.append(
        rendered[
          index
        ]
      )
      index += 1
      continue

    first_number_start = index + 1

    while (
      first_number_start < len(
        rendered
      )
      and rendered[
        first_number_start
      ].isspace()
    ):
      first_number_start += 1

    first_number_end = first_number_start

    while (
      first_number_end < len(
        rendered
      )
      and rendered[
        first_number_end
      ].isdigit()
    ):
      first_number_end += 1

    if first_number_end == first_number_start:
      characters.append(
        rendered[
          index
        ]
      )
      index += 1
      continue

    second_equals_index = first_number_end

    while (
      second_equals_index < len(
        rendered
      )
      and rendered[
        second_equals_index
      ].isspace()
    ):
      second_equals_index += 1

    if (
      second_equals_index >= len(
        rendered
      )
      or rendered[
        second_equals_index
      ] != "="
    ):
      characters.append(
        rendered[
          index
        ]
      )
      index += 1
      continue

    second_number_start = second_equals_index + 1

    while (
      second_number_start < len(
        rendered
      )
      and rendered[
        second_number_start
      ].isspace()
    ):
      second_number_start += 1

    second_number_end = second_number_start

    while (
      second_number_end < len(
        rendered
      )
      and rendered[
        second_number_end
      ].isdigit()
    ):
      second_number_end += 1

    first_number = rendered[
      first_number_start:
      first_number_end
    ]
    second_number = rendered[
      second_number_start:
      second_number_end
    ]

    if (
      not second_number
      or first_number != second_number
    ):
      characters.append(
        rendered[
          index
        ]
      )
      index += 1
      continue

    characters.append(
      rendered[
        index:
        first_number_end
      ]
    )
    index = second_number_end

  return "".join(
    characters
  )


'''

narrative_text = NARRATIVE.read_text(
  encoding="utf-8"
)

finalizer_anchor = (
  "def _finalize_toda_group_proof_narrative_markdown(\n"
)

if (
  "def _phase157_r11_r17_normalize_public_connectors("
  not in narrative_text
):
  if finalizer_anchor not in narrative_text:
    raise RuntimeError(
      "could not locate public finalizer insertion point"
    )

  NARRATIVE.write_text(
    narrative_text.replace(
      finalizer_anchor,
      public_helpers
      + finalizer_anchor,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Applied: public-route residual normalization helpers"
  )
else:
  print(
    "Already applied: public-route residual normalization helpers"
  )


finalizer_replacement = r'''def _finalize_toda_group_proof_narrative_markdown(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  rendered = (
    _phase157_r11_r17_normalize_public_connectors(
      rendered
    )
  )
  rendered = (
    _phase157_r11_r17_normalize_public_numeric_equalities(
      rendered
    )
  )
  lines = rendered.rstrip().splitlines()

  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  if (
    reference_header in lines
    and proof_header in lines
  ):
    reference_index = lines.index(
      reference_header
    )
    proof_index = lines.index(
      proof_header
    )

    if reference_index < proof_index:
      before_proof = lines[
        :proof_index
      ]
      proof_and_after = lines[
        proof_index:
      ]

      while (
        before_proof
        and not before_proof[-1].strip()
      ):
        before_proof.pop()

      if (
        before_proof
        and before_proof[-1].strip()
        == "---"
      ):
        before_proof.pop()

        while (
          before_proof
          and not before_proof[-1].strip()
        ):
          before_proof.pop()

      lines = [
        *before_proof,
        "",
        "---",
        "",
        *proof_and_after,
      ]

  while (
    lines
    and not lines[-1].strip()
  ):
    lines.pop()

  if (
    not lines
    or lines[-1].strip()
    != r"$\square$"
  ):
    lines.extend(
      (
        "",
        r"$\square$",
      )
    )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )
'''

replace_function(
  NARRATIVE,
  "def _finalize_toda_group_proof_narrative_markdown(\n",
  "\n\ndef _is_phase150_rc4_generic_route_target(\n",
  finalizer_replacement,
  "public Narrative finalizer",
)


phase156_text = PHASE156_TEST.read_text(
  encoding="utf-8"
)

old_test = r'''def test_phase156_r6_pi6_places_equation3_before_order_and_group_transport():
  rendered = _render_pi6_3()

  equation_two = (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
  )
  connector = "(1) と (2) より,"
  equation_three = (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
  )
  eta_cube_order = (
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
  )
  transported_group = (
    r"$\pi_{5}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$"
  )

  assert (
    rendered.index(
      equation_two
    )
    < rendered.index(
      connector
    )
    < rendered.index(
      equation_three
    )
    < rendered.index(
      eta_cube_order
    )
    < rendered.index(
      transported_group
    )
  )


'''

new_test = r'''def test_phase156_r6_pi6_places_equation3_before_transport_and_order():
  rendered = _render_pi6_3()

  equation_two = (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
  )
  connector = "(1) と (2) より,"
  equation_three = (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
  )
  transported_group_body = (
    "[R1]より, "
    r"$\pi_{5}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$."
  )
  injectivity = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
  )
  eta_cube_order = (
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
  )

  assert (
    rendered.index(
      equation_two
    )
    < rendered.index(
      connector
    )
    < rendered.index(
      equation_three
    )
    < rendered.index(
      transported_group_body
    )
    < rendered.index(
      injectivity
    )
    < rendered.index(
      eta_cube_order
    )
  )


'''

if new_test not in phase156_text:
  if old_test not in phase156_text:
    raise RuntimeError(
      "could not locate stale Phase156 ordering test"
    )

  PHASE156_TEST.write_text(
    phase156_text.replace(
      old_test,
      new_test,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Updated: stale Phase156 pi6 ordering expectation"
  )
else:
  print(
    "Already applied: Phase156 ordering expectation update"
  )


print("")
print("Phase157 R11-R17 repair1 applied successfully.")
