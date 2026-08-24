from proof import (
  CokernelStatement,
  ExactnessStatement,
  ImageStatement,
  KernelStatement,
  Proof,
  ProofStep,
  Relation,
)
from expression import (
  Composition,
  HomotopyElement,
  Multiple,
  Zero,
)


def format_abelian_structure(structure):
  if structure.free_rank == 0:
    free_parts = []
  elif structure.free_rank == 1:
    free_parts = ["Z"]
  else:
    free_parts = [
      f"Z^{structure.free_rank}"
    ]

  torsion_parts = [
    f"Z/{order}"
    for order in structure.torsion_orders
  ]

  parts = (
    free_parts
    + torsion_parts
  )

  if not parts:
    return "0"

  return " ⊕ ".join(parts)


def format_group_map(group_map):
  return group_map.name


def format_statement(statement):
  if isinstance(
    statement,
    KernelStatement,
  ):
    return (
      f"Ker("
      f"{format_group_map(statement.group_map)}"
      f") ≅ "
      f"{format_abelian_structure(statement.structure)}"
    )

  if isinstance(
    statement,
    ImageStatement,
  ):
    return (
      f"Im("
      f"{format_group_map(statement.group_map)}"
      f") ≅ "
      f"{format_abelian_structure(statement.structure)}"
    )

  if isinstance(
    statement,
    CokernelStatement,
  ):
    return (
      f"Coker("
      f"{format_group_map(statement.group_map)}"
      f") ≅ "
      f"{format_abelian_structure(statement.structure)}"
    )

  if isinstance(
    statement,
    ExactnessStatement,
  ):
    first_name = format_group_map(
      statement.first_map
    )

    second_name = format_group_map(
      statement.second_map
    )

    if statement.is_exact:
      return (
        f"Im({first_name}) "
        f"= Ker({second_name})"
      )

    return (
      f"Im({first_name}) "
      f"!= Ker({second_name})"
    )

  if isinstance(
    statement,
    Relation,
  ):
    return (
      f"{format_expression(statement.lhs)} "
      f"= "
      f"{format_expression(statement.rhs)}"
    )

  return str(statement)


def format_proof_step(
  step,
  number=None,
):
  conclusion = format_statement(
    step.conclusion
  )

  rule = step.rule.value.replace(
    "_",
    " ",
  )

  if number is None:
    first_line = conclusion
  else:
    first_line = (
      f"{number}. {conclusion}"
    )

  return (
    f"{first_line}\n"
    f"   [{rule}]"
  )


def format_proof(proof):
  if not isinstance(proof, Proof):
    raise TypeError(
      "proof must be a Proof"
    )

  lines = []

  for index, step in enumerate(
    proof.steps,
    start=1,
  ):
    lines.append(
      format_proof_step(
        step,
        number=index,
      )
    )

  lines.append("")
  lines.append("Conclusion:")
  lines.append(
    format_statement(
      proof.conclusion
    )
  )

  return "\n\n".join(lines)


def format_expression(expression):
  if isinstance(
    expression,
    Zero,
  ):
    return "0"

  if isinstance(
    expression,
    HomotopyElement,
  ):
    return (
      f"{expression.name}"
      f"_{expression.dimension}"
    )

  if isinstance(
    expression,
    Multiple,
  ):
    return (
      f"{expression.coefficient}"
      f"{format_expression(expression.expression)}"
    )

  if isinstance(
    expression,
    Composition,
  ):
    return (
      f"{format_expression(expression.left)}"
      f"{format_expression(expression.right)}"
    )

  return str(expression)






