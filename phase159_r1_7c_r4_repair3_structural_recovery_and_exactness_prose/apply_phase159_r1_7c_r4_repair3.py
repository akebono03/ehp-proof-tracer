
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_repair3"


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
    print(f"[updated] {label}")


def connect_public_proof_body_normalizer(
    path: Path,
) -> None:
    lines = path.read_text(
        encoding="utf-8",
    ).splitlines()

    helper_name = (
        "_phase159_r1_7c_r4_normalize_proof_body_prose"
    )

    if not any(
        helper_name in line
        for line in lines
    ):
        raise RuntimeError(
            "Phase159 R4 proof-body helper is missing."
        )

    function_index = next(
        (
            index
            for index, line in enumerate(
                lines
            )
            if line.startswith(
                "def _phase158_normalize_public_narrative_contract("
            )
        ),
        None,
    )

    if function_index is None:
        raise RuntimeError(
            "_phase158_normalize_public_narrative_contract not found"
        )

    function_end = next(
        (
            index
            for index in range(
                function_index + 1,
                len(
                    lines
                ),
            )
            if lines[index].startswith(
                "def "
            )
        ),
        len(
            lines
        ),
    )

    function_lines = lines[
        function_index:
        function_end
    ]

    if any(
        helper_name in line
        for line in function_lines
    ):
        print(
            "[already applied] connect proof-body prose normalizer"
        )
        return

    call_relative_index = next(
        (
            index
            for index, line in enumerate(
                function_lines
            )
            if (
                "_phase158_normalize_public_equation_numbers("
                in line
            )
        ),
        None,
    )

    if call_relative_index is None:
        raise RuntimeError(
            "equation-number normalization call not found"
        )

    assignment_relative_index = None

    for index in range(
        call_relative_index,
        -1,
        -1,
    ):
        if (
            function_lines[
                index
            ].strip()
            == "proof_body = ("
        ):
            assignment_relative_index = index
            break

    if assignment_relative_index is None:
        raise RuntimeError(
            "proof_body equation normalization assignment start not found"
        )

    depth = 0
    assignment_end_relative_index = None

    for index in range(
        assignment_relative_index,
        len(
            function_lines
        ),
    ):
        line = function_lines[
            index
        ]
        depth += line.count(
            "("
        )
        depth -= line.count(
            ")"
        )

        if (
            index
            > assignment_relative_index
            and depth == 0
        ):
            assignment_end_relative_index = index
            break

    if assignment_end_relative_index is None:
        raise RuntimeError(
            "proof_body equation normalization assignment end not found"
        )

    insertion_lines = [
        "  proof_body = (",
        "    _phase159_r1_7c_r4_normalize_proof_body_prose(",
        "      proof_body",
        "    )",
        "  )",
    ]

    absolute_insert_index = (
        function_index
        + assignment_end_relative_index
        + 1
    )

    lines[
        absolute_insert_index:absolute_insert_index
    ] = insertion_lines

    path.write_text(
        "\n".join(
            lines
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "[updated] connect proof-body prose normalizer"
    )


def main() -> None:
    files = (
        "toda_group_proof_narrative_reason_renderer.py",
        "toda_group_proof_generic_narrative_renderer.py",
        "toda_group_proof_narrative_renderer.py",
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

    connect_public_proof_body_normalizer(
        REPO_ROOT
        / "toda_group_proof_narrative_renderer.py"
    )

    contribution_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_contribution_renderer.py"
    )

    old_exactness = (
        '    return (\n'
        '      "完全性より, "\n'
        '      r"$\\\\ker "\n'
        '      + second_map\n'
        '      + r"=\\\\operatorname{Im}"\n'
        '      + first_map\n'
        '      + "="\n'
        '      + render_toda_primary_group_latex(\n'
        '        window.middle_term\n'
        '      )\n'
        '      + "$ である."\n'
        '    )\n'
    )
    new_exactness = (
        '    return (\n'
        '      "完全性より, "\n'
        '      r"$\\\\ker "\n'
        '      + second_map\n'
        '      + r"=\\\\operatorname{Im}"\n'
        '      + first_map\n'
        '      + "="\n'
        '      + render_toda_primary_group_latex(\n'
        '        window.middle_term\n'
        '      )\n'
        '      + "$."\n'
        '    )\n'
    )

    replace_once_or_confirm(
        contribution_path,
        old_exactness,
        new_exactness,
        "hidden zero-map exactness prose",
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

    replace_once_or_confirm(
        final_test,
        (
            '  assert "中央の群を生成する" in sentence\n'
            '  assert rendered.count(sentence) == 1\n'
        ),
        (
            '  assert "中央の群を生成する" in sentence\n'
            '  assert "である." not in sentence\n'
            '  assert "であるから" not in sentence\n'
            '  assert rendered.count(sentence) == 1\n'
        ),
        "final group structure normalized prose assertions",
    )

    repair16_test = (
        REPO_ROOT
        / "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py"
    )

    replace_once_or_confirm(
        repair16_test,
        '  assert r"$\\eta_{6}=E\\eta_{5}$ である." in body\n',
        '  assert r"$\\eta_{6}=E\\eta_{5}$." in body\n',
        "repair16 eta bridge normalized expectation",
    )

    replace_once_or_confirm(
        repair16_test,
        '    r"\\pi_{7}^{5}$ である."\n',
        '    r"\\pi_{7}^{5}$."\n',
        "repair16 kernel reason normalized expectation",
    )

    restoration_test = (
        REPO_ROOT
        / "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py"
    )

    replace_once_or_confirm(
        restoration_test,
        '    r"$\\eta_{6}=E\\eta_{5}$ である."\n',
        '    r"$\\eta_{6}=E\\eta_{5}$."\n',
        "reference restoration eta bridge normalized expectation",
    )

    replace_once_or_confirm(
        restoration_test,
        '    r"\\pi_{7}^{5}$ である."\n',
        '    r"\\pi_{7}^{5}$."\n',
        "reference restoration kernel reason normalized expectation",
    )

    focused_source = (
        PACKAGE_DIR
        / "test_phase159_r1_7c_r4_repair3_residual_proof_prose_normalization.py"
    )

    focused_target = (
        REPO_ROOT
        / "tests/test_phase159_r1_7c_r4_repair3_residual_proof_prose_normalization.py"
    )

    focused_target.write_text(
        focused_source.read_text(
            encoding="utf-8",
        ),
        encoding="utf-8",
    )

    print(
        "[added] Phase159 R4 repair3 focused regression test"
    )

    print("")
    print("Phase 159 R1-7c R4 repair3 applied.")
    print("Previous partial production edits preserved.")
    print("Imports changed: none.")


if __name__ == "__main__":
    main()
