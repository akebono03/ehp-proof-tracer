from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
AUDIT_FILE = (
  REPO_ROOT
  / "phase159_r1_7c_r3_known_result_direct_premise_specialization"
  / "audit_phase159_r1_7c_r3.py"
)


OLD_IMPORT = "from pathlib import Path\n\nfrom toda_calculation_facade import (\n"

NEW_IMPORT = "from pathlib import Path\nimport sys\n\n\nREPOSITORY_ROOT = (\n  Path(__file__).resolve().parents[1]\n)\n\nif str(\n  REPOSITORY_ROOT\n) not in sys.path:\n  sys.path.insert(\n    0,\n    str(\n      REPOSITORY_ROOT\n    ),\n  )\n\n\nfrom toda_calculation_facade import (\n"


def main() -> None:
  if not AUDIT_FILE.exists():
    raise FileNotFoundError(
      f"audit file not found: {AUDIT_FILE}"
    )

  source = AUDIT_FILE.read_text(
    encoding="utf-8"
  )

  if "REPOSITORY_ROOT = (" in source:
    print(
      "R3 repair3 already applied."
    )
    print(
      "Production code changes: none"
    )
    return

  count = source.count(
    OLD_IMPORT
  )

  if count != 1:
    raise RuntimeError(
      "expected exactly one audit import anchor; "
      f"found {count}"
    )

  AUDIT_FILE.write_text(
    source.replace(
      OLD_IMPORT,
      NEW_IMPORT,
      1,
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R3 repair3 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Updated audit:",
    AUDIT_FILE,
  )


if __name__ == "__main__":
  main()
