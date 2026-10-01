from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_repair3"

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

  old = '''      if (
        reference_heading_count == 1
        and proof_heading_count == 1
        and rendered.index(
          "## 使用する結果"
        )
        > rendered.index(
          "## 証明"
        )
      ):
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="ordering",
          detail="Reference section appears after proof section",
        )
'''

  new = '''      if (
        reference_heading_count == 1
        and proof_heading_count == 1
      ):
        reference_heading_index = next(
          index
          for index, line in enumerate(
            rendered_lines
          )
          if line.strip()
          == "## 使用する結果"
        )
        proof_heading_index = next(
          index
          for index, line in enumerate(
            rendered_lines
          )
          if line.strip()
          == "## 証明"
        )

        if (
          reference_heading_index
          > proof_heading_index
        ):
          _add_violation(
            violations,
            n=n,
            k=k,
            group=group,
            category="ordering",
            detail="Reference section appears after proof section",
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
      "updated: exact heading-line ordering"
    )
  elif new in text:
    print(
      "already-current: exact heading-line ordering"
    )
  else:
    raise RuntimeError(
      "expected heading-order block not found"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
