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
        / "test_phase153_r12_root_reference_exclusion.py"
      ).is_file()
      and (
        candidate
        / "toda_group_proof_narrative_renderer.py"
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
    / "test_phase153_r12_root_reference_exclusion.py"
  )
  source = (
    PACKAGE_DIR
    / "tests"
    / "test_phase153_r12_root_reference_exclusion.py"
  )

  backup_dir = (
    repo
    / "phase153_r12_reference_section_scope_repair_r1_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )
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
    "Phase 153-R12 Reference-section scope repair R1 applied."
  )
  print(
    "Production changes: none"
  )
  print(
    "Changed test:"
  )
  print(
    "  tests/test_phase153_r12_root_reference_exclusion.py"
  )


if __name__ == "__main__":
  main()
