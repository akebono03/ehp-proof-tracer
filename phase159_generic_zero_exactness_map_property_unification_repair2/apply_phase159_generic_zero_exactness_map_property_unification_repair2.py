from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST = (
    ROOT
    / "tests"
    / "test_phase159_pi4_3_exactness_surjectivity_unification.py"
)

OLD = (
    '  assert sentence == (\n'
    '    "完全性より, "\n'
    '    "$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ は全射."\n'
    '  )\n'
)

NEW = (
    '  assert sentence == (\n'
    '    "完全性より, "\n'
    '    r"$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ は全射."\n'
    '  )\n'
)


def main() -> None:
    if not TEST.exists():
        raise FileNotFoundError(
            f"test file not found: {TEST}"
        )

    text = TEST.read_text(
        encoding="utf-8"
    )

    if NEW in text and OLD not in text:
        print(
            "Phase 159 generic zero/exactness "
            "repair2 already applied."
        )
        return

    count = text.count(
        OLD
    )
    if count != 1:
        raise RuntimeError(
            "Expected exactly one stale non-raw "
            f"surjectivity expectation, found {count}."
        )

    TEST.write_text(
        text.replace(
            OLD,
            NEW,
            1,
        ),
        encoding="utf-8",
    )

    print(
        "Phase 159 generic zero/exactness "
        "map-property unification repair2 applied."
    )


if __name__ == "__main__":
    main()
