
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_repair6"


def backup_file(relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    target = BACKUP_DIR / relative_path
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        source,
        target,
    )


def replace_once_or_confirm(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )

    if new in text:
        print(f"[already applied] {label}")
        return

    count = text.count(
        old
    )

    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one old fragment, found {count}"
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
        f"[updated] {label}"
    )


def normalize_exactness_reason(
    path: Path,
) -> None:
    lines = path.read_text(
        encoding="utf-8",
    ).splitlines()

    start = next(
        (
            index
            for index, line in enumerate(
                lines
            )
            if line.strip()
            == "def exactness_reason("
        ),
        None,
    )

    if start is None:
        raise RuntimeError(
            "exactness_reason start was not found"
        )

    end = next(
        (
            index
            for index in range(
                start + 1,
                len(
                    lines
                ),
            )
            if lines[
                index
            ].strip()
            == "candidate_zero_steps = []"
        ),
        None,
    )

    if end is None:
        raise RuntimeError(
            "exactness_reason end anchor was not found"
        )

    old = '+ "$ である."'
    new = '+ "$."'

    matches = [
        index
        for index in range(
            start,
            end,
        )
        if lines[
            index
        ].strip()
        == old
    ]

    if len(
        matches
    ) == 1:
        index = matches[
            0
        ]
        indent = lines[
            index
        ][
            :len(
                lines[
                    index
                ]
            )
            - len(
                lines[
                    index
                ].lstrip()
            )
        ]
        lines[
            index
        ] = (
            indent
            + new
        )

        path.write_text(
            "\n".join(
                lines
            )
            + "\n",
            encoding="utf-8",
        )

        print(
            "[updated] nested exactness_reason prose"
        )
        return

    new_matches = [
        index
        for index in range(
            start,
            end,
        )
        if lines[
            index
        ].strip()
        == new
    ]

    if (
        not matches
        and len(
            new_matches
        ) == 1
    ):
        print(
            "[already applied] nested exactness_reason prose"
        )
        return

    raise RuntimeError(
        "exactness_reason closing prose match mismatch: "
        f"old={len(matches)}, new={len(new_matches)}"
    )


def main() -> None:
    files = (
        "toda_group_proof_narrative_contribution_renderer.py",
        "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py",
        "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py",
        "tests/test_phase157_r11_reference_reason_punctuation.py",
        "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py",
        "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py",
    )

    if BACKUP_DIR.exists():
        shutil.rmtree(
            BACKUP_DIR
        )

    for relative_path in files:
        backup_file(
            relative_path
        )

    normalize_exactness_reason(
        REPO_ROOT
        / "toda_group_proof_narrative_contribution_renderer.py"
    )

    short_test = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py"
    )

    replace_once_or_confirm(
        short_test,
        (
            '  expected = (\n'
            '    "この完全性と, 左の写像が単射, "\n'
            '    "右の写像が全射であることより, "\n'
            '    "次の短完全列を得る."\n'
            '  )\n'
        ),
        (
            '  expected = (\n'
            '    "この完全性と, 左の写像の単射性, "\n'
            '    "右の写像の全射性より, "\n'
            '    "次の短完全列が成り立つ."\n'
            '  )\n'
        ),
        "short exact helper expectation",
    )

    replace_once_or_confirm(
        short_test,
        (
            '  reason = (\n'
            '    "この完全性と, 左の写像が単射, "\n'
            '    "右の写像が全射であることより, "\n'
            '    "次の短完全列を得る."\n'
            '  )\n'
        ),
        (
            '  reason = (\n'
            '    "この完全性と, 左の写像の単射性, "\n'
            '    "右の写像の全射性より, "\n'
            '    "次の短完全列が成り立つ."\n'
            '  )\n'
        ),
        "short exact visible expectation",
    )

    punctuation_test = (
        REPO_ROOT
        / "tests/test_phase157_r11_reference_reason_punctuation.py"
    )

    replace_once_or_confirm(
        punctuation_test,
        (
            '  short_exact_reason = (\n'
            '    "この完全性と, 左の写像が単射, "\n'
            '    "右の写像が全射であることより, "\n'
            '    "次の短完全列を得る."\n'
            '  )\n'
        ),
        (
            '  short_exact_reason = (\n'
            '    "この完全性と, 左の写像の単射性, "\n'
            '    "右の写像の全射性より, "\n'
            '    "次の短完全列が成り立つ."\n'
            '  )\n'
        ),
        "Phase157 short exact public expectation",
    )

    final_test = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py"
    )

    text = final_test.read_text(
        encoding="utf-8",
    )

    additions = (
        '  assert "である." not in sentence\n'
        '  assert "であるから" not in sentence\n'
    )

    if additions in text:
        print(
            "[already applied] final group structure normalized assertions"
        )
    else:
        anchor = (
            '  assert "中央の群を生成する" in sentence\n'
        )

        if anchor not in text:
            raise RuntimeError(
                "final group structure assertion anchor not found"
            )

        final_test.write_text(
            text.replace(
                anchor,
                anchor + additions,
                1,
            ),
            encoding="utf-8",
        )

        print(
            "[updated] final group structure normalized assertions"
        )

    repair16_test = (
        REPO_ROOT
        / "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py"
    )

    replace_once_or_confirm(
        repair16_test,
        '  assert r"$\\eta_{6}=E\\eta_{5}$ である." in body\n',
        '  assert r"$\\eta_{6}=E\\eta_{5}$." in body\n',
        "repair16 eta bridge expectation",
    )

    replace_once_or_confirm(
        repair16_test,
        '    r"\\pi_{7}^{5}$ である."\n',
        '    r"\\pi_{7}^{5}$."\n',
        "repair16 kernel reason expectation",
    )

    restoration_test = (
        REPO_ROOT
        / "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py"
    )

    replace_once_or_confirm(
        restoration_test,
        '    r"$\\eta_{6}=E\\eta_{5}$ である."\n',
        '    r"$\\eta_{6}=E\\eta_{5}$."\n',
        "reference restoration eta bridge expectation",
    )

    replace_once_or_confirm(
        restoration_test,
        '    r"\\pi_{7}^{5}$ である."\n',
        '    r"\\pi_{7}^{5}$."\n',
        "reference restoration kernel reason expectation",
    )

    focused_source = (
        PACKAGE_DIR
        / "test_phase159_r1_7c_r4_repair6_residual_proof_prose_normalization.py"
    )

    focused_target = (
        REPO_ROOT
        / "tests/test_phase159_r1_7c_r4_repair6_residual_proof_prose_normalization.py"
    )

    focused_target.write_text(
        focused_source.read_text(
            encoding="utf-8",
        ),
        encoding="utf-8",
    )

    print(
        "[added] Phase159 R4 repair6 focused regression test"
    )

    print("")
    print("Phase 159 R1-7c R4 repair6 applied.")
    print("Imports changed: none.")


if __name__ == "__main__":
    main()
