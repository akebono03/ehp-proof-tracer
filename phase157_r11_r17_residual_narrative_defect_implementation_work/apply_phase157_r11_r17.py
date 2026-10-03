
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_r11_r17"
BACKUP.mkdir(exist_ok=True)

CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST_PATH = ROOT / "tests" / "test_phase157_r11_r17_residual_narrative_defects.py"


def backup(
  path: Path,
) -> None:
  if not path.exists():
    return

  destination = BACKUP / path.name

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


backup(
  CONTRIBUTION
)
backup(
  TEST_PATH
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


normalize_function = r'''def normalize_toda_group_proof_narrative_connectors(
  markdown: str,
) -> str:
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
  retained = []

  for index, paragraph in enumerate(
    paragraphs
  ):
    stripped = paragraph.strip()

    if (
      stripped == "以上より,"
      and index + 1 < len(
        paragraphs
      )
      and paragraphs[
        index + 1
      ].strip().startswith(
        "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"
      )
    ):
      continue

    retained.append(
      paragraph
    )

  normalized_paragraphs = retained
  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
  }
  index = 0

  while index < len(
    normalized_paragraphs
  ) - 1:
    stripped = normalized_paragraphs[
      index
    ].strip()

    if stripped not in standalone_connectors:
      index += 1
      continue

    next_paragraph = normalized_paragraphs[
      index + 1
    ]
    next_stripped = next_paragraph.lstrip()
    separator = (
      "\n"
      if next_stripped.startswith(
        r"\["
      )
      else " "
    )

    normalized_paragraphs[
      index:
      index + 2
    ] = [
      stripped
      + separator
      + next_paragraph,
    ]

  for index, paragraph in enumerate(
    normalized_paragraphs
  ):
    stripped = paragraph.strip()

    if not stripped:
      continue

    if stripped.startswith(
      "次に, "
    ):
      normalized_paragraphs[
        index
      ] = paragraph.replace(
        "次に, ",
        "まず, ",
        1,
      )

    break

  return "\n\n".join(
    normalized_paragraphs
  )
'''

replace_function(
  CONTRIBUTION,
  "def normalize_toda_group_proof_narrative_connectors(\n",
  "\n\ndef _toda_group_proof_narrative_equation_tag_number(\n",
  normalize_function,
  "connector normalization",
)


new_helpers = r'''def insert_toda_group_proof_narrative_hidden_zero_map_premises(
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

  def visible_paragraph_index(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = _render_generic_narrative_step(
      proof_step
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
      if (
        _phase157_r11_reference_statement_match_key(
          paragraph.strip()
        )
        == target_key
      )
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
    map_step = node.proof_step

    if (
      classify_toda_proof_step_role(
        map_step
      )
      is not TodaProofDependencyRole.MAP_PROPERTY
    ):
      continue

    consumer_index = visible_paragraph_index(
      map_step
    )

    if consumer_index is None:
      continue

    for premise in map_step.premises:
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
        and "より"
        in paragraphs[
          insertion_index - 1
        ]
      ):
        insertion_index -= 1

      insertions.append(
        (
          insertion_index,
          rendered_premise,
        )
      )

  for insertion_index, rendered_premise in sorted(
    insertions,
    reverse=True,
  ):
    if rendered_premise in paragraphs:
      continue

    paragraphs.insert(
      insertion_index,
      rendered_premise,
    )

  return "\n\n".join(
    paragraphs
  )


def trim_toda_group_proof_narrative_redundant_left_ehp_terms(
  markdown: str,
) -> str:
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
  injective_maps = []

  for index, paragraph in enumerate(
    paragraphs
  ):
    stripped = paragraph.strip()

    if (
      not stripped.startswith(
        "$E: "
      )
      or "$ は単射である."
      not in stripped
      or r" \to "
      not in stripped
    ):
      continue

    map_expression = stripped[
      len(
        "$E: "
      ):
      stripped.find(
        "$ は単射である."
      )
    ]
    pieces = map_expression.split(
      r" \to ",
      1,
    )

    if len(
      pieces
    ) != 2:
      continue

    injective_maps.append(
      (
        index,
        pieces[
          0
        ],
        pieces[
          1
        ],
      )
    )

  delta_arrow = r"\xrightarrow{\Delta} "

  for index, paragraph in enumerate(
    tuple(
      paragraphs
    )
  ):
    stripped = paragraph.strip()

    if (
      delta_arrow not in stripped
      or r"\xrightarrow{E}" not in stripped
      or r"\xrightarrow{H}" not in stripped
    ):
      continue

    matching_injective = next(
      (
        (
          injective_index,
          domain,
          codomain,
        )
        for (
          injective_index,
          domain,
          codomain,
        ) in injective_maps
        if (
          injective_index < index
          and (
            domain
            + r" \xrightarrow{E} "
            + codomain
          )
          in stripped
        )
      ),
      None,
    )

    if matching_injective is None:
      continue

    _, tail = stripped.split(
      delta_arrow,
      1,
    )
    paragraphs[
      index
    ] = (
      "$"
      + tail
    )

  return "\n\n".join(
    paragraphs
  )


def normalize_toda_group_proof_narrative_repeated_numeric_equalities(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  characters = []
  index = 0

  while index < len(
    markdown
  ):
    if markdown[
      index
    ] != "=":
      characters.append(
        markdown[
          index
        ]
      )
      index += 1
      continue

    first_equals_index = index
    first_number_start = (
      first_equals_index + 1
    )

    while (
      first_number_start < len(
        markdown
      )
      and markdown[
        first_number_start
      ].isspace()
    ):
      first_number_start += 1

    first_number_end = first_number_start

    while (
      first_number_end < len(
        markdown
      )
      and markdown[
        first_number_end
      ].isdigit()
    ):
      first_number_end += 1

    if first_number_end == first_number_start:
      characters.append(
        markdown[
          index
        ]
      )
      index += 1
      continue

    second_equals_index = first_number_end

    while (
      second_equals_index < len(
        markdown
      )
      and markdown[
        second_equals_index
      ].isspace()
    ):
      second_equals_index += 1

    if (
      second_equals_index >= len(
        markdown
      )
      or markdown[
        second_equals_index
      ] != "="
    ):
      characters.append(
        markdown[
          index
        ]
      )
      index += 1
      continue

    second_number_start = (
      second_equals_index + 1
    )

    while (
      second_number_start < len(
        markdown
      )
      and markdown[
        second_number_start
      ].isspace()
    ):
      second_number_start += 1

    second_number_end = second_number_start

    while (
      second_number_end < len(
        markdown
      )
      and markdown[
        second_number_end
      ].isdigit()
    ):
      second_number_end += 1

    first_number = markdown[
      first_number_start:
      first_number_end
    ]
    second_number = markdown[
      second_number_start:
      second_number_end
    ]

    if (
      not second_number
      or first_number != second_number
    ):
      characters.append(
        markdown[
          index
        ]
      )
      index += 1
      continue

    characters.append(
      markdown[
        first_equals_index:
        first_number_end
      ]
    )
    index = second_number_end

  return "".join(
    characters
  )


def link_toda_group_proof_narrative_unmarked_reference_consumers(
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

    candidate_consumers = []

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
          if (
            rendered_consumer
            in paragraph
          )
        )

        if len(
          matching_indices
        ) != 1:
          continue

        candidate_consumers.append(
          (
            id(
              consumer
            ),
            matching_indices[
              0
            ],
          )
        )

    unique_candidates = tuple(
      dict.fromkeys(
        candidate_consumers
      )
    )

    if len(
      unique_candidates
    ) != 1:
      continue

    _, consumer_index = unique_candidates[
      0
    ]
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

text = CONTRIBUTION.read_text(
    encoding="utf-8"
)

helper_anchor = (
  "def normalize_toda_group_proof_narrative_display_math_periods(\n"
)

if (
  "def insert_toda_group_proof_narrative_hidden_zero_map_premises("
  not in text
):
  if helper_anchor not in text:
    raise RuntimeError(
      "could not locate R11-R17 helper insertion point"
    )

  CONTRIBUTION.write_text(
    text.replace(
      helper_anchor,
      new_helpers
      + helper_anchor,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Applied: R11-R17 residual Narrative helper functions"
  )
else:
  print(
    "Already applied: R11-R17 residual Narrative helper functions"
  )


text = CONTRIBUTION.read_text(
    encoding="utf-8"
)

old_pipeline = '''  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
    )
  )

  generic_used_step_ids = (
'''

new_pipeline = '''  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
    )
  )
  rendered = (
    insert_toda_group_proof_narrative_hidden_zero_map_premises(
      presentation,
      rendered,
    )
  )
  rendered = (
    trim_toda_group_proof_narrative_redundant_left_ehp_terms(
      rendered
    )
  )
  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      rendered
    )
  )
  rendered = (
    normalize_toda_group_proof_narrative_repeated_numeric_equalities(
      rendered
    )
  )

  generic_used_step_ids = (
'''

if new_pipeline not in text:
  count = text.count(
    old_pipeline
  )

  if count != 1:
    raise RuntimeError(
      "could not locate R11-R17 body-finalization pipeline anchor"
    )

  CONTRIBUTION.write_text(
    text.replace(
      old_pipeline,
      new_pipeline,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Applied: R11-R17 body-finalization pipeline"
  )
else:
  print(
    "Already applied: R11-R17 body-finalization pipeline"
  )


text = CONTRIBUTION.read_text(
    encoding="utf-8"
)

old_final_reference = '''  (
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

new_final_reference = '''  (
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

  rendered = (
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

  reference_section = (
'''

if new_final_reference not in text:
  count = text.count(
    old_final_reference
  )

  if count != 1:
    raise RuntimeError(
      "could not locate R11-R17 final Reference linkage anchor"
    )

  CONTRIBUTION.write_text(
    text.replace(
      old_final_reference,
      new_final_reference,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Applied: R11-R17 final Reference linkage/filter"
  )
else:
  print(
    "Already applied: R11-R17 final Reference linkage/filter"
  )


test_content = r'''import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGETS = (
  (3, 3),
  (4, 6),
  (5, 3),
  (5, 7),
  (8, 7),
  (9, 7),
)

REFERENCE_HEADER_RE = re.compile(
  r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*"
)
REFERENCE_MARKER_RE = re.compile(
  r"\[R([0-9]+)\]"
)


def _render(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _reference_and_body(
  n: int,
  k: int,
) -> tuple[
  str,
  str,
]:
  rendered = _render(
    n,
    k,
  )

  return tuple(
    rendered.split(
      "\n## 証明\n",
      1,
    )
  )


def test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use():
  _, body = _reference_and_body(
    3,
    3,
  )

  zero_map = (
    r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ "
    "は零写像である."
  )
  use = (
    "この完全性と $Δ=0$ より, "
    r"$\ker E=\operatorname{Im}Δ=0$ である."
  )

  assert zero_map in body
  assert use in body
  assert body.index(
    zero_map
  ) < body.index(
    use
  )


def test_phase157_r11_r17_pi6_3_keeps_first_delta_sequence_but_trims_second():
  _, body = _reference_and_body(
    3,
    3,
  )

  first_sequence = (
    r"$\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$."
  )
  redundant_four_term = (
    r"$\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$."
  )
  trimmed_sequence = (
    r"$\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$."
  )

  assert first_sequence in body
  assert redundant_four_term not in body
  assert trimmed_sequence in body


def test_phase157_r11_r17_target_groups_have_no_standalone_connectors():
  connectors = {
    "以上より,",
    "したがって,",
    "これより,",
  }

  for n, k in TARGETS:
    _, body = _reference_and_body(
      n,
      k,
    )
    body_paragraphs = tuple(
      paragraph.strip()
      for paragraph in body.split(
        "\n\n"
      )
      if paragraph.strip()
    )

    assert not (
      connectors
      & set(
        body_paragraphs
      )
    )


def test_phase157_r11_r17_pi6_3_repeated_numeric_equality_is_normalized():
  _, body = _reference_and_body(
    3,
    3,
  )

  assert (
    r"\operatorname{ord}(\nu')=4=4"
    not in body
  )
  assert (
    r"\operatorname{ord}(\nu')=4"
    in body
  )


def test_phase157_r11_r17_target_group_public_references_have_body_markers():
  for n, k in TARGETS:
    reference, body = _reference_and_body(
      n,
      k,
    )
    headers = tuple(
      int(
        match.group(
          1
        )
      )
      for match in REFERENCE_HEADER_RE.finditer(
        reference
      )
    )
    markers = {
      int(
        match.group(
          1
        )
      )
      for match in REFERENCE_MARKER_RE.finditer(
        body
      )
    }

    assert set(
      headers
    ) <= markers


def test_phase157_r11_r17_ancestry_only_references_are_not_public():
  pi12_reference, _ = _reference_and_body(
    5,
    7,
  )
  pi16_reference, _ = _reference_and_body(
    9,
    7,
  )

  assert "(5.5)" not in pi12_reference
  assert "Lemma 5.13" not in pi16_reference


def test_phase157_r11_r17_needed_references_remain_public_and_linked():
  pi10_reference, pi10_body = _reference_and_body(
    4,
    6,
  )
  pi12_reference, pi12_body = _reference_and_body(
    5,
    7,
  )
  pi16_reference, pi16_body = _reference_and_body(
    9,
    7,
  )

  assert "Lemma 5.4" in pi10_reference
  assert "[R1]" in pi10_body

  assert "Lemma 5.13" in pi12_reference
  assert "[R1]" in pi12_body

  assert "Lemma 5.14" in pi16_reference
  assert "[R1]" in pi16_body
'''

TEST_PATH.write_text(
  test_content,
  encoding="utf-8",
)

print(
  "Written: tests/test_phase157_r11_r17_residual_narrative_defects.py"
)
print("")
print("Phase157 R11-R17 patch applied successfully.")
