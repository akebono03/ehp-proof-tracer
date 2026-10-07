from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST = (
    ROOT
    / "tests"
    / "test_phase159_pi4_3_exactness_surjectivity_unification.py"
)

OLD_BLOCK = r'''  assert rendered.count(sentence) == 1
  assert (
    "これより, この完全性と "
    not in rendered
  )

  conclusion = (
    "$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ "
    "は全射."
  )
  assert conclusion in rendered
  assert rendered.index(sentence) < rendered.index(
    conclusion
  )
'''

NEW_BLOCK = r'''  reason_body = (
    "この完全性と "
    "$\\pi_{4}^{5}=0$ より, "
    "$\\operatorname{Im}E=\\ker H=\\pi_{4}^{3}$."
  )
  assert rendered.count(
    reason_body
  ) == 1
  assert (
    "これより, この完全性と "
    not in rendered
  )

  conclusion = (
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
            "repair1 already applied."
        )
        return

    count = text.count(
        OLD_BLOCK
    )
    if count != 1:
        raise RuntimeError(
            "Expected exactly one stale sentence "
            f"visibility assertion block, found {count}."
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
        "unification repair1 applied."
    )


if __name__ == "__main__":
    main()
