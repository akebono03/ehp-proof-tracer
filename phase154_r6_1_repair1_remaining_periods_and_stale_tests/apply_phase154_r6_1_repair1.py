from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_repair1"


def backup(path: Path) -> None:
  relative = path.relative_to(
    REPO_ROOT
  )
  target = (
    BACKUP_ROOT
    / relative
  )
  target.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    target,
  )


def replace_required(
  path: Path,
  replacements,
) -> None:
  backup(
    path
  )
  text = path.read_text(
    encoding="utf-8",
  )

  for old, new, label in replacements:
    if old not in text:
      raise RuntimeError(
        "required pattern not found in "
        + str(
          path
        )
        + ": "
        + label
      )

    text = text.replace(
      old,
      new,
    )

  path.write_text(
    text,
    encoding="utf-8",
  )
  print(
    "updated:",
    path.relative_to(
      REPO_ROOT
    ),
  )


def main() -> int:
  reason_renderer = (
    REPO_ROOT
    / "toda_group_proof_narrative_reason_renderer.py"
  )

  replace_required(
    reason_renderer,
    (
      (
        'f"$2{target_latex}\\\\neq0$ である.\\n"',
        'f"$2{target_latex}\\\\neq0$ である。\\n"',
        "MULTIPLE_RELATION_TO_ORDER period",
      ),
      (
        'f"{right_order}={middle_order}$ である.\\n"',
        'f"{right_order}={middle_order}$ である。\\n"',
        "FINAL_GROUP_STRUCTURE order period",
      ),
    ),
  )

  test_replacements = {
    "tests/test_phase154_r2_internal_prose_fallback_leakage.py": (
      (
        '"は単射である."',
        '"は単射である。"',
        "injective current punctuation",
      ),
      (
        '"は完全である."',
        '"は完全である。"',
        "exactness current punctuation",
      ),
    ),
    "tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py": (
      (
        r'r"$\nu_{4}$ の分解を用いる."',
        r'r"$\nu_{4}$ の分解を用いる。" ',
        "nu4 decomposition current punctuation",
      ),
      (
        '"は単射である."',
        '"は単射である。"',
        "injective current punctuation",
      ),
      (
        '"は完全である."',
        '"は完全である。"',
        "exactness current punctuation",
      ),
    ),
    "tests/test_phase154_r2_fix2_semantic_sentence_composition.py": (
      (
        r'r"は単射である."',
        r'r"は単射である。" ',
        "semantic injective current punctuation",
      ),
      (
        r'r"は完全である."',
        r'r"は完全である。" ',
        "semantic exactness current punctuation",
      ),
      (
        r'r"$\nu_{4}$ の分解写像は同型写像である."',
        r'r"$\nu_{4}$ の分解写像は同型写像である。" ',
        "semantic isomorphism current punctuation",
      ),
      (
        r'r"$\nu_{4}$ の分解を用いる."',
        r'r"$\nu_{4}$ の分解を用いる。" ',
        "semantic decomposition current punctuation",
      ),
    ),
  }

  for relative_path, replacements in test_replacements.items():
    path = (
      REPO_ROOT
      / relative_path
    )
    replace_required(
      path,
      replacements,
    )

    text = path.read_text(
      encoding="utf-8",
    )
    text = text.replace(
      '。" ',
      '。"'
    )
    path.write_text(
      text,
      encoding="utf-8",
    )

  new_test_source = (
    PACKAGE_ROOT
    / "tests"
    / "test_phase154_r6_1_repair1_remaining_periods.py"
  )
  new_test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r6_1_repair1_remaining_periods.py"
  )
  shutil.copy2(
    new_test_source,
    new_test_target,
  )
  print(
    "added:",
    new_test_target.relative_to(
      REPO_ROOT
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
