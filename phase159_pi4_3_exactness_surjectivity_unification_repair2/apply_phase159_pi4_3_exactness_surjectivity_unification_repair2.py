from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"


NEW_FUNCTION = r'''def _normalize_exactness_to_map_property_reason_prose(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
) -> str:
  if (
    reason.kind
    is not TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  ):
    return markdown

  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  if sentence is None:
    return markdown

  lines = sentence.splitlines()

  while (
    lines
    and lines[-1].strip()
    in {
      "以上より,",
      "したがって,",
      "これより,",
      "これらより,",
    }
  ):
    lines.pop()

  reason_body = "\n".join(
    lines
  ).strip()

  if not reason_body:
    return markdown

  paragraphs = markdown.split(
    "\n\n"
  )
  prefixed_reason_body = (
    "これより, "
    + reason_body
  )
  matching_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if paragraph.strip()
    in {
      reason_body,
      prefixed_reason_body,
    }
  )

  if len(matching_indices) != 1:
    return markdown

  reason_index = matching_indices[0]
  reason_paragraph = paragraphs[
    reason_index
  ].strip()

  if reason_paragraph == prefixed_reason_body:
    paragraphs[
      reason_index
    ] = reason_body

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

  return "\n\n".join(
    paragraphs
  )


'''


def replace_function(
    text: str,
    function_name: str,
    replacement: str,
) -> str:
    marker = f"def {function_name}("
    start = text.find(marker)

    if start < 0:
        raise RuntimeError(
            f"function not found: {function_name}"
        )

    next_def = text.find(
        "\ndef ",
        start + len(marker),
    )

    if next_def < 0:
        raise RuntimeError(
            f"next function not found after: {function_name}"
        )

    return (
        text[:start]
        + replacement
        + text[next_def + 1:]
    )


def main() -> None:
    if not RENDERER.exists():
        raise FileNotFoundError(
            f"renderer not found: {RENDERER}"
        )

    text = RENDERER.read_text(
        encoding="utf-8"
    )

    if (
        "def _normalize_exactness_to_map_property_reason_prose("
        not in text
    ):
        raise RuntimeError(
            "Phase 159 surjectivity normalizer is not present. "
            "Apply the previous package first."
        )

    text = replace_function(
        text,
        "_normalize_exactness_to_map_property_reason_prose",
        NEW_FUNCTION,
    )

    RENDERER.write_text(
        text,
        encoding="utf-8",
    )

    print(
        "Phase 159 pi_4^3 exactness-to-surjectivity "
        "unification repair2 applied."
    )


if __name__ == "__main__":
    main()
