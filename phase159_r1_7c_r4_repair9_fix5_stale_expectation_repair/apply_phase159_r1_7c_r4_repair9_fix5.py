from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r20_repair30_final_reflexive_suppression.py"
)
BACKUP_DIR = (
  PACKAGE_DIR
  / "backup_before_apply"
)

OLD_FUNCTION = r'''def test_phase157_r20_repair30_eta_bridge_and_hopf_support_remain():
  rendered = _render_pi6_3_repair30()
  body = rendered.split(
    "---",
    1,
  )[1]

  required = (
    r"$\eta_{6}=E\eta_{5}$.",
    r"$H\left(\nu'\right) = \eta_{5}",
    r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}",
    r"$2\nu' = \eta_{3}^{3}",
  )

  for text in required:
    assert text in body
'''

NEW_FUNCTION = r'''def test_phase157_r20_repair30_eta_bridge_and_hopf_support_remain():
  rendered = _render_pi6_3_repair30()
  body = rendered.split(
    "---",
    1,
  )[1]

  required = (
    r"$\eta_{6}=E\eta_{5}$.",
    r"$H\left(\nu'\right) = \eta_{5}",
    r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}",
  )

  for text in required:
    assert text in body

  assert (
    r"$2\nu' = \eta_{3}^{3}"
    in body
    or (
      r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}"
      r" = \eta_{3}^{3}$"
      in body
    )
  )
'''


def main() -> int:
    if not TARGET.is_file():
        raise RuntimeError(
            f"Target test file not found: {TARGET}"
        )

    source = TARGET.read_text(
        encoding="utf-8"
    )

    if NEW_FUNCTION in source:
        print(
            "Test expectation repair already applied."
        )
        return 0

    if OLD_FUNCTION not in source:
        raise RuntimeError(
            "Expected stale test function was not found."
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

    updated = source.replace(
        OLD_FUNCTION,
        NEW_FUNCTION,
        1,
    )

    compile(
        updated,
        str(
            TARGET
        ),
        "exec",
    )

    TARGET.write_text(
        updated,
        encoding="utf-8",
    )

    print(
        "Updated stale expectation:"
    )
    print(
        TARGET
    )
    print(
        "Production code changes: none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
