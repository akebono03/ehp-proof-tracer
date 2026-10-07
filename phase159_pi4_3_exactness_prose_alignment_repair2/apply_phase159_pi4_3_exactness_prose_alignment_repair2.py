from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST = (
    ROOT
    / "tests"
    / "test_phase159_pi4_3_exactness_reason_unification.py"
)

OLD_ASSERTIONS = '''  assert kernel_conclusion
  assert kernel_conclusion in rendered
  assert (
    rendered.index(sentence)
    < rendered.index(kernel_conclusion)
  )
'''

NEW_ASSERTIONS = '''  assert kernel_conclusion
  assert kernel_conclusion not in rendered
'''


def main() -> None:
    if not TEST.exists():
        raise FileNotFoundError(
            f"test file not found: {TEST}"
        )

    text = TEST.read_text(
        encoding="utf-8"
    )

    if (
        NEW_ASSERTIONS in text
        and OLD_ASSERTIONS not in text
    ):
        print(
            "Phase 159 exactness prose alignment "
            "repair2 already applied."
        )
        return

    count = text.count(
        OLD_ASSERTIONS
    )
    if count != 1:
        raise RuntimeError(
            "Expected exactly one stale kernel "
            f"visibility assertion block, found {count}."
        )

    TEST.write_text(
        text.replace(
            OLD_ASSERTIONS,
            NEW_ASSERTIONS,
            1,
        ),
        encoding="utf-8",
    )

    print(
        "Phase 159 pi_4^3 exactness prose "
        "alignment repair2 applied."
    )


if __name__ == "__main__":
    main()
