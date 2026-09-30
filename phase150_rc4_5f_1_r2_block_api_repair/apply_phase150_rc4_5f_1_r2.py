from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = (
  ROOT
  / "phase150_rc4_5f_1_final_group_structure_reason_chain_audit"
  / "audit_phase150_rc4_5f_1.py"
)

OLD = "block.proof_steps"
NEW = "block.steps"


def main() -> None:
  text = AUDIT.read_text(encoding="utf-8")

  if OLD not in text:
    if NEW in text:
      print("RC4-5F-1-R2 block API already repaired.")
      return
    raise RuntimeError(
      "Neither obsolete nor current block step field was found."
    )

  count = text.count(OLD)
  text = text.replace(OLD, NEW)
  AUDIT.write_text(text, encoding="utf-8")

  print("RC4-5F-1-R2 block API repaired.")
  print(f"Replaced {count} occurrence(s):")
  print("  block.proof_steps -> block.steps")
  print("Changed audit harness only.")
  print("Production changes: none.")
  print("Existing test changes: none.")


if __name__ == "__main__":
  main()
