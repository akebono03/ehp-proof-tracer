from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
  Path(__file__).resolve().parent
  / "audit_phase144_6_r25_23_fixed.py"
)
TARGET = (
  ROOT
  / "phase144_6_r25_23_evidence_selection_dependency_order_audit"
  / "audit_phase144_6_r25_23.py"
)


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "R25-23 base audit directory is missing. "
      "Extract the original R25-23 package first."
    )

  TARGET.write_text(
    SOURCE.read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  print("R25-23-R2 audit harness repaired.")
  print("Production code changes: none.")
  print(
    "Group lookup now uses "
    "toda_calculation_facade.build_standard_toda_report."
  )
  print(
    "Narrative sidecar/block construction now follows "
    "the current repository API."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
