
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_repair5"


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


def replace_all_confirmed(
    path: Path,
    old: str,
    new: str,
    label: str,
    minimum_old_count: int = 0,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )

    if old not in text:
        if new in text:
            print(
                f"[already applied] {label}"
            )
            return

        if minimum_old_count > 0:
            raise RuntimeError(
                f"{label}: neither old nor new fragment was found"
            )

        print(
            f"[not present] {label}"
        )
        return

    count = text.count(
        old
    )

    if count < minimum_old_count:
        raise RuntimeError(
            f"{label}: expected at least {minimum_old_count} old fragments, "
            f"found {count}"
        )

    path.write_text(
        text.replace(
            old,
            new,
        ),
        encoding="utf-8",
    )

    print(
        f"[updated] {label}: {count} replacement(s)"
    )


def normalize_nested_exactness_reason(
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
            if line.strip().startswith(
                "def exactness_reason("
            )
        ),
        None,
    )

    if start is None:
        raise RuntimeError(
            "nested exactness_reason function not found"
        )

    start_indent = (
        len(
            lines[
                start
            ]
        )
        - len(
            lines[
                start
            ].lstrip()
        )
    )

    end = len(
        lines
    )

    for index in range(
        start + 1,
        len(
            lines
        ),
    ):
        stripped = lines[
            index
        ].lstrip()

        if not stripped:
            continue

        indent = (
            len(
                lines[
                    index
                ]
            )
            - len(
                stripped
            )
        )

        if (
            indent == start_indent
            and not stripped.startswith(
                "#"
            )
        ):
            end = index
            break

    old = '+ "$ である."'
    new = '+ "$."'

    matches = [
        index
        for index in range(
            start,
            end,
        )
        if old in lines[
            index
        ]
    ]

    if not matches:
        if any(
            new in lines[
                index
            ]
            for index in range(
                start,
                end,
            )
        ):
            print(
                "[already applied] nested exactness_reason prose"
            )
            return

        raise RuntimeError(
            "nested exactness_reason old/new closing prose not found"
        )

    if len(
        matches
    ) != 1:
        raise RuntimeError(
            "nested exactness_reason expected one closing prose match, "
            f"found {len(matches)}"
        )

    index = matches[
        0
    ]

    lines[
        index
    ] = lines[
        index
    ].replace(
        old,
        new,
        1,
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

    normalize_nested_exactness_reason(
        REPO_ROOT
        / "toda_group_proof_narrative_contribution_renderer.py"
    )

    short_test = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py"
    )

    replace_all_confirmed(
        short_test,
        (
            "この完全性と, 左の写像が単射, "
            "右の写像が全射であることより, "
            "次の短完全列を得る."
        ),
        (
            "この完全性と, 左の写像の単射性, "
            "右の写像の全射性より, "
            "次の短完全列が成り立つ."
        ),
        "Phase150 short exact prose expectations",
        minimum_old_count=0,
    )

    punctuation_test = (
        REPO_ROOT
        / "tests/test_phase157_r11_reference_reason_punctuation.py"
    )

    replace_all_confirmed(
        punctuation_test,
        (
            "この完全性と, 左の写像が単射, "
            "右の写像が全射であることより, "
            "次の短完全列を得る."
        ),
        (
            "この完全性と, 左の写像の単射性, "
            "右の写像の全射性より, "
            "次の短完全列が成り立つ."
        ),
        "Phase157 short exact prose expectation",
        minimum_old_count=0,
    )

    final_test = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py"
    )

    text = final_test.read_text(
        encoding="utf-8",
    )

    marker = (
        '  assert "中央の群を生成する" in sentence\n'
    )

    additions = (
        '  assert "である." not in sentence\n'
        '  assert "であるから" not in sentence\n'
    )

    if additions in text:
        print(
            "[already applied] final group structure normalized assertions"
        )
    elif marker in text:
        final_test.write_text(
            text.replace(
                marker,
                marker + additions,
                1,
            ),
            encoding="utf-8",
        )
        print(
            "[updated] final group structure normalized assertions"
        )
    else:
        raise RuntimeError(
            "final group structure assertion anchor not found"
        )

    repair16_test = (
        REPO_ROOT
        / "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py"
    )

    replace_all_confirmed(
        repair16_test,
        r'$\eta_{6}=E\eta_{5}$ である.',
        r'$\eta_{6}=E\eta_{5}$.',
        "repair16 eta bridge expectation",
        minimum_old_count=0,
    )

    replace_all_confirmed(
        repair16_test,
        r'\pi_{7}^{5}$ である.',
        r'\pi_{7}^{5}$.',
        "repair16 kernel reason expectation",
        minimum_old_count=0,
    )

    restoration_test = (
        REPO_ROOT
        / "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py"
    )

    replace_all_confirmed(
        restoration_test,
        r'$\eta_{6}=E\eta_{5}$ である.',
        r'$\eta_{6}=E\eta_{5}$.',
        "reference restoration eta bridge expectation",
        minimum_old_count=0,
    )

    replace_all_confirmed(
        restoration_test,
        r'\pi_{7}^{5}$ である.',
        r'\pi_{7}^{5}$.',
        "reference restoration kernel reason expectation",
        minimum_old_count=0,
    )

    focused_source = (
        PACKAGE_DIR
        / "test_phase159_r1_7c_r4_repair5_residual_proof_prose_normalization.py"
    )

    focused_target = (
        REPO_ROOT
        / "tests/test_phase159_r1_7c_r4_repair5_residual_proof_prose_normalization.py"
    )

    focused_target.write_text(
        focused_source.read_text(
            encoding="utf-8",
        ),
        encoding="utf-8",
    )

    print(
        "[added] Phase159 R4 repair5 focused regression test"
    )

    print("")
    print("Phase 159 R1-7c R4 repair5 applied.")
    print("Previously connected proof-body normalizer was preserved.")
    print("Imports changed: none.")


if __name__ == "__main__":
    main()
