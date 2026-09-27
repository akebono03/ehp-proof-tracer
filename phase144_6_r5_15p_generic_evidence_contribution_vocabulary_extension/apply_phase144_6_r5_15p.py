from pathlib import Path

path = Path("toda_group_proof_narrative_evidence_contributions.py")
if not path.exists():
  raise RuntimeError("15M prototype file is missing.")
text = path.read_text(encoding="utf-8")

enum_anchor = '  ESTABLISH_RELATION = "establish_relation"\n'
enum_add = (
  '  ESTABLISH_RELATION = "establish_relation"\n'
  '  ESTABLISH_EXACTNESS = "establish_exactness"\n'
  '  ESTABLISH_DEFINITION = "establish_definition"\n'
  '  ESTABLISH_MEMBERSHIP = "establish_membership"\n'
)
if 'ESTABLISH_EXACTNESS = "establish_exactness"' not in text:
  if enum_anchor not in text:
    raise RuntimeError("15M enum anchor not found.")
  text = text.replace(enum_anchor, enum_add, 1)

mapper_anchor = (
  "  if (\n"
  "    block.role\n"
  "    is TodaGroupProofNarrativeMathematicalBlockRole\n"
  "    .MAP_PROPERTY\n"
  "  ):\n"
)
mapper_add = (
  "  if (\n"
  "    block.role\n"
  "    is TodaGroupProofNarrativeMathematicalBlockRole\n"
  "    .EXACTNESS\n"
  "  ):\n"
  "    return (\n"
  "      TodaGroupProofNarrativeEvidenceContribution\n"
  "      .ESTABLISH_EXACTNESS\n"
  "    )\n\n"
  "  if (\n"
  "    block.role\n"
  "    is TodaGroupProofNarrativeMathematicalBlockRole\n"
  "    .DEFINITION\n"
  "  ):\n"
  "    return (\n"
  "      TodaGroupProofNarrativeEvidenceContribution\n"
  "      .ESTABLISH_DEFINITION\n"
  "    )\n\n"
  "  if (\n"
  "    block.role\n"
  "    is TodaGroupProofNarrativeMathematicalBlockRole\n"
  "    .MEMBERSHIP\n"
  "  ):\n"
  "    return (\n"
  "      TodaGroupProofNarrativeEvidenceContribution\n"
  "      .ESTABLISH_MEMBERSHIP\n"
  "    )\n\n"
  + mapper_anchor
)
if ".ESTABLISH_EXACTNESS" not in text:
  if mapper_anchor not in text:
    raise RuntimeError("15M mapper anchor not found.")
  text = text.replace(mapper_anchor, mapper_add, 1)

path.write_text(text, encoding="utf-8")
print("Applied Phase 144-6-R5-15P.")
