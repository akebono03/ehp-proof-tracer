from pathlib import Path

path = Path("toda_group_proof_narrative_arguments.py")
text = path.read_text(encoding="utf-8")

old_imports = '''from dataclasses import dataclass
from enum import Enum

from homotopy_groups import (
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
'''

new_imports = '''from dataclasses import dataclass
from enum import Enum

from expression import (
  Multiple,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
'''

if old_imports not in text:
  raise RuntimeError("Expected Phase143-12 import section was not found.")

text = text.replace(old_imports, new_imports, 1)

start_marker = "def extract_toda_group_proof_narrative_argument_purpose_subject(\n"
end_marker = "def build_toda_group_proof_narrative_arguments(\n"
start = text.find(start_marker)
end = text.find(end_marker, start)

if start < 0 or end < 0:
  raise RuntimeError("Purpose subject extractor boundaries were not found.")

replacement = 'def extract_toda_group_proof_narrative_argument_purpose_subject(\n  argument: TodaGroupProofNarrativeArgument,\n):\n  if not isinstance(\n    argument,\n    TodaGroupProofNarrativeArgument,\n  ):\n    raise TypeError(\n      "argument must be a "\n      "TodaGroupProofNarrativeArgument"\n    )\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_DEFINITION\n  ):\n    subjects = []\n    for proof_step in argument.conclusion_block.steps:\n      statement = proof_step.conclusion\n      if not hasattr(statement, "element"):\n        continue\n      subject = statement.element\n      if subject not in subjects:\n        subjects.append(subject)\n    if len(subjects) != 1:\n      return None\n    return subjects[0]\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_ORDER\n  ):\n    order_relations = tuple(\n      proof_step.conclusion\n      for proof_step in argument.conclusion_block.steps\n      if (\n        isinstance(proof_step.conclusion, Relation)\n        and proof_step.conclusion.relation_type\n        is RelationType.ORDER\n      )\n    )\n    if not order_relations:\n      return None\n    if len(order_relations) == 1:\n      return order_relations[0].lhs\n\n    scalar_multiple_subjects = []\n    for supporting_block in argument.supporting_blocks:\n      if (\n        supporting_block.role\n        is not TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION\n      ):\n        continue\n      for proof_step in supporting_block.steps:\n        statement = proof_step.conclusion\n        if not isinstance(statement, Relation):\n          continue\n        if statement.relation_type is not RelationType.EQUALITY:\n          continue\n        for expression in (\n          statement.lhs,\n          statement.rhs,\n        ):\n          if not isinstance(expression, Multiple):\n            continue\n          subject = expression.expression\n          if subject not in scalar_multiple_subjects:\n            scalar_multiple_subjects.append(subject)\n\n    matching_subjects = []\n    for relation in order_relations:\n      if (\n        relation.lhs in scalar_multiple_subjects\n        and relation.lhs not in matching_subjects\n      ):\n        matching_subjects.append(relation.lhs)\n    if len(matching_subjects) != 1:\n      return None\n    return matching_subjects[0]\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_GROUP_STRUCTURE\n  ):\n    groups = []\n    for proof_step in argument.conclusion_block.steps:\n      statement = proof_step.conclusion\n      if not isinstance(statement, Relation):\n        continue\n      if statement.relation_type is not RelationType.EQUALITY:\n        continue\n      if not isinstance(statement.lhs, TodaPrimaryGroup):\n        continue\n      if statement.lhs not in groups:\n        groups.append(statement.lhs)\n    if len(groups) != 1:\n      return None\n    return groups[0]\n\n  return None\n'

path.write_text(
  text[:start] + replacement + "\n\n" + text[end:],
  encoding="utf-8",
)

print(
  "Updated imports and replaced: "
  "extract_toda_group_proof_narrative_argument_purpose_subject"
)
