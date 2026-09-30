from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = (
  ROOT
  / "phase150_rc4_5f_1_final_group_structure_reason_chain_audit"
  / "audit_phase150_rc4_5f_1.py"
)

OLD = """from relation import (
  Relation,
  RelationType,
)
"""

NEW = """from proof import (
  Relation,
  RelationType,
)
"""


def main() -> None:
  text = AUDIT.read_text(encoding="utf-8")

  if NEW in text:
    print("RC4-5F-1-R1 audit import already repaired.")
    return

  count = text.count(OLD)
  if count != 1:
    raise RuntimeError(
      "Expected exactly one obsolete relation import block; "
      f"found {count}"
    )

  AUDIT.write_text(
    text.replace(OLD, NEW, 1),
    encoding="utf-8",
  )

  print("RC4-5F-1-R1 audit import repaired.")
  print("Changed audit harness only:")
  print(
    "  phase150_rc4_5f_1_final_group_structure_reason_chain_audit/"
    "audit_phase150_rc4_5f_1.py"
  )
  print("Production changes: none.")
  print("Existing test changes: none.")


if __name__ == "__main__":
  main()
