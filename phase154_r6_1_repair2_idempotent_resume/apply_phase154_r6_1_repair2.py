from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_repair2"


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


def ensure_replacement(
  text: str,
  old: str,
  new: str,
  label: str,
) -> tuple[
  str,
  str,
]:
  if new in text:
    return (
      text,
      "already-current",
    )

  if old in text:
    return (
      text.replace(
        old,
        new,
      ),
      "updated",
    )

  raise RuntimeError(
    "neither old nor current pattern found: "
    + label
  )


def update_idempotent(
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

  backup(
    path
  )
  text = path.read_text(
    encoding="utf-8",
  )
  statuses = []

  for old, new, label in replacements:
    text, status = ensure_replacement(
      text,
      old,
      new,
      label,
    )
    statuses.append(
      (
        label,
        status,
      )
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

  for label, status in statuses:
    print(
      "  "
      + status
      + ": "
      + label
    )


def main() -> int:
  reason_renderer = (
    REPO_ROOT
    / "toda_group_proof_narrative_reason_renderer.py"
  )

  update_idempotent(
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
        "injective expectation",
      ),
      (
        '"は完全である."',
        '"は完全である。"',
        "exactness expectation",
      ),
    ),
    "tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py": (
      (
        r'r"$\nu_{4}$ の分解を用いる."',
        r'r"$\nu_{4}$ の分解を用いる。"',
        "nu4 decomposition expectation",
      ),
      (
        '"は単射である."',
        '"は単射である。"',
        "injective expectation",
      ),
      (
        '"は完全である."',
        '"は完全である。"',
        "exactness expectation",
      ),
    ),
    "tests/test_phase154_r2_fix2_semantic_sentence_composition.py": (
      (
        r'r"は単射である."',
        r'r"は単射である。"',
        "semantic injective expectation",
      ),
      (
        r'r"は完全である."',
        r'r"は完全である。"',
        "semantic exactness expectation",
      ),
      (
        r'r"$\nu_{4}$ の分解写像は同型写像である."',
        r'r"$\nu_{4}$ の分解写像は同型写像である。"',
        "semantic isomorphism expectation",
      ),
      (
        r'r"$\nu_{4}$ の分解を用いる."',
        r'r"$\nu_{4}$ の分解を用いる。"',
        "semantic decomposition expectation",
      ),
    ),
    "tests/test_phase154_r2_fix3_reference_marker_completion.py": (
      (
        r'r"[R2]より、$\nu_{4}$ の分解写像は同型写像である."',
        r'r"[R2]より、$\nu_{4}$ の分解写像は同型写像である。"',
        "R2 linked expectation",
      ),
      (
        r'r"このことから、$\nu_{4}$ の分解写像は同型写像である."',
        r'r"このことから、$\nu_{4}$ の分解写像は同型写像である。"',
        "R2 forbidden linked expectation",
      ),
      (
        r'r"$\nu_{4}$ の分解を用いる."',
        r'r"$\nu_{4}$ の分解を用いる。"',
        "R2 decomposition expectation",
      ),
    ),
    "tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py": (
      (
        r'r"[R2]より、$\nu_{4}$ の分解写像は同型写像である."',
        r'r"[R2]より、$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 linked expectation",
      ),
      (
        r'r"このことから、$\nu_{4}$ の分解写像は同型写像である."',
        r'r"このことから、$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 forbidden old prose expectation",
      ),
      (
        r'r"$\nu_{4}$ の分解写像は同型写像である."',
        r'r"$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 consumer expectation",
      ),
    ),
    "tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py": (
      (
        r'r"[R2]より、$\nu_{4}$ の分解写像は同型写像である."',
        r'r"[R2]より、$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 Repair1 linked expectation",
      ),
      (
        r'r"このことから、$\nu_{4}$ の分解写像は同型写像である."',
        r'r"このことから、$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 Repair1 forbidden old prose expectation",
      ),
      (
        r'r"$\nu_{4}$ の分解写像は同型写像である."',
        r'r"$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 Repair1 consumer expectation",
      ),
    ),
    "tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py": (
      (
        r'r"[R2]より、$\nu_{4}$ の分解写像は同型写像である."',
        r'r"[R2]より、$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 Repair2 linked expectation",
      ),
      (
        r'r"このことから、$\nu_{4}$ の分解写像は同型写像である."',
        r'r"このことから、$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 Repair2 forbidden old prose expectation",
      ),
      (
        r'r"$\nu_{4}$ の分解写像は同型写像である."',
        r'r"$\nu_{4}$ の分解写像は同型写像である。"',
        "R5 Repair2 consumer expectation",
      ),
    ),
  }

  for relative_path, replacements in test_replacements.items():
    update_idempotent(
      REPO_ROOT
      / relative_path,
      replacements,
    )

  new_test_source = (
    PACKAGE_ROOT
    / "tests"
    / "test_phase154_r6_1_repair2_idempotent_resume.py"
  )
  new_test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r6_1_repair2_idempotent_resume.py"
  )

  if new_test_target.exists():
    backup(
      new_test_target
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
