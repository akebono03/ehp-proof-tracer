from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_r6_2_repair1"


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


def update_text(
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
    elif new in text:
      print(
        "  already-current:",
        label,
      )
    else:
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


def normalize_test_punctuation(
  relative_path: str,
) -> None:
  path = (
    REPO_ROOT
    / relative_path
  )

  if not path.exists():
    print(
      "skipped missing test:",
      relative_path,
    )
    return

  backup(
    path
  )
  text = path.read_text(
    encoding="utf-8",
  )
  updated = (
    text
    .replace(
      "、",
      ", ",
    )
    .replace(
      "。",
      ".",
    )
  )

  if updated == text:
    print(
      "already-current test:",
      relative_path,
    )
    return

  path.write_text(
    updated,
    encoding="utf-8",
  )
  print(
    "updated test punctuation:",
    relative_path,
  )


def main() -> int:
  update_text(
    REPO_ROOT
    / "toda_group_proof_narrative_exactness_method_renderer.py",
    (
      (
        'return "そのために、次の完全列を考える."',
        'return "そのために, 次の完全列を考える."',
        "exactness method transition comma",
      ),
    ),
  )

  update_text(
    REPO_ROOT
    / "toda_group_proof_narrative_transition_renderer.py",
    (
      (
        'return "以上より、"',
        'return "以上より, "',
        "Narrative transition connector comma",
      ),
    ),
  )

  update_text(
    REPO_ROOT
    / "toda_group_proof_narrative_argument_single_renderer.py",
    (
      (
        '".そのために、"',
        '".そのために, "',
        "single-argument spacing source",
      ),
      (
        '". そのために、"',
        '". そのために, "',
        "single-argument spacing target",
      ),
    ),
  )

  test_files = (
    "tests/test_phase154_r2_fix2_semantic_sentence_composition.py",
    "tests/test_phase153_r8_reference_use_prose_normalization.py",
    "tests/test_phase143_30_exactness_method_transition.py",
    "tests/test_phase143_34_argument_header_method.py",
    "tests/test_phase154_r6_1_repair3_ascii_period_policy.py",
    "tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py",
    "tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py",
    "tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py",
    "tests/test_phase154_r2_fix3_reference_marker_completion.py",
  )

  for relative_path in test_files:
    normalize_test_punctuation(
      relative_path
    )

  test_source = (
    PACKAGE_ROOT
    / "tests"
    / "test_phase154_r6_2_repair1_missing_shared_sources.py"
  )
  test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r6_2_repair1_missing_shared_sources.py"
  )

  if test_target.exists():
    backup(
      test_target
    )

  shutil.copy2(
    test_source,
    test_target,
  )

  print(
    "added:",
    test_target.relative_to(
      REPO_ROOT
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
