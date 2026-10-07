from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = ROOT / "tests" / "test_phase159_exactness_map_property_public_dedup.py"


NEW_FUNCTION = r'''def suppress_toda_group_proof_narrative_repeated_unique_step_statements(
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

  def normalized_step_key(
    line: str,
  ) -> str:
    key = (
      _phase157_r11_reference_statement_match_key(
        line
      )
    )

    for verbose, concise in (
      (
        " は単射である",
        " は単射",
      ),
      (
        " は全射である",
        " は全射",
      ),
    ):
      if key.endswith(
        verbose
      ):
        return (
          key[
            :-len(
              verbose
            )
          ]
          + concise
        )

    return key

  step_ids_by_key = {}

  for node in presentation.nodes:
    proof_step = node.proof_step
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      continue

    key = normalized_step_key(
      rendered
    )

    step_ids_by_key.setdefault(
      key,
      set(),
    ).add(
      id(
        proof_step
      )
    )

  unique_step_keys = {
    key
    for key, step_ids in step_ids_by_key.items()
    if len(
      step_ids
    ) == 1
  }

  if not unique_step_keys:
    return markdown

  connector_prefixes = (
    "以上より, ",
    "したがって, ",
    "これより, ",
    "これらより, ",
    "完全性より, ",
  )

  retained = []
  seen_unique_keys = set()

  for paragraph in markdown.split(
    "\n\n"
  ):
    stripped = paragraph.strip()
    comparable = stripped

    for prefix in connector_prefixes:
      if comparable.startswith(
        prefix
      ):
        comparable = comparable[
          len(
            prefix
          ):
        ]
        break

    key = normalized_step_key(
      comparable
    )

    if key not in unique_step_keys:
      retained.append(
        paragraph
      )
      continue

    if key in seen_unique_keys:
      continue

    seen_unique_keys.add(
      key
    )
    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )


'''


TEST_SOURCE = r'''from toda_calculation_facade import (
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


def _phase159_public_narrative(
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


def test_phase159_pi4_3_public_exactness_surjectivity_is_emitted_once():
  rendered = _phase159_public_narrative(
    3,
    1,
  )

  map_statement = (
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  )
  reason_statement = (
    "完全性より, "
    + map_statement
  )

  assert rendered.count(
    map_statement
  ) == 1
  assert rendered.count(
    reason_statement
  ) == 1


def test_phase159_pi6_3_public_exactness_injectivity_is_emitted_once():
  rendered = _phase159_public_narrative(
    3,
    3,
  )

  map_statement = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  )
  reason_statement = (
    "完全性より, "
    + map_statement
  )

  assert rendered.count(
    map_statement
  ) == 1
  assert rendered.count(
    reason_statement
  ) == 1
'''


def replace_function(
    text: str,
    function_name: str,
    replacement: str,
) -> str:
    marker = f"def {function_name}("
    start = text.find(
        marker
    )
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


def ensure_late_dedup(
    text: str,
) -> str:
    marker = (
        '  rendered = (\n'
        '    insert_toda_group_proof_narrative_map_property_dependencies(\n'
        '      presentation,\n'
        '      rendered,\n'
        '      reference_entries,\n'
        '    )\n'
        '  )\n'
        '  rendered = (\n'
        '    suppress_toda_group_proof_narrative_repeated_unique_step_statements(\n'
        '      presentation,\n'
        '      rendered,\n'
        '    )\n'
        '  )\n'
        '  rendered = (\n'
        '    order_toda_group_proof_narrative_injective_image_order_reason(\n'
    )

    if marker in text:
        return text

    old = (
        '  rendered = (\n'
        '    insert_toda_group_proof_narrative_map_property_dependencies(\n'
        '      presentation,\n'
        '      rendered,\n'
        '      reference_entries,\n'
        '    )\n'
        '  )\n'
        '  rendered = (\n'
        '    order_toda_group_proof_narrative_injective_image_order_reason(\n'
    )

    count = text.count(
        old
    )
    if count != 1:
        raise RuntimeError(
            "late map-property insertion block not found uniquely"
        )

    return text.replace(
        old,
        marker,
        1,
    )


def main() -> None:
    text = RENDERER.read_text(
        encoding="utf-8"
    )

    text = replace_function(
        text,
        "suppress_toda_group_proof_narrative_repeated_unique_step_statements",
        NEW_FUNCTION,
    )
    text = ensure_late_dedup(
        text
    )

    RENDERER.write_text(
        text,
        encoding="utf-8",
    )

    TEST.write_text(
        TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 exactness map-property public dedup "
        "repair7 applied."
    )


if __name__ == "__main__":
    main()
