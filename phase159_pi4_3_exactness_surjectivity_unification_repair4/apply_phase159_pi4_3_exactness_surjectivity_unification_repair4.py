from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST = (
    ROOT
    / "tests"
    / "test_phase159_pi4_3_exactness_surjectivity_unification.py"
)

OLD_BLOCK = r'''  conclusion = (
    "$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ "
    "は全射."
  )
  assert conclusion in rendered
  assert rendered.index(
    reason_body
  ) < rendered.index(
    conclusion
  )
'''

NEW_BLOCK = r'''  conclusion_prefix = (
    "$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ "
  )
  conclusion_index = rendered.find(
    conclusion_prefix
  )

  assert conclusion_index >= 0
  conclusion_paragraph = next(
    paragraph
    for paragraph in rendered.split(
      "\n\n"
    )
    if conclusion_prefix in paragraph
  )
  assert "全射" in conclusion_paragraph
  assert rendered.index(
    reason_body
  ) < conclusion_index
'''


def main() -> None:
    if not TEST.exists():
        raise FileNotFoundError(
            f"test file not found: {TEST}"
        )

    text = TEST.read_text(
        encoding="utf-8"
    )

    if NEW_BLOCK in text and OLD_BLOCK not in text:
        print(
            "Phase 159 surjectivity unification "
            "repair4 already applied."
        )
        return

    count = text.count(
        OLD_BLOCK
    )
    if count != 1:
        raise RuntimeError(
            "Expected exactly one stale surjectivity "
            f"conclusion assertion block, found {count}."
        )

    TEST.write_text(
        text.replace(
            OLD_BLOCK,
            NEW_BLOCK,
            1,
        ),
        encoding="utf-8",
    )

    print(
        "Phase 159 pi_4^3 exactness-to-surjectivity "
        "unification repair4 applied."
    )


if __name__ == "__main__":
    main()
