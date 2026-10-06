
from __future__ import annotations

from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_recovery"


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


def connect_public_proof_body_normalizer(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    helper_name = "_phase159_r1_7c_r4_normalize_proof_body_prose"
    if helper_name not in text:
        raise RuntimeError(
            "Phase159 R4 proof-body prose helper is missing."
        )

    function_marker = (
        "def _phase158_normalize_public_narrative_contract("
    )
    function_start = text.find(function_marker)
    if function_start < 0:
        raise RuntimeError(
            "_phase158_normalize_public_narrative_contract not found"
        )

    next_function_start = text.find(
        "\ndef ",
        function_start + len(function_marker),
    )
    function_end = (
        len(text)
        if next_function_start < 0
        else next_function_start + 1
    )

    function_text = text[function_start:function_end]

    connected_fragment = (
        "  proof_body = (\n"
        "    _phase159_r1_7c_r4_normalize_proof_body_prose(\n"
        "      proof_body\n"
        "    )\n"
        "  )"
    )

    if connected_fragment in function_text:
        print("[already applied] connect proof-body prose normalizer")
        return

    call_marker = "_phase158_normalize_public_equation_numbers("
    call_index = function_text.find(call_marker)
    if call_index < 0:
        raise RuntimeError(
            "equation-number normalization call not found "
            "inside public narrative normalization"
        )

    assignment_start = function_text.rfind(
        "  proof_body = (",
        0,
        call_index,
    )
    if assignment_start < 0:
        raise RuntimeError(
            "proof_body equation normalization assignment start not found"
        )

    assignment_end = function_text.find(
        "\n  )",
        call_index,
    )
    if assignment_end < 0:
        raise RuntimeError(
            "proof_body equation normalization assignment end not found"
        )

    insertion_index = assignment_end + len("\n  )")

    insertion = (
        "\n"
        "  proof_body = (\n"
        "    _phase159_r1_7c_r4_normalize_proof_body_prose(\n"
        "      proof_body\n"
        "    )\n"
        "  )"
    )

    updated_function = (
        function_text[:insertion_index]
        + insertion
        + function_text[insertion_index:]
    )

    updated_text = (
        text[:function_start]
        + updated_function
        + text[function_end:]
    )

    path.write_text(
        updated_text,
        encoding="utf-8",
    )

    print("[updated] connect proof-body prose normalizer")


def main() -> None:
    files = (
        "toda_group_proof_narrative_reason_renderer.py",
        "toda_group_proof_generic_narrative_renderer.py",
        "toda_group_proof_narrative_renderer.py",
        "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py",
        "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py",
        "tests/test_phase157_r11_reference_reason_punctuation.py",
    )

    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)

    for relative_path in files:
        backup_file(relative_path)

    connect_public_proof_body_normalizer(
        REPO_ROOT / "toda_group_proof_narrative_renderer.py"
    )

    short_test = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py"
    )

    old_expected = (
        '  expected = (\n'
        '    "この完全性と, 左の写像が単射, "\n'
        '    "右の写像が全射であることより, "\n'
        '    "次の短完全列を得る."\n'
        '  )\n'
    )
    new_expected = (
        '  expected = (\n'
        '    "この完全性と, 左の写像の単射性, "\n'
        '    "右の写像の全射性より, "\n'
        '    "次の短完全列が成り立つ."\n'
        '  )\n'
    )
    replace_once_or_confirm(
        short_test,
        old_expected,
        new_expected,
        "short exact helper expectation",
    )

    old_reason = (
        '  reason = (\n'
        '    "この完全性と, 左の写像が単射, "\n'
        '    "右の写像が全射であることより, "\n'
        '    "次の短完全列を得る."\n'
        '  )\n'
    )
    new_reason = (
        '  reason = (\n'
        '    "この完全性と, 左の写像の単射性, "\n'
        '    "右の写像の全射性より, "\n'
        '    "次の短完全列が成り立つ."\n'
        '  )\n'
    )
    replace_once_or_confirm(
        short_test,
        old_reason,
        new_reason,
        "short exact visible prose expectation",
    )

    punctuation_test = (
        REPO_ROOT
        / "tests/test_phase157_r11_reference_reason_punctuation.py"
    )
    old_public = (
        '  short_exact_reason = (\n'
        '    "この完全性と, 左の写像が単射, "\n'
        '    "右の写像が全射であることより, "\n'
        '    "次の短完全列を得る."\n'
        '  )\n'
    )
    new_public = (
        '  short_exact_reason = (\n'
        '    "この完全性と, 左の写像の単射性, "\n'
        '    "右の写像の全射性より, "\n'
        '    "次の短完全列が成り立つ."\n'
        '  )\n'
    )
    replace_once_or_confirm(
        punctuation_test,
        old_public,
        new_public,
        "Phase157 short exact public expectation",
    )

    final_test = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py"
    )
    old_final = (
        '  assert "中央の群を生成する" in sentence\n'
        '  assert rendered.count(sentence) == 1\n'
    )
    new_final = (
        '  assert "中央の群を生成する" in sentence\n'
        '  assert "である." not in sentence\n'
        '  assert "であるから" not in sentence\n'
        '  assert rendered.count(sentence) == 1\n'
    )
    replace_once_or_confirm(
        final_test,
        old_final,
        new_final,
        "final group structure prose assertions",
    )

    focused_source = (
        PACKAGE_DIR
        / "test_phase159_r1_7c_r4_repair1_residual_proof_prose_normalization.py"
    )
    focused_target = (
        REPO_ROOT
        / "tests/test_phase159_r1_7c_r4_repair1_residual_proof_prose_normalization.py"
    )
    focused_target.write_text(
        focused_source.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    print("[added/updated] Phase159 R4 repair1 focused regression test")

    print("")
    print("Phase 159 R1-7c R4 repair2 recovery applied.")
    print("Previous partial production edits were preserved.")
    print("Imports changed: none.")


if __name__ == "__main__":
    main()
