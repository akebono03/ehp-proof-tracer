from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_repair2"

AUDIT_PATH = (
  REPO_ROOT
  / "phase154_closure_audit"
  / "audit_phase154_closure.py"
)


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


def main() -> int:
  if not AUDIT_PATH.exists():
    raise RuntimeError(
      "missing closure audit: "
      + str(
        AUDIT_PATH
      )
    )

  text = AUDIT_PATH.read_text(
    encoding="utf-8",
  )

  old = '''      reference_heading_count = rendered.count(
        "## 使用する結果"
      )
      proof_heading_count = rendered.count(
        "## 証明"
      )
'''

  new = '''      rendered_lines = rendered.splitlines()

      reference_heading_count = sum(
        line.strip()
        == "## 使用する結果"
        for line in rendered_lines
      )
      proof_heading_count = sum(
        line.strip()
        == "## 証明"
        for line in rendered_lines
      )
'''

  if old in text:
    backup(
      AUDIT_PATH
    )
    AUDIT_PATH.write_text(
      text.replace(
        old,
        new,
      ),
      encoding="utf-8",
    )
    print(
      "updated: exact heading-line counting"
    )
  elif new in text:
    print(
      "already-current: exact heading-line counting"
    )
  else:
    raise RuntimeError(
      "expected heading-count block not found"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
