from pathlib import Path

path = Path("toda_group_proof_narrative_arguments.py")
text = path.read_text(encoding="utf-8")

old = """    group_generators = []

    for supporting_block in argument.supporting_blocks:
      for proof_step in supporting_block.steps:
        statement = proof_step.conclusion

        if not isinstance(
          statement,
          Relation,
        ):
          continue

        if (
          statement.relation_type
          is not RelationType.EQUALITY
        ):
          continue

        rhs = statement.rhs

        if not hasattr(
          rhs,
          "generator",
        ):
          continue

        generator = rhs.generator

        if generator not in group_generators:
          group_generators.append(
            generator
          )

    matching_subjects = []

    for relation in order_relations:
      if (
        relation.lhs in group_generators
        and relation.lhs not in matching_subjects
      ):
        matching_subjects.append(
          relation.lhs
        )

    if len(
      matching_subjects
    ) != 1:
      return None

    return matching_subjects[
      0
    ]
"""

new = """    calculation_expressions = []

    for supporting_block in argument.supporting_blocks:
      if (
        supporting_block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .CALCULATION
      ):
        continue

      for proof_step in supporting_block.steps:
        statement = proof_step.conclusion

        if not isinstance(
          statement,
          Relation,
        ):
          continue

        if (
          statement.relation_type
          is not RelationType.EQUALITY
        ):
          continue

        for expression in (
          statement.lhs,
          statement.rhs,
        ):
          if expression not in calculation_expressions:
            calculation_expressions.append(
              expression
            )

    matching_subjects = []

    for relation in order_relations:
      if (
        relation.lhs in calculation_expressions
        and relation.lhs not in matching_subjects
      ):
        matching_subjects.append(
          relation.lhs
        )

    if len(
      matching_subjects
    ) != 1:
      return None

    return matching_subjects[
      0
    ]
"""

if old not in text:
  raise RuntimeError(
    "Phase143-12 fix1 ORDER fallback block was not found."
  )

path.write_text(
  text.replace(
    old,
    new,
    1,
  ),
  encoding="utf-8",
)

print("Updated:", path)
