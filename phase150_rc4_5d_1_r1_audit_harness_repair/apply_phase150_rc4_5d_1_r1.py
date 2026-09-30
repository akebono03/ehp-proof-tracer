from pathlib import Path

ROOT = Path.cwd()
AUDIT = (
  ROOT
  / "phase150_rc4_5d_1_nu_prime_order_reason_audit"
  / "audit_phase150_rc4_5d_1.py"
)


def main():
  text = AUDIT.read_text(encoding="utf-8")

  old = "from toda_group_proof_provenance import (\n  extract_toda_recursive_proof_provenance,\n)\n"
  new = "from toda_proof_dependency import (\n  extract_toda_recursive_proof_provenance,\n)\n"

  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      "expected exactly one obsolete provenance import, "
      f"found {count}"
    )

  AUDIT.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
  )

  print("RC4-5D-1-R1 audit harness repair applied.")
  print("Changed: audit harness import only.")
  print("Production changes: none.")
  print("Existing test changes: none.")


if __name__ == "__main__":
  main()
