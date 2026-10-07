from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "tests" / "test_phase150_rc4_5c_2_exactness_to_map_property.py"

OLD = '    "$\\\\ker E=\\\\operatorname{Im}Δ=0$ である.\\n"\n'
NEW = '    "$\\\\ker E=\\\\operatorname{Im}Δ=0$.\\n"\n'


def main() -> None:
    if not TEST.exists():
        raise FileNotFoundError(
            f"test file not found: {TEST}"
        )

    text = TEST.read_text(encoding="utf-8")

    if NEW in text and OLD not in text:
        print(
            "Phase 159 repair3 already applied."
        )
        return

    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(
            "Expected exactly one stale exactness prose "
            f"expectation, found {count}."
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
        "Phase 159 pi_4^3 exactness reason "
        "unification repair3 applied."
    )


if __name__ == "__main__":
    main()
