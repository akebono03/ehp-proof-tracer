from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REASON_RENDERER = (
    ROOT / "toda_group_proof_narrative_reason_renderer.py"
)
TEST = (
    ROOT
    / "tests"
    / "test_phase159_pi4_3_exactness_reason_unification.py"
)


OLD_KERNEL_RETURN = '''    return (
      "完全性より, "
      f"$\\\\ker {second_map_name}"
      f"=\\\\operatorname{{Im}}{first_map_name}"
      f"={group_latex}$ である."
    )
'''

NEW_KERNEL_RETURN = '''    return (
      "完全性より, "
      f"$\\\\ker {second_map_name}"
      f"=\\\\operatorname{{Im}}{first_map_name}"
      f"={group_latex}$."
    )
'''

HELPER = r'''
def _normalize_exactness_to_kernel_reason_prose(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
) -> str:
  if (
    reason.kind
    is not TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_KERNEL
  ):
    return markdown

  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  if sentence is None:
    return markdown

  reason_lines = sentence.splitlines()

  while (
    reason_lines
    and reason_lines[-1].strip()
    in {
      "以上より,",
      "したがって,",
      "これより,",
      "これらより,",
    }
  ):
    reason_lines.pop()

  reason_body = "\\n".join(
    reason_lines
  ).strip()

  if not reason_body:
    return markdown

  paragraphs = markdown.split(
    "\\n\\n"
  )
  reason_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if paragraph.strip() == reason_body
  )

  if len(reason_indices) != 1:
    return markdown

  reason_index = reason_indices[0]

  if (
    reason_index > 0
    and paragraphs[
      reason_index - 1
    ].strip()
    == "これより,"
  ):
    paragraphs.pop(
      reason_index - 1
    )
    reason_index -= 1

  image_line = (
    _render_generic_narrative_step(
      reason.premise_steps[0]
    )
    if reason.premise_steps
    else ""
  )
  kernel_line = (
    _render_generic_narrative_step(
      reason.conclusion_step
    )
  )
  covered_lines = {
    line.strip()
    for line in (
      image_line,
      kernel_line,
    )
    if line
  }

  retained = paragraphs[
    :reason_index + 1
  ]

  for paragraph in paragraphs[
    reason_index + 1:
  ]:
    if paragraph.strip() in covered_lines:
      continue

    retained.append(
      paragraph
    )

  return "\\n\\n".join(
    retained
  )


'''

OLD_TAIL = '''    rendered = (
      rendered[:insertion_index]
      + prefix
      + rendered[insertion_index:]
    )

  return rendered
'''

NEW_TAIL = '''    rendered = (
      rendered[:insertion_index]
      + prefix
      + rendered[insertion_index:]
    )

  for reason in reason_sidecar.reasons:
    rendered = (
      _normalize_exactness_to_kernel_reason_prose(
        rendered,
        reason,
      )
    )

  return rendered
'''

TEST_FUNCTION = r'''

def test_phase159_pi4_3_exactness_reason_matches_existing_exactness_prose_style():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_KERNEL
    )
  )
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  image_line = (
    _render_generic_narrative_step(
      reason.premise_steps[0]
    )
  )
  kernel_line = (
    _render_generic_narrative_step(
      reason.conclusion_step
    )
  )

  assert sentence is not None
  assert sentence.startswith(
    "完全性より, "
  )
  assert " である." not in sentence
  assert (
    "これより, 完全性より,"
    not in rendered
  )
  assert rendered.count(
    sentence
  ) == 1
  assert rendered.count(
    image_line
  ) == 1
  assert kernel_line not in rendered
'''


def replace_once(
    text: str,
    old: str,
    new: str,
    label: str,
) -> str:
    count = text.count(old)

    if count == 0 and new in text:
        return text

    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one match, found {count}"
        )

    return text.replace(
        old,
        new,
        1,
    )


def main() -> None:
    reason_text = REASON_RENDERER.read_text(
        encoding="utf-8"
    )

    reason_text = replace_once(
        reason_text,
        OLD_KERNEL_RETURN,
        NEW_KERNEL_RETURN,
        "EXACTNESS_TO_KERNEL prose",
    )

    if (
        "def _normalize_exactness_to_kernel_reason_prose("
        not in reason_text
    ):
        marker = (
            "def insert_toda_group_proof_narrative_reason_prose(\\n"
        )
        if marker not in reason_text:
            raise RuntimeError(
                "reason insertion function marker not found"
            )
        reason_text = reason_text.replace(
            marker,
            HELPER + marker,
            1,
        )

    if (
        "_normalize_exactness_to_kernel_reason_prose(\\n"
        "        rendered,\\n"
        "        reason,"
        not in reason_text
    ):
        reason_text = replace_once(
            reason_text,
            OLD_TAIL,
            NEW_TAIL,
            "reason insertion tail",
        )

    REASON_RENDERER.write_text(
        reason_text,
        encoding="utf-8",
    )

    test_text = TEST.read_text(
        encoding="utf-8"
    )

    test_name = (
        "def test_phase159_pi4_3_exactness_reason_"
        "matches_existing_exactness_prose_style():"
    )

    if test_name not in test_text:
        test_text = (
            test_text.rstrip()
            + TEST_FUNCTION
            + "\\n"
        )
        TEST.write_text(
            test_text,
            encoding="utf-8",
        )

    print(
        "Phase 159 pi_4^3 exactness prose alignment applied."
    )


if __name__ == "__main__":
    main()
