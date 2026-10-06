
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_repair8"


def backup_file(path: Path) -> None:
    relative = path.relative_to(REPO_ROOT)
    target = BACKUP_DIR / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def replace_once_or_confirm(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(encoding="utf-8")

    if new in text and old not in text:
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


def replace_function(
    path: Path,
    function_name: str,
    replacement: str,
) -> None:
    text = path.read_text(encoding="utf-8")
    marker = "def " + function_name + "("
    start = text.find(marker)

    if start < 0:
        raise RuntimeError(
            f"{function_name}: function start not found"
        )

    next_start = text.find(
        "\ndef ",
        start + len(marker),
    )

    end = len(text) if next_start < 0 else next_start + 1

    replacement_text = replacement.rstrip() + "\n\n"

    if text[start:end] == replacement_text:
        print(f"[already applied] {function_name}")
        return

    path.write_text(
        text[:start]
        + replacement_text
        + text[end:],
        encoding="utf-8",
    )

    print(f"[updated] {function_name}")


def replace_stale_test_prose() -> tuple[Path, ...]:
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
        (REPO_ROOT / "tests").glob("test_*.py")
    ):
        text = path.read_text(encoding="utf-8")
        updated = text

        for old, new in replacements:
            updated = updated.replace(old, new)

        if updated == text:
            continue

        backup_file(path)

        path.write_text(
            updated,
            encoding="utf-8",
        )

        changed.append(path)

        print(
            "[updated stale prose expectation] "
            + str(path.relative_to(REPO_ROOT))
        )

    return tuple(changed)


def main() -> None:
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)

    reason_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_reason_renderer.py"
    )

    backup_file(reason_path)

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

    changed_test_paths = replace_stale_test_prose()

    phase150_path = (
        REPO_ROOT
        / "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py"
    )

    if phase150_path not in changed_test_paths:
        backup_file(phase150_path)

    phase150_function = r"""def test_phase150_rc4_5f_2_final_reason_is_visible_before_final_group_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reasons,
  ) = _pi6_final_reason_data()

  reason = reasons[0]
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert sentence is not None
  assert "この短完全列と両端の群の位数より" in sentence
  assert r"中央の群の位数は $2\cdot2=4$" in sentence
  assert "中央の群を生成する" in sentence
  assert "である." not in sentence
  assert "であるから" not in sentence
  assert r"\operatorname{ord}(\nu')=4=4" not in sentence

  visible_sentence = sentence.removesuffix(
    "\nしたがって, "
  )

  assert rendered.count(
    visible_sentence
  ) == 1

  conclusion = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
  assert conclusion in rendered
  assert rendered.index(
    visible_sentence
  ) < rendered.index(
    conclusion
  )
"""

    replace_function(
        phase150_path,
        "test_phase150_rc4_5f_2_final_reason_is_visible_before_final_group_conclusion",
        phase150_function,
    )

    focused_source = (
        PACKAGE_DIR
        / "test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py"
    )

    focused_target = (
        REPO_ROOT
        / "tests/test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py"
    )

    if focused_target.exists():
        backup_file(focused_target)

    focused_target.write_text(
        focused_source.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    print(
        "[added] Phase159 R4 repair8 focused regression test"
    )
    print("")
    print("Phase 159 R1-7c R4 repair8 applied.")
    print(
        "Stale prose test files updated: "
        + str(len(changed_test_paths))
    )
    print("Imports changed: none.")


if __name__ == "__main__":
    main()
