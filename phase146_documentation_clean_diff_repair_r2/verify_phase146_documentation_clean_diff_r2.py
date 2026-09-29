from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHECKS = {
  "docs/design.md": (
    "Phase 146 closure boundary",
  ),
  "docs/development_log.md": (
    "Phase 146 完了境界",
  ),
  "docs/roadmap.md": (
    "Phase 147 — RC1",
    "Phase 152 — RC6",
  ),
  "docs/proof_records.md": (
    "Phase 146 historical Narrative comparison / provenance record",
  ),
}

for relative_path, markers in CHECKS.items():
  path = ROOT / relative_path
  text = path.read_text(
    encoding="utf-8",
    errors="strict",
  )
  print(
    "UTF-8 strict decode PASS:",
    relative_path,
  )

  for marker in markers:
    if marker not in text:
      raise SystemExit(
        "ERROR: missing marker "
        + repr(marker)
        + " in "
        + relative_path
      )

print("Phase 146 documentation markers: PASS")
