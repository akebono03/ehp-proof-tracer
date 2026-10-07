from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTION_RENDERER = (
    ROOT / "toda_group_proof_narrative_contribution_renderer.py"
)
PI4_TEST = (
    ROOT
    / "tests"
    / "test_phase159_pi4_3_exactness_surjectivity_unification.py"
)
PI6_TEST = (
    ROOT
    / "tests"
    / "test_phase150_rc4_5c_2_exactness_to_map_property.py"
)


OLD_PREFIXES = (
    '  connector_prefixes = (\n'
    '    "以上より, ",\n'
    '    "したがって, ",\n'
    '    "これより, ",\n'
    '    "これらより, ",\n'
    '  )\n'
)

NEW_PREFIXES = (
    '  connector_prefixes = (\n'
    '    "以上より, ",\n'
    '    "したがって, ",\n'
    '    "これより, ",\n'
    '    "これらより, ",\n'
    '    "完全性より, ",\n'
    '  )\n'
)

PI4_OLD = (
    '  assert rendered.count(\n'
    '    sentence\n'
    '  ) == 1\n'
    '  assert (\n'
    '    "この完全性と "\n'
    '    not in rendered\n'
    '  )\n'
)

PI4_NEW = (
    '  assert rendered.count(\n'
    '    sentence\n'
    '  ) == 1\n'
    '  assert rendered.count(\n'
    '    r"$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ は全射."\n'
    '  ) == 1\n'
    '  assert (\n'
    '    "この完全性と "\n'
    '    not in rendered\n'
    '  )\n'
)

PI6_OLD = (
    '  assert rendered.count(\n'
    '    sentence\n'
    '  ) == 1\n'
    '  assert (\n'
    '    "この完全性と $Δ=0$ より"\n'
    '    not in rendered\n'
    '  )\n'
)

PI6_NEW = (
    '  assert rendered.count(\n'
    '    sentence\n'
    '  ) == 1\n'
    '  assert rendered.count(\n'
    '    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射."\n'
    '  ) == 1\n'
    '  assert (\n'
    '    "この完全性と $Δ=0$ より"\n'
    '    not in rendered\n'
    '  )\n'
)


def replace_once(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(
        encoding="utf-8"
    )

    if new in text and old not in text:
        print(
            f"{label}: already applied."
        )
        return

    count = text.count(
        old
    )
    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one match, found {count}"
        )

    path.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )

    print(
        f"{label}: applied."
    )


def main() -> None:
    replace_once(
        CONTRIBUTION_RENDERER,
        OLD_PREFIXES,
        NEW_PREFIXES,
        "connector-prefix repair",
    )
    replace_once(
        PI4_TEST,
        PI4_OLD,
        PI4_NEW,
        "pi_4^3 duplicate assertion",
    )
    replace_once(
        PI6_TEST,
        PI6_OLD,
        PI6_NEW,
        "pi_6^3 duplicate assertion",
    )

    print(
        "Phase 159 exactness map-property duplicate "
        "suppression repair4 applied."
    )


if __name__ == "__main__":
    main()
