from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_r6_2_repair2"


def backup(path: Path) -> None:
  relative = path.relative_to(REPO_ROOT)
  target = BACKUP_ROOT / relative
  target.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    target,
  )


def update_required(
  path: Path,
  replacements,
) -> None:
  if not path.exists():
    raise RuntimeError(
      "missing file: "
      + str(
        path
      )
    )

  backup(path)
  text = path.read_text(
    encoding="utf-8",
  )

  for old, new, label in replacements:
    if old in text:
      text = text.replace(
        old,
        new,
      )
      print(
        "  updated:",
        label,
      )
      continue

    if new in text:
      print(
        "  already-current:",
        label,
      )
      continue

    raise RuntimeError(
      "neither old nor new pattern found in "
      + str(
        path
      )
      + ": "
      + label
    )

  path.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "checked:",
    path.relative_to(
      REPO_ROOT
    ),
  )


def main() -> int:
  update_required(
    REPO_ROOT
    / "toda_group_proof_narrative_argument_body_renderer.py",
    (
      (
        '"これらより、"',
        '"これらより, "',
        "step derivation connector comma",
      ),
    ),
  )

  update_required(
    REPO_ROOT
    / "toda_group_proof_narrative_equation_numbering.py",
    (
      (
        'if lines[index] == "これらより、"',
        'if lines[index] == "これらより, "',
        "numbering connector lookup comma",
      ),
      (
        'reference_text + " より、"',
        'reference_text + " より, "',
        "numbered derivation connector comma",
      ),
    ),
  )

  test143 = (
    REPO_ROOT
    / "tests"
    / "test_phase143_57c_step_derivation_connector.py"
  )
  if test143.exists():
    backup(test143)
    text = test143.read_text(
      encoding="utf-8",
    )
    updated = (
      text
      .replace(
        "これらより、",
        "これらより, ",
      )
      .replace(
        "より、",
        "より, ",
      )
    )
    test143.write_text(
      updated,
      encoding="utf-8",
    )
    print(
      "updated test punctuation:",
      test143.relative_to(
        REPO_ROOT
      ),
    )

  r6_1_test_source = (
    PACKAGE_ROOT
    / "tests"
    / "test_phase154_r6_1_repair3_ascii_period_policy.py"
  )
  r6_1_test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r6_1_repair3_ascii_period_policy.py"
  )

  backup(r6_1_test_target)
  shutil.copy2(
    r6_1_test_source,
    r6_1_test_target,
  )
  print(
    "repaired test:",
    r6_1_test_target.relative_to(
      REPO_ROOT
    ),
  )

  repair_test_source = (
    PACKAGE_ROOT
    / "tests"
    / "test_phase154_r6_2_repair2_equation_numbering.py"
  )
  repair_test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r6_2_repair2_equation_numbering.py"
  )

  if repair_test_target.exists():
    backup(repair_test_target)

  shutil.copy2(
    repair_test_source,
    repair_test_target,
  )
  print(
    "added:",
    repair_test_target.relative_to(
      REPO_ROOT
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
