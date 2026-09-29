from pathlib import Path

path = Path(
  "toda_group_proof_narrative_evidence_contributions.py"
)

if not path.exists():
  raise RuntimeError(
    "15M prototype file is missing."
  )

text = path.read_text(
  encoding="utf-8"
)

enum_anchor = (
  '  ESTABLISH_RELATION = "establish_relation"\n'
)
enum_extension = (
  '  ESTABLISH_RELATION = "establish_relation"\n'
  '  ESTABLISH_EXACTNESS = "establish_exactness"\n'
  '  ESTABLISH_DEFINITION = "establish_definition"\n'
  '  ESTABLISH_MEMBERSHIP = "establish_membership"\n'
)

if (
  'ESTABLISH_EXACTNESS = "establish_exactness"'
  not in text
):
  if enum_anchor not in text:
    raise RuntimeError(
      "15M enum anchor not found."
    )
  text = text.replace(
    enum_anchor,
    enum_extension,
    1,
  )

function_start = text.find(
  "def _contribution_for_premise_block("
)
function_end = text.find(
  "\n\ndef build_toda_group_proof_narrative_evidence_contribution_sidecar(",
  function_start,
)

if (
  function_start < 0
  or function_end < 0
):
  raise RuntimeError(
    "15M contribution mapper function "
    "boundary not found."
  )

new_function = """def _contribution_for_premise_block(
  block: TodaGroupProofNarrativeBlock,
  edge: TodaProofEdge,
) -> TodaGroupProofNarrativeEvidenceContribution:
  role = block.role

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .REFERENCE
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .PROVIDE_REFERENCE
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .PRECONDITION
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .PROVIDE_PRECONDITION
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .GROUP_STRUCTURE
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_GROUP
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_EXACTNESS
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .DEFINITION
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_DEFINITION
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .MEMBERSHIP
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_MEMBERSHIP
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .MAP_PROPERTY
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_MAP
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .ORDER
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_ORDER
    )

  statement = (
    edge.premise_step.conclusion
  )

  if isinstance(
    statement,
    Relation,
  ):
    if (
      statement.relation_type
      is RelationType.ZERO
    ):
      return (
        TodaGroupProofNarrativeEvidenceContribution
        .ESTABLISH_ZERO
      )

    if (
      statement.relation_type
      is RelationType.ORDER
    ):
      return (
        TodaGroupProofNarrativeEvidenceContribution
        .ESTABLISH_ORDER
      )

    if (
      statement.relation_type
      is RelationType.EQUALITY
    ):
      return (
        TodaGroupProofNarrativeEvidenceContribution
        .ESTABLISH_RELATION
      )

  return (
    TodaGroupProofNarrativeEvidenceContribution
    .UNRESOLVED
  )
"""

text = (
  text[
    :function_start
  ]
  + new_function
  + text[
    function_end:
  ]
)

path.write_text(
  text,
  encoding="utf-8",
)

print(
  "Applied Phase 144-6-R5-15P-R1 "
  "generic EvidenceContribution mapper."
)
