from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST = (
    ROOT
    / "tests"
    / "test_phase150_rc4_5c_2_exactness_to_map_property.py"
)

OLD = (
    '  assert sentence == (\n'
    '    "完全性より, "\n'
    '    "$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射."\n'
    '  )\n'
)

NEW = (
    '  assert sentence == (\n'
    '    "完全性より, "\n'
    '    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射."\n'
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
            "repair3 already applied."
        )
        return

    count = text.count(
        OLD
    )
    if count != 1:
        raise RuntimeError(
            "Expected exactly one stale Phase 150 "
            f"non-raw expectation, found {count}."
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
        "map-property unification repair3 applied."
    )


if __name__ == "__main__":
    main()
