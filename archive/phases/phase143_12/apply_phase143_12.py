from pathlib import Path

path = Path("toda_group_proof_narrative_arguments.py")
text = path.read_text(encoding="utf-8")
old = "from proof import (\n  ProofStep,\n)\n"
new = "from proof import (\n  ProofStep,\n  Relation,\n  RelationType,\n)\n"
if old not in text:
  raise RuntimeError("Expected proof import block was not found.")
text = text.replace(old, new, 1)
marker = "def build_toda_group_proof_narrative_arguments(\n"
addition = '''def extract_toda_group_proof_narrative_argument_purpose_subject(
  argument: TodaGroupProofNarrativeArgument,
):
  if not isinstance(
    argument,
    TodaGroupProofNarrativeArgument,
  ):
    raise TypeError(
      "argument must be a TodaGroupProofNarrativeArgument"
    )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
  ):
    subjects = []
    for proof_step in argument.conclusion_block.steps:
      statement = proof_step.conclusion
      if hasattr(statement, "element"):
        if statement.element not in subjects:
          subjects.append(statement.element)
    return subjects[0] if len(subjects) == 1 else None

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
  ):
    relations = tuple(
      proof_step.conclusion
      for proof_step in argument.conclusion_block.steps
      if (
        isinstance(proof_step.conclusion, Relation)
        and proof_step.conclusion.relation_type is RelationType.ORDER
      )
    )
    if len(relations) == 1:
      return relations[0].lhs

    generators = []
    for block in argument.supporting_blocks:
      for proof_step in block.steps:
        statement = proof_step.conclusion
        if (
          isinstance(statement, Relation)
          and statement.relation_type is RelationType.EQUALITY
          and hasattr(statement.rhs, "generator")
        ):
          generator = statement.rhs.generator
          if generator not in generators:
            generators.append(generator)

    matches = []
    for relation in relations:
      if relation.lhs in generators and relation.lhs not in matches:
        matches.append(relation.lhs)
    return matches[0] if len(matches) == 1 else None

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
  ):
    groups = []
    for proof_step in argument.conclusion_block.steps:
      statement = proof_step.conclusion
      if (
        isinstance(statement, Relation)
        and statement.relation_type is RelationType.EQUALITY
        and isinstance(statement.lhs, TodaPrimaryGroup)
        and statement.lhs not in groups
      ):
        groups.append(statement.lhs)
    return groups[0] if len(groups) == 1 else None

  return None


'''
if marker not in text:
  raise RuntimeError("Argument builder insertion marker was not found.")
path.write_text(text.replace(marker, addition + marker, 1), encoding="utf-8")
print("Updated:", path)
