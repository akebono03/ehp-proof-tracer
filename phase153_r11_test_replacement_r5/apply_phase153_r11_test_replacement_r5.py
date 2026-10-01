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
      ).is_dir()
      and (
        candidate
        / "toda_group_proof_narrative_contribution_renderer.py"
      ).is_file()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def main() -> None:
  repo = find_repository_root()
  target = (
    repo
    / "tests"
    / "test_phase153_r11_generic_reference_attribution_filtering.py"
  )
  source = (
    PACKAGE_DIR
    / "tests"
    / "test_phase153_r11_generic_reference_attribution_filtering.py"
  )

  backup_dir = (
    repo
    / "phase153_r11_test_replacement_r5_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )

  if target.is_file():
    backup = (
      backup_dir
      / target.name
    )
    if not backup.exists():
      shutil.copy2(
        target,
        backup,
      )

  shutil.copy2(
    source,
    target,
  )

  print(
    "Phase 153-R11 test replacement R5 applied."
  )
  print(
    "Production changes: none"
  )
  print(
    "Replaced test file:"
  )
  print(
    "  tests/test_phase153_r11_generic_reference_attribution_filtering.py"
  )


if __name__ == "__main__":
  main()
