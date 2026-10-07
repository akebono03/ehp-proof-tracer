from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = ROOT / "tests" / "test_phase159_exactness_map_property_public_dedup.py"

OLD_BLOCK = (
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

NEW_BLOCK = (
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


def main() -> None:
    text = RENDERER.read_text(
        encoding="utf-8"
    )

    if NEW_BLOCK in text:
        print(
            "final map-property dedup pass: already applied."
        )
    else:
        count = text.count(
            OLD_BLOCK
        )
        if count != 1:
            raise RuntimeError(
                "Expected exactly one late map-property insertion block, "
                f"found {count}."
            )

        RENDERER.write_text(
            text.replace(
                OLD_BLOCK,
                NEW_BLOCK,
                1,
            ),
            encoding="utf-8",
        )
        print(
            "final map-property dedup pass: applied."
        )

    TEST.write_text(
        TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 exactness map-property public dedup "
        "repair6 applied."
    )


if __name__ == "__main__":
    main()
