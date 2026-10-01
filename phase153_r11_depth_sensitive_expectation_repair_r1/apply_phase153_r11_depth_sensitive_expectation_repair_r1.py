from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  for candidate in (
    PACKAGE_DIR.parent,
    Path.cwd(),
  ):
    if (
      (
        candidate
        / "tests"
        / "test_phase153_r11_generic_reference_attribution_filtering.py"
      ).is_file()
      and (
        candidate
        / "tests"
        / "test_phase144_6_r3_production_references.py"
      ).is_file()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise SystemExit(
      f"{label}: expected exactly one replacement target, "
      f"found {count}."
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_r11_test(
  repo: Path,
) -> None:
  path = (
    repo
    / "tests"
    / "test_phase153_r11_generic_reference_attribution_filtering.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  old_import = """from toda_group_proof_narrative_contribution_renderer import (\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\nfrom toda_group_proof_narrative_references import (\n  extract_toda_group_proof_step_literature_reference,\n)\n"""

  new_import = """from toda_group_proof_narrative_contribution_ordering import (\n  build_toda_group_proof_narrative_ordered_contributions,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  build_toda_group_proof_narrative_generic_used_step_ids,\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\nfrom toda_group_proof_narrative_proof_chains import (\n  build_toda_group_proof_narrative_proof_chains,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  extract_toda_group_proof_step_literature_reference,\n)\n"""

  text = replace_once(
    text,
    old_import,
    new_import,
    "R11 test imports",
  )

  old_test = """def test_phase153_r11_pi6_3_preserves_external_references_used_by_generic_proof():\n  _, rendered = _pi6_3_rendered()\n\n  for locator in (\n    \"(5.3) / Lemma 5.2\",\n    \"(5.2)\",\n    \"Proposition 4.4\",\n    \"Proposition 5.1\",\n  ):\n    assert locator in rendered\n"""

  new_test = """def test_phase153_r11_pi6_3_depth2_reference_section_matches_used_steps():\n  (\n    presentation,\n    sidecar,\n    blocks,\n    arguments,\n  ) = _pi6_3_data()\n\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n    )\n  )\n  proof_chains = (\n    build_toda_group_proof_narrative_proof_chains(\n      presentation,\n      sidecar,\n      arguments,\n    )\n  )\n  ordered_contributions = (\n    build_toda_group_proof_narrative_ordered_contributions(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n      proof_chains,\n      current_markdown=rendered,\n    )\n  )\n  used_step_ids = (\n    build_toda_group_proof_narrative_generic_used_step_ids(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  root_reference = (\n    extract_toda_group_proof_step_literature_reference(\n      presentation.root_step\n    )\n  )\n  expected_locators = tuple(\n    entry.reference.locator\n    for entry in build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n    if (\n      entry.reference != root_reference\n      and any(\n        id(\n          proof_step\n        )\n        in used_step_ids\n        for proof_step in entry.proof_steps\n      )\n    )\n  )\n\n  for locator in expected_locators:\n    assert locator in rendered\n\n  assert \"Proposition 5.6\" not in rendered.split(\n    \"まず\",\n    1,\n  )[0]\n"""

  text = replace_once(
    text,
    old_test,
    new_test,
    "R11 depth-2 reference expectation",
  )

  backup_dir = (
    repo
    / "phase153_r11_depth_sensitive_expectation_repair_r1_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )
  backup = (
    backup_dir
    / path.name
  )

  if not backup.exists():
    shutil.copy2(
      path,
      backup,
    )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\\n",
  )


def main() -> None:
  repo = find_repository_root()
  patch_r11_test(
    repo
  )

  print(
    "Phase 153-R11 depth-sensitive expectation repair R1 applied."
  )
  print(
    "Production changes: none"
  )
  print(
    "Changed test:"
  )
  print(
    "  tests/test_phase153_r11_generic_reference_attribution_filtering.py"
  )


if __name__ == "__main__":
  main()
