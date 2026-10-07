
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_repair7"


def backup_file(path: Path) -> None:
    relative = path.relative_to(
        REPO_ROOT
    )
    target = BACKUP_DIR / relative
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        path,
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

    if new in text and old not in text:
        print(
            f"[already applied] {label}"
        )
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


def replace_test_contract_fragments() -> tuple[Path, ...]:
    replacements = (
        (
            r"$\eta_{6}=E\eta_{5}$ である.",
            r"$\eta_{6}=E\eta_{5}$.",
        ),
        (
            r"\pi_{7}^{5}$ である.",
            r"\pi_{7}^{5}$.",
        ),
        (
            r"$\ker E=\operatorname{Im}Δ=0$ である.",
            r"$\ker E=\operatorname{Im}Δ=0$.",
        ),
        (
            r"$4\nu'=0$ かつ $2\nu'\neq0$ である.",
            r"$4\nu'=0$ かつ $2\nu'\neq0$.",
        ),
        (
            "この完全性と, 左の写像が単射, "
            "右の写像が全射であることより, "
            "次の短完全列を得る.",
            "この完全性と, 左の写像の単射性, "
            "右の写像の全射性より, "
            "次の短完全列が成り立つ.",
        ),
    )

    changed = []

    for path in sorted(
        (REPO_ROOT / "tests").glob(
            "test_*.py"
        )
    ):
        text = path.read_text(
            encoding="utf-8",
        )
        updated = text

        for old, new in replacements:
            updated = updated.replace(
                old,
                new,
            )

        if updated == text:
            continue

        backup_file(
            path
        )

        path.write_text(
            updated,
            encoding="utf-8",
        )

        changed.append(
            path
        )

        print(
            "[updated stale prose expectation] "
            + str(
                path.relative_to(
                    REPO_ROOT
                )
            )
        )

    return tuple(
        changed
    )


def update_phase150_visible_reason_test(
    path: Path,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )

    old = (
        '  assert sentence is not None\n'
        '  assert "この短完全列と両端の群の位数より" in sentence\n'
        '  assert r"中央の群の位数は $2\\\\cdot2=4$" in sentence\n'
        '  assert "中央の群を生成する" in sentence\n'
        '  assert "である." not in sentence\n'
        '  assert "であるから" not in sentence\n'
        '  assert rendered.count(sentence) == 1\n'
        '\n'
        '  conclusion = r"$\\\\pi_{6}^{3} = \\\\mathbb{Z}/4\\\\{\\\\nu\\'\\\\}$"\n'
        '  assert conclusion in rendered\n'
        '  assert rendered.index(sentence) < rendered.index(conclusion)\n'
    )

    new = (
        '  assert sentence is not None\n'
        '  assert "この短完全列と両端の群の位数より" in sentence\n'
        '  assert r"中央の群の位数は $2\\\\cdot2=4$" in sentence\n'
        '  assert "中央の群を生成する" in sentence\n'
        '  assert "である." not in sentence\n'
        '  assert "であるから" not in sentence\n'
        '  assert r"\\\\operatorname{ord}(\\\\nu\\')=4=4" not in sentence\n'
        '\n'
        '  visible_sentence = sentence.removesuffix(\n'
        '    "\\\\nしたがって, "\n'
        '  )\n'
        '\n'
        '  assert rendered.count(\n'
        '    visible_sentence\n'
        '  ) == 1\n'
        '\n'
        '  conclusion = r"$\\\\pi_{6}^{3} = \\\\mathbb{Z}/4\\\\{\\\\nu\\'\\\\}$"\n'
        '  assert conclusion in rendered\n'
        '  assert rendered.index(\n'
        '    visible_sentence\n'
        '  ) < rendered.index(\n'
        '    conclusion\n'
        '  )\n'
    )

    if new in text:
        print(
            "[already applied] Phase150 visible final reason contract"
        )
        return

    count = text.count(
        old
    )

    if count != 1:
        raise RuntimeError(
            "Phase150 visible final reason contract: "
            f"expected exactly one old fragment, found {count}"
        )

    backup_file(
        path
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
        "[updated] Phase150 visible final reason contract"
    )


def main() -> None:
    reason_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_reason_renderer.py"
    )

    backup_file(
        reason_path
    )

    replace_once_or_confirm(
        reason_path,
        (
            '      f"$\\\\operatorname{{ord}}({generator_latex})"\n'
            '      f"={order_statement.rhs}={middle_order}$ より, "\n'
        ),
        (
            '      f"$\\\\operatorname{{ord}}({generator_latex})"\n'
            '      f"={middle_order}$ より, "\n'
        ),
        "FINAL_GROUP_STRUCTURE duplicate numeric equality",
    )

    changed_test_paths = (
        replace_test_contract_fragments()
    )

    phase150_path = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py"
    )

    update_phase150_visible_reason_test(
        phase150_path
    )

    focused_source = (
        PACKAGE_DIR
        / "test_phase159_r1_7c_r4_repair7_final_group_reason_and_stale_expectations.py"
    )

    focused_target = (
        REPO_ROOT
        / "tests/test_phase159_r1_7c_r4_repair7_final_group_reason_and_stale_expectations.py"
    )

    if focused_target.exists():
        backup_file(
            focused_target
        )

    focused_target.write_text(
        focused_source.read_text(
            encoding="utf-8",
        ),
        encoding="utf-8",
    )

    print(
        "[added] Phase159 R4 repair7 focused regression test"
    )

    print("")
    print("Phase 159 R1-7c R4 repair7 applied.")
    print(
        "Stale prose test files updated: "
        + str(
            len(
                changed_test_paths
            )
        )
    )
    print("Imports changed: none.")


if __name__ == "__main__":
    main()
