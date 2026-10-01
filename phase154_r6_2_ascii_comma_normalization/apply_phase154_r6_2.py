from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_r6_2"

PRODUCTION_FILES = ['toda_group_proof_generic_narrative_renderer.py', 'toda_group_proof_narrative_reason_renderer.py', 'toda_group_proof_narrative_argument_discourse.py', 'toda_group_proof_narrative_argument_renderer.py', 'toda_group_proof_narrative_contribution_renderer.py', 'toda_group_proof_narrative_renderer.py']
TEST_FILES = ['tests/test_phase154_r6_1_repair3_ascii_period_policy.py', 'tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py', 'tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py', 'tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py', 'tests/test_phase154_r2_fix3_reference_marker_completion.py', 'tests/test_phase153_r8_reference_use_prose_normalization.py', 'tests/test_phase143_17_argument_discourse.py', 'tests/test_phase143_30_exactness_method_transition.py', 'tests/test_phase143_34_argument_header_method.py', 'tests/test_phase150_rc4_5b_3_reference_binding.py', 'tests/test_phase150_rc4_5c_2_exactness_to_map_property.py', 'tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py']


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


def normalize_ascii_comma(
  text: str,
) -> str:
  return text.replace(
    "、",
    ", ",
  )


def update_file(
  relative_path: str,
  *,
  required: bool,
) -> None:
  path = (
    REPO_ROOT
    / relative_path
  )

  if not path.exists():
    if required:
      raise RuntimeError(
        "missing file: "
        + str(
          path
        )
      )

    print(
      "skipped missing:",
      relative_path,
    )
    return

  backup(
    path
  )

  text = path.read_text(
    encoding="utf-8",
  )
  updated = normalize_ascii_comma(
    text
  )

  if updated == text:
    print(
      "already-current:",
      relative_path,
    )
    return

  path.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "updated:",
    relative_path,
  )


def main() -> int:
  for relative_path in PRODUCTION_FILES:
    update_file(
      relative_path,
      required=True,
    )

  for relative_path in TEST_FILES:
    update_file(
      relative_path,
      required=False,
    )

  new_test_source = (
    PACKAGE_ROOT
    / "tests"
    / "test_phase154_r6_2_ascii_comma_normalization.py"
  )
  new_test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r6_2_ascii_comma_normalization.py"
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
