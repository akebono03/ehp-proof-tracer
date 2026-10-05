from __future__ import annotations

from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase156_r5_repair9_test_contract_after_boundary_collapse.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase158_r3_stale_boundary_helper_repair4_backup"
)

OLD_HELPER = r'''
def _body(
  rendered: str,
) -> str:
  marker = "## 証明"
  index = rendered.find(
    marker
  )
  assert index >= 0

  body = rendered[
    index + len(
      marker
    ):
  ]

  return body.lstrip()
'''

NEW_HELPER = r'''
def _body(
  rendered: str,
) -> str:
  marker = "\n## 証明\n"
  index = rendered.find(
    marker
  )
  assert index >= 0

  body = rendered[
    index + len(
      marker
    ):
  ]

  return body.lstrip()
'''


def main() -> int:
  source = TARGET.read_text(
    encoding="utf-8",
  )

  if NEW_HELPER in source:
    print(
      "Exact proof-section boundary helper already applied."
    )
    return 0

  if OLD_HELPER not in source:
    raise RuntimeError(
      "Expected repair3 _body helper was not found."
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  backup = (
    BACKUP_DIR
    / TARGET.name
  )

  if not backup.exists():
    shutil.copy2(
      TARGET,
      backup,
    )

  source = source.replace(
    OLD_HELPER,
    NEW_HELPER,
    1,
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
  )

  compile(
    source,
    str(
      TARGET
    ),
    "exec",
  )

  print(
    "Phase 158-R3 stale boundary helper repair4 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Helper now matches exact '\\n## 証明\\n' boundary."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
