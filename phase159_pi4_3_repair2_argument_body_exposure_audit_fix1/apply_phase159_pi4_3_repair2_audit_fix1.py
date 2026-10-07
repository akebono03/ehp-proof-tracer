from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUDIT_PATH = (
  ROOT
  / "phase159_pi4_3_repair2_argument_body_exposure_audit"
  / "audit_phase159_pi4_3_repair2_argument_body_exposure.py"
)

OLD_IMPORT = """from toda_group_proof_narrative_argument_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
"""

NEW_IMPORT = """from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
"""


def main() -> int:
  if not AUDIT_PATH.exists():
    raise RuntimeError(
      "previous repair2 audit script not found: "
      + str(AUDIT_PATH)
    )

  source = AUDIT_PATH.read_text(
    encoding="utf-8"
  )

  count = source.count(
    OLD_IMPORT
  )

  if count != 1:
    raise RuntimeError(
      "expected exactly one incorrect method-evidence "
      f"import, found {count}"
    )

  updated = source.replace(
    OLD_IMPORT,
    NEW_IMPORT,
    1,
  )

  AUDIT_PATH.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 pi_4^3 repair2 audit fix1 applied."
  )
  print(
    "Changed audit script only:"
  )
  print(
    "  phase159_pi4_3_repair2_argument_body_exposure_audit/"
    "audit_phase159_pi4_3_repair2_argument_body_exposure.py"
  )
  print(
    "Production code changes: none"
  )
  print(
    "Existing test changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
