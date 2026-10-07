
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_repair4"


def backup_file(relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    target = BACKUP_DIR / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def replace_once_or_confirm(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(encoding="utf-8")

    if new in text:
        print(f"[already applied] {label}")
        return

    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one old fragment, found {count}"
        )

    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )
    print(f"[updated] {label}")


def connect_before_lines_block(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    helper_call = (
        "  proof_body = (\n"
        "    _phase159_r1_7c_r4_normalize_proof_body_prose(\n"
        "      proof_body\n"
        "    )\n"
        "  )\n"
    )

    function_marker = (
        "def _phase158_normalize_public_narrative_contract("
    )
    function_start = text.find(function_marker)

    if function_start < 0:
        raise RuntimeError(
            "_phase158_normalize_public_narrative_contract not found"
        )

    next_function = text.find(
        "\ndef ",
        function_start + len(function_marker),
    )
    function_end = len(text) if next_function < 0 else next_function + 1

    function_text = text[function_start:function_end]

    if helper_call.strip() in function_text:
        print("[already applied] connect proof-body prose normalizer")
        return

    lines_anchor = "\n  lines = [\n"
    anchor_index = function_text.find(lines_anchor)

    if anchor_index < 0:
        raise RuntimeError(
            "lines = [ anchor not found inside public narrative normalization"
        )

    updated_function = (
        function_text[:anchor_index + 1]
        + helper_call
        + "\n"
        + function_text[anchor_index + 1:]
    )

    updated = (
        text[:function_start]
        + updated_function
        + text[function_end:]
    )

    path.write_text(
        updated,
        encoding="utf-8",
    )
    print("[updated] connect proof-body prose normalizer before lines block")


def main() -> None:
    files = (
        "toda_group_proof_narrative_renderer.py",
        "toda_group_proof_narrative_contribution_renderer.py",
        "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py",
        "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py",
        "tests/test_phase157_r11_reference_reason_punctuation.py",
        "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py",
        "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py",
    )

    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)

    for relative_path in files:
        backup_file(relative_path)

    narrative_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_renderer.py"
    )
    connect_before_lines_block(
        narrative_path
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

    replacements = (
        (
            REPO_ROOT / "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py",
            '  expected = (\n    "この完全性と, 左の写像が単射, "\n    "右の写像が全射であることより, "\n    "次の短完全列を得る."\n  )\n',
            '  expected = (\n    "この完全性と, 左の写像の単射性, "\n    "右の写像の全射性より, "\n    "次の短完全列が成り立つ."\n  )\n',
            "short exact helper expectation",
        ),
        (
            REPO_ROOT / "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py",
            '  reason = (\n    "この完全性と, 左の写像が単射, "\n    "右の写像が全射であることより, "\n    "次の短完全列を得る."\n  )\n',
            '  reason = (\n    "この完全性と, 左の写像の単射性, "\n    "右の写像の全射性より, "\n    "次の短完全列が成り立つ."\n  )\n',
            "short exact visible expectation",
        ),
        (
            REPO_ROOT / "tests/test_phase157_r11_reference_reason_punctuation.py",
            '  short_exact_reason = (\n    "この完全性と, 左の写像が単射, "\n    "右の写像が全射であることより, "\n    "次の短完全列を得る."\n  )\n',
            '  short_exact_reason = (\n    "この完全性と, 左の写像の単射性, "\n    "右の写像の全射性より, "\n    "次の短完全列が成り立つ."\n  )\n',
            "Phase157 short exact public expectation",
        ),
        (
            REPO_ROOT / "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py",
            '  assert "中央の群を生成する" in sentence\n  assert rendered.count(sentence) == 1\n',
            '  assert "中央の群を生成する" in sentence\n  assert "である." not in sentence\n  assert "であるから" not in sentence\n  assert rendered.count(sentence) == 1\n',
            "final group structure assertions",
        ),
        (
            REPO_ROOT / "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py",
            '  assert r"$\\eta_{6}=E\\eta_{5}$ である." in body\n',
            '  assert r"$\\eta_{6}=E\\eta_{5}$." in body\n',
            "repair16 eta bridge expectation",
        ),
        (
            REPO_ROOT / "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py",
            '    r"\\pi_{7}^{5}$ である."\n',
            '    r"\\pi_{7}^{5}$."\n',
            "repair16 kernel reason expectation",
        ),
        (
            REPO_ROOT / "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py",
            '    r"$\\eta_{6}=E\\eta_{5}$ である."\n',
            '    r"$\\eta_{6}=E\\eta_{5}$."\n',
            "reference restoration eta bridge expectation",
        ),
        (
            REPO_ROOT / "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py",
            '    r"\\pi_{7}^{5}$ である."\n',
            '    r"\\pi_{7}^{5}$."\n',
            "reference restoration kernel reason expectation",
        ),
    )

    for path, old, new, label in replacements:
        replace_once_or_confirm(
            path,
            old,
            new,
            label,
        )

    focused_source = (
        PACKAGE_DIR
        / "test_phase159_r1_7c_r4_repair4_residual_proof_prose_normalization.py"
    )
    focused_target = (
        REPO_ROOT
        / "tests/test_phase159_r1_7c_r4_repair4_residual_proof_prose_normalization.py"
    )
    focused_target.write_text(
        focused_source.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    print("[added] Phase159 R4 repair4 focused regression test")

    print("")
    print("Phase 159 R1-7c R4 repair4 applied.")
    print("Imports changed: none.")


if __name__ == "__main__":
    main()
