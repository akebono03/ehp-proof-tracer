from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = REPO_ROOT / "phase153_r7_backup_before_apply"

FILES = (
  "toda_group_proof_narrative_contribution_renderer.py",
  "toda_group_proof_narrative_renderer.py",
)


def main() -> None:
  if not BACKUP_DIR.is_dir():
    raise SystemExit(
      "Required Phase 153-R7 backup directory was not found: "
      + str(
        BACKUP_DIR
      )
    )

  for filename in FILES:
    backup = BACKUP_DIR / filename
    destination = REPO_ROOT / filename

    if not backup.is_file():
      raise SystemExit(
        "Required backup file was not found: "
        + str(
          backup
        )
      )

    if backup.stat().st_size == 0:
      raise SystemExit(
        "Backup file is unexpectedly empty: "
        + str(
          backup
        )
      )

    shutil.copy2(
      backup,
      destination,
    )

    print(
      "Restored:",
      filename,
      "bytes=",
      destination.stat().st_size,
    )

  print(
    "Phase 153-R7 pre-apply production state restored "
    "from phase153_r7_backup_before_apply/."
  )


if __name__ == "__main__":
  main()
