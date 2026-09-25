from pathlib import Path

path = Path("toda_group_proof_narrative_arguments.py")
text = path.read_text(encoding="utf-8")

start_marker = (
  "def extract_toda_group_proof_narrative_argument_purpose_subject(\n"
)
end_marker = (
  "def build_toda_group_proof_narrative_arguments(\n"
)

start = text.find(
  start_marker
)
end = text.find(
  end_marker,
  start,
)

if start < 0:
  raise RuntimeError(
    "Purpose subject extractor start marker was not found."
  )

if end < 0:
  raise RuntimeError(
    "Argument builder marker was not found."
  )

replacement = 'def extract_toda_group_proof_narrative_argument_purpose_subject(\n  argument: TodaGroupProofNarrativeArgument,\n):\n  if not isinstance(\n    argument,\n    TodaGroupProofNarrativeArgument,\n  ):\n    raise TypeError(\n      "argument must be a "\n      "TodaGroupProofNarrativeArgument"\n    )\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_DEFINITION\n  ):\n    subjects = []\n\n    for proof_step in argument.conclusion_block.steps:\n      statement = proof_step.conclusion\n\n      if not hasattr(\n        statement,\n        "element",\n      ):\n        continue\n\n      subject = statement.element\n\n      if subject not in subjects:\n        subjects.append(\n          subject\n        )\n\n    if len(\n      subjects\n    ) != 1:\n      return None\n\n    return subjects[\n      0\n    ]\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_ORDER\n  ):\n    order_relations = tuple(\n      proof_step.conclusion\n      for proof_step in argument.conclusion_block.steps\n      if (\n        isinstance(\n          proof_step.conclusion,\n          Relation,\n        )\n        and proof_step.conclusion.relation_type\n        is RelationType.ORDER\n      )\n    )\n\n    if not order_relations:\n      return None\n\n    if len(\n      order_relations\n    ) == 1:\n      return order_relations[\n        0\n      ].lhs\n\n    calculation_expressions = []\n\n    for supporting_block in argument.supporting_blocks:\n      if (\n        supporting_block.role\n        is not TodaGroupProofNarrativeMathematicalBlockRole\n        .CALCULATION\n      ):\n        continue\n\n      for proof_step in supporting_block.steps:\n        statement = proof_step.conclusion\n\n        if not isinstance(\n          statement,\n          Relation,\n        ):\n          continue\n\n        if (\n          statement.relation_type\n          is not RelationType.EQUALITY\n        ):\n          continue\n\n        for expression in (\n          statement.lhs,\n          statement.rhs,\n        ):\n          if expression not in calculation_expressions:\n            calculation_expressions.append(\n              expression\n            )\n\n    matching_subjects = []\n\n    for relation in order_relations:\n      if (\n        relation.lhs in calculation_expressions\n        and relation.lhs not in matching_subjects\n      ):\n        matching_subjects.append(\n          relation.lhs\n        )\n\n    if len(\n      matching_subjects\n    ) != 1:\n      return None\n\n    return matching_subjects[\n      0\n    ]\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_GROUP_STRUCTURE\n  ):\n    groups = []\n\n    for proof_step in argument.conclusion_block.steps:\n      statement = proof_step.conclusion\n\n      if not isinstance(\n        statement,\n        Relation,\n      ):\n        continue\n\n      if (\n        statement.relation_type\n        is not RelationType.EQUALITY\n      ):\n        continue\n\n      if not isinstance(\n        statement.lhs,\n        TodaPrimaryGroup,\n      ):\n        continue\n\n      if statement.lhs not in groups:\n        groups.append(\n          statement.lhs\n        )\n\n    if len(\n      groups\n    ) != 1:\n      return None\n\n    return groups[\n      0\n    ]\n\n  return None\n' + "\n\n"

path.write_text(
  text[
    :start
  ]
  + replacement
  + text[
    end:
  ],
  encoding="utf-8",
)

print(
  "Replaced:",
  "extract_toda_group_proof_narrative_argument_purpose_subject",
)
