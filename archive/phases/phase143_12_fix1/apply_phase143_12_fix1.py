from pathlib import Path

path = Path("toda_group_proof_narrative_arguments.py")
text = path.read_text(encoding="utf-8")

if "extract_toda_group_proof_narrative_argument_purpose_subject" in text:
  raise RuntimeError("Phase143-12 purpose subject extractor already exists.")

old_imports = """from dataclasses import dataclass
from enum import Enum

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
"""

new_imports = """from dataclasses import dataclass
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
"""

if old_imports not in text:
  raise RuntimeError("Current Phase143-10 import section was not found.")

text = text.replace(old_imports, new_imports, 1)
marker = "def build_toda_group_proof_narrative_arguments(\n"

addition = """def extract_toda_group_proof_narrative_argument_purpose_subject(
  argument: TodaGroupProofNarrativeArgument,
):
  if not isinstance(
    argument,
    TodaGroupProofNarrativeArgument,
  ):
    raise TypeError(
      "argument must be a "
      "TodaGroupProofNarrativeArgument"
    )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    subjects = []
    for proof_step in argument.conclusion_block.steps:
      statement = proof_step.conclusion
      if not hasattr(statement, "element"):
        continue
      subject = statement.element
      if subject not in subjects:
        subjects.append(subject)
    if len(subjects) != 1:
      return None
    return subjects[0]

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER
  ):
    order_relations = tuple(
      proof_step.conclusion
      for proof_step in argument.conclusion_block.steps
      if (
        isinstance(proof_step.conclusion, Relation)
        and proof_step.conclusion.relation_type
        is RelationType.ORDER
      )
    )
    if not order_relations:
      return None
    if len(order_relations) == 1:
      return order_relations[0].lhs

    group_generators = []
    for supporting_block in argument.supporting_blocks:
      for proof_step in supporting_block.steps:
        statement = proof_step.conclusion
        if not isinstance(statement, Relation):
          continue
        if statement.relation_type is not RelationType.EQUALITY:
          continue
        rhs = statement.rhs
        if not hasattr(rhs, "generator"):
          continue
        generator = rhs.generator
        if generator not in group_generators:
          group_generators.append(generator)

    matching_subjects = []
    for relation in order_relations:
      if (
        relation.lhs in group_generators
        and relation.lhs not in matching_subjects
      ):
        matching_subjects.append(relation.lhs)
    if len(matching_subjects) != 1:
      return None
    return matching_subjects[0]

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE
  ):
    groups = []
    for proof_step in argument.conclusion_block.steps:
      statement = proof_step.conclusion
      if not isinstance(statement, Relation):
        continue
      if statement.relation_type is not RelationType.EQUALITY:
        continue
      if not isinstance(statement.lhs, TodaPrimaryGroup):
        continue
      if statement.lhs not in groups:
        groups.append(statement.lhs)
    if len(groups) != 1:
      return None
    return groups[0]

  return None


"""

if marker not in text:
  raise RuntimeError(
    "build_toda_group_proof_narrative_arguments marker was not found."
  )

path.write_text(
  text.replace(marker, addition + marker, 1),
  encoding="utf-8",
)
print("Updated:", path)
