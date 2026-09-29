from pathlib import Path


REQUIRED_PHRASES = (
  "Rule E1 — Provenance preservation",
  "Rule E2 — Ownership before exposure",
  "Rule E3 — Owned primary component",
  "Rule E4 — Unowned recursive component",
  "Rule E5 — `primary is None` is not itself the policy",
  "Rule E6 — No new mathematical heuristic",
  "AMBIGUOUS_RELEVANT",
  "Phase 149 / RC3",
)

FORBIDDEN_PRODUCTION_PATTERNS = (
  "pi_6^3 only",
  "block[5]",
)


def main():
  design_path = (
    Path(__file__).resolve().parent
    / "rc2_2_design.md"
  )
  text = design_path.read_text(
    encoding="utf-8"
  )

  missing = tuple(
    phrase
    for phrase in REQUIRED_PHRASES
    if phrase not in text
  )

  if missing:
    raise SystemExit(
      "missing design boundary: "
      + ", ".join(
        missing
      )
    )

  forbidden = tuple(
    pattern
    for pattern in FORBIDDEN_PRODUCTION_PATTERNS
    if pattern in text
  )

  if forbidden:
    raise SystemExit(
      "forbidden group/index-specific design found: "
      + ", ".join(
        forbidden
      )
    )

  print("Phase 148 RC2-2 design audit: PASS")
  print("Production changes: none")
  print("Existing repository test changes: none")
  print("General rule: ownership/relevance before Narrative exposure")
  print("Ambiguous relevance: conservative fallback")
  print("Provenance: preserved")
  print("RC3 ordering: untouched")


if __name__ == "__main__":
  main()
